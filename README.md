# Safenet Emergency Wi-Fi Connector

A lightweight Python Tkinter desktop application designed for Linux systems to quickly scan and connect to designated emergency Wi-Fi access points (such as **Safenet**) during power outages, routerless environments, or new property deployments.

---

## Features

* **Quick Connection:** Connect to open or WPA-protected Wi-Fi networks via a clean GUI.
* **NetworkManager Integration:** Uses native Linux `nmcli` for reliable connection management.
* **Simple Interface:** Lightweight desktop UI built with Python's native Tkinter library.
* **Status Feedback:** Live updates on connection status, timeouts, and errors.

---

## Prerequisites

This application relies on Linux's `NetworkManager` engine and Python 3.

Ensure `nmcli` and `python3-tk` are installed on your Linux distribution:

```bash
sudo apt update
sudo apt install python3-tk network-manager
