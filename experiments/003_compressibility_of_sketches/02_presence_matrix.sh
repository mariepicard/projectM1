#!/usr/bin/env bash
set -euo pipefail

archive="inputs/part_54/neisseria_gonorrhoeae__01.tar.xz"
outdir="json_files"
sketches="sketches"
stat_file="presence_linear.csv"
matrices="matrices"
src="src"



echo "s,Density of matrix,Normalized cumulative neighbouring distance" > "$stat_file"

extracted_archive=$(mktemp -d)
echo "Decompressing archive $archive..."
tar -xf "$archive" -C "$extracted_archive"
trap 'rm -rf "$extracted_archive"' EXIT
echo "Done."

if [ ! -d "$matrices" ]; then
	mkdir "$matrices"
fi

for ((s=1000;s<=10000;s=s+1000)); do
	echo "Computing sketches for s = $s"

	eval "$src/compute_sketches_from_archive.sh $extracted_archive $s" 2> /dev/null
	mkdir -p "$outdir"
	
	echo "Extracting json files from sketches..."

	for f in "$sketches"/*; do
		fname=$(basename "$f")
		eval "mash info -d $f" > "$outdir/${fname}_$s.json"
	done
	
	echo "Done."
	
	echo "Computing presence/absence matrix..."
	
	echo $(eval "$src/presence_matrix.py $outdir") >> "$stat_file"
	
	echo "Done."
	
	rm -rf "$sketches"
	rm -rf "$outdir"
done




