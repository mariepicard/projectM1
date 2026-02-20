#include "sketch_matrix.hpp"
#include <nlohmann/json.hpp>

PAM::PAM(std::vector<std::string> filenames, std::vector<uint64_t> union_hashes){
    g = filenames.size();
    r = union_hashes.size();
    matrix = sdsl::bit_vector(g*r, 0);

    size_t column_nb = 0;

    for (const auto& name : filenames) {
        // 1st step : read JSON file -> should be upgraded to directly read .msh file
        std::vector<uint64_t> vi;
        vi.reserve(name.size());
        std::ifstream in(name);
        if (!in) {
            throw std::runtime_error("Cannot open file: " + name);
        }

        nlohmann::json j;
        in >> j;

        if (!j.is_array()) {
            throw std::runtime_error("JSON is not an array in: " + name);
        }

        vi = j.get<std::vector<uint64_t>>();

        size_t row_i = 0;
        for (size_t row_nb = 0; row_nb < union_hashes.size(); row_nb++) {
            if (vi[row_i] == union_hashes[row_nb]) {
                matrix[r*column_nb + row_nb] = 1;
                row_i ++;
            }
        }
        column_nb ++;
    }
}

void PAM::dump(std::string filename){
    sdsl::store_to_file(matrix, filename);
}