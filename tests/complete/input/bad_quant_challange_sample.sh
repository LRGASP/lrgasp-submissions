if [ "$(uname -s)" = "Darwin" ] ; then
    sed=gsed
else
    sed=sed
fi

# mouse ES not valid in iso_quant
${sed} --in-place -e 's/"human"/"mouse"/' -e 's/ENCFF155CFF/ENCFF535DQA/' -e 's/ENCFF771DIX/ENCFF654JHQ/' -e 's/ENCFF600LIU/ENCFF310IPO/'  $1/iso_quant_ont_drna1/drnaA/experiment.json



