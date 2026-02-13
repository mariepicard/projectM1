#include "tools.hpp"

Mash::Mash(std::vector<std::string> filenames) : 
    union_hashes(std::vector<std::string> filenames)
    {
    matrix = PAM(filenames, union_hashes);
    sketch_names = std::map<std::string, uint> ;

}