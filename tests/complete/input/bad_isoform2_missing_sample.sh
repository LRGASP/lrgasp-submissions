# substitute ONT with PacBio
sed --in-place -e '/H1_mix_captrap_ont/d' -e '/"H1_mix",/d' $1/iso_detect_ref_darwin_captrap_ont/entry.json


