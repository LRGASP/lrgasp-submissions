if [ "$(uname -s)" = "Darwin" ] ; then
    sed=gsed
else
    sed=sed
fi

# change one column to something bogus
${sed} --in-place -e 's/ENCFF804BPC/ENCFFLIU600/' $1/iso_quant_drna_ont_darwin/H1_mix_drna_ont/expression.tsv
