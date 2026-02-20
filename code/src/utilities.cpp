#include "utilities.hpp"

std::vector<uint64_t> get_hashes_from_JSON (const std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        throw std::runtime_error("Failed to open JSON file: " + filename);
    }
    nlohmann::json j;
    file >> j;

    // Navigate using JSON pointer
    std::string path = "/sketches/0/hashes";
    nlohmann::json::json_pointer ptr(path);

    if (!j.contains(ptr)) {
        throw std::runtime_error("Path does not exist: " + path);
    }

    const nlohmann::json& target = j.at(ptr);

    if (!target.is_array()) {
        throw std::runtime_error("Target at path is not an array: " + path);
    }

    // Convert to vector<uint64_t>
    try {
        return target.get<std::vector<uint64_t>>();
    } catch (const nlohmann::json::exception& e) {
        throw std::runtime_error(
            std::string("Array conversion to uint64_t failed: ") + e.what());
    }
}

size_t log(uint64_t n){//gives the number of bits in the representation of an integer
    size_t l = 0;
    while (n != 0){
        l++;
        n >>= 1;
    }
    return l;
}

void binary_representation(uint64_t n) {
    size_t l = log(n);
    for (size_t i = 0; i < l; i++) {
        std::cout << ((n >> (l - 1 - i)) & 1ULL);
    }
    std::cout << std::endl;
}