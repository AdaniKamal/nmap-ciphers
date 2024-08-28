import subprocess
import sys
import re
import os
import requests

# ANSI color codes
ANSI_RESET = "\033[0m"
ANSI_YELLOW = "\033[33m"
ANSI_RED = "\033[31m"
ANSI_BLUE = "\033[34m"
ANSI_GREEN = "\033[32m"
ANSI_WHITE = "\033[37m"

# Function to check cipher security using the API
def check_cipher_security(cipher_name):
    url = f"https://ciphersuite.info/api/cs/{cipher_name}/"
    response = requests.get(url)
    
    if response.status_code == 200:
        cipher_data = response.json()
        if cipher_name in cipher_data:
            security_status = cipher_data[cipher_name].get('security', 'unknown')
            return security_status
        else:
            return "Cipher suite information not found"
    else:
        return "Error"

# Function to display the cipher security status
def display_security_status(cipher_name, security_status):
    color_map = {
        'weak': ANSI_YELLOW,
        'insecure': ANSI_RED,
        'recommended': ANSI_BLUE,
        'secure': ANSI_GREEN
    }
    
    color = color_map.get(security_status.lower(), ANSI_WHITE)
    return f"{cipher_name} --> {color}{security_status.capitalize()}{ANSI_RESET}"

# Function to run nmap and parse the output
def run_nmap_ssl_enum(ip, port):
    result = ""
    
    try:
        result = subprocess.run(
            ["nmap", "--script", "ssl-enum-ciphers", "-p", port, ip],
            capture_output=True,
            text=True
        ).stdout
    except Exception as e:
        print(f"An error occurred while running nmap: {e}")
    
    formatted_output = parse_nmap_output(ip, port, result)
    return formatted_output

# Function to parse nmap output and combine it with security checks
def parse_nmap_output(ip, port, output):
    formatted_output = (
        f"IP/URL: {ANSI_BLUE}{ip}{ANSI_RESET}\n"
        f"Port: {ANSI_BLUE}{port}{ANSI_RESET}\n\n"
        "Ciphers:\n"
    )

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
                if "NULL" not in cipher and "64" not in cipher:
                    ciphers_by_tls[current_tls].append(cipher)

    for tls_version, ciphers in ciphers_by_tls.items():
        if ciphers:
            formatted_output += f"{tls_version}\n"
            for cipher in ciphers:
                security_status = check_cipher_security(cipher)
                formatted_output += f"{display_security_status(cipher, security_status)}\n"
            formatted_output += "\n"

    return formatted_output.strip()

# Function to process the input file with IP and port list
def process_ip_port_file(filename):
    if not os.path.isfile(filename):
        print(f"File {filename} not found.")
        return

    try:
        with open(filename, "r") as file:
            for line in file:
                if line.strip():
                    ip_port_pair = line.strip().split()
                    ports = ip_port_pair[0].split(',')
                    ip = ip_port_pair[1]
                    for port in ports:
                        formatted_output = run_nmap_ssl_enum(ip, port)
                        print(formatted_output + "\n" + "-"*50 + "\n")
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python nmap_ciphers.py <ip_port_list.txt>")
        sys.exit(1)
    
    input_filename = sys.argv[1]
    
    process_ip_port_file(input_filename)

# By AdaniKamal
