package main

import (
	"bufio"
	"fmt"
	"os"
	"os/exec"
	"strings"
)

func main() {
	reader := bufio.NewReader(os.Stdin)

	fmt.Println("======================================")
	fmt.Println(" Safenet Emergency Wi-Fi CLI (Golang) ")
	fmt.Println("======================================")
	fmt.Println("1. Connect to a Wi-Fi Network")
	fmt.Println("2. Start a Virtual Hotspot")
	fmt.Println("3. Stop Virtual Hotspot")
	fmt.Print("\nSelect an option (1-3): ")

	option, _ := reader.ReadString('\n')
	option = strings.TrimSpace(option)

	switch option {
	case "1":
		fmt.Print("Enter SSID (default: Safenet): ")
		ssid, _ := reader.ReadString('\n')
		ssid = strings.TrimSpace(ssid)
		if ssid == "" {
			ssid = "Safenet"
		}

		fmt.Print("Enter Password (leave blank if open): ")
		password, _ := reader.ReadString('\n')
		password = strings.TrimSpace(password)

		connectWiFi(ssid, password)

	case "2":
		fmt.Print("Enter Hotspot SSID (default: Safenet_Hotspot): ")
		ssid, _ := reader.ReadString('\n')
		ssid = strings.TrimSpace(ssid)
		if ssid == "" {
			ssid = "Safenet_Hotspot"
		}

		fmt.Print("Enter Hotspot Password (min 8 chars): ")
		password, _ := reader.ReadString('\n')
		password = strings.TrimSpace(password)

		startHotspot(ssid, password)

	case "3":
		stopHotspot()

	default:
		fmt.Println("Invalid option. Exiting.")
	}
}

func connectWiFi(ssid, password string) {
	fmt.Printf("Connecting to %s...\n", ssid)
	var cmd *exec.Cmd
	if password == "" {
		cmd = exec.Command("nmcli", "dev", "wifi", "connect", ssid)
	} else {
		cmd = exec.Command("nmcli", "dev", "wifi", "connect", ssid, "password", password)
	}
	executeCommand(cmd)
}

func startHotspot(ssid, password string) {
	fmt.Printf("Starting Virtual AP '%s'...\n", ssid)
	cmd := exec.Command("nmcli", "device", "wifi", "hotspot", "ifname", "wlan0", "ssid", ssid, "password", password)
	executeCommand(cmd)
}

func stopHotspot() {
	fmt.Println("Stopping Hotspot...")
	cmd := exec.Command("nmcli", "connection", "down", "Hotspot")
	executeCommand(cmd)
}

func executeCommand(cmd *exec.Cmd) {
	output, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Printf("\n[ERROR] Command failed: %v\n", err)
	}
	fmt.Printf("\n[OUTPUT]:\n%s\n", string(output))
}
