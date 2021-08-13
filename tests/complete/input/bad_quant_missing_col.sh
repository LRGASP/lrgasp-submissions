# drop one column

tsv=$1/iso_quant_drna_ont_darwin/H1_mix_drna_ont/expression.tsv
awk -v 'OFS=\t' '{print $1,$2,$3}' $tsv >$tsv.tmp
mv -f $tsv.tmp $tsv
