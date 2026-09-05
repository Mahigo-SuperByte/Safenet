import os
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk


class EmergencyWifiApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Safenet Emergency Wi-Fi Connector")
    self.root.geometry("400x300")
    self.root.resizable(False, False)

    # Header
    self.header = tk.Label(
        root,
        text="Emergency Wi-Fi Manager",
        font=("Helvetica", 14, "bold"),
        fg="#2c3e50",
    )
    self.header.pack(pady=15)

    # Target SSID Entry
    self.ssid_frame = tk.Frame(root)
    self.ssid_frame.pack(pady=5)

    tk.Label(
        self.ssid_frame, text="Target Network:", font=("Helvetica", 10)
    ).pack(side=tk.LEFT, padx=5)
    self.ssid_entry = tk.Entry(
        self.ssid_frame, font=("Helvetica", 10), width=18
    )
    self.ssid_entry.insert(0, "Safenet")
    self.ssid_entry.pack(side=tk.LEFT, padx=5)

    # Password Entry (Leave blank if open/free network)
    self.pass_frame = tk.Frame(root)
    self.pass_frame.pack(pady=5)

    tk.Label(
        self.pass_frame, text="Password (Optional):", font=("Helvetica", 10)
    ).pack(side=tk.LEFT, padx=5)
    self.pass_entry = tk.Entry(
        self.pass_frame, font=("Helvetica", 10), width=18, show="*"
    )
    self.pass_entry.pack(side=tk.LEFT, padx=5)

    # Status Label
    self.status_label = tk.Label(
        root,
        text="Status: Ready to connect",
        font=("Helvetica", 9, "italic"),
        fg="#7f8c8d",
    )
    self.status_label.pack(pady=10)

    # Connect Button
    self.connect_btn = tk.Button(
        root,
        text="Connect to Safenet",
        font=("Helvetica", 11, "bold"),
        bg="#27ae60",
        fg="white",
        activebackground="#2ecc71",
        command=self.connect_wifi,
    )
    self.connect_btn.pack(pady=15, ipadx=10, ipady=5)

  def connect_wifi(self):
    ssid = self.ssid_entry.get().strip()
    password = self.pass_entry.get().strip()

    if not ssid:
      messagebox.showwarning(
          "Input Error", "Please specify an SSID network name."
      )
      return

    self.status_label.config(
        text=f"Scanning & connecting to '{ssid}'...", fg="#d35400"
    )
    self.root.update_idletasks()

    # Build nmcli command line
    cmd = ["nmcli", "dev", "wifi", "connect", ssid]
    if password:
      cmd.extend(["password", password])

    try:
      result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)

      if result.returncode == 0:
        self.status_label.config(
            text=f"Connected to '{ssid}'!", fg="#27ae60"
        )
        messagebox.showinfo(
            "Success", f"Successfully connected to Wi-Fi network: {ssid}"
        )
      else:
        self.status_label.config(text="Connection failed.", fg="#c0392b")
        messagebox.showerror(
            "Connection Error",
            f"Failed to connect to {ssid}.\n\nEnsure hardware/hotspot is active.\n\nDetails: {result.stderr}",
        )
    except subprocess.TimeoutExpired:
      self.status_label.config(text="Request timed out.", fg="#c0392b")
      messagebox.showerror(
          "Timeout", "The connection attempt timed out searching for Safenet."
      )
    except Exception as e:
      self.status_label.config(text="Error occurred.", fg="#c0392b")
      messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
  root = tk.Tk()
  app = EmergencyWifiApp(root)
  root.mainloop()
