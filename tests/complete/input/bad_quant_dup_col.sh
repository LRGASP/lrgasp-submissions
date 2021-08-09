# duplicate one column

tsv=$1/iso_quant_darwin/H1_mix_drna_ont_long/expression.tsv
awk -v 'OFS=\t' '{print $1,$2,$3,$3}' $tsv >$tsv.tmp
mv -f $tsv.tmp $tsv
