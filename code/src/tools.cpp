#include "tools.hpp"

Mash::Mash(std::vector<std::string> filenames) : 
    union_hashes(filenames), filenames_(filenames)
    {
    matrix = PAM(filenames, union_hashes.decompress_union());

}

void Mash::dump(std::string output_directory) {
    std::filesystem::create_directory(output_directory);
    union_hashes.dump(output_directory + "/union");
    matrix.dump(output_directory + "/matrix");

    /*

    std::ofstream output_file(output_directory+ "/filenames");

    std::ostream_iterator<std::string> output_iterator(output_file, "\n");
    std::copy(std::begin(filenames_), std::end(filenames_), output_iterator);
    */
}