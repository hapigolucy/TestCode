#include <map>
#include <string>

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
};

// Define the class to be used as the value for the std::map
class MyValue {
public:
    // Define any necessary member variables and methods here
    std::string value1;
    std::string value2;
    // Constructor
    MyValue(std::string v1, std::string v2) : value1(v1), value2(v2) {}
};

class FileStats {
public:
    // Define the constructor which takes a std::map<MyClass, MyValue> object as input
    FileStats(const std::map<MyClass, MyValue>& data) : data_(data) {}

    // Define any necessary member functions here
    int GetTotalCount() const {
        int total = 0;
        for (auto it = data_.cbegin(); it != data_.cend(); ++it) {
            total += it->second.value1.length() + it->second.value2.length();
        }
        return total;
    }

    int GetCountForName(const std::string& name) const {
        int count = 0;
        for (auto it = data_.cbegin(); it != data_.cend(); ++it) {
            if (it->first.last_name == name) {
                count += it->second.value1.length() + it->second.value2.length();
            }
        }
        return count;
    }

private:
    std::map<MyClass, MyValue> data_;
};
