calc_dist <- function(x,y,cx,cy,v,dist_method) {
  j <- NA
  
  if      ( dist_method == "jaccard" ) {
    j <- jaccard(  x,y,cx,cy,v )
  }
  else if ( dist_method == "jaccard_sqrt" ) {
    j <- jaccard_sqrt(  x,y,cx,cy,v )
  }
  else if ( dist_method == "cosine" ) {
    j <- cosine(   x,y,cx,cy,v )
  }
  else if ( dist_method == "tanimoto" ) {
    j <- tanimoto( x,y,cx,cy,v )
  }
  else if ( dist_method == "ochiai" ) {
    j <- ochiai(   x,y,cx,cy,v )
  }
  
  return(j)
}


jaccard_sym<-function(x,y,cx,cy,v){
#   z <- v ^ 2
#   v <- z
  cx <- as.numeric(cx)
  cy <- as.numeric(cy)
  v  <- as.numeric(v)
  s  <-   cx + cy
  u  <-   s  - v
  d  <- ( v  / u )
  j  <- d
  #c  <- 1.0-d
  #f  <- (((cx-v)+(cy-v)) / (((cx-v)+(cy-v)) + v))
  #j  <- c
#   j <- c

#   print(sprintf("jaccard    x %3.0f y %3.0f cx %e cy %e v %10.0f s %e u %e d %.7f c %.7f f %.7f j %.7f", 
#                 x,y,cx,cy,v,s,u,d,c,f,j))
  return(j)
}


jaccard<-function(x,y,cx,cy,v){
  return( ( 1 - jaccard_sym(x,y,cx,cy,v) ) )
}


jaccard_sqrt<-function(x,y,cx,cy,v){
  return( sqrt( jaccard(x,y,cx,cy,v) ) )
}


cosine<-function(x,y,cx,cy,v){
  u <- (as.numeric(cx)^2) * (as.numeric(cy)^2)
  d <- (v/u)
  j <- as.numeric(1.0e+0)-d
#   print(paste(x,y,cx,cy,v))
#   print((as.numeric(cx)^2))
#   print((as.numeric(cy)^2))
#   print(u)
#   print(d)
#   print(j)
#   stop("OK")
  #   print(sprintf("tanimoto x %3.0f y %3.0f cx %e cy %e v %10.0f u %e d %.7f j %.7f", 
  #                 x,y,cx,cy,v,u,d,j))
  return(j)
}


tanimoto<-function(x,y,cx,cy,v){
  u <- (as.numeric(cx)^2) + (as.numeric(cy)^2) - v
  d <- (v/u)
  j <- 1-d
  #   print(sprintf("tanimoto x %3.0f y %3.0f cx %e cy %e v %10.0f u %e d %.7f j %.7f", 
  #                 x,y,cx,cy,v,u,d,j))
  return(j)
}


ochiai<-function(x,y,cx,cy,v){
  u <- sqrt(as.numeric(cx)) * sqrt(as.numeric(cy))
  d <- (v/u)
  j <- 1-d
  #   print(sprintf("ochiai   x %3.0f y %3.0f cx %e cy %e v %10.0f u %e d %.7f j %.7f", 
  #                 x,y,cx,cy,v,u,d,j))
  return(j)
}
