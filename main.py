"""Main GUI entry point combining Wi-Fi client connection and Virtual Hotspot creation."""

import tkinter as tk
from tkinter import messagebox, ttk
import config
from virtual_ap import VirtualAPManager
import wifi_connector


class SafenetApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Safenet Wi-Fi & Virtual AP Suite")
    self.root.geometry("460x380")
    self.root.resizable(False, False)

    # Tab Container
    self.notebook = ttk.Notebook(root)
    self.notebook.pack(expand=True, fill="both")

    # Tab 1: Connect
    self.connect_tab = ttk.Frame(self.notebook)
    self.notebook.add(self.connect_tab, text="Connect to Network")
    self.setup_connect_ui()

    # Tab 2: Virtual Hotspot
    self.ap_tab = ttk.Frame(self.notebook)
    self.notebook.add(self.ap_tab, text="Virtual AP Host")
    self.setup_ap_ui()

  def setup_connect_ui(self):
    frame = tk.Frame(self.connect_tab, padding=10)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame, text="Client Wi-Fi Connector", font=("Helvetica", 12, "bold")
    ).pack(pady=10)

    self.ssid_entry = self._create_input_field(
        frame, "Network Name:", config.DEFAULT_SSID
    )
    self.pass_entry = self._create_input_field(
        frame, "Password (Optional):", "", show="*"
    )

    self.status_label = tk.Label(
        frame,
        text="Status: Ready",
        font=("Helvetica", 9, "italic"),
        fg="#7f8c8d",
    )
    self.status_label.pack(pady=10)

    tk.Button(
        frame,
        text="Connect to Network",
        bg="#27ae60",
        fg="white",
        font=("Helvetica", 10, "bold"),
        command=self.handle_connect,
    ).pack(pady=10, ipadx=10, ipady=3)

  def setup_ap_ui(self):
    frame = tk.Frame(self.ap_tab, padding=10)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame, text="Virtual Hotspot Broadcaster", font=("Helvetica", 12, "bold")
    ).pack(pady=10)

    self.ap_ssid_entry = self._create_input_field(
        frame, "Hotspot SSID:", config.DEFAULT_AP_SSID
    )
    self.ap_pass_entry = self._create_input_field(
        frame, "Hotspot Password:", config.DEFAULT_AP_PASSWORD, show="*"
    )

    self.ap_status_label = tk.Label(
        frame,
        text="Hotspot: Inactive",
        font=("Helvetica", 9, "italic"),
        fg="#7f8c8d",
    )
    self.ap_status_label.pack(pady=10)

    btn_frame = tk.Frame(frame)
    btn_frame.pack(pady=5)

    tk.Button(
        btn_frame,
        text="Start Hotspot",
        bg="#2980b9",
        fg="white",
        font=("Helvetica", 10, "bold"),
        command=self.handle_start_ap,
    ).pack(side=tk.LEFT, padx=5, ipadx=5)
    tk.Button(
        btn_frame,
        text="Stop Hotspot",
        bg="#c0392b",
        fg="white",
        font=("Helvetica", 10, "bold"),
        command=self.handle_stop_ap,
    ).pack(side=tk.LEFT, padx=5, ipadx=5)

  def _create_input_field(self, parent, label_text, default_val, show=None):
    f = tk.Frame(parent)
    f.pack(pady=5, fill="x")
    tk.Label(f, text=label_text, width=18, anchor="w").pack(side=tk.LEFT)
    e = tk.Entry(f, show=show) if show else tk.Entry(f)
    e.insert(0, default_val)
    e.pack(side=tk.LEFT, fill="x", expand=True)
    return e

  def handle_connect(self):
    ssid = self.ssid_entry.get().strip()
    pwd = self.pass_entry.get().strip()
    self.status_label.config(text=f"Connecting to {ssid}...", fg="#d35400")
    self.root.update_idletasks()

    success, msg = wifi_connector.connect_to_network(ssid, pwd)
    if success:
      self.status_label.config(text="Connected!", fg="#27ae60")
      messagebox.showinfo("Success", msg)
    else:
      self.status_label.config(text="Failed to connect.", fg="#c0392b")
      messagebox.showerror("Error", msg)

  def handle_start_ap(self):
    ssid = self.ap_ssid_entry.get().strip()
    pwd = self.ap_pass_entry.get().strip()
    success, msg = VirtualAPManager.create_hotspot(ssid, pwd)
    if success:
      self.ap_status_label.config(
          text=f"Broadcasting '{ssid}'", fg="#27ae60"
      )
      messagebox.showinfo("Hotspot Active", msg)
    else:
      self.ap_status_label.config(text="Failed to start AP.", fg="#c0392b")
      messagebox.showerror("Error", msg)

  def handle_stop_ap(self):
    success, msg = VirtualAPManager.stop_hotspot()
    if success:
      self.ap_status_label.config(text="Hotspot: Inactive", fg="#7f8c8d")
      messagebox.showinfo("Hotspot Stopped", msg)
    else:
      messagebox.showerror("Error", msg)


if __name__ == "__main__":
  root = tk.Tk()
  app = SafenetApp(root)
  root.mainloop()
