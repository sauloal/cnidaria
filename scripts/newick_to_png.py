#!/usr/bin/python

import sys
import os
from   ete2 import Tree
import Image
import ImageFont
import ImageDraw
import ImageMath
import math
import tempfile

#ls trees/*.tree | xargs -I{} -P 20 bash -c 'echo {};  ./newick_to_png.py {} pimp_problems.lst; ./newick_to_png.py {} cherry.lst;'


print_ascii        = False
transparent_color  = (255, 255, 255)
transparent_thresh = 5
frame_prop         = 0.05

TMP_DIR            = '/var/run/shm'
SCRIPT_PATH        = os.path.abspath( os.path.dirname( sys.argv[0] )  )
print "SCRIPT_PATH", SCRIPT_PATH
fontname = 'Consolas.ttf'
FONT_PATH = os.path.join( SCRIPT_PATH, fontname )
print "FONT_PATH", FONT_PATH



#http://stackoverflow.com/questions/765736/using-pil-to-make-all-white-pixels-transparent
def distance2(a, b):
    return (a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]) + (a[2] - b[2]) * (a[2] - b[2])

def makeColorTransparent(image, color, thresh2=0):
    image = image.convert("RGBA")
    red, green, blue, alpha = image.split()
    image.putalpha(ImageMath.eval("""convert(((((t - d(c, (r, g, b))) >> 31) + 1) ^ 1) * a, 'L')""",
        t=thresh2, d=distance2, c=color, r=red, g=green, b=blue, a=alpha))
    return image

def main(infile, inlist=None, capt=None, ofp=None, output=None, ladderize=True, addcaption=True, extension="png", dpi=1200, fontsize=14):
    add_file(infile, inlist=inlist, capt=capt, ofp=ofp, output=output, ladderize=ladderize, addcaption=addcaption, extension=extension, dpi=dpi, fontsize=fontsize)


def add_file(infile, inlist=None, capt=None, ofp=None, output=None, ladderize=True, addcaption=True, extension="png", dpi=1200, fontsize=14):
    if not os.path.exists( infile ):
        print "input file %s does not exists" % infile
        sys.exit( 1 )

    print "reading input file %s" % infile

    caption = infile
    caption = caption.replace("/", "_")

    if capt:
        caption = capt


    outfile = infile + "." + extension
    if ofp:
        outfile = ofp + "." + extension

    #tree = Tree(infile, format=9)
    try:
        tree = Tree(infile, format=5)
    except:
        tree = Tree(infile, format=1)


    #tree = Tree(open(infile, 'r').read())

    #root = tree.get_tree_root()

    #print tree.children
    #print tree.get_children()
    #print root.get_children()

    if inlist is not None:
        prune(inlist, tree, ladderize=ladderize)

        inlistn = inlist.replace("/", "_")

        caption = infile  + "_" + inlistn
        if capt:
            caption = capt + "_" + inlistn
            caption = caption.replace("/", "_")

        outfile = infile + "_" + inlistn + "." + extension

        if ofp:
            outfile = ofp + "_" + inlistn + "." + extension

        if output:
            outfile = output


    makeimage(infile, outfile, caption, tree, addcaption=addcaption, dpi=dpi, fontsize=fontsize)

    return outfile


def add_seq(inseq, inlist=None, capt=None, ladderize=True, addcaption=False, extension="png", dpi=1200, fontsize=14):
    fnm = tempfile.mkstemp(suffix=".tree", prefix=os.path.basename(sys.argv[0]) + '_tmp_', text=True, dir=TMP_DIR)[1]

    print "saving tree", fnm
    with open(fnm, 'w') as fhi:
        fhi.write(inseq)

    ofn  = add_file(fnm, inlist=inlist, capt=capt, ladderize=ladderize, addcaption=addcaption, extension=extension, dpi=dpi, fontsize=fontsize)

    data = None
    print "opening png", ofn
    if os.path.exists( ofn ):
        with open(ofn, 'rb') as fho:
            data = fho.read()
        os.remove(ofn)
        
    else:
        print "tree image %s does not exists" % ofn

    os.remove(fnm)

    return data


