#include <iostream>
#include <map>
#include <string>
#include <fstream>
#include <mutex>

// Define the class to be used as the key for the std::map
class MyClass {
public:
    // Define any necessary member variables and methods here
    std::string first_name;
    std::string last_name;
    // Constructor
    MyClass(std::string first, std::string last) : first_name(first), last_name(last) {}
    // Define the < operator for use as the key in std::map
    bool operator<(const MyClass& other) const {
        if (last_name == other.last_name) {
            return first_name < other.first_name;
        }
        return last_name < other.last_name;
    }
    // Define the output operator for MyClass objects
    friend std::ostream& operator<<(std::ostream& os, const MyClass& obj) {
        os << "MyClass(" << obj.first_name << ", " << obj.last_name << ")";
        return os;
    }
};

// Define the class to be used as the value for the std::map
class MyValue {
public:
    // Define any necessary member variables and methods here
    std::string value1;
    std::string value2;
    // Constructor
    MyValue(std::string v1, std::string v2) : value1(v1), value2(v2) {}
    // Define the output operator for MyValue objects
    friend std::ostream& operator<<(std::ostream& os, const MyValue& obj) {
        os << "MyValue(" << obj.value1 << ", " << obj.value2 << ")";
        return os;
    }
};

class FileStats {
public:
    FileStats(const std::map<MyClass, MyValue>& data) {}

    int GetTotalCount() const {
        std::lock_guard<std::mutex> lock(mutex_);
        int total = 0;
        for (auto it = data_.cbegin(); it != data_.cend(); ++it) {
            total += it->second.value1.length() + it->second.value2.length();
        }
        return total;
    }

    int GetCountForName(const std::string& name) const {
        std::lock_guard<std::mutex> lock(mutex_);
        int count = 0;
        for (auto it = data_.cbegin(); it != data_.cend(); ++it) {
            if (it->first.last_name == name) {
                count += it->second.value1.length() + it->second.value2.length();
            }
        }
        return count;
    }

    void WriteToFile(const std::string& filename) const {
        std::lock_guard<std::mutex> lock(mutex_);
        std::ofstream outfile(filename);
        if (!outfile.is_open()) {
            std::cerr << "Error: Unable to open file " << filename << " for writing." << std::endl;
            return;
        }
        for (auto it = data_.cbegin(); it != data_.cend(); ++it) {
            outfile << it->first.first_name << "," << it->first.last_name << ","
                    << it->second.value1 << "," << it->second.value2 << std::endl;
        }
        outfile.close();
    }

private:
    static std::map<MyClass, MyValue> data_;
    mutable std::mutex mutex_;
};

std::map<MyClass, MyValue> FileStats::data_;
