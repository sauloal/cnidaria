# if (!require("ggplot2")) {
#   install.packages("ggplot2", dependencies = TRUE)
#   library(ggplot2)
# }


if (!require("ape")) {
  install.packages("ape", dependencies = TRUE)
  library(ape)
}

# if (!require("phangorn")) {
#   install.packages("phangorn", dependencies = TRUE)
#   library(phangorn)
# }
# 
# if (!require("pvclust")) {
#   install.packages("pvclust", dependencies = TRUE)
#   library(pvclust)
# }
# 
# if (!require("mclust")) {
#   install.packages("mclust", dependencies = TRUE)
#   library(mclust)
# }

if (!require("gplots")) {
  install.packages("gplots", dependencies = TRUE)
  library(gplots)
}



# if (!require("RColorBrewer")) {
#   install.packages("RColorBrewer", dependencies = TRUE)
#   library(RColorBrewer)
# }


# if (!require("phangorn")) {
#   install.packages("phangorn", dependencies = TRUE)
#   library(phangorn)
# }


# if (!require("rjson")) {
#   install.packages("rjson", dependencies = TRUE)
#   library(rjson)
# }
# json_file <- "http://webonastick.com/uscl/feeds/uscl.json.txt"
# json_data <- fromJSON(file=json_file)
# .Machine$integer.max


# library(cluster)

source( "jaccard.R"     )
source( "read_titles.R" )
source( "stats.R"       )

to_heapmap <- function (
                          incsv, 
                          countcsv,
                          filetype        = "pdf",
#                           pallet          = c("red"  , "white", "blue"  ),
                          pallet          = c("white", "black"  ),
                          cex             =   20,
                          size            = 5120,
                          cluster_method  = "average",
                          dist_method     = "jaccard",
                          center_data     = F,
                          NA_diagonal     = T,
                          BOTTOM_BORDER   =  5, #20
                          RIGHT_BORDER    =  2  #20
                        ) {
  bn <- basename(incsv)
  bn <- gsub("/", "_", incsv)
  bn <- gsub("\\.", "_", bn    )
  of <- paste("images/csv_", bn, ".", dist_method, sep="")


  
  
  
  
  
  print(paste("opening data csv ", incsv))  
  print(paste("saving to        ", of      ))
  #http://willchernoff.com/2012/09/21/import-csv-adjacency-matrix-with-row-and-column-names-into-r/
  dat <- read.csv(incsv, header=TRUE, sep="\t", stringsAsFactors=FALSE)[,-1]
  # head(dat)
  # tail(dat)
  # length(dat[1,])
  # length(dat[,1])
  # dat[1,]
  # dat[,1]
  
  # cNames<-as.vector(as.character(dat[,1]))       # Get column names
  # cNames
  # length(cNames)
  dat <- apply(as.matrix(dat),2,as.numeric) # Get network matrix
#   print(head(dat))
  # tail(dat)
  # dat[is.na(dat)] <- 0                             # Set missing ties to 0
  # row.names(dat)
  # colnames(dat)
#   colnames(dat) <- cnames
#   return(NA)

  row.names(dat) <- colnames(dat)                    # Give row names
  # colnames(dat) <- cNames                            # Give column names
  # head(dat)

  
  
  
  



  

  print(paste("opening count csv", countcsv))
  cou    <- read.csv(countcsv, header=TRUE, sep="\t", stringsAsFactors=FALSE)
  nrows  <- nrow(dat)
  ncols  <- ncol(dat)
  rnames <- cou[,1]
  rvals  <- cou[,3]
  ndat   <- matrix(data=NA, nrow=nrows, ncol=ncols)
#     print(colnames(cou))
#     print(head(cou))
#     print(head(rvals))
#     print(cou[1,3])
#     print(cou[2,3])
#     return(NA)
#     cou<-apply(as.matrix(dat),2,as.numeric)
#     print(head(dat))
# return(NA)
  diag(dat) <- rvals
  if (NA_diagonal) {
    diag(dat) <- NA
  }

#     print(head(dat))
#     print(cou   )
#     print(rnames)
#     print(rvals )
#     return(NA)









  for (x in 1:nrows ) {
    for (y in 1:ncols ) {
#         print(paste("l",length(dat[,1]),"x",x,"y",y,"v",dat[x,y]))
#         print(paste("l",length(dat[,1]),"x",x,"y",y,"v",dat[x,y],"u",dat[y,x]))
      
      j <- calc_dist( x,y,rvals[x],rvals[y],dat[x,y], dist_method )
#         print(paste("j", j))
      ndat[x,y] <- j
    }
  }
  
  colnames( ndat) <- colnames(dat)
  row.names(ndat) <- colnames(dat)
  if (NA_diagonal) {
    diag(ndat) <- NA
  }
  print(paste("saving distance  ", dist_method))
  write.csv(ndat, file=paste(of, ".csv", sep=""))
#     print(head(ndat))
  dat <- ndat
#     return

  
  #http://stackoverflow.com/questions/12646691/trying-to-determine-why-my-heatmap-made-using-heatmap-2-and-using-breaks-in-r-is
  #http://stackoverflow.com/questions/5320814/order-of-rows-in-heatmap







  if( center_data ) {
    plot_j_histo(dat, filetype, paste(of, "_histo_orig", sep=""), size, 120)
    
    dat <- center_matrix(dat)
  }
  dathist <- plot_j_histo(dat, filetype, paste(of, "_histo", sep=""), size, 120)
  




  matrix_average <- gen_average_report(dat)
  
  print(paste("saving matrix average csv"))
  write.csv(matrix_average, file=paste(of, "_average.csv", sep=""))  
  
  get_fh( filetype, paste(of, "_average", sep=""), size )
  
  print(paste("plotting matrix average"))
  plot_average_report( matrix_average, BOTTOM_BORDER )
  
  dev.off()





  print("plotting dendrogram")
  gen_dendrogram(dat, of, as.dist, cluster_method, RIGHT_BORDER, pallet, cex, filetype, size, dathist )
  print("dendrogram plotted")


# print( dathist   )
# print( hcountT   )
# print( datBreaks )
# print( datCounts )
# print( datCLog   )
# 
# print( length(datBreaks))
# print( length(datCounts))
# print( length(datCLog  ))

# for ( i in 1:length(datBreaks) ) {
#   l <- datCLog[i]
#   v <- hbreaks[i]
# #   print(paste("i",i,'l',l,'v',v))
#   if ( l > 1 ) {
#     if (i == 1 ) {
#       n <- hbreaks[i+1]
#       p <- ( n - v ) / l
# #       print(paste(" n",n,'p',p))
#       for (j in 1:l) {
#         nv <- v + (j-1) * p
# #         print(paste("  nv",nv))
#         datBreaksF <- c(datBreaksF, nv)
# #         print(datBreaksF)
#       }
#     } else {
#       n <- hbreaks[i-1]
#       p <- ( v - n ) / l
# #       print(paste(" n",n,'p',p))
#       for (j in 1:l) {
#         nv <- n + j * p
# #         print(paste("  nv",nv))
#         datBreaksF <- c(datBreaksF, nv)
# #         print(datBreaksF)
#       }
#     }
#   }
# }
# print(datBreaksF)
# datBreaks <- datBreaksF
# print(length(datBreaksF))
# return(NA)


# return(NA)
#   print(head(dat))

  
  if ( !NA_diagonal ) {
  #   dev.off()
    
  #   b = boot.phylo( as.phylo(clusterD), dat, function(xx) { as.phylo(as.hclust(hclustfun(distfun(xx)))) }, B=10, trees=T )
  #   print(b)
  #   plot(b)
  #   plot(b$trees)
  #   c = consensus(b$trees)
  #   print(c)
  #   plot(c)
  
  
  #   ?pvclust
  #   cluster.bootstrap <- pvclust(dat, nboot=10, method.hclust=cluster_method, method.dist="abscor")
  #   plot(cluster.bootstrap)
  #   pvrect(cluster.bootstrap)  
  
  #   dist.topo(x, y, method = "PH85")
  
  #   TR <- replicate(100, rtree(10), FALSE)
  #   pp10 <- prop.part(TR)
  #   length(pp10)
  #   print(pp10)
  #   plot(pp10, pch = "x", col = 2)
  
  # http://research.stowers-institute.org/mcm/efg/R/Visualization/cor-cluster/index.htm
  #   http://www.statmethods.net/advstats/cluster.html
  #   fit <- Mclust(dat)
  #   plot(fit) # plot results 
  #   summary(fit) # display the best model
    
  }
  # return(NA)



  print("")
}


