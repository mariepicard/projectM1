#ifndef UTILITIES_HPP
#define UTILITIES_HPP

#include <fstream>
#include <vector>
#include <string>
#include <stdexcept>
#include <nlohmann/json.hpp>
#include <iostream>

std::vector<uint64_t> get_hashes_from_JSON (const std::string& filename);

void binary_representation(uint64_t n);

size_t log(uint64_t n);

#endif