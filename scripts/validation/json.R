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

if (!require("ape")) {
  install.packages("ape", dependencies = TRUE)
  library(ape)
}
.Machine$integer.max


source( "distance.R"    )
source( "read_titles.R" )
source( "stats.R"       )
source( "classifier.R"  )




DO_ANALYSE_JSON       <- F
DO_GEN_GRAPHS         <- F
DO_GEN_CLASS_MATRIX   <- T
DO_COMPARE_MATRICES   <- F

out_base_name         <- ""

desired_spps_filename <- "desired_rows.csv"

titles_file           <- "filelist.csv"

json_files            <- c( 
  "data/11_test10.json",
  "data/15_test12.json",
  "data/17_test12.json",
  "data/21_test10.json",
  "data/31_test10.json"
)



distances             <- c("jaccard", "jaccard_sqrt", "cosine", "tanimoto", "ochiai")
distances             <- c("jaccard")



classes_file <- c(
  #"classes_all/classes.csv.filled.csv.named.csv",
  #"classes_all/classes.csv.filled.csv.named.csv.oneeach.csv"
  "classes_all/classes.csv.filled.csv.named.csv.slyc.csv",
  #"classes_all/report_validation_3.txt",
  "classes_all/report_validation_4.txt",
  "classes_all/report_validation_tomatoes.txt"
)

classes_file <- c(
  "classes_all/report_validation_tomatoes.txt"
)


classes_out_folder <- "classes_all"

#classes_polytomy_handlers <- c(NA, "ANY", "ALL", "MAJORITY")
classes_polytomy_handlers <- c(NA, "ALL", "MAJORITY")





if (F) { # 2% of test21
  out_base_name <- "_2percent"
  
  json_files            <- c( 
    "data/21_test10_0001_0050.json"
  )
  
  classes_file <- c(
    #"classes_2percent/classes.csv.filled.csv.named.csv",
    #"classes_2percent/classes.csv.filled.csv.named.csv.oneeach.csv"
    "classes_2percent/classes.csv.filled.csv.named.csv.slyc.csv",
    #"classes_2percent/report_validation_3.txt",
    "classes_2percent/report_validation_4.txt"
  )
  classes_out_folder <- "classes_2percent"
  DO_COMPARE_MATRICES   <- F
}




if (F) { #extended
  out_base_name <- "_21extended"
  
  json_files    <- c( 
    "data/21_e.json"
  )
  
  desired_spps_filename <- "desired_rows_extended.csv"
  DO_COMPARE_MATRICES   <- F
}














