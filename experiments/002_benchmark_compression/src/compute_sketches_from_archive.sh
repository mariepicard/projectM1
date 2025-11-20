#! /usr/bin/env bash

usage() {
    echo "Usage : $0 <archive.tar.xz | input_directory> <s>"
    exit 1
}


# checking exactly 2 parameter was given, and if not, call usage
[[ $# -ne 2 ]] && usage

extracted_archive="$1"
SKETCH_SIZE="$2"

if [[ ! -d "$extracted_archive" ]]; then
	archive="$1"

	if [[ "$archive" != *.tar.xz ]]; then
		echo "Error : archive format should be .tar.xz"
		exit 2
	fi

	if [[ ! -f "$archive" ]]; then
		echo "Error : file '$archive' not found."
		exit 3
	fi

	extracted_archive=$(mktemp -d)
	trap 'rm -rf "$extracted_archive"' EXIT #delete temporary directory upon escape
	# decompress
	tar -xf "$archive" -C "$extracted_archive"
	if [[ $? -ne 0 ]]; then
		echo "Error during decompression"
		exit 4
	fi
fi

# loop on files
OUTPUT_DIR="sketches/"
mkdir -p "$OUTPUT_DIR"
find "$extracted_archive" -type f | while read -r file; do
    filename=$(echo "$file" | sed "s/.*\///")
    eval "mash sketch -s $SKETCH_SIZE -o $OUTPUT_DIR/$filename $file"
done
echo "Done."
