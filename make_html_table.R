library(dplyr)
library(DT)

dat <- read.table("rnaseq-data-matrix.tsv", header=TRUE, sep='\t')

tbDt <- datatable(dat,extensions = c('Buttons','ColReorder','FixedColumns', 'FixedHeader', 'KeyTable','RowGroup'), filter='top', rownames=FALSE, options= list(
	dom = 'Blfrtip',
	buttons = c('csv','colvis'), 
	colReorder=TRUE, 
	fixedColumns = TRUE,
	fixedHeader = TRUE, 
	pageLength =200,
	keys = TRUE,
	rowId =0,
	rowGroup = list(dataSrc = c(2,3)),
	selection = 'none',
	initComplete = JS(
    "function(settings, json) {",
    "$('body').css({'font-family': 'Helvetica'});",
    "}"
  )
	)
	)
DT::saveWidget(tbDt, 'rnaseq-data-matrix.html')