open_json <- function(json_file, desired_spps_filename=NA) {
  # json_file <- "http://webonastick.com/uscl/feeds/uscl.json.txt"
  json_data <- fromJSON(file=json_file)
  #   print(json_data)

  print( attributes(json_data) )
  # $names
  # [ 1] "num_infiles"              "num_srcfiles"             "num_combinations"         "complete_registers"       "min_val"                 
  # [ 6] "max_val"                  "save_every"               "num_pieces"               "piece_num"                "kmer_size"               
  # [11] "kmer_bytes"               "data_bytes"               "block_bytes"              "j_offset"                 "j_size"                  
  # [16] "j_matrices_size"          "j_matrices"               "version"                  "filetype"                 "in_filenames"            
  # [21] "src_filenames"            "num_kmer_total_spp"       "num_kmer_valid_spp"       "matrix"                   "num_kmers_prop_spp"      
  # [26] "matrix_simple"            "matrix_distance"          "dist_method"              "matrix_distance_centered" "matrix_average"       
  
  
  json_data$in_filenames             <- as.vector(           unlist(json_data$in_filenames            ))
  json_data$num_kmer_total_spp       <- as.vector(as.numeric(unlist(json_data$num_kmer_total_spp      )))
  json_data$num_kmer_valid_spp       <- as.vector(as.numeric(unlist(json_data$num_kmer_valid_spp      )))
  json_data$num_kmers_prop_spp       <- as.vector(as.numeric(unlist(json_data$num_kmers_prop_spp      )))
  json_data$matrix_simple            <- matrix(   as.numeric(unlist(json_data$matrix_simple           )), ncol=json_data$num_infiles, nrow=json_data$num_infiles, byrow=F)
  json_data$matrix_distance          <- matrix(   as.numeric(unlist(json_data$matrix_distance         )), ncol=json_data$num_infiles, nrow=json_data$num_infiles, byrow=F)
  json_data$matrix_distance_centered <- matrix(   as.numeric(unlist(json_data$matrix_distance_centered)), ncol=json_data$num_infiles, nrow=json_data$num_infiles, byrow=F)
  
  colnames(json_data$matrix_simple           ) <- json_data$in_filenames
  rownames(json_data$matrix_simple           ) <- json_data$in_filenames
  
  colnames(json_data$matrix_distance         ) <- json_data$in_filenames
  rownames(json_data$matrix_distance         ) <- json_data$in_filenames  
  
  colnames(json_data$matrix_distance_centered) <- json_data$in_filenames
  rownames(json_data$matrix_distance_centered) <- json_data$in_filenames    
  
  if ( is.na(desired_spps_filename) ) {
    return(json_data)
  }

  desired_spps <- as.vector(unlist(read.csv(desired_spps_filename, header=F, sep="\t", stringsAsFactors=F, strip.white=T, blank.lines.skip=T, comment.char = "#")))
  print("desired tips")
  print(desired_spps)

  print("in filenames")
  print(json_data$in_filenames)
  #rows_to_keep <- sapply(json_data$in_filenames, function(x) { print(x); print(x %in% desired_spps); return( x %in% desired_spps ) } )
  rows_to_keep <- json_data$in_filenames %in% desired_spps
  
#   print("rows_to_keep")
#   print(rows_to_keep)
  print("num rows_to_keep")
  print(sum(rows_to_keep))
  
  json_data$in_filenames             <- json_data$in_filenames[rows_to_keep]
  json_data$num_kmer_total_spp       <- json_data$num_kmer_total_spp[rows_to_keep]
  json_data$num_kmer_valid_spp       <- json_data$num_kmer_valid_spp[rows_to_keep]
  json_data$num_kmers_prop_spp       <- json_data$num_kmers_prop_spp[rows_to_keep]
  json_data$matrix_simple            <- json_data$matrix_simple[rows_to_keep,rows_to_keep]
  json_data$matrix_distance          <- json_data$matrix_distance[rows_to_keep,rows_to_keep]
  json_data$matrix_distance_centered <- json_data$matrix_distance_centered[rows_to_keep,rows_to_keep]
  json_data$num_infiles              <- sum(rows_to_keep)
  
  print("num_infiles")
  print(json_data$num_infiles)
  
  if(F) {
    print("in_filenames")
    print(json_data$in_filenames)
    
    print("num_kmer_total_spp")
    print(json_data$num_kmer_total_spp)
    
    print("num_kmer_valid_spp")
    print(json_data$num_kmer_valid_spp)
    
    print("num_kmers_prop_spp")
    print(json_data$num_kmers_prop_spp)
    
    print("matrix_simple")
    print(head(json_data$matrix_simple, n=1))
    
    print("matrix_distance")
    print(head(json_data$matrix_distance, n=1))
    
    print("matrix_distance_centered")
    print(head(json_data$matrix_distance_centered, n=1))
  }
  
  return(json_data)
}


