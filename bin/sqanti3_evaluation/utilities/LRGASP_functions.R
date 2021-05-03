
#### LRGASP Functions
TP_function=function(X){
  abs(as.integer(X["diff_to_TSS"]))<=50 & abs(as.integer(X["diff_to_TTS"]))<=50
}

TP_gene_function=function(X){
  abs(as.integer(X["diff_to_gene_TSS"]))<=50 & abs(as.integer(X["diff_to_gene_TTS"]))<=50
}

ref5TP_function=function(X){
  abs(as.integer(X["diff_to_TSS"]))<=50 
}

ref5TP_gene_function=function(X){
  abs(as.integer(X["diff_to_gene_TSS"]))<=50 
}

ref3TP_function=function(X){
  abs(as.integer(X["diff_to_TTS"]))<=50 
}

ref3TP_gene_function=function(X){
  abs(as.integer(X["diff_to_gene_TTS"]))<=50 
}

fiveTP_function=function(X){
  if(X["within_cage_peak"]=="True"){TRUE}else{FALSE}
}

threeTP_function=function(X){
  !is.na(X["polyA_motif"])
}

allTP_function=function(X){
  as.logical(as.logical(abs(as.integer(X["diff_to_gene_TSS"]))<=50) | X["within_cage_peak"]=="True") & 
    (as.logical(abs(as.integer(X["diff_to_gene_TTS"]))<=50) | as.logical(!is.na(X["polyA_motif"])))
}

allTP_norm=function(X){
  (as.logical(as.logical(X["TP_ref5"]) | as.logical(X["TP_5prime"])) & as.logical(as.logical(X["TP_ref3"]) | as.logical(X["TP_3prime"])))
}

mean_cov_novel=function(X , sqanti_data_junc){
  novel_SJ=sqanti_data_junc[which(sqanti_data_junc$isoform==as.character(X["isoform"]) & sqanti_data_junc$junction_category=="novel"),]
  mean(novel_SJ$total_coverage)
}

mean_cov_all=function(X, sqanti_data_junc){
  all_SJ=sqanti_data_junc[which(sqanti_data_junc$isoform==X["isoform"]),]
  mean(all_SJ$total_coverage)
}

SJ_wo_cov=function(X, sqanti_data_junc ){
  all_SJ=sqanti_data_junc[which(sqanti_data_junc$isoform==X["isoform"]),]
  length(which(all_SJ$total_coverage==0))
}

novel_SJ_isof=function(X, sqanti_data_junc ){
  all_SJ=sqanti_data_junc[which(sqanti_data_junc$isoform==X["isoform"]),]
  as.integer(length(which(all_SJ$junction_category=="novel")))
}

novel_SJ_isof_perc=function(X, sqanti_data_junc = sqanti_data_junc){
  all_SJ=sqanti_data_junc[which(sqanti_data_junc$isoform==X["isoform"]),]
  as.integer(length(which(all_SJ$junction_category=="novel")))*100/dim(all_SJ)[1]
}

non_canonical_SJ=function(X, sqanti_data_junc = sqanti_data_junc){
  all_SJ=sqanti_data_junc[which(sqanti_data_junc$isoform==X["isoform"]),]
  as.integer(length(which(all_SJ$canonical=="non_canonical")))
}

allTP_function_novel=function(X){
  return(as.logical((abs(as.integer(X["diff_to_gene_TSS"]))<=50) | X["within_cage_peak"]=="True") & (as.logical(abs(as.integer(X["diff_to_gene_TTS"]))<=50) | !is.na(X["polyA_motif"])))
}

distancias <- function (CLASS, category, dist) {
  cap2 <- function (list) {
    b <- list()
    for ( i in 1:11 ) {
      a <- list[[i]]
      a[a > 1000] <- 1000
      a[a < -1000] <- -1000
      b[[i]] <- a
    }
    b
  }
  myPalette = c(rep("blue",5), rep("red",6))
  diff_to_TSS_data <- sapply(CLASS, function (x) subset(x, structural_category==category)[,dist])
  type.dist <- colnames(CLASS[[1]][dist])
  diff_to_TSS_data_capped <- cap2(diff_to_TSS_data)
  #myhist <- hist(diff_to_TSS_data_capped[[9]], breaks = 100,  plot = FALSE)
  #plot( myhist$mids, myhist$counts,type = "l",
  #   main = paste(category, "\n", type.dist),
  #   xlab = "Distance",
  #   ylab = "", col = myPalette[1], 
  #   ylim = c(0,5000), xlim = c(-1100,1100)
  #   )
  #for ( j in 1 : 8) {
  #myhist <- hist(diff_to_TSS_data_capped[[j]], breaks = 100,  plot = FALSE)
  #lines(myhist$mids, myhist$counts, col = myPalette[j])
  #}
  d=hist(diff_to_TSS_data_capped[[1]], breaks=100, plot = F)
  plot(d$mids, d$counts,col = myPalette[1],
    type="l", main = paste(category, "\n", type.dist),
       xlab = "Distance",
       ylab = "",
       #ylim = c(0,10000),
    xlim = c(-1100,1100)
       )
  for (j in 2:11){
    d=hist(diff_to_TSS_data_capped[[j]], breaks=100, plot = F)
    lines(d$mids, d$counts, type="l", col = myPalette[j])
  }
  
  dens=density(diff_to_TSS_data_capped[[5]])
  PM <- round(sapply(diff_to_TSS_data, function (x) length(which(x == 0)) / length(x)) * 100,2)
  barplot(PM, names.arg = c(1:11), col =  myPalette,
          ylim = c(0,100), yaxp = c(0, 100, 5) , ylab = "Distance",
          main = paste("% Perfect reference match", "\n", category, "\n",type.dist))
}

library(scales)


### New functions Fran

chaining_ISM <- function(x){
  sj=sqanti_data_junc[which(sqanti_data_junc$isoform==x["isoform"]),]
}

f.mean_cov_novel=function(X, Y){
  novel_SJ=Y[which(Y$isoform==X["isoform"] & Y$junction_category=="novel"),"total_coverage"]
  mean(novel_SJ)
}

f.mean_cov_all=function(X, Y){
  all_SJ=Y[which(Y$isoform==X["isoform"]),]
  mean(all_SJ$total_coverage)
}

f.SJ_wo_cov=function(X, Y){
  all_SJ=Y[which(Y$isoform==X["isoform"]),]
  length(which(all_SJ$total_coverage==0))
}

f.novel_SJ_isof=function(X,Y){
  all_SJ=Y[which(Y$isoform==X["isoform"]),]
  as.integer(length(which(all_SJ$junction_category=="novel")))
}

f.novel_SJ_isof_perc=function(X,Y){
  all_SJ=Y[which(Y$isoform==X["isoform"]),]
  as.integer(length(which(all_SJ$junction_category=="novel")))*100/dim(all_SJ)[1]
}

f.non_canonical_SJ=function(X,Y){
  all_SJ=Y[which(Y$isoform==X["isoform"]),]
  as.integer(length(which(all_SJ$canonical=="non_canonical")))
}

f.allTP_function_novel=function(X){
  return(as.logical((abs(as.integer(X["diff_to_gene_TSS"]))<=50) | X["within_cage_peak"]=="True") & (as.logical(abs(as.integer(X["diff_to_gene_TTS"]))<=50) | !is.na(X["polyA_motif"])))
}

### new functions
missing_exons_function=function(X){
  as.integer(X["ref_exons"]) - as.integer(X["exons"])
}
