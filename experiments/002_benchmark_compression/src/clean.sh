#!/bin/bash

DIRS=("sketches")

for DIR in $DIRS; do
	eval "rm -r $DIR"
done

echo "All output files deleted"
