#! /usr/bin/bash

ARCHIVE="sketches_archive.tar"

eval "tar -cf $ARCHIVE sketches"

for QUALITY in $(seq 1 9); do
	CMD="xz -T1 -k -"
	#echo "Running: ${CMD}$QUALITY $ARCHIVE"
	eval "${CMD}${QUALITY} ${ARCHIVE}"
	XZ_FILE_SIZE=$(stat -c %s "${ARCHIVE}.xz")
	eval "rm ${ARCHIVE}.xz"
	
	CMD="gzip -k -"
	#echo "Running: ${CMD}$QUALITY $ARCHIVE"
	eval "${CMD}${QUALITY} ${ARCHIVE}"
	GZ_FILE_SIZE=$(stat -c %s "${ARCHIVE}.gz")
	eval "rm ${ARCHIVE}.gz"
	
	echo "${XZ_FILE_SIZE}"
	echo "$GZ_FILE_SIZE"

	#echo "${QUALITY},${XZ_FILE_SIZE},${GZ_FILE_SIZE}" >> "$MEMORY_FILE"
done

#echo $(stat -c %s "$ARCHIVE")

rm "$ARCHIVE"
#echo "Done. Results saved to $MEMORY_FILE"

