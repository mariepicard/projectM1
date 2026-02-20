#ifndef MATRIX_HPP
#define MATRIX_HPP

#include <vector>
#include <string>
#include <sdsl/bit_vectors.hpp>

#include "utilities.hpp"


using namespace sdsl;

class PAM {

    size_t g; // nb of colmuns
    size_t r; // nb of rows
    sdsl::bit_vector matrix;

public :
    PAM() {};
    PAM(std::vector<std::string> filenames, std::vector<uint64_t> union_hashes); //build from archive
    PAM(std::string filename); //load from disk

    void dump(std::string filename); //dump on disk

    std::vector<bool> get_column(uint i);//to retrieve sketch

    std::vector<std::vector<bool>> get_rows(std::vector<uint> rows); //rows from intersection
    
};

#endif