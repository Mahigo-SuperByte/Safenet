#!/bin/bash
# Safenet Emergency Wi-Fi - Zenity GUI Version

# Ensure Zenity and nmcli are installed
if ! command -v zenity &> /dev/null; then
    echo "Zenity is required but not installed. Install it via: sudo apt install zenity"
    exit 1
fi

# Main Menu
CHOICE=$(zenity --list --title="Safenet Emergency Tool" \
    --text="Select an operation mode:" \
    --radiolist \
    --column="Select" --column="Mode" \
    TRUE "1. Connect to Wi-Fi" \
    FALSE "2. Start Virtual Hotspot" \
    FALSE "3. Stop Virtual Hotspot" \
    --width=400 --height=250)

# Cancelled
if [ -z "$CHOICE" ]; then
    exit 0
fi

if [[ "$CHOICE" == *"1. Connect"* ]]; then
    SSID=$(zenity --entry --title="Client Mode" --text="Enter target network SSID:" --entry-text="Safenet")
    if [ -z "$SSID" ]; then exit 0; fi
    
    PASS=$(zenity --entry --title="Client Mode" --text="Enter Password (leave blank if open):" --hide-text)
    
    zenity --info --title="Connecting..." --text="Attempting to connect to $SSID. Please wait..." --timeout=2
    
    if [ -z "$PASS" ]; then
        OUTPUT=$(nmcli dev wifi connect "$SSID" 2>&1)
    else
        OUTPUT=$(nmcli dev wifi connect "$SSID" password "$PASS" 2>&1)
    fi
    
    zenity --info --title="Result" --text="$OUTPUT"

elif [[ "$CHOICE" == *"2. Start"* ]]; then
    SSID=$(zenity --entry --title="Hotspot Mode" --text="Enter Hotspot SSID:" --entry-text="Safenet_Hotspot")
    PASS=$(zenity --entry --title="Hotspot Mode" --text="Enter Hotspot Password (min 8 chars):" --entry-text="SafenetPassword123")
    
    zenity --info --title="Starting..." --text="Starting virtual AP '$SSID'..." --timeout=2
    OUTPUT=$(nmcli device wifi hotspot ifname wlan0 ssid "$SSID" password "$PASS" 2>&1)
    zenity --info --title="Result" --text="$OUTPUT"

elif [[ "$CHOICE" == *"3. Stop"* ]]; then
    OUTPUT=$(nmcli connection down Hotspot 2>&1)
    zenity --info --title="Result" --text="$OUTPUT"
fi
