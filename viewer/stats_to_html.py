#!/usr/bin/env python

import os
import sys
import argparse
from collections import OrderedDict, defaultdict

def sanitize(n):
    return n.lower().replace(" ", "_").replace(".", "_")

class table(object):
    def __init__(self, lines, has_header=True, has_row_name=True):
        self.lines        = lines
        self.has_header   = has_header
        self.has_row_name = has_row_name
        self.header       = []
        self.rows         = []
        self.data         = []
        self.process()
        
    def process(self):
        for line_num, line in enumerate(self.lines.split("\n")):
            cols = [l.strip() for l in line.split("\t")]
            
            if line_num == 0:
                if   self.has_header:
                    self.header = cols
                
                elif self.has_row_name:
                    self.rows.append(cols[0] )
                    self.data.append(cols[1:])
                    
                else:
                    if len(cols) > 0 and sum([len(c) for c in cols]) > 0:
                        self.data.append(cols)
                    
            else:
                if len(cols) > 0 and sum([len(c) for c in cols]) > 0:
                    if self.has_row_name:
                        self.rows.append(cols[0] )
                        self.data.append(cols[1:])
                        
                    else:
                        self.data.append(cols)

    def to_html(self, tb_id, tb_class, decimals=1, colored=False, no_diag=False):
        tb_class = sanitize(tb_class)
        #return OrderedDict((('header', self.header), ('rows', self.rows), ('data', self.data)))

        if no_diag:
            for a in xrange(len(self.data)):
                self.data[a][a] = None

        min_val = min([min([float(e) for e in d if e is not None]) for d in self.data])
        max_val = max([max([float(e) for e in d if e is not None]) for d in self.data])

        print "min_val {} max_val {}".format(min_val, max_val)

        res     = ['            <table id="{}" class="table_header {}" min_val="{}" max_val="{}">'.format(tb_id, tb_class + (" colored" if colored else ""), min_val, max_val)]
        
        if   self.has_header:
            res.append( '                <tr row_num="-1" row_name="_HEADER_" class="header_row {tb_class}_header">'.format(**{
                'tb_class'  : tb_class            ,
            }) )
                
            for col_num, col_name in enumerate(self.header):
                res.append( '                    <th col_num="{col_num}" col_name="{col_name}" class="header_cell {tb_class}_header {tb_class}_th"><div><span>{col_name}</span></div></th>'.format(**{
                    'col_num'   : col_num           ,
                    'col_name'  : col_name          ,
                    'tb_class'  : tb_class          ,
                    }) )
                
            res.append( '                </tr>' )
        
        for row_num, row in enumerate(self.data):
            row_name = row_num

            if len(row) == 0:
                continue

            res.append( '                <tr row_num="{row_num}" row_name="{row_name}" class="table_row {tb_class}_row">'.format(**{
                'row_num'   : row_num             ,
                'row_name'  : row_name            ,
                'tb_class'  : tb_class            ,
            }) )
            
            for col_num, col_val in enumerate(row):
                if self.has_row_name and col_num == 0:
                    row_name = self.rows[row_num]
                    res.append( '                    <th col_num="{col_num}" col_name="{col_name}" row_num="{row_num}" row_name="{row_name}" class="row_name {tb_class}_row_name {tb_class}_th">{row_name}</th>'.format(**{
                        'col_num' :   col_num             ,
                        'col_name'  : self.header[col_num],
                        'row_num'   : row_num             ,
                        'row_name'  : row_name            ,
                        'tb_class'  : tb_class
                    }) )

                if self.has_row_name:
                    col_num += 1
                    
                col_name = col_num
                
                if self.has_header:
                    col_name = self.header[col_num]
                
                if col_val is None:
                    col_val = "-"
                
                else:
                    if '.' in col_val:
                        col_val = ("{:,."+str(decimals)+"f}").format(float(col_val))
                    else:
                        col_val = "{:,d}".format(int(col_val))
                
                res.append( '                    <td col_num="{col_num}" col_name="{col_name}" row_num="{row_num}" row_name="{row_name}" class="cell {tb_class}_td">{col_val}</th>'.format(**{
                        'col_num' :   col_num             ,
                        'col_name'  : self.header[col_num],
                        'row_num'   : row_num             ,
                        'row_name'  : row_name            ,
                        'row_name_s': sanitize(row_name)  ,
                        'tb_class'  : tb_class            ,
                        'col_val'   : col_val
                    }) )
            
            res.append( '                </tr>' )

        res.append( '            </table>' )

        return "\n".join(res)

