#include <city.h>
#include <citycrc.h>

#include <iostream>
#include <cstdlib>


inline std::ostream& operator<< (std::ostream& s, const uint128& d) {
    s << "H: " << d.first << " L: " << d.second;
    return s;
}


int main() {
    const char data[] = "dAAAAAAAAAAAAAAta";
    std::cout << "CityHash64: " << CityHash64(data, sizeof(data)) << std::endl;
    //std::cout << "CityHashCrc128: " << CityHashCrc128(data, sizeof(data)) << std::endl;
    return EXIT_SUCCESS;
}
