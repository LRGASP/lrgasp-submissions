if [ "$(uname -s)" = "Darwin" ] ; then
    sed=gsed
else
    sed=sed
fi
${sed} --in-place -e '/transcript_id "transcript_113.nnic"/d' $1/iso_quant_darwin/WTC11_drna_ont_long/models.gtf

