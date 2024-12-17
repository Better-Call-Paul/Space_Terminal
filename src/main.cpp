#include <utils.hpp>


int main() {
    std::cout << "Stable" << "\n";
    std::cout << Terminal::get_time() << "\n";
    auto now = std::chrono::system_clock::now();
    std:: cout << Terminal::convert_time(now) << "\n";
    return 0;
}