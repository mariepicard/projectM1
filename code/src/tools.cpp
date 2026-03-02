#include "tools.hpp"

Mash::Mash(std::vector<std::string> filenames) : 
    union_hashes(filenames)
    {
    matrix = PAM(filenames, union_hashes.decompress_union());
    sketch_names = std::map<std::string, uint> (); //should be fixed to associate filenames to indices in the matrix

}

void Mash::dump(std::string output_directory) {
    std::filesystem::create_directory(output_directory);
    union_hashes.dump(output_directory + std::string("/union"));
    matrix.dump(output_directory + std::string("/matrix"));
}