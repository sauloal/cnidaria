calc_dist <- function(x,y,cx,cy,v,dist_method) {
  j <- NA
  
  if      ( dist_method == "jaccard" ) {
    j <- jaccard(  x,y,cx,cy,v )
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
  
  j
}



jaccard<-function(x,y,cx,cy,v){
#   z <- v ^ 2
#   v <- z
  s <- as.numeric(cx) + as.numeric(cy)
#   s <- cx + cy
  u <- s-v
  d <- (v/u)
  c <- 1-d
  f <- (((cx-v)+(cy-v)) / (((cx-v)+(cy-v)) + v))
  j <- sqrt( c )
#   j <- c

#   print(sprintf("jaccard    x %3.0f y %3.0f cx %e cy %e v %10.0f s %e u %e d %.7f c %.7f f %.7f j %.7f", 
#                 x,y,cx,cy,v,s,u,d,c,f,j))
  j
}


cosine<-function(x,y,cx,cy,v){
  u <- as.numeric(cx) * as.numeric(cy)
  d <- (v/u)
  j <- 1-d
  #   print(sprintf("tanimoto x %3.0f y %3.0f cx %e cy %e v %10.0f u %e d %.7f j %.7f", 
  #                 x,y,cx,cy,v,u,d,j))
  j
}


tanimoto<-function(x,y,cx,cy,v){
  u <- as.numeric(cx^2) + as.numeric(cy^2) - v
  d <- (v/u)
  j <- 1-d
  #   print(sprintf("tanimoto x %3.0f y %3.0f cx %e cy %e v %10.0f u %e d %.7f j %.7f", 
  #                 x,y,cx,cy,v,u,d,j))
  j
}


ochiai<-function(x,y,cx,cy,v){
  u <- as.numeric(sqrt(cx)) * as.numeric(sqrt(cy))
  d <- (v/u)
  j <- 1-d
  #   print(sprintf("ochiai   x %3.0f y %3.0f cx %e cy %e v %10.0f u %e d %.7f j %.7f", 
  #                 x,y,cx,cy,v,u,d,j))
  j
}
