# substitute dRNA with CapTrap
sed --in-place -e 's/ENCFF155CFF/ENCFF654SNK/' -e 's/ENCFF771DIX/ENCFF934KDM/' -e 's/ENCFF600LIU/ENCFF104BNW/' \
    $1/iso_detect_ref_darwin_drna_ont/WTC11_drna_ont/experiment.json