def main():
    basename = sys.argv[1]
    
    f_json, f_stats, f_count, f_matrix = [x.format(basename) for x in ("{}.json","{}.json.count.csv","{}.json.csv","{}.json.jaccard.matrix")]
    
    for f in (f_json, f_stats, f_count, f_matrix):
        if not os.path.exists(f):
            print "input file {} does not exists".format(f)
            sys.exit(1)
            
    json     = open(f_json  , 'r').read()
    stats    = open(f_stats , 'r').read()
    count    = open(f_count , 'r').read()
    matrix   = open(f_matrix, 'r').read()
    
    stats_t  = table(stats , has_header=True, has_row_name=True ).to_html( 'stats_table' , 'stats_table' , decimals=1, colored=False, no_diag=False )
    count_t  = table(count , has_header=True, has_row_name=True ).to_html( 'count_table' , 'count_table' , decimals=1, colored=True , no_diag=True  )
    matrix_t = table(matrix, has_header=True, has_row_name=True ).to_html( 'matrix_table', 'matrix_table', decimals=5, colored=True , no_diag=True )
    
    res      = TEMPLATE.format(**{
        "title" : basename,
        "json"  : ''      , #json    ,
        "count" : count_t ,
        "stats" : stats_t ,
        "matrix": matrix_t,
        "script": '<script>{}</script>'.format(SCRIPT),
        "css"   : '<style>{}</style>'  .format(CSS   ),
        # "script": '<script src="{}.js"></script>'.format(basename),
        # "css"   : '<link rel="stylesheet" href="{}.css">'.format(basename)
    })
    
    #print res
    
    open("{}.html".format(basename), 'w').write(res)

TEMPLATE = """<!doctype html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
{css}
        <script src="https://cdn.rawgit.com/gka/chroma.js/master/chroma.min.js"></script>
{script}
    </head>
    <body>
        <script type="application/json" id="json">
{json}
        </script>
        <div id="stats">
{stats}
        </div>
        <div id="count">
{count}
        </div>
        <div id="matrix">
{matrix}
        </div>
    </body>
</html>
"""

SCRIPT = """
function isNumeric(n) {
  //https://stackoverflow.com/questions/18082/validate-decimal-numbers-in-javascript-isnumeric
  return !isNaN(parseFloat(n)) && isFinite(n);
}

var bscale = chroma.scale(['yellow' , 'orange', 'red' ]);
var fscale = chroma.scale(['black', 'white']);

function heatMapColorforValue(min_val, max_val, value){
  /*
  2-3-4-5 = (2 - 2) / (5 - 2) = 0 / 3 = 0
  2-3-4-5 = (3 - 2) / (5 - 2) = 1 / 3 = 0.3
  2-3-4-5 = (4 - 2) / (5 - 2) = 2 / 3 = 0.6
  2-3-4-5 = (5 - 2) / (5 - 2) = 3 / 3 = 1.0
  */
  var ival   = (value - min_val) / (max_val - min_val);
  var bcolor = bscale(ival).hex();
  var fcolor = fscale(ival).hex();
  return [ival, bcolor, fcolor];
}

function color_cells() {
  var coloreds = document.getElementsByClassName("colored");
  
  console.log(coloreds.length, coloreds);
  
  for (var c = 0; c < coloreds.length; c++) {
    var e = coloreds[c];
    
    var min_val = parseFloat(e.getAttribute('min_val'));
    var max_val = parseFloat(e.getAttribute('max_val'));
    
    console.log("C",c,"E",e,"min",min_val,"max",max_val);
    
    var tds = e.getElementsByTagName("td");
    
    //console.log(" TDS", tds.length, tds);
    
    for ( var t = 0; t < tds.length; t++) {
      var td    = tds[t];
      var value = parseFloat(td.innerHTML.replace(/,/g, ""));
      if ( isNumeric(value) ) {
        var cdata  = heatMapColorforValue(min_val, max_val, value);
        var prop   = cdata[0];
        var bcolor = cdata[1];
        var fcolor = cdata[2];
        td.style.backgroundColor = bcolor;
        //td.style.color           = fcolor;
      }
    }
  }
}


document.addEventListener("DOMContentLoaded", color_cells);
"""

CSS = """
th.header_cell {
    text-align: left;
    height: 500px;
}

th.header_cell > div {
    /*float: left;*/
    transform:
    /*translate(25px, 51px)*/
    /*rotate(315deg);*/
    translate(15px, 180px)
    rotate(270deg);
    width: 50px;
	/*transform-origin: left top 0;*/
}

th.header_cell > div > span {
    /*border-bottom: 1px solid #ccc;*/
    padding: 5px 10px;
}

th.row_name {
    text-align: left;
}

td.cell {
    text-align: right;
    /*text-shadow: 1px 1px 1px #000;*/
}

th {
    white-space: nowrap;
}
"""

