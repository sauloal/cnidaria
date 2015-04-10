read_titles <- function(filename, names) {
#   return(names)
  ?read.csv
  data <- read.csv(filename, header=F, sep="\t", stringsAsFactors=F, comment.char="#", blank.lines.skip=T, strip.white=T)
  
  print(head(data))
  print(head(names))
  print(paste("#data" , length(data[,1])))
  print(paste("#names", length(names   )))

  
#   for (i in 1:length(data[,1])) {
#     prefix <- data[i,1]
#     nname  <- data[i,2]
#     print(paste(" i ", i, " prefix '", prefix, "' new name '", nname, "' len ", nchar(prefix), sep=""))
#   }
#   return(NA)

  for (n in 1:length(names)) {
    name <- names[n]
#     print(paste("n", n, "name", name))
    for (i in 1:length(data[,1])) {
      prefix <- data[i,1]
      nname  <- data[i,2]
      
      if ( nchar(prefix) == 0 ) { next }
      
      pmatch <- grep(prefix, name, fixed=T)
#       print(paste(" i ", i, " prefix '", prefix, "' new name '", nname, "' grep ", pmatch, " l ", length(pmatch), sep=""))

      if ( length(pmatch) > 0 ) {
        print(paste("  replacing '", name, "' with i: ", i, " prefix '", prefix, "' new name '", nname, "'", sep=""))
        names[n] <- nname
#         data <- data[(i*-1)]
        break
      }
    }
    ?grep
#     print("")
  }
#   print(head(names))
  return(names)
}

