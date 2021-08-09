if [ "$(uname -s)" = "Darwin" ] ; then
    sed=gsed
else
    sed=sed
fi
${sed} --in-place -e '/transcript_270.known/d' $1/iso_detect_ref_darwin/H1_mix_drna_ont_long/read_model_map.tsv
