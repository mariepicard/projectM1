#!/usr/bin/env bash

# Exit on error
set -e

inputs_dir="inputs"
src_path="src"
URL="https://zenodo.org/records/15367750/files/"
sketches="sketches/"

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


#Figure : comparison of XZ and GZIP compression rate of 4000 genomes of ngono according to sketch size
size_variation () {
	echo "Computing compression rate of neisseria gonorrhoeae according to size..."
	
	tmp=$(mktemp -d)
	trap 'rm -rf "$tmp"' EXIT 
	file_sizes="$tmp/sketch_file_sizes.csv"
	echo "s,size" > "$file_sizes"
	
	archive="$inputs_dir/part_54/neisseria_gonorrhoeae__01.tar.xz"
	extracted_archive=$(mktemp -d)
	echo "Decompressing archive $archive..."
	tar -xf "$archive" -C "$extracted_archive"
	trap 'rm -rf "$extracted_archive"' EXIT 

	for ((s=500;s<=16000;s=s*2)); do
		echo "Computing sketches for s = $s"
		eval "$src_path/compute_sketches_from_archive.sh $extracted_archive $s" 2> /dev/null
		echo "Computing compression rate according to preset"
		size=$(eval "$src_path/benchmark.sh $sketches $tmp/memory_$s.csv")
		echo "$s,$size" >> "$file_sizes"
		echo "Cleaning up..."
		eval "$src_path/clean.sh"
	done
	
	eval "$src_path/plot_compression_ratio_according_to_label.py $tmp s 'Comparison of ngono compression rate for XZ and GZIP according to size'"
}

#Figure : comparison of dustbin and phylogenetically ordered ngono (4000 genomes) compression rate using XZ and GZIP 
compare_dustbin_ngono () {
	s="$1"
	tmp=$(mktemp -d)
	trap 'rm -rf "$tmp"' EXIT 
	file_sizes="$tmp/sketch_file_sizes.csv"
	echo "type,size" > "$file_sizes"
	
	#mix dustbin sketches to obtain 4000 genomes
	type="dustbin"
	dustbin_files=("part_17/dustbin__01.tar.xz" "part_17/dustbin__02.tar.xz" "part_24/dustbin__21.tar.xz" "part_24/dustbin__22.tar.xz")
	echo "Computing mash sketches for 4000 dustbin genomes..."
	for dustbin_file in "${dustbin_files[@]}"; do
		echo "Computing sketches from $dustbin_file"
		eval "$src_path/compute_sketches_from_archive.sh $inputs_dir/$dustbin_file $s" 2> /dev/null
	done
	echo "Computing compression rate according to preset"
	size=$(eval "$src_path/benchmark.sh $sketches $tmp/memory_$type.csv")
	echo "$type,$size" >> "$file_sizes"
	
	eval "$src_path/clean.sh"
	
	#compute compression ratio for ngono
	type="ngono"
	echo "Computing mash sketches for 4000 ngono genomes (phylogenetically ordered)..."
	eval "$src_path/compute_sketches_from_archive.sh $inputs_dir/part_54/neisseria_gonorrhoeae__01.tar.xz $s" 2> /dev/null
	echo "Computing compression rate according to preset"
	size=$(eval "$src_path/benchmark.sh $sketches $tmp/memory_$type.csv")
	echo "$type,$size" >> "$file_sizes"
	eval "$src_path/clean.sh"
	
	#plot
	eval "$src_path/plot_compression_ratio_according_to_label.py $tmp type 'Comparison of dustbin and ngono compression for s = $s'"
}

#Figure : comparison between phylogenetically ordered ngono's and randomly ordered ngono's compression rate
compare_order_ngono () {
	s="$1"
	n=30
	tmp=$(mktemp -d)
	trap 'rm -rf "$tmp"' EXIT 
	file_sizes="$tmp/sketch_file_sizes.csv"
	echo "order,size" > "$file_sizes"
	
	#phylogenetic order
	order="phylogenetic"
	echo "Computing mash sketches for 4000 ngono genomes (phylogenetically ordered)..."
	eval "$src_path/compute_sketches_from_archive.sh $inputs_dir/part_54/neisseria_gonorrhoeae__01.tar.xz $s" 2> /dev/null
	echo "Computing compression rate according to preset"
	size=$(eval "$src_path/benchmark.sh $sketches $tmp/memory_$order.csv")
	echo "$order,$size" >> "$file_sizes"
	
	#Random orders
	min_order="min"
	max_order="max"
	min_file="$tmp/memory_$min_order.csv"
	max_file="$tmp/memory_$min_order.csv"
	echo "preset,XZ memory usage,GZIP memory usage">"$min_file"
	echo "preset,XZ memory usage,GZIP memory usage">"$max_file"
	
	min_values=()
	max_values=()
	
	echo "Computing compression rate for $n random orders"
	for i in $(seq 1 "$n"); do
		echo "Order #$i"
		eval "$src_path/shuffle.py $sketches $i"
		mapfile -t current_values < <("$src_path/benchmark_yield.sh")
		
		#update min/max values
		if [ $i -eq 1 ]; then
			min_values=("${current_values[@]}")
			max_values=("${current_values[@]}")
		else
			for j in "${!current_values[@]}"; do
				if (( $(echo "${current_values[j]} < ${min_values[j]}" | bc -l) )); then
					min_values[j]=${current_values[j]}
				fi
			done
			for j in "${!current_values[@]}"; do
				if (( $(echo "${current_values[j]} > ${max_values[j]}" | bc -l) )); then
					max_values[j]=${current_values[j]}
				fi
			done
		fi
	done
	#writing results in files
	for i in $(seq 0 8); do
		index_xz=$((2 * i))
		index_gzip=$((index + 1))
		preset=$((i + 1))
		echo "$preset,${min_values[index_xz]},${min_values[index_gzip]}" >> "$min_file"
		echo "$preset,${max_values[index_xz]},${max_values[index_gzip]}" >> "$max_file"
	done
	eval "$src_path/clean.sh"
	echo "$min_order,$size" >> "$file_sizes"
	echo "$max_order,$size" >> "$file_sizes"
	
	#plot
	eval "$src_path/plot_compression_ratio_according_to_label.py $tmp order 'Comparison of phylogenetically ordered ngonos vs random ngonos compression rate for s = $s'"
}

#  ******** Create and download inputs ********
parts=("part_54" "part_17" "part_24")

if [ ! -d "$inputs_dir" ]; then 
	echo "Creating input directory: $inputs_dir"
	mkdir -p "$inputs_dir"
fi
for part in "${parts[@]}"; do 
	download_part "$part"
done
echo "Inputs created."
echo;
#  ******** Create figures from input ********
#size_variation

#compare_dustbin_ngono 1000

compare_order_ngono 500
