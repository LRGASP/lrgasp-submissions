args = commandArgs(trailingOnly=TRUE)

if (length(args) == 0) {
    stop("Wrong # args: make_html_table.R output.html", call.=FALSE)
} else {
    outHtml = args[1]
}
library(DT)

dat <- read.table("docs/rnaseq-data-matrix.tsv", header=TRUE, sep='\t')

tbDt <- datatable(dat,extensions = c('Buttons','ColReorder','FixedColumns', 'FixedHeader', 'KeyTable','RowGroup'), filter='top', rownames=FALSE, options= list(
	dom = 'Blfrtip',
	buttons = c('csv','colvis'), 
	colReorder=TRUE, 
	fixedColumns = TRUE,
	fixedHeader = TRUE, 
	pageLength =200,
	keys = TRUE,
	rowId =0,
	rowGroup = list(dataSrc = c(5,6)),
	selection = 'none',
	initComplete = JS(
    "function(settings, json) {",
    "$('body').css({'font-family': 'Helvetica'});",
    "}"
  )
)
)
DT::saveWidget(tbDt, outHtml)