def prune(inlist, tree, ladderize=True):
    print "pruning", inlist

    reqlist  = []
    names    = {}
    existing = []

    for leaf in tree.traverse():
        #print "leaf name:", leaf.name, type(leaf.name)
        
        name = leaf.name #.replace("'", "")
        
        if name == 'NoName': continue
        
        existing.append( name )

    #print existing

    with open( inlist, 'r' ) as fhd:
        for line in fhd:
            line  = line.strip()

            if len( line ) == 0:
                continue

            if line[0] == "#":
                continue

            cols = [ "'" + x + "'" for x in line.split( "\t" ) ]
            #print cols
            
            if cols[0] in existing:
                #print "including %s" % line
                if len( cols ) == 2:
                    names[ cols[0] ] = cols[1]
                    reqlist.append( cols[1] )
                
                else:
                    reqlist.append( cols[0] )



    if len(names.keys()) == 0:
        print "no names in list"
        sys.exit(1)
    
    #print repr(names.keys())
    
    for leaf in tree.traverse():
        name = leaf.name #.replace("'", "")
        
        if name in names.keys():
            #print "leaf name B:", leaf.name, type(leaf.name)
            leaf.name = names[ name ]
            #print "leaf name A:", leaf.name, '\n'

        elif leaf.name == 'NoName':
            pass
        
        else:
            print "leaf.name not in names '" + leaf.name + "'"
            sys.exit(1)
                

    #print reqlist
    tree.prune( reqlist, preserve_branch_length=True )
    if ladderize:
        tree.ladderize()
    
    return tree


def makeimage(infile, outfile, caption, tree, addcaption=True, dpi=1200, fontsize=14):
    if os.path.exists( outfile ):
        os.remove( outfile )

    #print tree.get_midpoint_outgroup()
    #print tree.get_sisters()
    #print tree.get_tree_root()
    #root = tree.get_tree_root()
    #tree.delete( root )
    #print "root", root
    #root.unroot()

    if print_ascii:
    #if True:
        print "rendering tree", infile, "to", outfile,'in ASCII'
        print tree.get_ascii()
        print tree.write()

    print "rendering tree", infile, "to", outfile
    tree.render( outfile, dpi=dpi )

    if not os.path.exists( outfile ):
        print "rendering tree", infile, "to", outfile, 'FAILED'
        return None

    orig             = Image.open( outfile )
    orig             = makeColorTransparent(orig, transparent_color, thresh2=transparent_thresh);
    (orig_w, orig_h) = orig.size
    orig_dpi         = orig.info["dpi"]


    print "ORIG width",orig_w,"height",orig_h,"dpi",orig_dpi

    charsperline    = int( math.floor( orig_w/math.ceil(fontsize/1.6) ) )

    textlines       = []
    if addcaption:
        print "charsperline", charsperline
        print "caption     ", caption

        for pos in xrange(0, len(caption), charsperline):
            #print "pos",pos,"end", pos+charsperline, caption[pos: pos+charsperline]
            textlines.append( caption[pos: pos+charsperline] )

    numlines        = len(textlines)
    print "numlines", numlines
    htext           = (fontsize*numlines)
    himgtext        = orig_h + htext

    frame_w         = int( orig_w * frame_prop )
    orig_w_frame    =      orig_w + ( 2 * frame_w )
    out             = Image.new( 'RGBA', (orig_w_frame, himgtext), (255,255,255) )
    out.info["dpi"] = (dpi, dpi)

    maski           = Image.new('L', (orig_w_frame, himgtext), color=255)
    mask            = ImageDraw.Draw( maski )
    mask.rectangle((0, 0, orig_w_frame, himgtext), fill=0)
    out.putalpha( maski )
    out.paste( orig, ( frame_w, 0 ) )


    if addcaption:
        if os.path.exists( FONT_PATH ):
            zoomout = 20
            font    = ImageFont.truetype(FONT_PATH, fontsize*zoomout)
            texti   = Image.new("RGBA", (orig_w*zoomout, htext*zoomout))
            text    = ImageDraw.Draw( texti )
            for linepos in xrange( len(textlines) ):
                hline = linepos * fontsize
                line  = textlines[linepos]
                text.text( (fontsize*zoomout, hline*zoomout), line, (0,0,0), font=font)
            texti   = texti.resize((orig_w,htext), Image.ANTIALIAS)
            out.paste( texti, ( frame_w, orig_h ) )
        else:
            print "NO FONT FILE", os.path.join( SCRIPT_PATH, fontname )


    (out_w, out_h)  = out.size
    out_dpi         = out.info["dpi"]
    print "OUT width", out_w, "height", out_h, "dpi", out_dpi

    out.save( outfile, optimize=True, dpi=(dpi,dpi) )

    print "saved to %s" % outfile

    return


if __name__ == '__main__':
    try:
        infile = sys.argv[1]

    except:
        print "no input file given"
        sys.exit( 1 )


    try:
        inlist = sys.argv[2]

    except:
        print "no input list given"
        inlist = None


    main(infile, inlist=inlist)
