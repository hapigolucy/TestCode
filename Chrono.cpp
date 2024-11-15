#include <iostream>
#include <fstream>
#include <chrono>
#include <string>
#include <iomanip>
#include <sstream>

int main() {
    // Original filename
    std::string baseFilename = "abc.out";

    // Get the current time point
    auto now = std::chrono::system_clock::now();

    // Convert to time_t to get seconds since the epoch
    auto timeT = std::chrono::system_clock::to_time_t(now);

    // Get the microseconds part
    auto microseconds = std::chrono::duration_cast<std::chrono::microseconds>(
                            now.time_since_epoch()).count() % 1000000;

    // Create a timestamp string with microseconds
    std::ostringstream timestampStream;
    timestampStream << std::put_time(std::localtime(&timeT), "%Y%m%d%H%M%S")
                    << "." << std::setfill('0') << std::setw(6) << microseconds;

    std::string timestamp = timestampStream.str();

    // Append the timestamp to the filename
    std::string timestampedFilename = baseFilename + "." + timestamp;

    // Create and open the file
    std::ofstream file(timestampedFilename);
    if (file.is_open()) {
        std::cout << "File created: " << timestampedFilename << std::endl;
        file.close();
    } else {
        std::cerr << "Error creating file: " << timestampedFilename << std::endl;
    }

    return 0;
}
