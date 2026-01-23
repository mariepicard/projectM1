#!/usr/bin/env bash
set -euo pipefail

#archive="inputs/part_24/dustbin__23.tar.xz"
archive="inputs/part_54/neisseria_gonorrhoeae__01.tar.xz"
outdir="json_files"
sketches="sketches"
stat_file="presence_base10.csv"
matrices="matrices"
src="src"



#echo "s,Density of matrix,Normalized cumulative neighbouring distance" > "$stat_file"

extracted_archive=$(mktemp -d)
echo "Decompressing archive $archive..."
tar -xf "$archive" -C "$extracted_archive"
trap 'rm -rf "$extracted_archive"' EXIT
echo "Done."

if [ ! -d "$matrices" ]; then
	mkdir "$matrices"
fi

s=1000

for ((S=1;S<=10000;S=S*10)); do
	echo "Computing sketches for S = $S"

	eval "displayed_matrix/sub_matrix.sh $extracted_archive $S $s"
	
	#echo "Computing presence/absence matrix..."
	eval "displayed_matrix/plot_presence_absence_matrix.py json_files_sub/s${s}_S${S} 'no plot'"
	
	#echo "Done."
done




