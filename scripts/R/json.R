if (!require("ggplot2")) {
  install.packages("ggplot2", dependencies = TRUE)
  library(ggplot2)
}

if (!require("gplots")) {
  install.packages("gplots", dependencies = TRUE)
  library(gplots)
}

if (!require("rjson")) {
  install.packages("rjson", dependencies = TRUE)
  library(rjson)
}
.Machine$integer.max

if (!require("ape")) {
  install.packages("ape", dependencies = TRUE)
  library(ape)
}


source( "jaccard.R"     )
source( "read_titles.R" )
source( "stats.R"       )




parser <- function(
                     json_file,
                     BOTTOM_BORDER   =  5, #20
                     RIGHT_BORDER    =  2,  #20
                     SPACE_PER_COL   = 10,
                     cluster_method  = "average",
                     dist_method     = "jaccard",
                     filetype        = "png",
                     #                           pallet          = c("red"  , "white", "blue"  ),
                     pallet          = c("white", "black"),
                     pallet_N        =   60,
                     cex             =   20,
                     size            = 5120,
                     NA_diagonal     = T,
                     center_data     = F,
                     titles_file     = NA
                   ) {
  bn <- basename(json_file)
  bn <- gsub("/", "_"  , json_file)
  bn <- gsub("\\.", "_", bn    )
  of <- paste("images/json_", bn, ".", dist_method, sep="")
#   size <- ((l+10) * SPACE_PER_COL)
  
  
  # json_file <- "http://webonastick.com/uscl/feeds/uscl.json.txt"
  json_data <- fromJSON(file=json_file)
#   print(json_data)
  print( attributes(json_data) )
#   $names
#   [1] "num_infiles"        "num_srcfiles"       "num_combinations"   "complete_registers"
#   [5] "min_val"            "max_val"            "save_every"         "num_pieces"        
#   [9] "piece_num"          "kmer_size"          "kmer_bytes"         "data_bytes"        
#   [13] "block_bytes"        "j_offset"           "j_size"             "j_matrices_size"   
#   [17] "j_matrices"         "version"            "filetype"           "in_filenames"      
#   [21] "src_filenames"      "num_kmer_total_spp" "num_kmer_valid_spp" "matrix"






  if (! is.na(titles_file) ) {
    json_data$in_filenames <- read_titles(titles_file, json_data$in_filenames)
    print(json_data$in_filenames)
#     return(NA)
  }
  
  json_data$num_kmers_prop_spp <- json_data$num_kmer_valid_spp / json_data$num_kmer_total_spp






  count <- t(matrix(c(json_data$num_kmer_total_spp, json_data$num_kmer_valid_spp, json_data$num_kmers_prop_spp), ncol=json_data$num_infiles, nrow=3, byrow=T))
#   print(count)
  colnames(count) <- c("num_kmer_total_spp", "num_kmer_valid_spp", "num_kmer_prop_spp")
  rownames(count) <- json_data$in_filenames
#   print(count)
  
  write.csv(count, file=paste(of, "_count.csv", sep=""))



  print(length(json_data$matrix))

  json_data$matrix_simple  <- matrix(, ncol=json_data$num_infiles, nrow=json_data$num_infiles, byrow=T)
  json_data$matrix_jaccard <- matrix(, ncol=json_data$num_infiles, nrow=json_data$num_infiles, byrow=T)


  for (x in 1:length(json_data$matrix)) {
    for (y in 1:length(json_data$matrix)) {
      v  <- sum( array( json_data$matrix[[x]][[y]] ) )
      cx <- json_data$num_kmer_valid_spp[x]
      cy <- json_data$num_kmer_valid_spp[y]

      if ( x == y ) {
        v <- json_data$num_kmer_valid_spp[x]
      }
      
      j <- calc_dist( x,y,cx,cy,v,dist_method )

#       print(paste("x",x,"y",y,"v",v,"cx",cx,"cy",cy,"j",j))

      json_data$matrix_simple[ x,y] <- v
      json_data$matrix_jaccard[x,y] <- j
    }
  }


  colnames(json_data$matrix_simple ) <- json_data$in_filenames
  rownames(json_data$matrix_simple ) <- json_data$in_filenames
  
  colnames(json_data$matrix_jaccard) <- json_data$in_filenames
  rownames(json_data$matrix_jaccard) <- json_data$in_filenames

  write.csv(json_data$matrix_simple , file=paste(of, "_simple.csv", sep=""))  
  write.csv(json_data$matrix_jaccard, file=paste(of, ".csv"       , sep=""))  

  


  if (NA_diagonal) {
    diag(json_data$matrix_jaccard) <- NA
  }






  if (center_data) {
    plot_j_histo(json_data$matrix_jaccard, filetype, paste(of, "_histo_orig", sep=""), size, 120)
    
    json_data$matrix_jaccard <- center_matrix(json_data$matrix_jaccard)
  }
  dathist <- plot_j_histo(json_data$matrix_jaccard, filetype, paste(of, "_histo", sep=""), size, 120)






  json_data$matrix_average <- gen_average_report(json_data$matrix_jaccard)

  print(paste("saving matrix average csv"))
  write.csv(json_data$matrix_average, file=paste(of, "_average.csv", sep=""))  

  get_fh( filetype, paste(of, "_average", sep=""), size )

  print(paste("plotting matrix average"))
  plot_average_report( json_data$matrix_average, BOTTOM_BORDER )

  dev.off()






  gen_dendrogram(json_data$matrix_jaccard, of, as.dist, cluster_method, RIGHT_BORDER, pallet, cex, filetype, size, dathist )
}


titles_file <- "filelist.csv"
json_file   <- "21_extra/cnidaria_db.json"
json_file   <- "test_12_17/test12.json"
# parser(json_file, cex=20, BOTTOM_BORDER=20, RIGHT_BORDER=2000, titles_file=titles_file)
parser(json_file, titles_file=titles_file, filetype = "pdf")




dev.off()
dev.off()
dev.off()
dev.off()
dev.off()
dev.off()
dev.off()
dev.off()
dev.off()

