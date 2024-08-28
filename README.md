# nmap-ciphers
This tools will scan for ciphers and then will output the result together with the ciphers used &amp;cipher status from ciphersuite info.

## Problem Statement
The current cipher checker scanner is effective for analyzing SSL/TLS cipher suites for individual IP addresses or a small number of IPs. However, when faced with a larger set of IPs—such as 15 to 25 or more—the process becomes inefficient and time-consuming. Manually running `nmap` scans for each IP address to collect cipher suites and then determining the security status of each cipher (whether they are strong or weak) requires significant effort and can lead to delays. This manual process poses challenges in scalability, accuracy, and the ability to respond quickly to security assessments, necessitating a more automated and streamlined approach to handle multiple IP addresses efficiently.

## How to use

```
Usage:
python nmap_ciphers.py iplist.txt
```

see example <b>iplist.txt</b>

## RESULT
<img width="377" alt="Screenshot 2024-08-28 at 8 27 35 PM" src="https://github.com/user-attachments/assets/af45c866-0a1b-4a15-bb73-fa598c17e313">

<img width="427" alt="Screenshot 2024-08-28 at 8 27 48 PM" src="https://github.com/user-attachments/assets/b3163b80-9414-45f9-a6c9-16e492dd9dc0">

## Improvement

|No|Details|Status|
|--|-------|------|
|1|output the result for more port in different line. Eventhough stated in IP List in one line. <br/>For example: <br/>IP/URL: Insecure.Org<br/>Port: 80<br/><br/>IP/URL:Insecure.Org<br/>Port: 443||
|2|If no result. then try ping and telnet.||
|3|Output the result as below<br/>For example: <br/>IP/URL: Insecure.Org <br/>Port: 80 <br/>Cipher status: No <br/>Ping: Host reachable / Host not reachable <br/>Telnet: Port closed / Port open <br/>||
|4|Remove "colorama", make color code static.||