incsv1v <- "csv/21/test10/test10.json.csv"
incsv1c <- "csv/21/test10/test10.json.count.csv"

incsv2v <- "csv/31/test10/test10.json.csv"
incsv2c <- "csv/31/test10/test10.json.count.csv"

incsv3v <- "21_extra/cnidaria_db.json.csv"
incsv3c <- "21_extra/cnidaria_db.json.count.csv"

incsv4v <- "test_10_11/test10.json.csv"
incsv4c <- "test_10_11/test10.json.count.csv"

incsv5v <- "qry_small_cnidaria_db.json.txt"
incsv5c <- "qry_small_cnidaria_db.json.count.txt"


pallet          = c( "red"  , "white" , "blue"                   )
pallet          = c( "red"  , "black" , "green"                  )
pallet          = c( "red"  , "yellow", "green"                  )
pallet          = c( "blue4", "yellow", "white" , "green", "red2")
pallet          = c( "blue4", "white" , "red2"                   )
pallet          = c( "blue" , "white" , "red"                    )
pallet          = c( "black", "red"   , "yellow", "white"        )
pallet          = c( "white", "yellow", "red"   , "black"        )
pallet          = c( "red"  , "orange", "yellow", "green"        )

pallet          = c( "red4" , "red3" , "red2"   , "red"   , "orange", "yellow2", "yellow", "limegreen"        )
# pallet          = cm.colors(256)
# pallet          = heat.colors(256)


# pallet          = c("black", "white"                           )
# pallet          = c("white", "black"                           )
# pallet_N        = 80
filetype        = "eps"
filetype        = "pdf"
filetype        = "png"

# to_heapmap(incsv1v, incsv1c, filetype=filetype, pallet=pallet, pallet_N=pallet_N )
# to_heapmap(incsv2v, incsv2c, filetype=filetype, pallet=pallet, pallet_N=pallet_N )
# to_heapmap(incsv3v, incsv3c, filetype=filetype, pallet=pallet, pallet_N=pallet_N )
# to_heapmap(incsv4v, incsv4c, filetype=filetype, pallet=pallet, pallet_N=pallet_N )
to_heapmap(incsv5v, incsv5c, filetype=filetype, pallet=pallet )




# ?heatmap