gen_graphs <- function(
  json_file,
  BOTTOM_BORDER         =  5, #20
  RIGHT_BORDER          =  2,  #20
  SPACE_PER_COL         = 10,
  cluster_method        = "average",
  dist_method           = "jaccard",
  filetype              = "pdf",
  pallet                = c("white", "black"),
  pallet_N              =   60,
  cexRow                =   20,
  cexCol                =   20,
  size                  = 5120,
  use_centered          = F,
  COLOR_TRACE           = "red",
  COLOR_DENS            = "white",
  COLOR_NA              = "white",
  desired_spps_filename = NA,
  out_base_name         = ""
) {
#     bn <- json_file
  of <- paste(json_file, out_base_name, sep="")
#   bn <- basename(json_file)
#   bn <- gsub("/", "_"  , json_file)
#   bn <- gsub("\\.", "_", bn    )
#   of <- bn
  #   size <- ((l+10) * SPACE_PER_COL)
  
  json_data       <- open_json(json_file, desired_spps_filename=desired_spps_filename)

  count           <- t(matrix(c(json_data$num_kmer_total_spp, json_data$num_kmer_valid_spp, json_data$num_kmers_prop_spp), ncol=json_data$num_infiles, nrow=3, byrow=T))
  #   print(count)
  colnames(count) <- c("num_kmer_total_spp", "num_kmer_valid_spp", "num_kmer_prop_spp")
  rownames(count) <- json_data$in_filenames
  #   print(count)
  
  print(paste("saving count csv"))
  write.table(count, file=paste(of, out_base_name,"_count.csv", sep=""), sep="\t", quote=F, na="", row.names=T, col.names=T)

  
  print(paste("saving raw data csv"))

  
  print(paste("length matrix_simple           ", length(json_data$matrix_simple[,1]           )))
  print(paste("length matrix_distance         ", length(json_data$matrix_distance[,1]         )))
  print(paste("length matrix_distance_centered", length(json_data$matrix_distance_centered[,1])))

  write.table(json_data$matrix_simple           , file=paste(of, "_matrix_simple.csv"           , sep=""), sep="\t", quote=F, na="", row.names=T, col.names=NA)
  write.table(json_data$matrix_distance         , file=paste(of, "_matrix_distance.csv"         , sep=""), sep="\t", quote=F, na="", row.names=T, col.names=NA)
  write.table(json_data$matrix_distance_centered, file=paste(of, "_matrix_distance_centered.csv", sep=""), sep="\t", quote=F, na="", row.names=T, col.names=NA)


  
  print(paste("creating histograms"))
  dathist_simple            <- plot_j_histo(json_data$matrix_simple           , filetype, paste(of, "_histo_simple"           , sep=""), size, 120)
  dathist_distance          <- plot_j_histo(json_data$matrix_distance         , filetype, paste(of, "_histo_distance"         , sep=""), size, 120)
  dathist_distance_centered <- plot_j_histo(json_data$matrix_distance_centered, filetype, paste(of, "_histo_distance_centered", sep=""), size, 120)
  
  dathist <- dathist_distance
  if ( use_centered ) {
    dathist <- dathist_distance_centered
  }

  

  
  
  print(paste("saving matrix average csv"))
  
  json_data$matrix_average           <- matrix(as.numeric(unlist(json_data$matrix_average)), ncol=2, nrow=json_data$num_infiles, byrow=F)
  colnames(json_data$matrix_average) <- c("average", "std_dev")
  rownames(json_data$matrix_average) <- rownames(json_data$matrix_distance)
  
  write.table(json_data$matrix_average, file=paste(of, "_average.csv", sep=""), sep="\t", quote=F, na="", row.names=T, col.names=NA)
  
  
  get_fh( filetype, paste(of, "_average", sep=""), size )
  
  print(paste("plotting matrix average"))
  plot_average_report( json_data$matrix_average, BOTTOM_BORDER )
  
  dev.off()
  
  
  
  #   json_data$matrix_distance_mp <- medpolish(json_data$matrix_distance, maxiter=1000, trace.iter=T, na.rm=T)
  #   print(head(json_data$matrix_distance_mp$residuals))
  # 
  #   gen_dendrogram(json_data$matrix_distance_mp$residuals, of, as.dist, cluster_method, RIGHT_BORDER, pallet, cex, filetype, size, dathist )
  
  print(paste("plotting dendrogram"))


  gen_dendrogram(json_data$matrix_distance, of, as.dist, dathist,
    cluster_method  = cluster_method,
    filetype        = filetype,
    pallet          = pallet,
    pallet_N        = pallet_N,
    cexRow          = cexRow,
    cexCol          = cexCol,
    size            = size,
    BOTTOM_BORDER   = BOTTOM_BORDER, #20
    RIGHT_BORDER    = RIGHT_BORDER,  #20
    COLOR_DENS      = COLOR_DENS,
    COLOR_NA        = COLOR_NA,
    COLOR_TRACE     = COLOR_TRACE
  )


  print(paste("finished plotting"))
}



