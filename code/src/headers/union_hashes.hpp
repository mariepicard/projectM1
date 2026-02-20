#ifndef UNION_HPP
#define UNION_HPP

#include <vector>
#include <string>
#include <sdsl/bit_vectors.hpp>

class Union {
    uint64_t n; //nb of elements in the union
    uint64_t m; //max elt
    sdsl::bit_vector elias_fano_representation;

public :
    Union(const std::vector<std::string>& filenames); //build from different sketches
    // Union(std::string filename); //load from disk

    void dump(std::string filename);

    std::vector<uint64_t> decompress_union();

    uint64_t get_hash(uint i);//get a specific hash
    uint get_hash_position(uint64_t hash); //get position from a specific hash -> useful for intersection
};

#endif