gen_average_report  <- function(matrix_data) {
  means <- apply(matrix_data, 1, mean, na.rm=TRUE)
  sds   <- apply(matrix_data, 1, sd  , na.rm=TRUE)
  
  matrix_average <- t(matrix(c(means, sds), ncol=length(matrix_data[,1]), nrow=2, byrow=T))
  
  #   print(head(json_data$matrix_average, n=1))
  
  colnames(matrix_average) <- c("average", "std_dev")
  rownames(matrix_average) <- rownames(matrix_data)
  
  return(matrix_average)
}


center_matrix       <- function(dat) {
  mi  <- min(dat, na.rm=T)
  #     mi  <- apply(dat, 2, function(x) { min(x, na.rm=T) } )
  print(paste("min ", mi))
  
  ma  <- max(dat, na.rm=T)
  #     ma  <- apply(dat, 2, function(x) { max(x, na.rm=T) } )
  print(paste("max ", ma))
  
  di  <- ma - mi
  print(paste("diff", di))
  
  print("subtracting")
  # dat <- ((2*( dat - mi )) / di)-1
  res <- ( dat - mi )
  res <- ( res / di )
  res[is.nan(res)] = 0
  print(head(res, n=1))
  
  print("returning")
  return(res)
}


plot_average_report <- function( matrix_average, BOTTOM_BORDER ) {

  #   d <- qplot(json_data$in_filenames, data=data.frame(json_data$matrix_data))
  #   d + stat_summary
  #   plot(d)
  
#   print(head(matrix_average))
  
  CI.up   <- matrix_average[,1] + matrix_average[,2]
  CI.dn   <- matrix_average[,1] - matrix_average[,2]
#   print(paste("CI up:", CI.up))
#   print(paste("CI dn:", CI.dn))
  
  dev_min <- min(CI.dn, na.rm=TRUE)
  dev_max <- max(CI.up, na.rm=TRUE)
#   print(paste("dev min:", dev_min))
#   print(paste("dev max:", dev_max))
  
  in_filenames <- rownames(matrix_average)
#   print(in_filenames)
  
  x <- 1:length(in_filenames)
  
  op <- par(mar=c(BOTTOM_BORDER,4,4,2))
  
  plot(matrix_average[,1]~x, ylim=c(dev_min,dev_max), cex=1, xaxt='n', xlab='', ylab='Jaccard distance', col='blue', pch=16)
  
  axis(1, at=x, labels=in_filenames, las=2)
  
  arrows(x, CI.dn, x, CI.up, code=3, length=0.05, col="red", angle=90)

  rm(op)
}


gen_dendrogram      <- function(
  matrix_data, of, distfun, dathist,
  cluster_method  = "average",
  filetype        = "pdf",
  pallet          = c("white", "black"),
  pallet_N        =   60,
  cexRow          =   20,
  cexCol          =   20,
  size            = 5120,
  BOTTOM_BORDER   =  5, #20
  RIGHT_BORDER    =  2,  #20
  COLOR_DENS      = "white",
  COLOR_NA        = "white",
  COLOR_TRACE     = "red"
  ) {
  
  
  hclustfun   <- function(x) {
    hclust(x, method=cluster_method)
  }
  
  ?hclust

  hcount      <- dathist$count
  hbreaks     <- dathist$breaks
  hcountT     <- mapply( function(x) { if (x > 0) return(T) else return(F) }, hcount[1:length(hcount)-1])
  datBreaks   <- hbreaks[hcountT == T]
  datCounts   <- hcount[ hcountT == T]
  datCLog     <- sapply(datCounts, log2 )
  datCLog     <- sapply(datCLog  , floor)
  datBreaksF  <- c()
  
  distance    <- distfun(matrix_data)
  clusterD    <- as.hclust(hclustfun(distance))
  dendro      <- as.dendrogram(clusterD, hang = -1)
  Rowv        <- rowMeans(matrix_data, na.rm = T)
  dendro      <- reorder(dendro, Rowv)
  reorderfun  <- function(d,w) { d }  
  rowInd      <- rev(order.dendrogram(dendro))
  colInd      <- rowInd
  dat         <- matrix_data[rowInd, colInd]
#   print("jaccard")
  #   print(head(json_data$matrix_data, n=1))
  #   print(head(dato, n=1))
  #   return
  



  print("plotting dendrogram")
  get_fh( filetype, paste(of, "_tree", sep=""), size )
  # op <- par(cex=0.25)
  # op <- par(mar=c(5,4,4,20))
  print(clusterD)
  print(as.phylo(clusterD))
  plot(as.phylo(clusterD), horiz=T, cex=0.2, cexRow=0.2, cexCol=0.2) #, adj=1, hang=-1, use.edge.length=F, 
#   plot(dendro, horiz=T, cex=0.1, cexRow=0.1, cexCol=0.1, hang=-1)
#   plot(clusterD, horiz=T, cex=0.25)
  dev.off()
  print("dendrogram plotted")


  print("saving newick tree")
  write.tree(as.phylo(clusterD), file=paste(of, "_tree.nwk", sep=""))


  print("plotting heatmap")
  op <- par(mar=c(5,4,4,RIGHT_BORDER))
  
  print("plotting heatmap :: get_fh")
  get_fh( filetype, paste(of, "_heatmap", sep=""), size )
  
  print("plotting heatmap :: get_pallet")
  tryCatch({
    my_palette <- colorRampPalette(pallet)(n = length(datBreaks)-1)
  }, error=function(r){
    print("error generating heatmap")
    print(r)
  } , warning=function(r){
    print("warning generating heatmap")
    print(r)
  }, finally={
    print("finished generating heatmap")
  })

#   if ( is.na(cex) ) {
#     cex = 0.2 + 1/log10(ncol(matrix_data))
#   }

  print(head(dat, n=1))

  print("plotting heatmap :: plotting")
  
  heatmap.2(
    dat,
    cexRow      = cexRow,
    cexCol      = cexCol,
    
    distfun     = distfun,
    hclustfun   = hclustfun,
    reorderfun  = reorderfun,
    
    col         = my_palette,
    
    RowV        = dendro, #dendrogram, 
    ColV        = dendro, #dendrogram,
    density.info="histogram",
    breaks      = datBreaks,
    
    sepcolor    = NA,
    sepwidth    = c(0,0),
    tracecol    = COLOR_TRACE,
    denscol     = COLOR_DENS,
    na.color    = COLOR_NA,
    trace       = "none",
    dendrogram  = "row",
    scale       = "none",
    
    labCol      = T,
    keep.dendro = F,
    symm        = T
  )
    
  rm(op)

  dev.off()
  print("heatmap plotted")
}


plot_j_histo        <- function(matrix_data, filetype, filename, size, breaks) {
  print(paste("saving histogram", filename))
  print(head(matrix_data, n=1))
  get_fh( filetype, filename, size )
  
  dathist   <- hist(matrix_data, breaks=breaks)
  
#   print(paste("+dathist",dathist))

  dev.off()
  
  return(dathist)
}


get_fh              <- function(filetype, fn, size) {
  filename <- paste(fn,".",filetype, sep="")
  print(paste("saving image to:",filename))
  
  if ( filetype == "eps" ) {
    setEPS()
    postscript(filename)#, width=1024, height=1024)
  } else 
    if ( filetype == "png" ) {
      #png("json_jaccard_average.png", width=size, height=size )
      png(filename, width=size, height=size)
  } else 
    if ( filetype == "pdf" ) {
      pdf(filename)#, width=5120, height=5120 )    
  }
}
