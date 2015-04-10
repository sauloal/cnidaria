if (!require("ape")) {
  install.packages("ape", dependencies = TRUE)
  library(ape)
}





fix_string      <- function(dat) {
  dat <- gsub(" " , "_", dat, fixed=T)
  dat <- gsub("." , "_", dat, fixed=T)
  dat <- gsub("'" , "" , dat, fixed=T)
  dat <- gsub("_+", "_", dat)
  return(dat)
}


m_fix_string    <- function(dat) {
  #   print(dat)
  #   print(nrow(dat))
  #   print(ncol(dat))
  
  for (c in 1:ncol(dat)) {
    for (r in 1:nrow(dat)) {
      v <- dat[r,c]
      #       print(paste("r",r,"c",c,"v",v,"n",fix_string(v)))
      dat[r,c] <- fix_string(v)
    }
  }
  
  return(dat)
}


translate_names <- function(translation_table, values) {
  from_col <- translation_table[,1]
  to_col   <- translation_table[,2]
  
  for ( vpos in 1:length(values) ) {
    val          <- values[vpos]
    poses        <- which(from_col %in% val, arr.ind=T)
    
    if (length(poses) != 0) {
      values[vpos] <- to_col[poses[1]]
      #       print(paste(" val", val, "poses", poses[1], "to", to_col[poses[1]], "nval", values[vpos]))
    }
  }
  
  return(values)
}


filter_tree     <- function(tree, desirable=NA, undesirable=NA, translation_table=NA, trim.internal=TRUE) {
  if ( is.na(desirable) && is.na(undesirable) ) {
    stop("can't have the cake and eat it too")
  }
  
  if ( (!is.na(desirable)) && (!is.na(undesirable)) ) {
    stop("can't eat the cake and have it too")
  }
  
  tree$tip.label <- fix_string(tree$tip.label)
  if ( ! is.na(translation_table) ) {
    tree$tip.label <- translate_names(translation_table, tree$tip.label)
  }
  tip_labels     <- tree$tip.label
  
  if ( ! is.na(desirable) ) {
    desirable      <- fix_string(desirable)
    
    if ( ! is.na(translation_table) ) {
      desirable <- translate_names(translation_table, desirable)
    }
    
    
    for ( tip in tip_labels ) {
      if ( ! (tip %in% desirable) ) {
        #         print(paste("dropping", tip))
        tree <- drop.tip(tree, tip, trim.internal=trim.internal)
      }
    }
  } else {
    undesirable      <- fix_string(undesirable)
    
    if ( ! is.na(translation_table ) ) {
      undesirable    <- translate_names(translation_table, undesirable)
    }
    
    tree <- drop.tip(tree, undesirable, trim.internal=trim.internal)
  }
  
  return(tree)
}
