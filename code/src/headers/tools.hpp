#ifndef TOOLS_HPP
#define TOOLS_HPP

#include <vector>
#include <string>
#include <map>
#include <filesystem>
#include "sketch_matrix.hpp"
#include "union_hashes.hpp"

/** @brief : Implementation of an archive of mash sketches 
 */
class Mash {
    PAM matrix;
    Union union_hashes;
    std::map<std::string, uint> sketch_names;
    //add correspondance table between names of files and indices ?

public :
    //build
    Mash(std::vector<std::string> filenames);
    //load from compressed version
    Mash(std::string input_filename);

    //dump compressed version
    void dump(std::string output_filename);

    //decompression : retrieving whole archive
    void decompress(std::string output_directory);

    /****** UTILITIES ******/

    //get sketch at position i
    std::vector<uint64_t> get_sketch(uint i);

    //get distance between sketches at positions i and j
    double distance(uint i, uint j);


};

#endif