analise_json <- function(
  json_file,
  NA_diagonal = T,
  titles_file = NA,
  save_to     = NA,
  dist_method = "jaccard"
) {
  # json_file <- "http://webonastick.com/uscl/feeds/uscl.json.txt"
  json_data       <- open_json(json_file, desired_spps_filename=NA)
  
  
  
  
  if (! is.na(titles_file) ) {
    json_data$in_filenames <- read_titles(titles_file, json_data$in_filenames)
    print(json_data$in_filenames)
    #     return(NA)
  }
  
  json_data$num_kmers_prop_spp <- json_data$num_kmer_valid_spp / json_data$num_kmer_total_spp
  
  
  
  
  
  
#   count <- t(matrix(c(json_data$num_kmer_total_spp, json_data$num_kmer_valid_spp, json_data$num_kmers_prop_spp), ncol=json_data$num_infiles, nrow=3, byrow=T))
#   #   print(count)
#   colnames(count) <- c("num_kmer_total_spp", "num_kmer_valid_spp", "num_kmer_prop_spp")
#   rownames(count) <- json_data$in_filenames
#   #   print(count)
  

  
  print(length(json_data$matrix))
  
  json_data$matrix_simple   <- matrix(, ncol=json_data$num_infiles, nrow=json_data$num_infiles, byrow=T)
  json_data$matrix_distance <- matrix(, ncol=json_data$num_infiles, nrow=json_data$num_infiles, byrow=T)
  json_data$dist_method     <- dist_method

  print(paste("in_filenames"            , length(json_data$in_filenames)))
  print(paste("json_data$num_infiles"   , json_data$num_infiles))
  print(paste("length(json_data$matrix)", length(json_data$matrix)))
#   print(json_data$matrix)
  
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
      
      json_data$matrix_simple[  x,y]  <- v
      json_data$matrix_distance[x,y]  <- j
    }
  }
  
  
  colnames(json_data$matrix_simple )  <- json_data$in_filenames
  rownames(json_data$matrix_simple )  <- json_data$in_filenames
  
  colnames(json_data$matrix_distance) <- json_data$in_filenames
  rownames(json_data$matrix_distance) <- json_data$in_filenames
  
  
  
  if (NA_diagonal) {
    diag(json_data$matrix_distance) <- NA
  }
  
  
  print("centering")
  json_data$matrix_distance_centered <- center_matrix(json_data$matrix_distance)

  print("average")
  json_data$matrix_average           <- gen_average_report(json_data$matrix_distance)
  
  if (! is.na(save_to)) {
    print(paste("saving to", save_to))
    new_json    <- toJSON(json_data)
    sink(save_to)
    cat(new_json)
    sink()    
  }
  
  return ( json_data )
}


