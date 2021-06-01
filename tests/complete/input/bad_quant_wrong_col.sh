if [ "$(uname -s)" = "Darwin" ] ; then
    sed=gsed
else
    sed=sed
fi

# change one column to another sample
${sed} --in-place -e 's/ENCFF804BPC/ENCFF600LIU/' $1/iso_quant_ont_drna/H1_mix_drna_ont_long/expression.tsv
