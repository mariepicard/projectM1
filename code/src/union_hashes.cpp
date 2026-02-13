#include "union_hashes.cpp"

#include <algorithm>
#include <cmath>
#include <iostream>
#include <iterator>
#include <vector>
#include <string>
#include <stdexcept>
#include <fstream>
#include <nlohmann/json.hpp>



std::vector<uint64_t> merge_all(const std::vector<std::string>& filenames) {
    std::vector<uint64_t> union_hashes;
    std::vector<uint64_t> new_union;
    for (const auto& name : filenames) {
        // 1st step : read JSON file -> should be upgraded to directly read .msh file
        std::vector<uint64_t> vi;
        vi.reserve(name.size())
        std::ifstream in(name);
        if (!in) {
            throw std::runtime_error("Cannot open file: " + name);
        }

        nlohmann::json j;
        in >> j;

        if (!j.is_array()) {
            throw std::runtime_error("JSON is not an array in: " + name);
        }

        vi.emplace_back(j.get<std::vector<uint64_t>>());

        //2nd step : merge with precedent

        new_union.clear()
        std::set_union(union_hashes.cbegin(), union_hashes.cend(),
                        vi.cbegin(), vi.cend(),
                        std::back_inserter(new_union));
        union_hashes = new_union;
    }
    return new_union;
}

size_t log(int n){//gives the number of bits in the representation of an integer
    size_t l = 0
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

    const size_t n = input.size();
    const uint64_t max_value = input.back();

    const size_t U = log(n); // number of upper bits
    const size_t L = log(m) - u; // number od lower bits
    const size_t upper_size = (1ULL << U) + n;
    const size_t lower_size = L*n;

    // Mask to extract lower L bits
    uint64_t lower_mask = (L == 64) ? ~0ULL : ((1ULL << L) - 1ULL);

    sdsl::bit_vector bv(upper_size + lower_size, 0);

    for (size_t i = 0; i < n; ++i) {
        // encode upper bits
        size_t pos = upper_values[i] + i;
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
    std::vector<uint64_t> sorted_union = sorted_union_from_files(filenames);
    elias_fano_representation = elias_fano_encoding(sorted_union);
    
}