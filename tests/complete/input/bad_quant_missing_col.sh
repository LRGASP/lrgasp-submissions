# drop one column

tsv=$1/iso_quant_ont_drna/H1_mix_drna_ont_long/expression.tsv
awk -v 'OFS=\t' '{print $1,$2,$3}' $tsv >$tsv.tmp
mv -f $tsv.tmp $tsv
