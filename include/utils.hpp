#ifndef UTILS_HPP
#define UTILS_HPP

#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <sstream>
#include <type_traits>
#include <iomanip>
#include <ctime>
#include <thread>
#include <random>

namespace Terminal {

std::string join_strings(const std::vector<std::string> input_strings, const std::string delimiter) {

    std::string result;

    for (const auto& input_string : input_strings) {
        result += input_string + delimiter;
    }
    
    return result.substr(0, result.size() - delimiter.size());
}

/*
 * Returns current time in (YYYY-MM-DD milliseconds)
 */
std::string get_time() {

    auto now = std::chrono::system_clock::now();
    std::time_t now_c = std::chrono::system_clock::to_time_t(now);

    // change to local time 
    std::tm now_tm = *std::localtime(&now_c);

    // format time 
    std::stringstream ss;
    ss << std::put_time(&now_tm, "%Y-%m-%d %H:%M:%S");

    // get the milliseconds separately
    auto milli = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()) % 1000;
    ss << '.' << std::setfill('0') << std::setw(3) << milli.count();

    return ss.str();
}

/*
 * convert from time point format to string
 */
std::string convert_time(std::chrono::system_clock::time_point now) {

    std::time_t now_c = std::chrono::system_clock::to_time_t(now);

    // change to local time 
    std::tm now_tm = *std::localtime(&now_c);

    // format time 
    std::stringstream ss;
    ss << std::put_time(&now_tm, "%Y-%m-%d %H:%M:%S");

    // get the milliseconds separately
    auto milli = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()) % 1000;
    ss << '.' << std::setfill('0') << std::setw(3) << milli.count();

    return ss.str();
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