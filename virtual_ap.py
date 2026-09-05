"""Module to create and manage a Virtual Wi-Fi Access Point (Hotspot) on Linux."""

import subprocess
import config


class VirtualAPManager:

  @staticmethod
  def create_hotspot(
      ssid=config.DEFAULT_AP_SSID,
      password=config.DEFAULT_AP_PASSWORD,
      interface=config.AP_INTERFACE,
  ):
    """Creates and starts a virtual Wi-Fi access point."""
    cmd = [
        "nmcli",
        "device",
        "wifi",
        "hotspot",
        "ifname",
        interface,
        "ssid",
        ssid,
        "password",
        password,
    ]
    try:
      result = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
      if result.returncode == 0:
        return True, f"Virtual AP '{ssid}' started successfully."
      return False, f"Failed to start Hotspot: {result.stderr.strip()}"
    except Exception as e:
      return False, f"Error launching Hotspot: {str(e)}"

  @staticmethod
  def stop_hotspot(ssid=config.DEFAULT_AP_SSID):
    """Stops the virtual Wi-Fi access point."""
    cmd = ["nmcli", "connection", "down", "Hotspot"]
    try:
      result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
      if result.returncode == 0:
        return True, "Virtual AP stopped successfully."
      return False, f"Failed to stop Hotspot: {result.stderr.strip()}"
    except Exception as e:
      return False, f"Error stopping Hotspot: {str(e)}"
