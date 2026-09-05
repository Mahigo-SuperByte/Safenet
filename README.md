# Safenet Emergency Wi-Fi & Virtual AP Suite

A lightweight, multi-purpose Python Tkinter desktop application for Linux. Designed for emergency deployments, power outages, and routerless environments, this suite allows you to quickly connect to designated emergency networks (Client Mode) or turn your Linux machine into a Wi-Fi router to broadcast a network (Virtual AP Mode).

---

## Features

* **Dual-Mode Interface:** Tabbed GUI to easily switch between connecting to Wi-Fi and hosting a Wi-Fi hotspot.
* **Client Mode:** Quickly scan and connect to open or WPA-protected networks (e.g., `Safenet`).
* **Virtual AP Mode:** Broadcast a virtual Wi-Fi network (Hotspot) directly from your Linux machine's wireless interface to share local connectivity with other devices.
* **NetworkManager Integration:** Built natively on Linux's `nmcli` for robust and system-level connection management.
* **Modular Codebase:** Cleanly separated Python files for configuration, connection logic, and GUI management.

---

## Repository Structure

```text
safenet-wifi-connector/
├── README.md           # Project documentation
├── main.py             # Main GUI application and entry point
├── config.py           # Centralized configuration and default settings
├── wifi_connector.py   # Client-mode connection logic
├── virtual_ap.py       # Virtual Hotspot/Access Point creation logic
└── setup.sh            # Automated dependency installer script
