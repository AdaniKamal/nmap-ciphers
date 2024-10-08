# nmap-ciphers
This tools will scan for ciphers and then will output the result together with the ciphers used & cipher status from ciphersuite info.

## Purposes
To do the validation for <br/>
<b>`Finding`</b> : `SSL Weak Cipher Suites Supported`

## Problem Statement
The current cipher checker scanner is effective for analyzing SSL/TLS cipher suites for individual IP addresses or a small number of IPs. <br/>
However, when faced with a larger set of IPs—such as 15 to 25 or more—the process becomes inefficient and time-consuming. <br/>
Manually running `nmap` scans for each IP address to collect cipher suites and then determining the security status of each cipher (whether they are strong or weak) requires significant effort and time. <br/>
This manual process poses challenges to respond quickly.

## How to use

```
Usage:
python nmap_ciphers.py iplist.txt
```

see example <b>iplist.txt</b>

## Version

|Current Version|Descriptions|
|---------------|------------|
|nmap17.py|Output combine all ciphers for port and hosts in one line (Eg: 80,443 site.com)|
|nmap18.py|Fix nmap17.py|

## Improvement

|No|Details|Status|
|--|-------|------|
|1|output the result for more port in different line. Eventhough stated in IP List in one line.|`Done`|
|2|If no result. then try ping and telnet.||
|3|Output the result as below<br/>For example: <br/>IP/URL: Insecure.Org <br/>Port: 80 <br/>Cipher status: No <br/>Ping: Host reachable / Host not reachable <br/>Telnet: Port closed / Port open <br/>||
|4|Remove "colorama", make color code static.|`Done`|
|5|Add "optionally" user can just add command "save.txt" to save all the output into txt||


