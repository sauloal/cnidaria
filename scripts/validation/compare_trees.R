source( "tree_lib.R"     )

DO_TREE_DISTANCE <- F

#   "S09_merged4_names_fixed.nwk"
tree_files <- c(
  "trees/F5_whole_genome_snp_20140611_names_fixed.nwk",
  "trees/S10_homozygous_SNPs_in_10_domestication_genes_names_fixed.nwk",
  
  "trees/11_test10.json.no_scale.jaccard_dissimilarity.nj",
  "trees/11_test10.json.no_scale.jaccard_dissimilarity.upgma",
  "trees/11_test10.json.no_scale.jaccard_dissimilarity_sqrt.nj",
  "trees/11_test10.json.no_scale.jaccard_dissimilarity_sqrt.upgma",
  
  "trees/15_test12.json.no_scale.jaccard_dissimilarity.nj",
  "trees/15_test12.json.no_scale.jaccard_dissimilarity.upgma",
  "trees/15_test12.json.no_scale.jaccard_dissimilarity_sqrt.nj",
  "trees/15_test12.json.no_scale.jaccard_dissimilarity_sqrt.upgma",
  
  "trees/17_test12.json.no_scale.jaccard_dissimilarity.nj",
  "trees/17_test12.json.no_scale.jaccard_dissimilarity.upgma",
  "trees/17_test12.json.no_scale.jaccard_dissimilarity_sqrt.nj",
  "trees/17_test12.json.no_scale.jaccard_dissimilarity_sqrt.upgma",
  
  "trees/21_test10.json.no_scale.jaccard_dissimilarity.nj",
  "trees/21_test10.json.no_scale.jaccard_dissimilarity.upgma",
  "trees/21_test10.json.no_scale.jaccard_dissimilarity_sqrt.nj",
  "trees/21_test10.json.no_scale.jaccard_dissimilarity_sqrt.upgma",
  
  "trees/31_test10.json.no_scale.jaccard_dissimilarity.nj",
  "trees/31_test10.json.no_scale.jaccard_dissimilarity.upgma",
  "trees/31_test10.json.no_scale.jaccard_dissimilarity_sqrt.nj",
  "trees/31_test10.json.no_scale.jaccard_dissimilarity_sqrt.upgma"
)
out_base_name = ""

analysis_name = '10SNP'
analysis_name = '135common'





if(F) { # gen desired tips from tree
  reference_tree    <- "trees/S10_homozygous_SNPs_in_10_domestication_genes_names_fixed.nwk"
  desirable_tips    <- read.tree(reference_tree)$tip.label
  write.table(desirable_tips[desirable_tips != ""], file="trees/desired_tips_10SNP.csv", sep="\t",  quote=F, row.names=F, col.names=F)
  stop("OK")
}  
  
  


if (F) { # 21 2%
  out_base_name = "2percent_"
  tree_files <- c(
    "trees/21_test10.json.no_scale.jaccard_dissimilarity.nj",
    "trees/21_test10.json.no_scale.jaccard_dissimilarity.upgma",
    "trees/21_test10.json.no_scale.jaccard_dissimilarity_sqrt.nj",
    "trees/21_test10.json.no_scale.jaccard_dissimilarity_sqrt.upgma",
    
    "trees/21_test10_0001_0050.json.no_scale.jaccard_dissimilarity.nj",
    "trees/21_test10_0001_0050.json.no_scale.jaccard_dissimilarity_sqrt.nj",
    "trees/21_test10_0001_0050.json.no_scale.jaccard_dissimilarity_sqrt.upgma",
    "trees/21_test10_0001_0050.json.no_scale.jaccard_dissimilarity.upgma"
  )
}


if (F) { # 21 extra
  out_base_name = "21extra_"
  tree_files <- c(
    "trees/21_e_cnidaria_db.json.no_scale.jaccard_dissimilarity.nj",
    "trees/21_e_cnidaria_db.json.no_scale.jaccard_dissimilarity.upgma",
    "trees/21_e_cnidaria_db.json.no_scale.jaccard_dissimilarity_sqrt.nj",
    "trees/21_e_cnidaria_db.json.no_scale.jaccard_dissimilarity_sqrt.upgma"
  )

  analysis_name = '169extra'
}


if (T) { # 21 solanales
  out_base_name = "21solanales_"
  tree_files <- c(
    "trees/21_test10.json.no_scale.jaccard_dissimilarity.nj",
    "trees/21_test10.json.no_scale.jaccard_dissimilarity.upgma",
    "trees/21_test10.json.no_scale.jaccard_dissimilarity_sqrt.nj",
    "trees/21_test10.json.no_scale.jaccard_dissimilarity_sqrt.upgma"
  )
  
  analysis_name = '100solanales'
}


translation_table <- read.csv("trees/translation_table.txt", sep="\t", header=F, stringsAsFactors=F)
translation_table <- m_fix_string(translation_table)
print("TRANSLATION TABLE")
print(translation_table)




desirable_tips    <- read.csv(paste("trees/desired_tips_", analysis_name, ".csv", sep="") , header=F, sep="\t", stringsAsFactors=F)
desirable_tips    <- fix_string(unlist(desirable_tips))
desirable_tips    <- translate_names(translation_table, desirable_tips)
print("DESIRED LABELS")
print(desirable_tips)
print(length(desirable_tips))




undesirable_tips  <- NA




res           <- matrix(,nrow=length(tree_files), ncol=length(tree_files), byrow=T)
colnames(res) <- tree_files
rownames(res) <- tree_files

for ( x in 1:length(tree_files) ) {
  x_tree_file <- tree_files[x]
  print(x_tree_file     )
  
  x_tree      <- read.tree(x_tree_file)
  x_tree      <- filter_tree(x_tree, desirable=desirable_tips, undesirable=undesirable_tips, translation_table=translation_table)
  print(paste("x labels", length(x_tree$tip.label)))
  write.tree(      x_tree           , file=paste(x_tree_file, ".", analysis_name, ".filtered.nwk"          , sep="") )
  write.csv(  sort(x_tree$tip.label), file=paste(x_tree_file, ".", analysis_name, ".filtered.nwk.tiplabels", sep=""), quote=F, row.names=F, col.names=F )
  
  if (DO_TREE_DISTANCE){
    for ( y in x:length(tree_files) ) {
      y_tree_file <- tree_files[y]
      print(paste(" vs", y_tree_file))
      
      y_tree      <- read.tree(y_tree_file)
      y_tree      <- filter_tree(y_tree, desirable=desirable_tips, undesirable=undesirable_tips, translation_table=translation_table)
      
      x_y_dist    <- dist.topo(x_tree, y_tree)
      
      print(paste("  y labels", length(y_tree$tip.label), "dist", x_y_dist))
      print("")
      res[x,y] <- x_y_dist
      res[y,x] <- x_y_dist
    }
  }
}

if (DO_TREE_DISTANCE){
  print(res) 
  write.table(res, file=paste("trees/report_",out_base_name,analysis_name,".csv", sep=""), sep="\t", col.names=NA, quote=F)
}