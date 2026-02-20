#include "tools.hpp"

Mash::Mash(std::vector<std::string> filenames) : 
    union_hashes(filenames)
    {
    matrix = PAM(filenames, union_hashes.decompress_union());
    sketch_names = std::map<std::string, uint> ();

}