if [ "$(uname -s)" = "Darwin" ] ; then
    sed=gsed
else
    sed=sed
fi
${sed} --in-place -e 's/H1_mix_drna_ont_long/ready_mix/' $1/iso_detect_ref_darwin/H1_mix_drna_ont_long/experiment.json
