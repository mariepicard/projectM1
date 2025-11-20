#! /usr/bin/bash

usage() {
    echo "Usage : $0 <input_directory> <output.csv>"
    exit 1
}

[[ $# -ne 2 ]] && usage

mem_usage_file="$2"
resources_file="output/compression_stats.csv"

monitoring_cmd="/usr/bin/time -f '%C,%e,%U,%M'"

echo "preset,XZ memory usage,GZIP memory usage">"$mem_usage_file"
echo "Command,elapsed time (real),elapsed time(user),peak memory consumption" > "$resources_file"
archive="sketches_archive.tar"

eval "tar -cf $archive $1"
archive_size=$(stat -c %s "$archive")

for preset in $(seq 1 9); do
	cmd="xz -T1 -k -"
	eval "$monitoring_cmd ${cmd}${preset} ${archive}" >> "$resources_file" 2>&1
	xz_file_size=$(stat -c %s "${archive}.xz")
	eval "rm ${archive}.xz"
	
	cmd="gzip -k -"
	eval "$monitoring_cmd ${cmd}${preset} ${archive}" >> "$resources_file" 2>&1
	gz_file_size=$(stat -c %s "${archive}.gz")
	eval "rm ${archive}.gz"
	
	#echo -e "\t ${preset},$xz_file_size,$gz_file_size"

	echo "${preset},$xz_file_size,$gz_file_size" >> "$mem_usage_file"
done

echo "$archive_size"
rm "$archive"
#echo "Done. Results saved to $mem_usage_file"

