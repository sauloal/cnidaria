dat <- read.csv("blast2.small.csv", header=TRUE, sep="\t", stringsAsFactors=FALSE, row.names=1)

rn <- row.names(dat)

dat <- apply(as.matrix(dat),2,as.numeric)

row.names(dat) <- rn

heatmap(dat)