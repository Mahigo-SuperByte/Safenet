use std::io::{self, Write};
use std::process::Command;

fn get_input(prompt: &str, default: &str) -> String {
    print!("{}", prompt);
    io::stdout().flush().unwrap();
    
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    
    let trimmed = input.trim();
    if trimmed.is_empty() {
        default.to_string()
    } else {
        trimmed.to_string()
    }
}

fn execute_command(cmd: &mut Command) {
    match cmd.output() {
        Ok(output) => {
            println!("\n[OUTPUT]:\n{}", String::from_utf8_lossy(&output.stdout));
            if !output.stderr.is_empty() {
                println!("[ERROR]:\n{}", String::from_utf8_lossy(&output.stderr));
            }
        }
        Err(e) => println!("Failed to execute command: {}", e),
    }
}

fn main() {
    println!("======================================");
    println!(" Safenet Emergency Wi-Fi CLI (Rust)");
    println!("======================================");
    println!("1. Connect to a Wi-Fi Network");
    println!("2. Start a Virtual Hotspot");
    println!("3. Stop Virtual Hotspot\n");
    
    let choice = get_input("Select an option (1-3): ", "");

    match choice.as_str() {
        "1" => {
            let ssid = get_input("Enter SSID (default: Safenet): ", "Safenet");
            let password = get_input("Enter Password (leave blank if open): ", "");
            
            println!("Connecting to {}...", ssid);
            let mut cmd = Command::new("nmcli");
            cmd.arg("dev").arg("wifi").arg("connect").arg(&ssid);
            
            if !password.is_empty() {
                cmd.arg("password").arg(&password);
            }
            execute_command(&mut cmd);
        }
        "2" => {
            let ssid = get_input("Enter Hotspot SSID (default: Safenet_Hotspot): ", "Safenet_Hotspot");
            let password = get_input("Enter Hotspot Password (min 8 chars): ", "SafenetPassword123");
            
            println!("Starting Hotspot {}...", ssid);
            let mut cmd = Command::new("nmcli");
            cmd.args(["device", "wifi", "hotspot", "ifname", "wlan0", "ssid", &ssid, "password", &password]);
            execute_command(&mut cmd);
        }
        "3" => {
            println!("Stopping Hotspot...");
            let mut cmd = Command::new("nmcli");
            cmd.args(["connection", "down", "Hotspot"]);
            execute_command(&mut cmd);
        }
        _ => println!("Invalid option. Exiting."),
    }
}
