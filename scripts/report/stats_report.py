#!/usr/bin/python

import os
import sys
import simplejson as json
from datetime import datetime as dt
import zlib
import base64

from read_titles import readFilesTitles

#import backports.lzma as lzma
#backports.lzma


# 20K test07_21.json
#244K test07_21_kmer_stats_report.html
# 20K test07_31.json
#244K test07_31_kmer_stats_report.html
# 19M test10_21.json
# 11M test10_21_kmer_stats_report.html
# 18M test10_31.json
#9.6M test10_31_kmer_stats_report.html

# 20K test07_21.json
#236K test07_21_kmer_stats_report.html
# 20K test07_31.json
#236K test07_31_kmer_stats_report.html
# 19M test10_21.json
#8.4M test10_21_kmer_stats_report.html
# 18M test10_31.json
#7.4M test10_31_kmer_stats_report.html




REPORT_NAME = "kmer_stats_report"

template_dir = os.path.dirname( os.path.abspath( sys.argv[0] ) )

templates	= {
	'css'         : 'stats_report.template.css',
	'js'          : 'stats_report.template.js',
	'html'        : 'stats_report.template.html',
	#'b64'         : 'stats_report.template.b64.js',
	'b64'         : 'stats_report.template.b64.min.js',
	'inflate'     : 'stats_report.template.inflate.js',
	'deflate'     : 'stats_report.template.deflate.js',
	#'jsphylo'     : 'stats_report.template.jsphylosvg.js',
	'jsphylo'     : 'stats_report.template.jsphylosvg.min.js',
	'raphael'     : 'stats_report.template.raphael.js',
	'math'        : 'stats_report.template.math.js',
	'd3'          : 'stats_report.template.d3.js',
	'd3layout'    : 'stats_report.template.d3.layout.js',
	#'d3phylogram' : 'stats_report.template.d3.phylogram.js',
	'd3phylogram' : 'stats_report.template.d3.phylogram.min.js',
	#'d3phylonator': 'stats_report.template.d3.phylonator.js',
	'd3phylonator': 'stats_report.template.d3.phylonator.min.js',
	'newick'      : 'stats_report.template.newick.js',
	#'lzma'        : 'stats_report.template.lzma-d-min.js'
}


def templater( tpl ):
	print "reading template ::", tpl
	return open(os.path.join( template_dir, templates[tpl]), 'r').read()

def getjson(data):
	print "getting json"

	#return base64.b64encode( lzma.compress( json.dumps(data, sort_keys=True, indent=''), preset=lzma.PRESET_EXTREME, format=lzma.FORMAT_ALONE ) )
	#return base64.b64encode( zlib.compress( json.dumps(data, sort_keys=True, indent=''), zlib.Z_BEST_COMPRESSION ) )
	data = json.dumps(data, sort_keys=True, indent='')
	dl   = len(data)
	cobj = zlib.compressobj( zlib.Z_BEST_COMPRESSION, zlib.DEFLATED, 15, 9 )
	cout = cobj.compress( data ) + cobj.flush()
	cl   = len(cout)
	b64  = base64.b64encode( cout )
	bl   = len(b64)
	print "size %d compressed %d ( %6.2f %%) b64 %d ( %6.2f %% / %6.2f %%  )" % (dl, cl, (cl*1.0/dl*100), bl, (bl*1.0/dl*100), (bl*1.0/cl*100))
	return b64
	#return json.dumps(data, sort_keys=True, indent='')


def fixTitles( titles, data ):
	print "fixing titles"
	#print titles.keys()
	for p in xrange(len(data['in_filenames'])):
		name = data['in_filenames'][p]
		print " name",name
		if name in titles:
			data['in_filenames'][p] = titles[name]
			print "  renaming",name,"to",titles[name]

def addtrees( data, trees ):
	print "adding trees"
	data["trees"] = {}
	bn = os.path.commonprefix( trees )
	for treefile in trees:
		treename = treefile.replace( bn, '' )
		fn, ext  = os.path.splitext(treename)
		ext      = ext[1:]
		grps     = fn.split('.')
		print "adding trees", treefile, "to", treename, ext, grps[0], grps[1]
		#data["trees"][treename] = trees[treefile]
		if ext     not in data["trees"]:
			data["trees"][ext] = {}
		if grps[0] not in data["trees"][ext]:
			data["trees"][ext][grps[0]] = {}
		data["trees"][ext][grps[0]][grps[1]] = trees[treefile]
	

def makehtml(nname, gdata):
	#https://google-developers.appspot.com/chart/interactive/docs/gallery/candlestickchart

	html = templater('html'   )
	tpl  = {}
	tpl["data"] = getjson( gdata );
	tpl["now" ] = str(dt.now().isoformat());
	for k in templates:
		tpl[k] = templater(k)

	html = html % tpl

	#html = html % {
		#"css"      : templater('css'    ),
		#"js"       : templater('js'     ),
		#"b64"      : templater('b64m'   ),
		#"inflate"  : templater('inflate'),
		#"raphael"  : templater('raphael'),
		#"jsphylo"  : templater('jsphylo'),
		#"math"     : templater('math'   ),
		#"data"     : getjson( gdata ),
		#"now"      : str(dt.now().isoformat())
		#css=open( sys.argv[0] + '.css', 'r' ).read()
		#<!-- <link rel="stylesheet" type="text/css" href="%(stylefile)s"> -->
		#"stylefile": sys.argv[0] + '.css'
	#}

	#print html
	print "saving html"
	open(nname + '_' + REPORT_NAME + '.html', 'w').write( html )

def main(infiles):
	in_json = infiles[0]
	titles  = None
	trees   = None
	
	if len(infiles) > 1:
		in_csv  = infiles[1]
		print "loading titles", in_csv
		titles  = readFilesTitles(in_csv)

	if len(infiles) > 2:
		trees    = {}
		intrees  = infiles[2:]
		print "loading trees", intrees
		for tree in intrees:
			if not os.path.exists(tree):
				print "tree %s does not exists" % tree
				sys.exit(1)
			trees[ tree ] = open(tree, 'r').read()

	gdata = {}
	print "reading", in_json
	if not in_json.endswith('.json'):
		print "not a json file"
		sys.exit(0)

	nname = os.path.basename( os.path.abspath( in_json ) )
	nname = nname.replace(  '.json', '')
	gdata[ nname ] = json.load( open(in_json, 'r') )
	if titles is not None:
		fixTitles( titles, gdata[ nname ] )

	if trees is not None:
		addtrees( gdata[ nname ], trees )

	print "generating html"
	makehtml(nname, gdata)
	print "finished"

if __name__ == '__main__':
	main(sys.argv[1:])
