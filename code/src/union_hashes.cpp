#include "union_hashes.hpp"

#include <algorithm>
#include <cmath>
#include <iostream>
#include <iterator>
#include <vector>
#include <string>
#include <stdexcept>
#include <fstream>


std::vector<uint64_t> merge_all(const std::vector<std::string>& filenames) {
    std::vector<uint64_t> union_hashes;
    std::vector<uint64_t> new_union;
    for (const auto& name : filenames) {
        // 1st step : read JSON file -> should be upgraded to directly read .msh file
        std::vector<uint64_t> vi = get_hashes_from_JSON(name);

        //2nd step : merge with precedent

        new_union.clear();
        std::set_union(union_hashes.cbegin(), union_hashes.cend(),
                        vi.cbegin(), vi.cend(),
                        std::back_inserter(new_union));
        union_hashes = new_union;
    }
    return new_union;
}

size_t log(uint64_t n){//gives the number of bits in the representation of an integer
    size_t l = 0;
    while (n != 0){
        l++;
        n >>= 1;
    }
    return l;
}

sdsl::bit_vector elias_fano_encode(const std::vector<uint64_t>& input) {
    //basic EF -implementation -> could probably be improved
    if (input.empty())
        return {};

    const uint64_t n = input.size();
    const uint64_t max_value = input.back();

    const size_t U = log(n); // number of upper bits
    const size_t L = log(max_value) - U; // number od lower bits
    const size_t upper_size = (1ULL << U) + n;
    const size_t lower_size = L*n;

    // mask to extract lower L bits
    uint64_t lower_mask = (L == 64) ? ~0ULL : ((1ULL << L) - 1ULL);

    sdsl::bit_vector bv(upper_size + lower_size, 0);

    for (size_t i = 0; i < n; ++i) {
        // encode upper bits
        size_t pos = (input[i] >> L) + i;
        bv[pos] = 1;

        //encode lower bits (hard encode)
        uint64_t lower = input[i] & lower_mask;

        for (size_t b = 0; b < L; ++b) {
            bv[upper_size + i * L + b] = (lower >> b) & 1ULL;
        }
    }

    return bv;
}

Union::Union(const std::vector<std::string>& filenames) {
    std::vector<uint64_t> sorted_union = merge_all(filenames);
    n = sorted_union.size();
    m = sorted_union.back();
    elias_fano_representation = elias_fano_encode(sorted_union);
    
}

std::vector<uint64_t> Union::decompress_union() {
    std::vector<uint64_t> result;
    result.reserve(n);
    const size_t U = log(n);
    const size_t upper_bits_size = (1 << U) + n;

    const size_t nb_lower_bits = log(m) - U;

    uint64_t zeros_count = 0;
    uint64_t position_in_upper_bits = 0;

    for (uint64_t i = 0; i < n; i ++){
        //could probably be improved to limit cache misses because we constantly jump from one part of the array to another
        uint64_t value = 0;
        //decode lower bits
        for (uint64_t b = 0; b < nb_lower_bits; ++b) {
            if (elias_fano_representation[i * nb_lower_bits + b + upper_bits_size]) {
                value |= (1ULL << b);
            }
        }

        //decode upper bits
        while (!elias_fano_representation[position_in_upper_bits]) { //reading ones : increment the value
            zeros_count ++;
            position_in_upper_bits++;
        }
        value |= (zeros_count << (nb_lower_bits)); //found a 1
        result.push_back(value);
    }
    return result;

}