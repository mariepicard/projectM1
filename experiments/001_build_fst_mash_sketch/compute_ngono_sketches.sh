inputs_dir="inputs"
URL="https://zenodo.org/records/15367750/files/"
s=10000

#  ******** Create and download inputs ********
download_part () {
	part="$1"
	if [[ -d "$inputs_dir/$part" ]]; then
		echo "$inputs_dir/$part already exists. Skipping download and extraction."
	else
		echo "Downloading $part.tar archive..."
		curl -s -L "${URL}${part}.tar?download=1" | tar -xv -C "$inputs_dir"
	fi
}


if [ ! -d "$inputs_dir" ]; then 
	echo "Creating input directory: $inputs_dir"
	mkdir -p "$inputs_dir"
fi
download_part "part_54"
echo "Inputs created."
echo;

echo "Compute sketches for s = $s"
eval "./compute_sketches_from_archive.sh '$inputs_dir'/part_54/neisseria_gonorrhoeae__01.tar.xz '$s'"
