#ifndef UTILITIES_HPP
#define UTILITIES_HPP

#include <fstream>
#include <vector>
#include <string>
#include <stdexcept>
#include <nlohmann/json.hpp>

std::vector<uint64_t> get_hashes_from_JSON (const std::string& filename);

#endif