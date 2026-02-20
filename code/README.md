# Phylogenetic-ordered sketch compression (POSC)

## What is it ?

POSC is a tool meant for compression of large amounts of closely related genome sketches. At the moment, it is only meant to compress `mash` sketches. 

POSC relies on phylogenetic closeness of the genomes : it is mostly meant to compress large amounts of mash sketches from the same species. Please look at 

## Install

### Dependencies

This project uses [`sdsl-lite`](https://github.com/simongog/sdsl-lite)

Clone git directory, then run :

```bash

cmake -S . -B build
cmake --build build

```

## Run

The programm can then be run using 

```bash

build/bin/posc -options

```