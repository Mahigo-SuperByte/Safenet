#include <iostream>
#include <string>
#include <array>
#include <memory>
#include <stdexcept>

// Helper function to execute a shell command and capture its output
std::string executeCommand(const std::string& cmd) {
    std::array<char, 128> buffer;
    std::string result;
    // Open pipe to command
    std::unique_ptr<FILE, decltype(&pclose)> pipe(popen(cmd.c_str(), "r"), pclose);
    if (!pipe) {
        throw std::runtime_error("popen() failed!");
    }
    // Read output till end
    while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
        result += buffer.data();
    }
    return result;
}

void connectWiFi() {
    std::string ssid, password;
    std::cout << "Enter SSID (default: Safenet): ";
    std::getline(std::cin, ssid);
    if (ssid.empty()) ssid = "Safenet";

    std::cout << "Enter Password (leave blank if open): ";
    std::getline(std::cin, password);

    std::string cmd = "nmcli dev wifi connect \"" + ssid + "\"";
    if (!password.empty()) {
        cmd += " password \"" + password + "\"";
    }

    std::cout << "\nConnecting...\n";
    std::cout << executeCommand(cmd) << std::endl;
}

void startHotspot() {
    std::string ssid, password;
    std::cout << "Enter Hotspot SSID (default: Safenet_Hotspot): ";
    std::getline(std::cin, ssid);
    if (ssid.empty()) ssid = "Safenet_Hotspot";

    std::cout << "Enter Hotspot Password (min 8 chars): ";
    std::getline(std::cin, password);

    std::string cmd = "nmcli device wifi hotspot ifname wlan0 ssid \"" + ssid + "\" password \"" + password + "\"";
    
    std::cout << "\nStarting Hotspot...\n";
    std::cout << executeCommand(cmd) << std::endl;
}

void stopHotspot() {
    std::cout << "\nStopping Hotspot...\n";
    std::cout << executeCommand("nmcli connection down Hotspot") << std::endl;
}

int main() {
    std::string choice;
    std::cout << "======================================\n";
    std::cout << " Safenet Emergency Wi-Fi CLI (C++)\n";
    std::cout << "======================================\n";
    std::cout << "1. Connect to a Wi-Fi Network\n";
    std::cout << "2. Start a Virtual Hotspot\n";
    std::cout << "3. Stop Virtual Hotspot\n\n";
    std::cout << "Select an option (1-3): ";
    
    std::getline(std::cin, choice);

    if (choice == "1") connectWiFi();
    else if (choice == "2") startHotspot();
    else if (choice == "3") stopHotspot();
    else std::cout << "Invalid option. Exiting.\n";

    return 0;
}
