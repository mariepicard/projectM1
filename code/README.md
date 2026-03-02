# Phylogenetic-ordered sketch compression (POSC)

## What is it ?

POSC is a tool meant for compression of large amounts of closely related genome sketches. At the moment, it is only meant to compress `mash` sketches. 

POSC relies on phylogenetic closeness of the genomes : it is mostly meant to compress large amounts of mash sketches from the same species. Please look at [this archive](https://zenodo.org/records/15367750) for examples of high-quality phylogenetically ordered genomes.

## Install

### Dependencies

This project uses [`sdsl-lite`](https://github.com/simongog/sdsl-lite). 
It uses a [JSON parser](https://github.com/nlohmann/json) from nlohmann.

### Build

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