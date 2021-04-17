if [ "$(uname -s)" = "Darwin" ] ; then
    sed=gsed
else
    sed=sed
fi
${sed} --in-place -e 's/iso_quant/iso_detect_ref/' $1/iso_quant_ont_drna1/entry.json

