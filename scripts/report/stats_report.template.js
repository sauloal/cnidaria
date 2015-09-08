var VAXIS_FONTSIZE   = 11;
var HAXIS_FONTSIZE   = 11;
var LEGEND_FONTSIZE  = 11;
var TOOLTIP_FONTSIZE = 11;
var TREE_PLACE_ID    = "treeplace";
var TREE_SCALE_ID    = "treeplace_scale";
var TREE_TICKS_ID    = "treeplace_ticks";
var TREE_DOWNLOAD_ID = "treeplace_download";
var TREE_COL_ID      = "treeplace_col";
var TREE_COL_DIST_TR = "treeplace_dist_col_tr";
var TREE_COL_DIST_ID = "treeplace_dist_col";
var TREE_SELECT_ID   = "treeplace_select";
var TREE_SELECT_NAME = "methods";
var treeFontHeight   = 10;
var BARMAXLENGTH     = 100;


function fixStr( src ) {
  return src.replace(/\//g, "_")
            .replace(/\\\\/g,"_")
            .replace(/\./g,"_")
            .replace(/ /g,"_")
            .replace(/\)/g,"_")
            .replace(/\(/g,"_")
            .replace(/\:/g,"_")
            .replace(/\-/g,"_")
            .replace(/#/g,"_")
            .replace(/\\%%/g,"_")
            .replace(/_+/g,"_");
}


function createDiv( dn, el, className ) {
    var nel = fixStr( el        );
    var ncn = className.join(" "); //fixStr( className );

    var ndiv = document.createElement('div');
    ndiv.setAttribute( "id"   , nel        );
    ndiv.setAttribute( "class", ncn        );

    var src = document.getElementById( dn );
    //console.log("createDiv DN", dn, 'SRC', src, 'EL', nel, 'NDIV', ndiv);
    src.appendChild( ndiv );
    return nel;
}


function drawVisualization(datain, el, options, chartType, firstrowasdata) {
  //console.log("drawVisualization",datain, el, options, chartType, firstrowasdata);
  var data  = google.visualization.arrayToDataTable(datain, firstrowasdata);
  var chart = new chartType( document.getElementById(el) );
  chart.draw(data, options);
}


//http://stackoverflow.com/questions/2901102/how-to-print-a-number-with-commas-as-thousands-separators-in-javascript
function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}


function printer( title, vAxis, hAxis, datain, dn, el, classes, charType, frad ) {
  var options = {
      title          :   title,
      vAxis          : { title: vAxis ,                   textStyle: {fontSize: VAXIS_FONTSIZE   } },
      hAxis          : { title: hAxis , showTextEvery: 1, textStyle: {fontSize: HAXIS_FONTSIZE   } },
      legend         : {                                  textStyle: {fontSize: LEGEND_FONTSIZE  } },
      tooltip        : {                                  textStyle: {fontSize: TOOLTIP_FONTSIZE } },
      backgroundColor: { fill: 'transparent' },
      //legend         : 'none'
    };

  var nel = createDiv( dn, el, classes );

  drawVisualization(datain, nel, options, charType, false);
}


function printcount(  filename, dn, name, data, title, vAxis, hAxis, headers, classes ) {
  //console.log( "print count", filename, dn, name, data );

  var datain = [ headers ];

  for ( key in data ) {
     var count = data[key];
     datain.push([ key, count ]);
  }
  //console.log("data in", datain);

  var el      = dn + '_' + name;

  var charType = google.visualization.ColumnChart;

  printer(title, vAxis, hAxis, datain, dn, el, classes, charType, false);
};


function printsingle( filename, dn, name, data, title, vAxis, hAxis, headers, classes ) {
  //console.log( "print single", filename, dn, name, data );

  var datain = [ headers ];

  for ( key in data ) {
     var vals = data[key];
     //-stddev +stddev min max
     var avg    = vals.average;
     var stddev = vals.stddev;
     var minV   = vals.min;
     var maxV   = vals.max;
     var low    = avg - stddev;
     var high   = avg + stddev;
     datain.push([ key, minV, low, high, maxV ]);
  }
  //console.log("data in", datain);

  var el      = dn + '_' + name;

  var charType = google.visualization.CandlestickChart;

  printer(title, vAxis, hAxis, datain, dn, el, classes, charType, false);
};


function printdouble( filename, dn, name, data, title, vAxis, hAxis, headers, classes1, classes2 ) {
  //console.log( "print double", filename, dn, name, data );

  var grp      = createDiv( dn, dn + '_' + name, classes1 );
  var clh      = classes1;
  clh.push("lbl2");
  var header   = createDiv( grp, dn + '_' + name + '_header', clh );
  document.getElementById( header ).innerHTML = name;

  for ( dclass in data ) {
    var ddata  = data[dclass];
    var name2  = name  + '_'   + dclass;
    var title2 = title + ' - ' + dclass;
    var vAxis2 = vAxis + ' - ' + dclass;
    var hAxis2 = hAxis;
    var classes22 = classes2;
    classes22.push( fixStr(dclass)              );
    classes22.push( fixStr(name + ' ' + dclass) );

    printsingle( filename, dn, name2, ddata, title2, vAxis2, hAxis2, headers, classes22 )
  }
};






function hideAllFilenames(){
  var flds = document.getElementsByTagName('*');
  for ( var f in flds ) {
     if ( ( ' ' + flds[f].className + ' ').indexOf(" filename ") > 1 ) {
       flds[f].style.visibility = 'hidden';
     }
  }
}

function selchange() {
  var x = document.getElementById("selector").selectedIndex;
  var v = document.getElementsByTagName("option")[x].value;
  if ( v == "_NONE_" ) {
    //hideAllFilenames();
    deletedata();
  } else {
    //hideAllFilenames();

    //alert( v );
    deletedata();
    showdata( v );
  }
}

function deletedata() {
  var el = document.getElementById( 'display' );
  if ( el ) {
    el.parentNode.removeChild( el );
  }
}

function add(a, b) {
    return a + b;
}

function arrayMedian( arr ) {
  var sum = arr.reduce(add, 0);
  if (sum == 0) {
    return -1;
  }
  var mid = sum / 2.0;
  var cum = 0;
  for ( var i = 0; i < arr.length; ++i ) {
    cum += arr[i];
    if ( cum >= mid ) {
      return i + 1;
    }
  }
  return arr.length;
}

function mergeArr( p, c, i, a ) {
  //console.log('p',p,'c',c,'i',i,'a',a);
  var res = [];
  res.length = p.length;
  
  for ( var q = 0; q < res.length; ++q ) {
    res[q] = p[q] + c[q];
  }
  return res;
}

//http://derickbailey.com/2014/09/21/calculating-standard-deviation-with-array-map-and-array-reduce-in-javascript/
function standardDeviation(values){
  var avg = average(values);
  
  var squareDiffs = values.map(function(value){
    var diff    = value - avg;
    var sqrDiff = diff * diff;
    return sqrDiff;
  });
  
  var avgSquareDiff = average(squareDiffs);
 
  var stdDev = Math.sqrt(avgSquareDiff);
  return stdDev;
}
 
function average(data){
  var sum = data.reduce(function(sum, value){
    return sum + value;
  }, 0);
 
  var avg = sum / data.length;
  return avg;
}








var dst_div = 'chart_div';

function showdata( filename ) {
  var filedata = window.dataall[ filename ];
  var divname  = fixStr( filename );
  console.log(" ", divname, filedata);

  var displaydiv = createDiv( dst_div   , "display"          , [] );

  var ndivname   = createDiv(   displaydiv, divname            , [ "l0", "filename" ] );

  var header     = createDiv(   ndivname, divname + '_header', [ "l0", "filename", "lbl1" ] );
  document.getElementById( header ).innerHTML = filename;

  var countdata        = filedata.count;
  var distancedata     = filedata.dist;
  var formatdata       = filedata.format;
  var infodata         = filedata.info;
  var polymorphismdata = filedata.polytype;
  var qualitydata      = filedata.qual;

  //console.log( "  count"   , countdata        );
  //console.log( "  distance", distancedata     );
  //console.log( "  format"  , formatdata       );
  //console.log( "  info"    , infodata         );
  //console.log( "  poly"    , polymorphismdata );
  //console.log( "  qualy"   , qualitydata      );

  name = "Count";        fname=fixStr(name); printcount(  filename, ndivname, name, countdata       , filename + ' - ' + name, name, 'Chromosome', ['Chromosome', 'Count']                    , [ "l1", "count"                ] );
  name = "Distance";     fname=fixStr(name); printsingle( filename, ndivname, name, distancedata    , filename + ' - ' + name, name, 'Chromosome', ['Chromosome', 'Min', 'Low', 'High', 'Max'], [ "l1", fname ]                  );
  name = "Quality";      fname=fixStr(name); printsingle( filename, ndivname, name, qualitydata     , filename + ' - ' + name, name, 'Chromosome', ['Chromosome', 'Min', 'Low', 'High', 'Max'], [ "l1", fname ], [ 'l2', fname ] );
  name = "Format";       fname=fixStr(name); printdouble( filename, ndivname, name, formatdata      , filename + ' - ' + name, name, 'Chromosome', ['Chromosome', 'Min', 'Low', 'High', 'Max'], [ "l1", fname ], [ 'l2', fname ] );
  name = "Info";         fname=fixStr(name); printdouble( filename, ndivname, name, infodata        , filename + ' - ' + name, name, 'Chromosome', ['Chromosome', 'Min', 'Low', 'High', 'Max'], [ "l1", fname ], [ 'l2', fname ] );
  name = "Polymorphism"; fname=fixStr(name); printdouble( filename, ndivname, name, polymorphismdata, filename + ' - ' + name, name, 'Chromosome', ['Chromosome', 'Min', 'Low', 'High', 'Max'], [ "l1", fname ], [ 'l2', fname ] );

  document.getElementById(ndivname).style.visibility = 'visible';
}






function showtree(dbname, algo, scale, method, col, distSppName) {
  //
  // INITIALIZE
  //
  //console.log( "parsing tree", tree_str );
  console.log( "parsing tree");
  var numNewickElements = 0;
  var numNewickNodes    = 0;
  var numNewickBranches = 0;
  var max_len           = 0;
  var val_min           = 0;
  var val_max           = 0;
  var val_min_str       = "";
  var val_max_str       = "";
  var cols              = null;
  var max_node_str_len  = 0;
  
  

  //
  // CALCULATE MIN AND MAX FROM THE DESIRED DATA COLUMN
  //
  if (col === 'null') {
    col = null;
  }
  else if (col) {
    console.log('col',col);

    if (col === 'Distance') {
      console.log( 'Distance' );
      
      if (!distSppName) { // created element
        return;
      } else { // has element selected.
        var sppId = window.dataall[dbname]["in_filenames"].indexOf(distSppName);
        cols = window.dataall[dbname][col][sppId];
        console.log("spp name", distSppName, "cols", cols);
      }
    } else {
      cols      = window.dataall[dbname][col];
    }

    val_min   = Math.min.apply(null, cols );
    val_max   = Math.max.apply(null, cols );
  
    if (val_min == Math.floor(val_min)) {
      val_min_str  = numberWithCommas( val_min )
    } else {
      val_min_str  = numberWithCommas( val_min.toFixed(2) )
    }
  
    if (val_max == Math.floor(val_max)) {
      val_max_str  = numberWithCommas( val_max )
    } else {
      val_max_str  = numberWithCommas( val_max.toFixed(2) )
    }
  } else {
    console.log("col is null");
  }
  



  //
  // GET DATA AND TARGET
  //
  var tree_str = window.dataall[dbname]["trees"][algo][scale][method];
  var dst      = document.getElementById( TREE_PLACE_ID );
  while (dst.hasChildNodes()) {
    dst.removeChild(dst.lastChild);
  }
  dst.innerHtml = 'clean';
  var newick            = Newick.parse( tree_str );

  
  //var dstd = document.createElement('div');
  //dstd.setAttribute( "id", TREE_PLACE_ID + '_DIV');
  
  //dst.appendChild( dstd ); 
  
  //alert(dbname + " " + algo + " " + scale + " " + method);
  //console.log( tree_str );
  //phylocanvas = new Smits.PhyloCanvas(
  //    { newick: tree_str },      // Newick or XML string
  //    TREE_PLACE_ID, // Div Id where to render
  //    1000, 1000     // Height, Width in pixels
  //);
  
  
  
  
  







  //
  // COUNT NODES AND ADD EXTRA DATA
  //
  function buildNewickNodes(node, callback) {
    ++numNewickElements;
    if (node.branchset) {
      ++numNewickBranches;
      for (var i=0; i < node.branchset.length; i++) {
        buildNewickNodes(node.branchset[i])
      }
    } else {
      ++numNewickNodes;
      if ( node.name.length > max_len ) {
        max_len = node.name.length;
      }

      node.length = parseFloat(node.length.toFixed(4));
      
      if (col) {
        var nname1 = node.name;
        var nname2 = node.name.replace(/_/g, ' ');
        var i1     = window.dataall[dbname]['in_filenames'].indexOf(nname1);
        var i2     = window.dataall[dbname]['in_filenames'].indexOf(nname2);
        var i      = i1 == -1 ? i2 : i1;
        //var vals  = window.dataall[dbname][col           ];
        if ( i == -1 ) {
          console.log("error converting '" + node.name + "' to '" + nname + "' not in ", window.dataall[dbname]['in_filenames']);
        } else {
          node.val  = cols[i];
          if (node.val == Math.floor(node.val)) {
            //console.log("val",node.val,"floor",Math.floor(node.val));
            node.str  = numberWithCommas( node.val );
          } else {
            //console.log("val",node.val,"floor",Math.floor(node.val),"tofixed",numberWithCommas( node.val.toFixed(2) ));
            node.str  = numberWithCommas( node.val.toFixed(2) );
            node.val  = node.val.toFixed(4);
          }
          
          if (node.str.length > max_node_str_len) {
            max_node_str_len = node.str.length;
          }
          
          //console.log('val', node.val, 'min', val_min, 'max', val_max, 'delta', ( val_max - val_min ), 'diff', ( node.val - val_min ), 'prop', ( ( node.val - val_min ) / ( val_max - val_min ) ), 'size', BARMAXLENGTH * ( ( node.val - val_min ) / ( val_max - val_min ) ));
          node.size = BARMAXLENGTH * ( ( node.val - val_min ) / ( val_max - val_min ) );
        }
      }
    }
  }
  

  console.log( "building nodes" );
  buildNewickNodes(newick)
  //console.log("newick"           , newick           );
  console.log("numNewickNodes"   , numNewickNodes   );
  console.log("numNewickBranches", numNewickBranches);
  console.log("numNewickElements", numNewickElements);





  //
  // CALCULATE DIMENTIONS
  //
  var theight    = numNewickNodes * treeFontHeight * 1.7; //10px
  var twidth     = (max_len * (treeFontHeight/2));// + (newickNodes.length * (treeFontHeight/3));
  if (twidth < theight / 5) {
    twidth = theight / 5;
  }
  console.log( "building phylogram" );
  
  
  
  
  
  //
  // CREATE DOWNLOAD LINK
  //
  //console.log( html );
  var tree_dld = d3.select("#"+TREE_DOWNLOAD_ID);
  tree_dld.html("");

  //d3.select("#"+TREE_DOWNLOAD_ID).selectAll("*").remove();
  tree_dld.append("a")
      .attr("id"    , "download")
      .attr("target", "_blank"  )
      .attr("class" , "lnk"     )
      .html("Download")
      .on("click", function(){
        var html = d3.select('#'+TREE_PLACE_ID).select('svg')
            .attr("title"  , title)
            .attr("version", 1.2)
            .attr("xmlns"  , "http://www.w3.org/2000/svg")
            .node().parentNode.innerHTML;
        
        window.open("data:image/svg+xml;base64," + btoa(html))
          
        d3.event.stopPropagation();
      })
      
  
  
  
  //
  // CREATE TREE
  //
  d3.phylonator.build('#'+TREE_PLACE_ID, newick, {
      width                  : twidth,
      height                 : theight,
      skipTicks              :  document.getElementById(TREE_TICKS_ID).checked,
      skipBranchLengthScaling: !document.getElementById(TREE_SCALE_ID).checked,
      skipLabels             : false
  });
  



  //
  // POPULATE BARS
  //
  var svg_len = 0;
  if (col) {
    var labelMaxLen = 0;
    
    d3.select('#'+TREE_PLACE_ID).selectAll('text')
      .text( function(d) { if (this.innerHTML.length > labelMaxLen) { labelMaxLen = this.innerHTML.length; }; return this.innerHTML; } );
    console.log( "labelMaxLen ", labelMaxLen );
  
    var cmap = {};
    for ( var c in cols ) {
      cmap[ window.dataall[dbname]['in_filenames'      ][c] ] = cols[c];
    }
  
    var bar_x = (labelMaxLen * (treeFontHeight / 2)) + (treeFontHeight*2);
    d3.select('#'+TREE_PLACE_ID).selectAll('g.leaf.node')
      .append('rect')
        .attr('x'     ,  bar_x )
        .attr('y'     ,  -0.5 * treeFontHeight)
        .attr('height',  treeFontHeight * .8)
        .attr('width' ,  function(d) {
          return d.data.size;
        });

    var txt_len = (max_node_str_len*(treeFontHeight/2));
    var txt_x   = bar_x + BARMAXLENGTH + (treeFontHeight*2) + txt_len;
    d3.select('#'+TREE_PLACE_ID).selectAll('g.leaf.node')
      .append('text')
        .attr('dx'         ,  txt_x )
        .attr('dy'         ,  3     )
        .attr("text-anchor", "end"  )
        .attr('font-family', 'Helvetica Neue, Helvetica, sans-serif')
        .attr('font-size'  , treeFontHeight+'px' )
        .attr('fill'       , 'black')
        .text(function(d) {
          return d.data.str;
        });

    svg_len = twidth + 300 + BARMAXLENGTH + txt_len;
    d3.select('#'+TREE_PLACE_ID).select('svg')
        .attr("width", svg_len);
  }

  
  
  //
  // ADD TITLE
  //
  var title    = dbname + " : " + algo + " : " + scale + " : " + method;
  if (!document.getElementById(TREE_SCALE_ID).checked) { title += " : no scaling"; };
  if (col                                            ) {
    if (col === 'Distance') {
      title += " :: " + col + " to " + distSppName + " ("+val_min_str+"<->"+val_max_str+")";
    } else {
      title += " :: " + col + "("+val_min_str+"<->"+val_max_str+")";
    }
  };
    
  var titleLen = title.length;

  d3.select('#'+TREE_PLACE_ID).select('svg').select('g').select('g')
    .append("text")
      .attr('dx'         ,  0      )
      .attr('dy'         ,  function(d) {console.log("label this", this.parentNode.getBoundingClientRect().height); return this.parentNode.getBoundingClientRect().height + treeFontHeight;})
      .attr("text-anchor", "start" )
      .attr('font-family', 'Helvetica Neue, Helvetica, sans-serif')
      .attr('font-size'  , treeFontHeight+'px'  )
      .attr('fill'       , 'black' )
      .text( title  );

  if ( ( titleLen > svg_len ) && (titleLen > (twidth+300)) ) {
    d3.select('#'+TREE_PLACE_ID).select('svg')
        .attr("width", titleLen);
  }
  
  
 
  console.log( "finished" );
}



function test_showtree(dbname) {
  console.log("test_showtree", dbname);
  
  var col               = document.getElementById(TREE_COL_ID).value;
  var spp               = null;
  
  if (col === 'Distance') {
    var sels              = document.getElementById(TREE_COL_DIST_ID);
  
    if (sels) {
      console.log("getting distance name");
      
      var spp = sels.value;
      
      if (spp === 'null') {
        console.log("getting distance name :: null checked");
        spp = null;
      
      } else {
        console.log("getting distance name :: spp checked", spp);
      }
    } else { // create specie selector
      var in_filenames       = window.dataall[dbname]['in_filenames'      ];
      var selS               = document.createElement('select');
      selS.setAttribute( "id"  , TREE_COL_DIST_ID );
      selS.onchange          = function() { test_showtree(dbname); };
    
      var optN = document.createElement("option");
      optN.innerHTML = 'select';
      optN.value     = null;
      selS.appendChild( optN );
    
      for (var s in in_filenames) {
        var opt       = document.createElement("option");
        opt.innerHTML = in_filenames[s];
        opt.value     = in_filenames[s];
        selS.appendChild( opt );
      }

      var tr_cD               = document.getElementById(TREE_COL_DIST_TR);
      var td_cD_1             = document.createElement('td'); tr_cD.appendChild( td_cD_1 ); td_cD_1.innerHTML = "Show Distance"; td_cD_1.colSpan = 2;
      var td_cD_2             = document.createElement('td'); tr_cD.appendChild( td_cD_2 ); td_cD_2.appendChild( selS );

      return;
    }
  } else {
    var sels              = document.getElementById(TREE_COL_DIST_ID);
  
    if (sels) {
      var tr_cD               = document.getElementById(TREE_COL_DIST_TR);
      tr_cD.innerHTML = "";
    }
  }
  
  
  
  
  //
  // CHECK WHETHER ALL COMPULSORY FIELDS HAVE BEEN FILLED
  //
  var sels = document.getElementsByName(TREE_SELECT_NAME);
  //console.log(sels       );
  //console.log(sels.length);
  
  for ( var s = 0; s < sels.length; ++s ) {
    var sel = sels[s];
    if ( sel.checked ) {
      //console.log(sel);
      
      //var dbname = sel.getAttribute("dbname");
      var algo   = sel.getAttribute("algo"  );
      var scale  = sel.getAttribute("scale" );
      var method = sel.getAttribute("value" );
      
      showtree(dbname, algo, scale, method, col, spp);
      
      //alert("testing " + dbname + " " + algo + " " + scale + " " + method );
    }
  }  
}


function toggle_visibility(e) {
  //console.log("toggle_visibility", "this", this);
  //console.log("toggle_visibility", "e", e);
  var tgt_id = this.getAttribute('vis_tgt');
  //console.log("toggle_visibility", "tgt_id", tgt_id);
  if (tgt_id) {
    var tgt    = document.getElementById(tgt_id);
    //console.log("toggle_visibility", "tgt", tgt);
    if (tgt) {
      var vis    = tgt.style.visibility;
      //console.log("toggle_visibility", "vis", vis);
      if (vis == "hidden") {
        tgt.style.visibility = "visible";
        tgt.style.display    = "block";
        this.setAttribute("class", "up");
      } else if (vis == "" || vis == "visible") {
        tgt.style.visibility = "hidden";
        tgt.style.display    = "none";
        this.setAttribute("class", "down");
      }
    }
  }
}









//http://commons.wikimedia.org/wiki/File:Black_Arrow_Down.svg

function getArrow( dst, tgt, isopen ) {
  isopen = (typeof isopen === "undefined") ? true : isopen;
  
  var svg = d3.select( dst )
    .append("svg")
      //.attr("xmlns:xlink","http://www.w3.org/1999/xlink")
      .attr("xmlns"      ,"http://www.w3.org/2000/svg")
      .attr("class"      ,"up")
      .attr("width"      ,"15pt")
      .attr("height"     ,"15pt")
      .attr("viewBox"    ,"0 0 560 560")
      .attr("vis_tgt"    ,tgt)
      .on("click", toggle_visibility);

  svg.append("g")
        .attr("transform","translate(-0.511702, 8e-07)")
        .attr("style","fill:#161413; fill-rule:evenodd; stroke:none; stroke-width:1; stroke-linecap:butt; stroke-linejoin:miter; stroke-dasharray:none;")
        .append("path")
          .attr("d","M560.512 0.570216 C560.512 2.05696 280.518 560.561 280.054 560 C278.498 558.116 0 0.430888 0.512416 0.22416 C0.847112 0.089136 63.9502 27.1769 140.742 60.4192 C140.742 60.4192 280.362 120.86 280.362 120.86 C280.362 120.86 419.756 60.4298 419.756 60.4298 C496.422 27.1934 559.456 0 559.831 0 C560.205 0 560.512 0.2566 560.512 0.570216 Z");

  if (!isopen) {
    var e = new Event('click');
    //e.initUIEvent('click', true, true);
    svg.node().dispatchEvent(e);
  }
}

function onLoad() {
  console.log(window.dataall);
  //
  // GET GLOBAL VARIABLES
  //
  var dbs    = Object.keys(window.dataall);
  var dbname = dbs[0];
  var header = {
    "DB name"            : dbname,
    "Number Registers"   : numberWithCommas( window.dataall[dbname]['complete_registers'] ),
    "Kmer Size"          : window.dataall[dbname]['kmer_size'         ],
    "Min Shared"         : window.dataall[dbname]['min_val'           ],
    "Max Shared"         : window.dataall[dbname]['max_val'           ],
    "Number Samples"     : window.dataall[dbname]['num_infiles'       ],
    "Number Input Files" : window.dataall[dbname]['num_srcfiles'      ],
    "Save Every"         : window.dataall[dbname]['save_every'        ],
  };
  
  var num_infiles        = window.dataall[dbname]['num_infiles'       ];
  var num_srcfiles       = window.dataall[dbname]['num_srcfiles'      ];
  var src_filenames      = window.dataall[dbname]['src_filenames'     ];
  var in_filenames       = window.dataall[dbname]['in_filenames'      ];
  var num_kmer_total_spp = window.dataall[dbname]['num_kmer_total_spp'];
  var num_kmer_valid_spp = window.dataall[dbname]['num_kmer_valid_spp'];

  var header_sel         = document.getElementById( "header" );


  //
  // PRINT STATS
  //
  var h1                 = document.createElement('h1'); h1  .innerHTML = "Cnidaria Stats :: " + dbname; header_sel.appendChild( h1   );
  var h2_h               = document.createElement('h2'); h2_h.innerHTML = "General";                     header_sel.appendChild( h2_h );
  var tbl_h              = document.createElement('table');
  tbl_h.setAttribute("id", "tbl_header");
  
  //console.log(window.dataall);
  console.log("adding header");
  for ( var h_key in header ) {
    console.log("adding header :: " + h_key + " " + header[h_key]);
    var tr  = document.createElement('tr')
    var td1 = document.createElement('td'); td1.innerHTML = h_key;         td1.setAttribute( "class", "td_cell"  );
    var td2 = document.createElement('td'); td2.innerHTML = header[h_key]; td2.setAttribute( "class", "td_number");
    tr.appendChild( td1 );
    tr.appendChild( td2 );
    tbl_h.appendChild( tr );
  }
  header_sel.appendChild( tbl_h );
  getArrow(h2_h, "tbl_header");
  

  
  


  //
  // PRINT SOURCE FILES
  //
  var h2_s               = document.createElement('h2'); h2_s.innerHTML = "Source Files";                 header_sel.appendChild( h2_s );
  var tbl_s              = document.createElement('table');
  tbl_s.setAttribute('id', 'tbl_source_files');
  
  for (var i = 0; i < num_srcfiles; ++i) {
    var tr  = document.createElement('tr');
    var td1 = document.createElement('td'); td1.innerHTML = src_filenames[i]; td1.setAttribute( "class", "td_cell"  );
    tr.appendChild( td1 );
    tbl_s.appendChild( tr );
  }
  header_sel.appendChild( tbl_s );
  getArrow(h2_s, "tbl_source_files", false);

  
  


  //
  // GATHER ALL STATS PER FILE
  //
  var avai_headers = ["total kmers", "shared kmers", "% shared kmers", "Max Shared", "Min Shared", "Avg Shared", "StdDev Shared", "Max Jaccard Dist", "Min Jaccard Dist", "Avg Jaccard Dist", "StdDev Jaccard Dist", "Median Number of Shares"];
  window.dataall[dbname]["avai_headers"] = avai_headers;

  for (var a in avai_headers) {
    window.dataall[dbname][avai_headers[a]]        = [];
    window.dataall[dbname][avai_headers[a]].length = num_infiles;
  }
  
  window.dataall[dbname]["Distance"]        = [];
  window.dataall[dbname]["Distance"].length = num_infiles;
  
  for (var i = 0; i < num_infiles; ++i) {
    var perc_shared_kmers = ((num_kmer_valid_spp[i] * 1.0) / num_kmer_total_spp[i] * 100);

    var vals_raw     = [];
    var vals_jac     = [];
    var vals_shr     = window.dataall[dbname]['matrix'][i].reduce( mergeArr );
    var vals_raw_med = arrayMedian( vals_shr );
    //console.log("median", in_filenames[i], vals_raw_med)
    
    
    for (var j = 0; j < num_infiles; ++j) {
      var val_arr = window.dataall[dbname]['matrix'][i][j];
      var val     = val_arr.reduce(add, 0);
      var jac     = ( val / (( num_kmer_valid_spp[i] + num_kmer_valid_spp[j] - val ) * 1.0) );
      vals_raw.push(   val     );
      vals_jac.push(   jac     );
    }

    var vals_raw_max = Math.max.apply(null,                    vals_raw );
    var vals_raw_min = Math.min.apply(null,                    vals_raw );
    var vals_raw_avg =                      average(           vals_raw );
    var vals_raw_dev =                      standardDeviation( vals_raw );
    
    var vals_jac_max = Math.max.apply(null,                    vals_jac );
    var vals_jac_min = Math.min.apply(null,                    vals_jac );
    var vals_jac_avg =                      average(           vals_jac );
    var vals_jac_dev =                      standardDeviation( vals_jac );

    window.dataall[dbname]["total kmers"            ][i] = num_kmer_valid_spp[i];
    window.dataall[dbname]["shared kmers"           ][i] = num_kmer_total_spp[i];
    window.dataall[dbname]["% shared kmers"         ][i] = perc_shared_kmers;
    window.dataall[dbname]["Max Shared"             ][i] = vals_raw_max;
    window.dataall[dbname]["Min Shared"             ][i] = vals_raw_min;
    window.dataall[dbname]["Avg Shared"             ][i] = vals_raw_avg;
    window.dataall[dbname]["StdDev Shared"          ][i] = vals_raw_dev;
    window.dataall[dbname]["Max Jaccard Dist"       ][i] = vals_jac_max;
    window.dataall[dbname]["Min Jaccard Dist"       ][i] = vals_jac_min;
    window.dataall[dbname]["Avg Jaccard Dist"       ][i] = vals_jac_avg;
    window.dataall[dbname]["StdDev Jaccard Dist"    ][i] = vals_jac_dev;
    window.dataall[dbname]["Median Number of Shares"][i] = vals_raw_med;
    window.dataall[dbname]["Distance"               ][i] = vals_jac;
  }

  
  





  //
  // PRINT STATS PER FILE
  //
  var h2_i               = document.createElement('h2'); h2_i.innerHTML = "Samples";                      header_sel.appendChild( h2_i );
  var tbl_i              = document.createElement('table');
  tbl_i.setAttribute("id", "tbl_infiles");

  var th                 = document.createElement('tr');
  var td_titles          = [ "sample name", "total kmers", "shared kmers", "% shared kmers", "Max Shared", "Min Shared", "Avg Shared", "StdDev Shared", "Max Jaccard Dist", "Min Jaccard Dist", "Avg Jaccard Dist", "StdDev Jaccard Dist", "Median Number of Shares"];
  for (var i = 0; i < td_titles.length; ++i) {
    var td1 = document.createElement('th'); td1.innerHTML = td_titles[i]; td1.setAttribute( "class", "td_cell"  ); th.appendChild( td1 );
  }
  tbl_i.appendChild( th );

  
  for (var i = 0; i < num_infiles; ++i) {
    var tr  = document.createElement('tr')
    if (i % 2 == 1) {
      tr.setAttribute( "class", "band");
    }

    var td1  = document.createElement('td'); td1 .innerHTML = in_filenames[i];                                                                            td1 .setAttribute( "class", "td_cell"  ); tr.appendChild( td1  );
    var td2  = document.createElement('td'); td2 .innerHTML = numberWithCommas( num_kmer_total_spp[i]                                                );   td2 .setAttribute( "class", "td_number"); tr.appendChild( td2  );
    var td3  = document.createElement('td'); td3 .innerHTML = numberWithCommas( num_kmer_valid_spp[i]                                                );   td3 .setAttribute( "class", "td_number"); tr.appendChild( td3  );
    var td4  = document.createElement('td'); td4 .innerHTML =                   window.dataall[dbname]["% shared kmers"         ][i].toFixed(2) + " %";   td4 .setAttribute( "class", "td_number"); tr.appendChild( td4  );
    var td5  = document.createElement('td'); td5 .innerHTML = numberWithCommas( window.dataall[dbname]["Max Shared"             ][i]                 );   td5 .setAttribute( "class", "td_number"); tr.appendChild( td5  );
    var td6  = document.createElement('td'); td6 .innerHTML = numberWithCommas( window.dataall[dbname]["Min Shared"             ][i]                 );   td6 .setAttribute( "class", "td_number"); tr.appendChild( td6  );
    var td7  = document.createElement('td'); td7 .innerHTML = numberWithCommas( window.dataall[dbname]["Avg Shared"             ][i].toFixed(2)      );   td7 .setAttribute( "class", "td_number"); tr.appendChild( td7  );
    var td8  = document.createElement('td'); td8 .innerHTML = numberWithCommas( window.dataall[dbname]["StdDev Shared"          ][i].toFixed(2)      );   td8 .setAttribute( "class", "td_number"); tr.appendChild( td8  );
    var td9  = document.createElement('td'); td9 .innerHTML =                   window.dataall[dbname]["Max Jaccard Dist"       ][i].toFixed(2);          td9 .setAttribute( "class", "td_number"); tr.appendChild( td9  );
    var td10 = document.createElement('td'); td10.innerHTML =                   window.dataall[dbname]["Min Jaccard Dist"       ][i].toFixed(2);          td10.setAttribute( "class", "td_number"); tr.appendChild( td10 );
    var td11 = document.createElement('td'); td11.innerHTML =                   window.dataall[dbname]["Avg Jaccard Dist"       ][i].toFixed(2);          td11.setAttribute( "class", "td_number"); tr.appendChild( td11 );
    var td12 = document.createElement('td'); td12.innerHTML =                   window.dataall[dbname]["StdDev Jaccard Dist"    ][i].toFixed(2);          td12.setAttribute( "class", "td_number"); tr.appendChild( td12 );
    var td13 = document.createElement('td'); td13.innerHTML = numberWithCommas( window.dataall[dbname]["Median Number of Shares"][i]                 );   td13.setAttribute( "class", "td_number"); tr.appendChild( td13 );

    
    /*
    for (var j = 0; j < num_infiles; ++j) {
      //var td5 = document.createElement('td'); td5.innerHTML = numberWithCommas( window.dataall[dbname]['matrix'][i][j].reduce(add, 0) );                                          td5.setAttribute( "class", "td_number");
      var val = window.dataall[dbname]['matrix'][i][j].reduce(add, 0);
      var jac = ( val / (( num_kmer_valid_spp[i] + num_kmer_valid_spp[j] - val ) * 1.0) );
      var td5 = document.createElement('td'); td5.innerHTML = jac.toFixed(3);                                          td5.setAttribute( "class", "td_number");
      tr.appendChild( td5 );
    }
    */
    tbl_i.appendChild( tr );
  }
  header_sel.appendChild( tbl_i );
  getArrow(h2_i, "tbl_infiles", false);





  //
  // PRINT TREE
  //
  var h2_t                = document.createElement('h2'); h2_t.innerHTML = "Trees";                      header_sel.appendChild( h2_t );
  
  var tbl_i               = document.createElement('table');
  var tr_i                = document.createElement('tr'); tbl_i.appendChild( tr_i );
  var td_i_1              = document.createElement('td'); tr_i.appendChild( td_i_1 ); td_i_1.setAttribute( "class", "treeblock");
  var td_i_2              = document.createElement('td'); tr_i.appendChild( td_i_2 ); td_i_2.setAttribute( "class", "treeblock");
  td_i_2.setAttribute( "id", TREE_PLACE_ID );

  var tbl_t               = document.createElement('table'); td_i_1.appendChild( tbl_t );
  


  
  
  //
  // PRINT TREE :: OPTIONS
  //  
  //
  // PRINT TREE :: OPTIONS :: SKIP BRANCH
  //  
  var selB                = document.createElement('input');
  selB.setAttribute( "type", "checkbox"    );
  selB.setAttribute( "id"  , TREE_SCALE_ID );
  selB.onchange = function() { test_showtree(dbname); };
  var tr_cB               = document.createElement('tr'); tbl_t.appendChild( tr_cB );
  var td_cB_1             = document.createElement('td'); tr_cB.appendChild( td_cB_1 ); td_cB_1.innerHTML = "Skip Branch Length Scaling"; td_cB_1.colSpan = 2;
  var td_cB_2             = document.createElement('td'); tr_cB.appendChild( td_cB_2 ); td_cB_2.appendChild( selB );
  
  


  //
  // PRINT TREE :: OPTIONS :: SKIP TICKS
  //  
  var selT               = document.createElement('input');
  selT.setAttribute( "type", "checkbox"    );
  selT.setAttribute( "id"  , TREE_TICKS_ID );
  selT.onchange = function() { test_showtree(dbname); };
  selT.checked  = true;
  var tr_cT               = document.createElement('tr'); tbl_t.appendChild( tr_cT );
  var td_cT_1             = document.createElement('td'); tr_cT.appendChild( td_cT_1 ); td_cT_1.innerHTML = "Skip Show Ticks"; td_cT_1.colSpan = 2;
  var td_cT_2             = document.createElement('td'); tr_cT.appendChild( td_cT_2 ); td_cT_2.appendChild( selT );
  
  


  //
  // PRINT TREE :: OPTIONS :: STATS TO SHOW
  //  
  var selS               = document.createElement('select');
  selS.setAttribute( "id"  , TREE_COL_ID );
  selS.onchange = function() { test_showtree(dbname); };
  //selT.checked = true;

  var optN = document.createElement("option");
  optN.innerHTML = 'select';
  optN.value     = null;
  selS.appendChild( optN );

  var optD = document.createElement("option");
  optD.innerHTML = 'Distance';
  optD.value     = 'Distance';
  selS.appendChild( optD );

  for (var s in avai_headers) {
    var opt = document.createElement("option");
    opt.innerHTML = avai_headers[s];
    opt.value     = avai_headers[s];
    selS.appendChild( opt );
  }
  var tr_cS               = document.createElement('tr'); tbl_t.appendChild( tr_cS );
  var td_cS_1             = document.createElement('td'); tr_cS.appendChild( td_cS_1 ); td_cS_1.innerHTML = "Show Stats"; td_cS_1.colSpan = 2;
  var td_cS_2             = document.createElement('td'); tr_cS.appendChild( td_cS_2 ); td_cS_2.appendChild( selS );

  var tr_cD               = document.createElement('tr'); tbl_t.appendChild( tr_cD );   tr_cD.setAttribute( "id"  , TREE_COL_DIST_TR );

  
  


  //
  // PRINT TREE :: OPTIONS :: TYPE
  //  
  //
  // PRINT TREE :: OPTIONS :: TYPE :: HEADER
  //
  var tr_v                = document.createElement('tr'  );  tbl_t.appendChild(  tr_v   );
  var td_v_1              = document.createElement('td'  );  tr_v.appendChild(   td_v_1 ); td_v_1.colSpan = 3;
  var tb_v                = document.createElement('form');  td_v_1.appendChild( tb_v   ); tb_v.setAttribute( "id"  , TREE_SELECT_ID );
  tb_v.onchange = function() { test_showtree(dbname); };
  var tbl_v               = document.createElement('table'); tb_v.appendChild(   tbl_v  );

  var tr_cH               = document.createElement('tr'); tbl_v.appendChild( tr_cH );
  var td_cH_1             = document.createElement('th'); tr_cH.appendChild( td_cH_1 ); td_cH_1.innerHTML = "Algorithm";
  var td_cH_2             = document.createElement('th'); tr_cH.appendChild( td_cH_2 ); td_cH_2.innerHTML = "Scale";
  var td_cH_3             = document.createElement('th'); tr_cH.appendChild( td_cH_3 ); td_cH_3.innerHTML = "Distance";
    
  
  
  
  
  //
  // PRINT TREE :: OPTIONS :: TYPE :: VALUES
  //  
  var rnum                 = 0;
  for ( var algo   in window.dataall[dbname]["trees"]              ) {
    ++rnum;
    
    var tr_t_a             = document.createElement('tr'); tbl_v.appendChild(  tr_t_a );
    var td_a_1             = document.createElement('td'); tr_t_a.appendChild( td_a_1 ); td_a_1.innerHTML = algo;
    var td_a_2             = document.createElement('td'); tr_t_a.appendChild( td_a_2 ); td_a_2.colSpan   = 2;
    //var td_a_3             = document.createElement('td'); tr_t_a.appendChild( td_a_3 );
    //if (rnum == 1) {
    //  var td_a_4           = document.createElement('td'); tr_t_a.appendChild( td_a_4 );
    //  var stkey      = Object.keys( window.dataall[dbname]["trees"]                 )[0];
    //  var stndkey    = Object.keys( window.dataall[dbname]["trees"][stkey]          )[0];
    //  var stLen      = Object.keys( window.dataall[dbname]["trees"]                 ).length;
    //  var ndLen      = Object.keys( window.dataall[dbname]["trees"][stkey]          ).length;
    //  var rdLen      = Object.keys( window.dataall[dbname]["trees"][stkey][stndkey] ).length;
    //  var numRows    = stLen + stLen * ndLen + stLen * ndLen * rdLen;
    //  td_a_4.rowSpan = numRows;
    //  td_a_4.setAttribute( "id", TREE_PLACE_ID );
    //}

    
    for ( var scale  in window.dataall[dbname]["trees"][algo]        ) {
      var tr_t_s           = document.createElement('tr'); tbl_v.appendChild(  tr_t_s );
      var td_s_1           = document.createElement('td'); tr_t_s.appendChild( td_s_1 ); 
      var td_s_2           = document.createElement('td'); tr_t_s.appendChild( td_s_2 ); td_s_2.innerHTML = scale;
      
      for ( var method in window.dataall[dbname]["trees"][algo][scale] ) {
        //var method_a       = document.createElement('a');
        //method_a.innerHTML = method;
        //method_a.onclick   = function(d, a, s, m){ return function() { showtree(d, a, s, m); }; }(dbname, algo, scale, method);
        //method_a.setAttribute( "class", "lnk");
        
        var method_s       = document.createElement('input');
        method_s.setAttribute( "id"    , "radio_"+method  );
        method_s.setAttribute( "type"  , "radio"          );
        method_s.setAttribute( "dbname",  dbname          );
        method_s.setAttribute( "algo"  ,  algo            );
        method_s.setAttribute( "scale" ,  scale           );
        method_s.setAttribute( "value" ,  method          );
        method_s.setAttribute( "name"  , TREE_SELECT_NAME );
        
        var a_method       = document.createElement("label"); a_method.setAttribute("for", "radio_"+method); a_method.innerHTML = method;
        var tr_t_m         = document.createElement('tr'); tbl_v.appendChild(  tr_t_m );
        var td_m_1         = document.createElement('td'); tr_t_m.appendChild( td_m_1 ); td_m_1.colSpan   = 2;
        //var td_m_2         = document.createElement('td'); tr_t_m.appendChild( td_m_2 );
        var td_m_3         = document.createElement('td'); tr_t_m.appendChild( td_m_3 ); td_m_3.appendChild( method_s ); td_m_3.appendChild( a_method );
        
        //var treeStr = window.dataall[dbname]["trees"][algo][scale][method];
      }
    }
  }
  header_sel.appendChild( tbl_i );
  
  
  
  //
  // PRINT TREE :: OPTIONS :: DOWNLOAD
  //  
  var tr_cD               = document.createElement('tr'); tbl_t.appendChild( tr_cD );
  var td_cD_1             = document.createElement('td'); tr_cD.appendChild( td_cD_1 ); td_cD_1.innerHTML = "Download"; td_cD_1.setAttribute( "id"  , TREE_DOWNLOAD_ID ); td_cD_1.colSpan = 3;
}