#ifndef UTILS_HPP
#define UTILS_HPP

#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <type_traits>

namespace Terminal {

std::string join_strings(const std::vector<std::string> input_strings, const std::string delimiter) {

    std::string result;

    for (const auto& input_string : input_strings) {
        result += input_string + delimiter;
    }
    
    return result.substr(0, result.size() - delimiter.size());
}

std::string get_time() {


    
}

/*
 *
 */
std::string convert_time() {

}

/*
 * Primary Template for GCD
 */
template<int A, int B>
struct GCD {
    static constexpr int value = GCD<B, A % B>::value;
};

/*
 * Base case specalization
 */
template<int A>
struct GCD<A, 0> {
    static constexpr int value = A;
};





}


#endif 