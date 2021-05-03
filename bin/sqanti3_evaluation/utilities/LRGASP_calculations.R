### New version by Fran. Jan 2021

LRGASP_calculations <- function (NAME, class.file, junc.file, out.dir, platform, functions.dir) {
  # Get functions and spike-ins IDs
  setwd(functions.dir)
  source("LRGASP_functions.R")
  sirv_list=read.table("SIRVs_ids.txt", header = F)$V1
  ercc_list=read.table("ERCC_ids.txt", header = F)$V1
  
  # identify files in directory
  cat("Evaluation script has being run.\nData used for ", NAME, " pipeline are \n", class.file , "\n", junc.file , "\n")
  sqanti_data=read.table(class.file , sep = "\t", as.is = T, header = T)
  sqanti_data$submission = NAME
  sqanti_data$Platform = platform
  sqanti_data.junc=read.table(junc.file, sep = "\t", as.is = T, header = T)
  sqanti_data.junc$submission = NAME
  sqanti_data.junc$Platform = platform
  if(all(is.na(sqanti_data$iso_exp))){
    sqanti_data$iso_exp <- 0
  }
  # separate spike-ins and isoforms
  sirv_data=sqanti_data[grep("SIRV",sqanti_data$chrom),]
  ercc_data=sqanti_data[grep("ERCC",sqanti_data$chrom),]
  sirv_data.junc=sqanti_data.junc[grep("SIRV",sqanti_data.junc$chrom),]
  ercc_data.junc=sqanti_data.junc[grep("ERCC",sqanti_data.junc$chrom),]
  sqanti_data=sqanti_data[grep("SIRV|ERCC",sqanti_data$chrom, invert=T),]
  sqanti_data.junc=sqanti_data.junc[grep("SIRV|ERCC",sqanti_data.junc$chrom, invert=T),]
  
  
  ### Evaluation of FSM
  #####################
  print ("FSM evaluation")
  sqanti_data_FSM=subset(sqanti_data, structural_category=="full-splice_match") # should we filter out mono-exons?
  
  # FSM with both 3' and 5'end at less than 50bp of the TSS/TTS associated to the reference match
  sqanti_data_FSM$TP=apply(sqanti_data_FSM,1,TP_function)
  FSM_TPR_TP=length(which(sqanti_data_FSM$TP==TRUE))*100/dim(sqanti_data_FSM)[1]
  
  # FSM with both 3' and 5'end at less than 50bp of any TSS/TTS annotated for that gene
  sqanti_data_FSM$TP_gene=apply(sqanti_data_FSM,1,TP_gene_function)
  FSM_TPR_TP_gene=length(which(sqanti_data_FSM$TP_gene==TRUE))*100/dim(sqanti_data_FSM)[1]
  
  # Analysis 5' and 3' ends
  sqanti_data_FSM$TP_ref5=apply(sqanti_data_FSM,1,ref5TP_function)  # 5' end matches the reference
  sqanti_data_FSM$TP_ref5_gene=apply(sqanti_data_FSM,1,ref5TP_gene_function) #5' end matches any TSS of the same gene in the reference
  sqanti_data_FSM$TP_ref3=apply(sqanti_data_FSM,1,ref3TP_function)  # 3' end matches the reference
  sqanti_data_FSM$TP_ref3_gene=apply(sqanti_data_FSM,1,ref3TP_gene_function) #3' end matches any TTS of the same gene in the reference
  sqanti_data_FSM$TP_5prime=apply(sqanti_data_FSM,1,fiveTP_function) # 5' end matches a CAGE peak
  sqanti_data_FSM$TP_3prime=apply(sqanti_data_FSM,1,threeTP_function) # 3' end has polyA motif
  
  FSM_TPR_ref5=length(which(sqanti_data_FSM$TP_ref5==TRUE))*100/dim(sqanti_data_FSM)[1]
  FSM_TPR_ref5_gene=length(which(sqanti_data_FSM$TP_ref5_gene==TRUE))*100/dim(sqanti_data_FSM)[1]
  FSM_TPR_ref3=length(which(sqanti_data_FSM$TP_ref3==TRUE))*100/dim(sqanti_data_FSM)[1]
  FSM_TPR_ref3_gene=length(which(sqanti_data_FSM$TP_ref3_gene==TRUE))*100/dim(sqanti_data_FSM)[1]
  
  FSM_TPR_5primeTP=length(which(sqanti_data_FSM$TP_5prime==TRUE))*100/dim(sqanti_data_FSM)[1] # rate for 5'end matching CAGE
  FSM_TPR_3primeTP=length(which(sqanti_data_FSM$TP_3prime==TRUE))*100/dim(sqanti_data_FSM)[1] # rate for 3'end with polyA
  
  # "All TP" have any support (by reference gene/transcript or CAGE/polyA) at both 5' and 3' end
  sqanti_data_FSM$TP_all=apply(sqanti_data_FSM,1,allTP_function)
  FSM_TPR_allTP=length(which(sqanti_data_FSM$TP_all==TRUE))*100/dim(sqanti_data_FSM)[1]
  
  ##### NEEDED?
  # Normalized values
  normalized_FSM_TP=sqanti_data_FSM[,c("associated_transcript","TP_ref5","TP_ref3", "TP", "TP_5prime","TP_3prime","polyA_motif","pos_cage_peak")]
  normalized_FSM_TP=unique(normalized_FSM_TP)
  normalized_FSM_TPR_TP=length(which(normalized_FSM_TP$TP==TRUE))*100/dim(normalized_FSM_TP)[1]
  normalized_FSM_TPR_3primeTP=length(which(normalized_FSM_TP$TP_3prime==TRUE))*100/dim(normalized_FSM_TP)[1]
  normalized_FSM_TPR_5primeTP=length(which(normalized_FSM_TP$TP_5prime==TRUE))*100/dim(normalized_FSM_TP)[1]
  normalized_FSM_TP$allTP=apply(normalized_FSM_TP,1,allTP_norm)
  normalized_FSM_TP[which(is.na(normalized_FSM_TP$allTP)),"allTP"]=TRUE
  normalized_FSM_TPR_allTP=length(which(normalized_FSM_TP$allTP==TRUE))*100/dim(normalized_FSM_TP)[1]
  ######
  
  # Redundancy
  FSM_reference_redundancy=dim(sqanti_data_FSM)[1]/length(unique(sqanti_data_FSM$associated_transcript))
  
  # SJ mean coverage
  sqanti_data_FSM$mean_all_coverage=apply(sqanti_data_FSM,1, mean_cov_all,sqanti_data.junc)
  
  # Write out results
  a.FSM_results=data.frame(row.names = c("Name", "Platform", "Number",
                                         "TP rate (%) Associated transcript", "5' reference TP rate (%)", "3' reference TP rate (%)", 
                                         "TP rate (%) Associated gene", "5' reference gene TP rate (%)", "3' reference gene TP rate (%)", 
                                         "5' CAGE TP rate (%)" , "3' polyA motif TP rate (%)",
                                         "All TP rate (%)", "Normalized TP rate (%)", "Reference redundancy Level"))
  a.FSM_results$value=0
  a.FSM_results["Name",] = NAME
  a.FSM_results["Platform",]=platform
  a.FSM_results["Number",]=as.integer(dim(sqanti_data_FSM)[1])
  a.FSM_results["TP rate (%) Associated transcript",]= round(FSM_TPR_TP, digits = 2)
  a.FSM_results["5' reference TP rate (%)",]= round(FSM_TPR_ref5, digits = 2)
  a.FSM_results["3' reference TP rate (%)",]= round(FSM_TPR_ref3, digits = 2)
  a.FSM_results["TP rate (%) Associated gene",]= round(FSM_TPR_TP_gene, digits = 2)
  a.FSM_results["5' reference gene TP rate (%)",]= round(FSM_TPR_ref5_gene, digits = 2)
  a.FSM_results["3' reference gene TP rate (%)",]= round(FSM_TPR_ref3_gene, digits = 2)
  a.FSM_results["5' CAGE TP rate (%)",]= round(FSM_TPR_5primeTP, digits = 2)
  a.FSM_results["3' polyA motif TP rate (%)",]= round(FSM_TPR_3primeTP, digits = 2)
  a.FSM_results["All TP rate (%)",]= round(FSM_TPR_allTP, digits = 2)
  a.FSM_results["Normalized TP rate (%)",]= round(normalized_FSM_TPR_allTP, digits = 2)
  a.FSM_results["Reference redundancy Level",]= round(FSM_reference_redundancy, digits = 2)
  
  ### Evaluation of ISM
  ######################
  print ("ISM evaluation")
  sqanti_data_ISM=subset(sqanti_data, structural_category=="incomplete-splice_match")
  
  # ISM with both 3' and 5'end at less than 50bp of the TSS/TTS associated to the reference match
  sqanti_data_ISM$TP=apply(sqanti_data_ISM,1,TP_function)
  ISM_TPR_TP=length(which(sqanti_data_ISM$TP==TRUE))*100/dim(sqanti_data_ISM)[1]
  
  # ISM with both 3' and 5'end at less than 50bp of any TSS/TTS annotated for that gene
  sqanti_data_ISM$TP_gene=apply(sqanti_data_ISM,1,TP_gene_function)
  ISM_TPR_TP_gene=length(which(sqanti_data_ISM$TP_gene==TRUE))*100/dim(sqanti_data_ISM)[1]
  
  # Analysis 5' and 3' ends
  sqanti_data_ISM$TP_ref5=apply(sqanti_data_ISM,1,ref5TP_function)
  sqanti_data_ISM$TP_ref5_gene=apply(sqanti_data_ISM,1,ref5TP_gene_function) #5' end matches any TSS of the same gene in the reference
  sqanti_data_ISM$TP_ref3=apply(sqanti_data_ISM,1,ref3TP_function)
  sqanti_data_ISM$TP_ref3_gene=apply(sqanti_data_ISM,1,ref3TP_gene_function) #3' end matches any TTS of the same gene in the reference
  sqanti_data_ISM$TP_5prime=apply(sqanti_data_ISM,1,fiveTP_function)
  sqanti_data_ISM$TP_3prime=apply(sqanti_data_ISM,1,threeTP_function)
  
  # Calculate missing exons
  sqanti_data_ISM$missing_exons=apply(sqanti_data_ISM , 1, missing_exons_function)
  sqanti_data_ISM$missing_exons_perc=apply(sqanti_data_ISM,1, function(x){ as.integer(x["missing_exons"])/as.integer(x["ref_exons"])})
  
  ISM_TPR_5primeTP=length(which(sqanti_data_ISM$TP_5prime==TRUE))*100/dim(sqanti_data_ISM)[1]
  ISM_TPR_3primeTP=length(which(sqanti_data_ISM$TP_3prime==TRUE))*100/dim(sqanti_data_ISM)[1]
  ISM_TPR_ref5=length(which(sqanti_data_ISM$TP_ref5==TRUE))*100/dim(sqanti_data_ISM)[1]
  ISM_TPR_ref5_gene=length(which(sqanti_data_ISM$TP_ref5_gene==TRUE))*100/dim(sqanti_data_ISM)[1]
  ISM_TPR_ref3=length(which(sqanti_data_ISM$TP_ref3==TRUE))*100/dim(sqanti_data_ISM)[1]
  ISM_TPR_ref3_gene=length(which(sqanti_data_ISM$TP_ref3_gene==TRUE))*100/dim(sqanti_data_ISM)[1]
  
  # All TP, have any support at either 5' or 3' end
  sqanti_data_ISM$TP_all=apply(sqanti_data_ISM,1,allTP_function)
  ISM_TPR_allTP=length(which(sqanti_data_ISM$TP_all==TRUE))*100/dim(sqanti_data_ISM)[1]
  
  # Normalized values
  normalized_ISM_TP=sqanti_data_ISM[ , c("associated_transcript","TP_ref5","TP_ref3", "TP","TP_5prime","TP_3prime","polyA_motif","pos_cage_peak")]
  normalized_ISM_TP=unique(normalized_ISM_TP)
  normalized_ISM_TPR_TP=length(which(normalized_ISM_TP$TP==TRUE))*100/dim(normalized_ISM_TP)[1]
  normalized_ISM_TPR_3primeTP=length(which(normalized_ISM_TP$TP_3prime==TRUE))*100/dim(normalized_ISM_TP)[1]
  normalized_ISM_TPR_5primeTP=length(which(normalized_ISM_TP$TP_5prime==TRUE))*100/dim(normalized_ISM_TP)[1]
  normalized_ISM_TP$allTP=apply(normalized_ISM_TP,1,allTP_norm)
  normalized_ISM_TP[which(is.na(normalized_ISM_TP$allTP)),"allTP"]=TRUE
  normalized_ISM_TPR_allTP=length(which(normalized_ISM_TP$allTP==TRUE))*100/dim(normalized_ISM_TP)[1]
  
  # Redundancy ### NEEDED??
  ISM_reference_redundancy=dim(sqanti_data_ISM)[1]/length(unique(sqanti_data_ISM$associated_transcript))
 
   # SJ mean coverage
  sqanti_data_ISM$mean_all_coverage=apply(sqanti_data_ISM,1, mean_cov_all,sqanti_data.junc)
  
  # Write out results
  b.ISM_results=data.frame(row.names = c("Name", "Platform", "Number",
                                         "TP rate (%) Associated transcript", "5' reference TP rate (%)", "3' reference TP rate (%)", 
                                         "TP rate (%) Associated gene", "5' reference gene TP rate (%)", "3' reference gene TP rate (%)", 
                                         "5' CAGE TP rate (%)" , "3' polyA motif TP rate (%)",
                                         "All TP rate (%)", "Normalized TP rate (%)", "Reference redundancy Level"))
  b.ISM_results$value=0
  b.ISM_results["Name",] = NAME
  b.ISM_results["Platform",]=platform
  b.ISM_results["Number",]=as.integer(dim(sqanti_data_ISM)[1])
  b.ISM_results["TP rate (%) Associated transcript",]=round(ISM_TPR_TP, digits = 2)
  b.ISM_results["5' reference TP rate (%)",]=round(ISM_TPR_ref5, digits = 2)
  b.ISM_results["3' reference TP rate (%)",]=round(ISM_TPR_ref3, digits = 2)
  b.ISM_results["TP rate (%) Associated gene",]=round(ISM_TPR_TP_gene, digits = 2)
  b.ISM_results["5' reference gene TP rate (%)",]=round(ISM_TPR_ref5_gene, digits = 2)
  b.ISM_results["3' reference gene TP rate (%)",]=round(ISM_TPR_ref3_gene, digits = 2)
  b.ISM_results["5' CAGE TP rate (%)",]=round(ISM_TPR_5primeTP, digits = 2)
  b.ISM_results["3' polyA motif TP rate (%)",]=round(ISM_TPR_3primeTP, digits = 2)
  b.ISM_results["All TP rate (%)",]=round(ISM_TPR_allTP, digits = 2)
  b.ISM_results["Normalized TP rate (%)",]=round(normalized_ISM_TPR_allTP, digits = 2)
  b.ISM_results["Reference redundancy Level",]=round(ISM_reference_redundancy, digits = 2)
  
  ### Evaluation of NIC
  ########################
  print ("NIC evaluation")
  sqanti_data_NIC=subset(sqanti_data, structural_category=="novel_in_catalog")
  sqanti_data_NIC$mean_novel_coverage=apply(sqanti_data_NIC,1, mean_cov_novel, sqanti_data.junc)
  sqanti_data_NIC$mean_all_coverage=apply(sqanti_data_NIC,1, mean_cov_all,sqanti_data.junc)
  sqanti_data_NIC$SJ_wo_cov=apply(sqanti_data_NIC,1,SJ_wo_cov,sqanti_data.junc)
  sqanti_data_NIC$novel_SJ=apply(sqanti_data_NIC,1,novel_SJ_isof,sqanti_data.junc)
  sqanti_data_NIC$TP_ref5_gene=apply(sqanti_data_NIC,1, ref5TP_gene_function)
  sqanti_data_NIC$TP_ref3_gene=apply(sqanti_data_NIC,1, ref3TP_gene_function)
  sqanti_data_NIC$TP_gene=apply(sqanti_data_NIC,1,TP_gene_function)
  sqanti_data_NIC$TP_5prime=apply(sqanti_data_NIC,1,fiveTP_function)
  sqanti_data_NIC$TP_3prime=apply(sqanti_data_NIC,1,threeTP_function)
  

  sqanti_data_NIC$TP_all=apply(sqanti_data_NIC,1,allTP_function_novel)
  
  subcat_levels=c("combination_of_known_junctions", "combination_of_known_splicesites" , "intron_retention")
  subcat_labels=c("Comb. known SJ", "Comb. known splice sites", "IR")
  
  sqanti_data_NIC$subcategory=factor(sqanti_data_NIC$subcategory, labels=subcat_labels,
                      levels=subcat_levels, ordered=TRUE)

  NIC_TPR_TP_gene=length(which(sqanti_data_NIC$TP_gene==TRUE))*100/dim(sqanti_data_NIC)[1]
  NIC_TPR_TP_ref5_gene=length(which(sqanti_data_NIC$TP_ref5_gene==TRUE))*100/dim(sqanti_data_NIC)[1]
  NIC_TPR_TP_ref3_gene=length(which(sqanti_data_NIC$TP_ref3_gene==TRUE))*100/dim(sqanti_data_NIC)[1]
  NIC_TPR_5primeTP=length(which(sqanti_data_NIC$TP_5prime==TRUE))*100/dim(sqanti_data_NIC)[1]
  NIC_TPR_3primeTP=length(which(sqanti_data_NIC$TP_3prime==TRUE))*100/dim(sqanti_data_NIC)[1]
  NIC_TPR_allTP=length(which(sqanti_data_NIC$TP_all==TRUE))*100/dim(sqanti_data_NIC)[1]
  NIC_IR_incidence=length(which(sqanti_data_NIC$subcategory=="IR"))*100/dim(sqanti_data_NIC)[1] 
  
  ## Write results
  c.NIC_results=data.frame(row.names = c("Name", "Platform", "Number",
                                         "TP rate (%) Associated gene", "5' reference gene TP rate (%)", "3' reference gene TP rate (%)",
                                         "5' CAGE TP rate (%)" , "3' polyA motif TP rate (%)",
                                         "All TP rate (%)", "Intron retention incidence (%)"))
  c.NIC_results$value=0
  c.NIC_results["Name",] = NAME
  c.NIC_results["Platform",]=platform
  c.NIC_results["Number","value"]=as.integer(dim(sqanti_data_NIC)[1])
  c.NIC_results["TP rate (%) Associated gene",]=round(NIC_TPR_TP_gene, digits = 2)
  c.NIC_results["5' reference gene TP rate (%)",]=round(NIC_TPR_TP_ref5_gene, digits = 2)
  c.NIC_results["3' reference gene TP rate (%)",]=round(NIC_TPR_TP_ref3_gene, digits = 2)
  c.NIC_results["5' CAGE TP rate (%)",]=round(NIC_TPR_5primeTP, digits = 2)
  c.NIC_results["3' polyA motif TP rate (%)",]=round(NIC_TPR_3primeTP, digits = 2)
  c.NIC_results["All TP rate (%)", "value" ]=round(NIC_TPR_allTP, digits = 2)
  c.NIC_results["Intron retention incidence (%)","value"]=round(NIC_IR_incidence, digits = 2)
  
  ### Evaluation of NNC
  ########################
  print ("NNC evaluation")
  sqanti_data_NNC=subset(sqanti_data, structural_category=="novel_not_in_catalog")
  
  sqanti_data_NNC$mean_novel_coverage=apply(sqanti_data_NNC,1, mean_cov_novel,sqanti_data.junc)
  sqanti_data_NNC$mean_all_coverage=apply(sqanti_data_NNC,1, mean_cov_all,sqanti_data.junc)
  sqanti_data_NNC$SJ_wo_cov=apply(sqanti_data_NNC,1,SJ_wo_cov,sqanti_data.junc)
  sqanti_data_NNC$novel_SJ=apply(sqanti_data_NNC,1,novel_SJ_isof,sqanti_data.junc)
  sqanti_data_NNC$TP_ref5_gene=apply(sqanti_data_NNC,1, ref5TP_gene_function)
  sqanti_data_NNC$TP_ref3_gene=apply(sqanti_data_NNC,1, ref3TP_gene_function)
  sqanti_data_NNC$TP_gene=apply(sqanti_data_NNC,1,TP_gene_function)
  sqanti_data_NNC$TP_5prime=apply(sqanti_data_NNC,1,fiveTP_function)
  sqanti_data_NNC$TP_3prime=apply(sqanti_data_NNC,1,threeTP_function)
  sqanti_data_NNC$TP_all=apply(sqanti_data_NNC,1,allTP_function_novel)
  
  sqanti_data_NNC$SJ_non_canonical=apply(sqanti_data_NNC,1,non_canonical_SJ,sqanti_data.junc)
  
  subcat_levels=c("at_least_one_novel_splicesite", "intron_retention")
  subcat_labels=c("At least 1 novel SJ", "IR")
  
  sqanti_data_NNC$subcategory=factor(sqanti_data_NNC$subcategory,
                                      labels=subcat_labels,
                                      levels=subcat_levels, 
                                      ordered=TRUE)
  
  NNC_TPR_TP_gene=length(which(sqanti_data_NNC$TP_gene==TRUE))*100/dim(sqanti_data_NNC)[1]
  NNC_TPR_TP_ref5_gene=length(which(sqanti_data_NNC$TP_ref5_gene==TRUE))*100/dim(sqanti_data_NNC)[1]
  NNC_TPR_TP_ref3_gene=length(which(sqanti_data_NNC$TP_ref3_gene==TRUE))*100/dim(sqanti_data_NNC)[1]
  NNC_TPR_5primeTP=length(which(sqanti_data_NNC$TP_5prime==TRUE))*100/dim(sqanti_data_NNC)[1]
  NNC_TPR_3primeTP=length(which(sqanti_data_NNC$TP_3prime==TRUE))*100/dim(sqanti_data_NNC)[1]
  NNC_TPR_allTP=length(which(sqanti_data_NNC$TP_all==TRUE))*100/dim(sqanti_data_NNC)[1]
  NNC_non_canonical_incidence=length(which(sqanti_data_NNC$SJ_non_canonical>0))*100/dim(sqanti_data_NNC)[1]
  NNC_RT_switching_incidence=length(which(sqanti_data_NNC$RTS_stage==TRUE))*100/dim(sqanti_data_NNC)[1]
  
  
  ## Write results
  d.NNC_results=data.frame(row.names = c("Name", "Platform", "Number", 
                                         "TP rate (%) Associated gene", "5' reference gene TP rate (%)", "3' reference gene TP rate (%)",
                                         "5' CAGE TP rate (%)" , "3' polyA motif TP rate (%)",
                                         "All TP rate (%)", "Non-canonical SJ incidence (%)", "RT-switching incidence (%)"))
  d.NNC_results$value=0
  d.NNC_results["Name",] = NAME
  d.NNC_results["Platform",]=platform
  d.NNC_results["Number","value"]=as.integer(dim(sqanti_data_NNC)[1])
  d.NNC_results["TP rate (%) Associated gene",]=round(NNC_TPR_TP_gene, digits = 2)
  d.NNC_results["5' reference gene TP rate (%)",]=round(NNC_TPR_TP_ref5_gene, digits = 2)
  d.NNC_results["3' reference gene TP rate (%)",]=round(NNC_TPR_TP_ref3_gene, digits = 2)
  d.NNC_results["5' CAGE TP rate (%)",]=round(NNC_TPR_5primeTP, digits = 2)
  d.NNC_results["3' polyA motif TP rate (%)",]=round(NNC_TPR_3primeTP, digits = 2)
  d.NNC_results["All TP rate (%)", ]=round(NNC_TPR_allTP, digits = 2)
  d.NNC_results["Non-canonical SJ incidence (%)",]=round(NNC_non_canonical_incidence, digits = 2)
  d.NNC_results["RT-switching incidence (%)",]=round(NNC_RT_switching_incidence, digits = 2)
  
  
  ### Evaluation of SIRVs
  ##############################################
  print ("SIRVs evaluation")
  SIRVs_called=intersect(sirv_data[which(sirv_data$structural_category=="full-splice_match" & 
                                           abs(sirv_data$diff_to_TSS)<=50 & abs(sirv_data$diff_to_TTS)<=50),"associated_transcript"],
                         sirv_list)
  SIRVs_not_detected=setdiff(sirv_list,sirv_data[which(sirv_data$structural_category=="full-splice_match"),"associated_transcript"])
  FP_sirvs_detected=sirv_data[-which(sirv_data$structural_category=="full-splice_match" & 
                                      abs(sirv_data$diff_to_TSS)<=50 & abs(sirv_data$diff_to_TTS)<=50),]
#  known_sirvs=sirv_data[which(sirv_data$associated_transcript %in% sirv_list & sirv_data$structural_category=="full-splice_match") ,]
#  known_sirvs$iso_exp_lengthCorr=apply(known_sirvs,1,function(X){as.numeric(X["iso_exp"])/as.numeric(X["length"])})
  
  # Write out results
  e.SIRVs_results=data.frame(row.names = c("Name", "Platform", "Total number of SIRVs", "Number of SIRVs detected correctly (TP based on SJ, TSS and TTS)", 
                                           "Number of SIRVs not detected (FN)", "Number of new SIRVs (FP)", 
                                           "Mean Expression", "Standard Deviation of expression values", 
                                           "Sensitivity", "Precision", "False Discovery Rate"))
  e.SIRVs_results$value=NA
  e.SIRVs_results["Name",] = NAME
  e.SIRVs_results["Platform",]=platform
  e.SIRVs_results["Total number of SIRVs","value"]=as.integer(length(sirv_data$isoform))
  e.SIRVs_results["Number of SIRVs detected correctly (TP based on SJ, TSS and TTS)","value"]=as.integer(length(SIRVs_called))
  e.SIRVs_results["Number of SIRVs not detected (FN)","value"]=as.integer(length(SIRVs_not_detected))
  e.SIRVs_results["Number of new SIRVs (FP)","value"]=as.integer(length(FP_sirvs_detected[,"isoform"]))
  e.SIRVs_results["Mean Expression","value"]=round(mean(sirv_data$iso_exp), digits = 2)
  e.SIRVs_results["Standard Deviation of expression values","value"]=round(sd(sirv_data$iso_exp), digits = 2)
  e.SIRVs_results["Sensitivity","value"]=round(length(SIRVs_called)/length(sirv_list), digits = 2)
  e.SIRVs_results["Precision","value"]=round(length(SIRVs_called)/dim(sirv_data)[1], digits = 2)
  e.SIRVs_results["False Discovery Rate","value"]=round(length(FP_sirvs_detected[,"isoform"])/dim(sirv_data)[1], digits = 2)
  
  
  
  ####Create a list with all results and save all
  ###############################################
  
  files <- ls(pattern = "_results")
  all.results <- list()
  for ( i in 1: length(files) ) {
    all.results[[i]] <- eval(parse(text = files[i]))
  }
  setwd(out.dir)
  names(all.results) <- c("FSM", "ISM", "NIC", "NNC", "SIRV") ### TO INCLUDE "ERCC")
  
  save(all.results , file = paste(NAME, "_results.RData", sep = ''))
  save(sqanti_data, file=paste(NAME, "_classification.RData", sep = ''))
  save(sqanti_data.junc, file=paste(NAME, "_junctions.RData", sep = ''))
  
  save(sqanti_data_FSM, file = paste(NAME, "_FSM.RData", sep=''))
  save(sqanti_data_ISM, file = paste(NAME, "_ISM.RData", sep=''))
  save(sqanti_data_NIC, file = paste(NAME, "_NIC.RData", sep=''))
  save(sqanti_data_NNC, file = paste(NAME, "_NNC.RData", sep=''))
  
  save(sirv_data, file=paste(NAME, "_SIRVs_class.RData", sep=''))
  save(sirv_data.junc, file=paste(NAME, "_SIRVs_junc.RData", sep=''))
  #save(ercc_data, file=paste(NAME, "_ERCCs_class.RData"))
  #save(ercc_data.junc, file=paste(NAME, "_ERCCs_junc.RData"))
  
}