"""
<div id="stats">
    <table id="stats_table" class=table_header "stats_table">
        <tr row_num="-1" row_name="_HEADER_" class="header_row stats_table_header">
            <th col_num="0" col_name="NAME" class="header_cell stats_table_header stats_table_th">NAME</th>
            <th col_num="1" col_name="TOTAL" class="header_cell stats_table_header stats_table_th">TOTAL</th>
            <th col_num="2" col_name="VALID" class="header_cell stats_table_header stats_table_th">VALID</th>
            <th col_num="3" col_name="PROP" class="header_cell stats_table_header stats_table_th">PROP</th>
        </tr>
        <tr row_num="176" row_name="176" class="table_row stats_table_row">
            <th col_num="0" col_name="NAME" row_num="176" row_name="Tribolium castaneum" class="row_name stats_table_row_name stats_table_th">Tribolium castaneum</th>
            <td col_num="1" col_name="TOTAL" row_num="176" row_name="Tribolium castaneum" class="cell stats_table_td">6581748</th>
            <td col_num="2" col_name="VALID" row_num="176" row_name="Tribolium castaneum" class="cell stats_table_td">1505999</th>
            <td col_num="3" col_name="PROP" row_num="176" row_name="Tribolium castaneum" class="cell stats_table_td"> 22.88</th>
        </tr>
        <tr row_num="177" row_name="177" class="table_row stats_table_row">
        </tr>
    </table>
</div>
<div id="count">
    <table id="count_table" class=table_header "count_table">
        <tr row_num="-1" row_name="_HEADER_" class="header_row count_table_header">
            <th col_num="0" col_name="" class="header_cell count_table_header count_table_th"></th>
            <th col_num="1" col_name="Arabidopsis lyrata" class="header_cell count_table_header count_table_th">Arabidopsis lyrata</th>
            <th col_num="2" col_name="Arabidopsis thaliana TAIR10" class="header_cell count_table_header count_table_th">Arabidopsis thaliana TAIR10</th>
            <th col_num="3" col_name="Citrus sinensis" class="header_cell count_table_header count_table_th">Citrus sinensis</th>
            <th col_num="176" col_name="Struthio camelus australis" class="header_cell count_table_header count_table_th">Struthio camelus australis</th>
            <th col_num="177" col_name="Tribolium castaneum" class="header_cell count_table_header count_table_th">Tribolium castaneum</th>
        </tr>
        <tr row_num="0" row_name="0" class="table_row count_table_row">
            <th col_num="0" col_name="" row_num="0" row_name="Arabidopsis lyrata" class="row_name count_table_row_name count_table_th">Arabidopsis lyrata</th>
            <td col_num="1" col_name="Arabidopsis lyrata" row_num="0" row_name="Arabidopsis lyrata" class="cell count_table_td">0</th>
            <td col_num="176" col_name="Struthio camelus australis" row_num="176" row_name="Tribolium castaneum" class="cell count_table_td">47911</th>
            <td col_num="177" col_name="Tribolium castaneum" row_num="176" row_name="Tribolium castaneum" class="cell count_table_td">0</th>
        </tr>
        <tr row_num="177" row_name="177" class="table_row count_table_row">
        </tr>
    </table>
</div>
<div id="matrix">
    <table id="matrix_table" class=table_header "matrix_table">
        <tr row_num="-1" row_name="_HEADER_" class="header_row matrix_table_header">
            <th col_num="0" col_name="" class="header_cell matrix_table_header matrix_table_th"></th>
            <th col_num="1" col_name="Arabidopsis lyrata" class="header_cell matrix_table_header matrix_table_th">Arabidopsis lyrata</th>
            <th col_num="176" col_name="Struthio camelus australis" class="header_cell matrix_table_header matrix_table_th">Struthio camelus australis</th>
            <th col_num="177" col_name="Tribolium castaneum" class="header_cell matrix_table_header matrix_table_th">Tribolium castaneum</th>
            <th col_num="178" col_name="" class="header_cell matrix_table_header matrix_table_th"></th>
        </tr>
        <tr row_num="0" row_name="0" class="table_row matrix_table_row">
            <th col_num="0" col_name="" row_num="0" row_name="Arabidopsis lyrata" class="row_name matrix_table_row_name matrix_table_th">Arabidopsis lyrata</th>
            <td col_num="1" col_name="Arabidopsis lyrata" row_num="0" row_name="Arabidopsis lyrata" class="cell matrix_table_td">1.0000000000</th>
            <td col_num="2" col_name="Arabidopsis thaliana TAIR10" row_num="0" row_name="Arabidopsis lyrata" class="cell matrix_table_td">0.7233067471</th>
            <td col_num="176" col_name="Struthio camelus australis" row_num="176" row_name="Tribolium castaneum" class="cell matrix_table_td">0.9962171649</th>
            <td col_num="177" col_name="Tribolium castaneum" row_num="176" row_name="Tribolium castaneum" class="cell matrix_table_td">1.0000000000</th>
        </tr>
        <tr row_num="177" row_name="177" class="table_row matrix_table_row">
        </tr>
        <tr row_num="178" row_name="178" class="table_row matrix_table_row">
        </tr>
    </table>
</div>
"""

if __name__ == '__main__':
    main()