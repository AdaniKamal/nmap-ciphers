import subprocess
import sys
import re
import os
import requests
from colorama import Fore, Style, init

# Initialize colorama
init()

# Define the API endpoint
API_ENDPOINT = "https://ciphersuite.info/api/cs"

def get_cipher_security_status(cipher_name):
    try:
        # Make a GET request to the API
        response = requests.get(f"{API_ENDPOINT}/{cipher_name}/")
        response.raise_for_status()
        data = response.json()
        security_status = data.get('security', 'Unknown')
        return security_status
    except Exception as e:
        print(f"Error fetching security status for {cipher_name}: {e}")
        return "Error"

def display_security_status(cipher_name, security_status):
    color_map = {
        'weak': Fore.YELLOW,
        'insecure': Fore.RED,
        'recommended': Fore.BLUE,
        'secure': Fore.GREEN
    }
    
    color = color_map.get(security_status.lower(), Fore.WHITE)
    print(f"{cipher_name} --> {color}{security_status.capitalize()}{Style.RESET_ALL}")

def run_nmap_ssl_enum(ip_port, output_file):
    port, ip = ip_port.strip().split()
    result = ""
    
    try:
        # Running the nmap command
        result = subprocess.run(
            ["nmap", "--script", "ssl-enum-ciphers", "-p", port, ip],
            capture_output=True,
            text=True
        ).stdout

    except Exception as e:
        print(f"An error occurred while running nmap: {e}")
    
    # Process and format the output
    formatted_output = parse_nmap_output(ip, port, result)
    
    # Write formatted output to file
    if output_file:
        with open(output_file, "a") as f:
            f.write(formatted_output + "\n")
    else:
        print(formatted_output)

def parse_nmap_output(ip, port, output):
    # Output formatting
    formatted_output = (
        f"IP/URL: \033[34m{ip}\033[0m\n"
        f"Port: \033[34m{port}\033[0m\n\n"
        "Ciphers:\n"
    )

    # Regular expressions to capture TLS versions and ciphers
    tls_version_re = re.compile(r"\|\s+(TLSv[0-9]\.[0-9]):")
    cipher_re = re.compile(r"\|\s+([A-Z0-9_]+(?:_[A-Z0-9]+)*)")

    tls_versions = tls_version_re.findall(output)
    ciphers_by_tls = {}

    for tls_version in tls_versions:
        ciphers_by_tls[tls_version] = []

    current_tls = None
    for line in output.splitlines():
        tls_match = tls_version_re.match(line)
        if tls_match:
            current_tls = tls_match.group(1)
        elif current_tls:
            cipher_match = cipher_re.match(line)
            if cipher_match:
                cipher = cipher_match.group(1)
                # Exclude "NULL" and "64" from the results
                if "NULL" not in cipher and "64" not in cipher:
                    ciphers_by_tls[current_tls].append(cipher)

    # Build the formatted output
    for tls_version, ciphers in ciphers_by_tls.items():
        if ciphers:  # Only print if there are valid ciphers
            formatted_output += f"{tls_version}\n"
            for cipher in ciphers:
                security_status = get_cipher_security_status(cipher)
                display_security_status(cipher, security_status)
                formatted_output += f"{cipher}\n"
            formatted_output += "\n"  # New line after each TLS version block

    return formatted_output.strip()

def process_ip_port_file(filename, output_file):
    if not os.path.isfile(filename):
        print(f"File {filename} not found.")
        return

    try:
        with open(filename, "r") as file:
            for line in file:
                if line.strip():  # Avoid processing empty lines
                    run_nmap_ssl_enum(line, output_file)
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python nmap_ssl_enum_with_status.py <ip_port_list.txt> [output_file.txt]")
        sys.exit(1)
    
    # Get the filename from the command-line arguments
    input_filename = sys.argv[1]
    output_filename = sys.argv[2] if len(sys.argv) == 3 else None
    
    # Process the IP and port list from the file
    process_ip_port_file(input_filename, output_filename)
