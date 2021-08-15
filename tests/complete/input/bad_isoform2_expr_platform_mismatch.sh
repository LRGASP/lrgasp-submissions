# substitute ONT with PacBio
sed --in-place -e 's/ENCFF654SNK/ENCFF105WIJ/' -e 's/ENCFF934KDM/ENCFF212HLP/' -e 's/ENCFF104BNW/ENCFF003QZT/' \
    $1/iso_detect_ref_darwin_captrap_ont/WTC11_captrap_ont/experiment.json