gen_classes_matrix      <- function( json_files, classes_file, polytomy_handler=NA, desired_spps_filename=NA, out_base_name="" ) {
  classes_matrix <- NA
  debug_matrix   <- NA
  debug_matrix   <- NA
  class(debug_matrix)

  debug_matrix               <- matrix(,nrow=0,ncol=len_col_names_debug_matrix_data)
  colnames(debug_matrix)     <- col_names_debug_matrix_data
  
  
  ana_mode <- "polytomy_skip"
  ana_func <- NA
  if (is.na(polytomy_handler)) {
    ana_mode <- "polytomy_skip"
    ana_func <- NA
  } else
  if (polytomy_handler == "ANY") {
    ana_mode <- "polytomy_any"
    ana_func <- function(x) { return( any(x, na.rm=T) ) }
  } else
  if (polytomy_handler == "ALL") {
    ana_mode <- "polytomy_all"
    ana_func <- function(x) { return( all(x, na.rm=T) ) }
  } else
  if (polytomy_handler == "MAJORITY") {
    ana_mode <- "polytomy_majority"
    ana_func <- function(x) { return( (mean(x, na.rm=T) > 0.50) ) }
  }
  else {
    stop(paste("unknown polytomy handler:", polytomy_handler))
  }
  
  print(paste("RUNNING POLYTOMY HANDLER:", ana_mode))
  
  row_names <- NA
  for ( json_file in json_files ) {
    json_data <- open_json(json_file, desired_spps_filename=desired_spps_filename)
    res       <- nearest_neighbour_classifier(json_file, json_data, classes_file, polytomy_handler=ana_func)
    m         <- res$res
    debug     <- res$debug
    
    if ( class(classes_matrix) == "logical" ) {
      classes_matrix <- m
      row_names      <- row.names(m)
    } else {
      classes_matrix <- rbind(classes_matrix, m[3,])
      row_names      <- c(row_names, row.names(m)[3])
    }
    
    debug_matrix <- rbind(debug_matrix, debug)
  }

  row.names(classes_matrix) <- row_names
  print("print class matrix")
  print(classes_matrix)


  out_bn  <- paste(classes_file, ".",ana_mode , out_base_name, sep="")
  out_csv <- paste(out_bn      , ".report.csv",                sep="")
  out_dbg <- paste(out_csv     , ".log"       ,                sep="")

#   colnames(classes_matrix) <- c(out_bn, colnames(classes_matrix))
  print(paste("saving matrix to", out_csv))
  write.table(classes_matrix        , file=out_csv, sep="\t", na="", quote=F, col.names=NA)
  
  print(paste("saving log to", out_dbg))
  write.table(debug_matrix          , file=out_dbg, sep="\t", na="", quote=F, row.names=F)
}


extract_matrices        <- function( json_files, desired_spps_filename=NA ) {
  res <- list()
  num_infiles = NA
  
  for ( i in 1:length(json_files) ) {
    json_file      <- json_files[i]
    print(paste("extracting", json_file))
    
    json_data      <- open_json(json_file, desired_spps_filename=desired_spps_filename)
    distance       <- json_data$matrix_distance    
    num_infiles    <- json_data$num_infiles
    spp_names      <- json_data$in_filenames
    #distance       <- matrix(as.numeric(distance), ncol=l_num_infiles, nrow=l_num_infiles, byrow=T)
    diag(distance) <- 0
    spp_list_match <- NA

    print(paste(" num files", num_infiles))
    
    res[[i]]      <- distance
  }

  print(length(res))
  
  return( res )
}


compare_matrices_mantel <- function( matrices, row_names, outfolder='.', out_base_name="" ) {  
  res <- matrix(,nrow=length(matrices),ncol=length(matrices))
    
  for (i in 1:length(matrices)) {
    for (j in 1:length(matrices)) {
      if (j > i) {
        next 
      }

      m1 <- matrices[[i]]
      m2 <- matrices[[j]]

#       print(head(m1))
#       print(tail(m1))
      
#       print(head(m2))
#       print(tail(m2))

#       print(is.numeric(m1))
#       print(is.numeric(m2))
      
      r   <- mantel.test(m1, m2, nperm=99, graph=F)
#       print(attributes(r))

      p   <- ((i-1)*length(matrices)) + (j-1) + 1
      print(paste("i",i,"j",j,"p",p,"z",r$z.stat,"pv",r$p,"alternative",r$alternative))
#       res[[ p ]] <- r$z.stat
      res[i,j] <- r$z.stat
      res[j,i] <- r$z.stat
    }
  }


  rownames(res) <- row_names
  colnames(res) <- row_names
  
  out_csv <- paste(outfolder,"/","compare_matrices.mantel_test",out_base_name,".csv", sep="")
  
  print(paste("saving to", out_csv))
  
  write.table(res, file=out_csv, sep="\t")
}


