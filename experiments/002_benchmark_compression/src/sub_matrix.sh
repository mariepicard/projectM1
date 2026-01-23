#!/usr/bin/env bash
set -euo pipefail

outdir="json_files_sub"
src="src"

usage() {
    echo "Usage : $0 <input_archive | directory > <number of genomes> <s> [output_directory]"
    exit 1
}

if [[ $# -ne 4 ]]; then 
	[[ $# -ne 3 ]] && usage
else
	outdir="$4"
fi

archive="$1"
nb_genomes="$2"
s="$3"
extracted_archive=""
outdir="$outdir/s${s}_g${nb_genomes}"

if [[ ! -d "$outdir" ]]; then
	mkdir -p "$outdir"
else
	echo "$outdir already exists. Exiting."
	exit 0
fi


if [[ ! -d "$archive" ]]; then
	extracted_archive=$(mktemp -d)
	trap 'rm -rf "$extracted_archive"' EXIT
	echo "Decompressing archive $archive..."
	tar -xf "$archive" -C "$extracted_archive"
	echo "Done."
else
	extracted_archive="$archive"
fi

sketches=$(mktemp -d)
trap 'rm -rf "$sketches"' EXIT

find "$extracted_archive" -type f | head -n "$nb_genomes" | while read -r file; do
    filename=$(echo "$file" | sed "s/.*\///")
    eval "mash sketch -s $s -o $sketches/$filename $file" 2> /dev/null
    eval "mash info -d $sketches/$filename.msh" > "$outdir/${filename}.json"
done

exit 0
