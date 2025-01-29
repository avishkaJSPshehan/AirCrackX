import os
import re
import time

def scan_wifi():
    """Scans available Wi-Fi networks and returns them as a list of (SSID, Signal Strength)."""
    output = os.popen("netsh wlan show networks mode=Bssid").read()
    networks = output.split("SSID ")

    wifi_list = []  # Store Wi-Fi details

    for net in networks[1:]:  # Skip the first part before SSID 1
        ssid_match = re.search(r":\s(.+)", net.splitlines()[0])  # Extract SSID
        signal_match = re.findall(r"Signal\s*:\s([\d]+)%?", net)  # Extract all signal strengths
        
        if ssid_match:
            ssid = ssid_match.group(1).strip()
            signal_strength = signal_match[0] if signal_match else "Unknown"
            wifi_list.append((ssid, signal_strength))  # Append SSID and Signal Strength

    return wifi_list

def connect_to_wifi(ssid, password):
    """Connects to the selected Wi-Fi network using the provided SSID and password."""
    profile = f"""
    <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
        <name>{ssid}</name>
        <SSIDConfig>
            <SSID>
                <name>{ssid}</name>
            </SSID>
        </SSIDConfig>
        <connectionType>ESS</connectionType>
        <connectionMode>manual</connectionMode>
        <MSM>
            <security>
                <authEncryption>
                    <authentication>WPA2PSK</authentication>
                    <encryption>AES</encryption>
                    <useOneX>false</useOneX>
                </authEncryption>
                <sharedKey>
                    <keyType>passPhrase</keyType>
                    <protected>false</protected>
                    <keyMaterial>{password}</keyMaterial>
                </sharedKey>
            </security>
        </MSM>
    </WLANProfile>
    """

    # Save the Wi-Fi profile as an XML file
    profile_path = f"{ssid}.xml"
    with open(profile_path, "w") as file:
        file.write(profile)

    # Add the Wi-Fi profile
    os.system(f'netsh wlan add profile filename="{profile_path}"')

    # Connect to the Wi-Fi network
    os.system(f'netsh wlan connect name="{ssid}"')

    print(f"\nConnecting to {ssid}...")
    
    # Wait a few seconds for connection attempt
    time.sleep(5)

    # Check if the connection is successful
    if check_wifi_status(ssid):
        print(f"✅ Successfully connected to '{ssid}'.")
    else:
        print(f"❌ Not Connected or Wrong Password for '{ssid}'.")

def check_wifi_status(expected_ssid):
    """Checks if the system is connected to the specified Wi-Fi SSID."""
    output = os.popen("netsh wlan show interfaces").read()
    connected_match = re.search(r"SSID\s*:\s(.+)", output)

    if connected_match:
        current_ssid = connected_match.group(1).strip()
        return current_ssid == expected_ssid  # Check if connected to the desired SSID

    return False

# Main Execution
wifi_networks = scan_wifi()

if wifi_networks:
    print("\nAvailable Wi-Fi Networks:")
    for index, (ssid, signal) in enumerate(wifi_networks, start=1):
        print(f"{index}. SSID: {ssid} | Signal Strength: {signal}%")

    # Ask the user to select a network
    try:
        choice = int(input("\nEnter the number of the Wi-Fi network you want to connect to: "))
        if 1 <= choice <= len(wifi_networks):
            selected_ssid = wifi_networks[choice - 1][0]
            wifi_password = input(f"Enter password for '{selected_ssid}': ")
            connect_to_wifi(selected_ssid, wifi_password)
        else:
            print("Invalid choice. Please run the script again and select a valid option.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
else:
    print("No Wi-Fi networks found.")