compare_matrices_cadm   <- function( matrices, row_names, outfolder='.', out_base_name="" ) {  
  nmats                          <- length(row_names)
  ncols                          <- dim(matrices[[1]])[1]
  
  spairs                         <- {}
  spairs$Chi2                    <- matrix(, nrow=length(matrices), ncol=length(matrices) )
  spairs$Prob                    <- matrix(, nrow=length(matrices), ncol=length(matrices) )
  spairs$W                       <- matrix(, nrow=length(matrices), ncol=length(matrices) )
  spairs$Mantel.mean.1           <- matrix(, nrow=length(matrices), ncol=length(matrices) )
  spairs$Mantel.mean.2           <- matrix(, nrow=length(matrices), ncol=length(matrices) )
  spairs$ProbC.1                 <- matrix(, nrow=length(matrices), ncol=length(matrices) )
  spairs$ProbC.2                 <- matrix(, nrow=length(matrices), ncol=length(matrices) )
  
  rownames(spairs$Chi2         ) <- paste("Chi2|"         , row_names)
  rownames(spairs$Prob         ) <- paste("Prob|"         , row_names)
  rownames(spairs$W            ) <- paste("W|"            , row_names)
  rownames(spairs$Mantel.mean.1) <- paste("Mantel.mean.1|", row_names)
  rownames(spairs$Mantel.mean.2) <- paste("Mantel.mean.2|", row_names)
  rownames(spairs$ProbC.1      ) <- paste("ProbC.1|"      , row_names)
  rownames(spairs$ProbC.2      ) <- paste("ProbC.2|"      , row_names)  
  
  colnames(spairs$Chi2         ) <- rownames(spairs$Chi2         )
  colnames(spairs$Prob         ) <- rownames(spairs$Prob         )
  colnames(spairs$W            ) <- rownames(spairs$W            )
  colnames(spairs$Mantel.mean.1) <- rownames(spairs$Mantel.mean.1)
  colnames(spairs$Mantel.mean.2) <- rownames(spairs$Mantel.mean.2)
  colnames(spairs$ProbC.1      ) <- rownames(spairs$ProbC.1      )
  colnames(spairs$ProbC.2      ) <- rownames(spairs$ProbC.2      )
  
  dat        <- NA
  
  for (i in 1:length(matrices)) {
    m1  <- matrices[[i]]
    
    if ( is.na(dat) ) {
      dat <- m1
    } else {
      dat <- rbind(dat, m1)
    }

    for (j in i:length(matrices)) {
      print(paste("pairwise comparison",i,j))
      m2  <- matrices[[j]]
      p   <- ((i-1)*length(matrices)) + (j-1) + 1
      mm  <- rbind(m1, m2)
      
      g   <- CADM.global(mm, 2, ncols, nperm=99, make.sym=T)
      p   <- CADM.post(  mm, 2, ncols, nperm=99, make.sym=T)
      
#       $A_posteriori_tests
#       Dmat.1 Dmat.2
#       Mantel.mean      1.00   1.00
#       Prob             0.01   0.01
#       Corrected.prob   0.02   0.02
      
      spairs$Chi2[i,j]          <- g$congruence_analysis["Chi2"          , "Statistics"]
      spairs$Chi2[j,i]          <- spairs$Chi2[i,j]

      spairs$Prob[i,j]          <- g$congruence_analysis["Prob.perm"     , "Statistics"]
      spairs$Prob[j,i]          <- spairs$Prob[i,j]

      spairs$W[i,j]             <- g$congruence_analysis["W"             , "Statistics"]
      spairs$W[j,i]             <- spairs$W[i,j]

      spairs$Mantel.mean.1[i,j] <- p$A_posteriori_tests[ "Mantel.mean"   , "Dmat.1"]
      spairs$Mantel.mean.1[j,i] <- spairs$Mantel.mean.1[i,j]

      spairs$Mantel.mean.2[i,j] <- p$A_posteriori_tests[ "Mantel.mean"   , "Dmat.2"]
      spairs$Mantel.mean.2[j,i] <- spairs$Mantel.mean.2[j,i]

      spairs$ProbC.1[i,j]       <- p$A_posteriori_tests[ "Corrected.prob", "Dmat.1"]
      spairs$ProbC.1[j,i]       <- spairs$ProbC.1[j,i]

      spairs$ProbC.2[i,j]       <- p$A_posteriori_tests[ "Corrected.prob", "Dmat.2"]
      spairs$ProbC.2[j,i]       <- spairs$ProbC.2[j,i]
    }
  }
  

  nrows <- (ncols*nmats)
  print(paste("nmats",nmats,"ncols",ncols,"nrows",nrows))

  resG <- CADM.global(dat, nmats, ncols, nperm=ncols, make.sym=T)$congruence_analysis
  resP <- CADM.post(  dat, nmats, ncols, nperm=ncols, make.sym=T)$A_posteriori_tests

  print( resG )
  print( resP )
  print(spairs)
  
  out_csv <- paste(outfolder, "/", "compare_matrices.cadm.",out_base_name,"csv", sep="")
  
  print(paste("saving to", out_csv))
  
  write.table(spairs$Chi2         , file=out_csv, sep="\t")
  write.table(spairs$Prob         , file=out_csv, sep="\t", append=T)
  write.table(spairs$W            , file=out_csv, sep="\t", append=T)

  write.table(spairs$Mantel.mean.1, file=out_csv, sep="\t", append=T)
  write.table(spairs$Mantel.mean.2, file=out_csv, sep="\t", append=T)

  write.table(spairs$ProbC.1      , file=out_csv, sep="\t", append=T)
  write.table(spairs$ProbC.2      , file=out_csv, sep="\t", append=T)
  
  write.table(resG                , file=out_csv, sep="\t", append=T)
  write.table(resP                , file=out_csv, sep="\t", append=T)
}






