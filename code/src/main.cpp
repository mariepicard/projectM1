#include <iostream>
#include <string>
#include <filesystem>

#include "tools.hpp"

void usage(std::string process_name){
    std::cerr << "Usage : " << std::endl;
    std::cerr << process_name << " <archive of JSON files> [output_directory = test_archive]" << std::endl;
    return;
}

void help(){
    return;
}

int main(int argc, char** argv){
    //parse command : compress, decompress, get_sketch, get_distance
    std::cout << "Warning : parsing not well implemented yet" << std::endl;
    if (argc < 2 || argc > 3) {
        usage(std::string(argv[0]));
        return 1;
    }
    std::string archive = std::string(argv[1]);
    std::string output_directory = "./test_archive";
    if (argc == 3) {
        output_directory = std::string(argv[2]);
    }
    std::vector<std::string> filenames;
    for (const auto & entry : std::filesystem::directory_iterator(archive)){
        filenames.push_back(entry.path());
    }

    Mash compacted_archive = Mash(filenames);
    compacted_archive.dump(output_directory);
    return 0;
}