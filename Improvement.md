# Improvement

1. output the result for more port in different line. Eventhough stated in IP List in one line.
   
  For example: <br/>
  IP/URL: Insecure.Org <br/>
  Port: 80

  IP/URL: Insecure.Org <br/>
  Port: 443

2. If no result. then try ping and telnet.
3. Output the result as below
   
  For example: <br/>
  -------Output---------------
  IP/URL: Insecure.Org <br/>
  Port: 80 <br/>
  Cipher status: No <br/>
  Ping: Host reachable / Host not reachable <br/>
  Telnet: Port closed / Port open <br/>

4. Remove "colorama", make color code static.