print("desired_spps_filename")
print(desired_spps_filename)

print("titles_file")
print(titles_file)

print("json_files")
print(json_files)

print("distances")
print(distances)







json_files_analised <- c()
for ( json_file in json_files ) {
  print(paste("analising", json_file))
  for ( dist_method in distances ) {
    print(paste("using distance", dist_method))
    of                  <- paste(json_file, ".analised.",dist_method,".json", sep="")
    json_files_analised <- c(json_files_analised, of)
    if (DO_ANALYSE_JSON) {
      analise_json(json_file, titles_file=titles_file, save_to=of, dist_method=dist_method)
    }
  }
}




if (DO_GEN_GRAPHS) {
  for ( json_file in json_files_analised ) {
    gen_graphs(
              json_file, 
              pallet                = c("red", "white", "blue"  ), 
              COLOR_NA              = 'black', 
              COLOR_TRACE           = "red",
              COLOR_DENS            = "black",
              filetype              = "pdf", 
              cexRow                = 0.25, 
              cexCol                = 0.01,
              desired_spps_filename = desired_spps_filename
              )
  }
}




# json_files <- json_files[c(2,3)]
if ( DO_GEN_CLASS_MATRIX ) {
  for (class_file in classes_file) {
    print(paste("analysing class matrix for",class_file))
    for (polytomy_handler in classes_polytomy_handlers) {
      print(paste("analysing class matrix for",class_file,"handler",polytomy_handler))
      gen_classes_matrix(json_files_analised, class_file, polytomy_handler=polytomy_handler, desired_spps_filename=desired_spps_filename)
    }
  }
}






if ( DO_COMPARE_MATRICES ) {
  # json_files <- json_files[2]
  # json_files <- json_files[c(2:3)]
  matrices   <- extract_matrices( json_files_analised, desired_spps_filename=desired_spps_filename )
  
  # compare_matrices_mantel(matrices, json_files)
  compare_matrices_cadm(  matrices, json_files_analised, outfolder=classes_out_folder )
}


