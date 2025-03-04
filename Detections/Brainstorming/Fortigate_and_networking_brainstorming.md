
Analyzing FortiGate logs within Splunk enables the detection of various network threats and anomalies. Below are 10 detection use cases, each accompanied by its general detection logic and the corresponding Splunk query.

1. **Detection of Port Scanning Activities**
    
    **Detection Logic:** Identify multiple connection attempts from a single source IP to multiple destination ports within a short time frame, which may indicate a port scan.
    

```JSON
    `sourcetype="fgt_traffic" action="deny" | bucket _time span=1m | stats dc(dst_port) AS unique_ports values(dst_port) AS ports BY src_ip, _time | where unique_ports > 20`
```


2. **Detection of Brute Force Login Attempts**
    
    **Detection Logic:** Identify multiple failed login attempts from a single source IP within a short period, indicating a possible brute force attack.

```JSON
    `sourcetype="fgt_event" subtype="vpn" user="*" status="fail" | bucket _time span=5m | stats count BY src_ip, user, _time | where count > 5`
```
 
3. **Detection of Malware Downloads**
    
    **Detection Logic:** Detect instances where the antivirus feature has identified and blocked malware during a file download.

```JSON
    `sourcetype="fgt_utm" subtype="virus" action="blocked" | stats count BY src_ip, dst_ip, url`
```

4. **Detection of Data Exfiltration via DNS**
    
    **Detection Logic:** Identify unusually large DNS query sizes or high frequencies of DNS queries, which may indicate data exfiltration attempts.

```JSON
    `sourcetype="fgt_traffic" app="DNS" | stats avg(bytes_sent) AS avg_bytes_sent BY src_ip | where avg_bytes_sent > 500`
```

5. **Detection of Unauthorized Administrative Access**
    
    **Detection Logic:** Monitor for administrative access attempts from unauthorized or unusual source IP addresses.

```JSON
    `sourcetype="fgt_event" subtype="admin" user="admin" action="login" status="success" | search NOT [| inputlookup authorized_admin_ips | fields src_ip]`
```
    
6. **Detection of Suspicious URL Access**
    
    **Detection Logic:** Identify access to URLs known for hosting malicious content or those that match patterns associated with phishing sites.

```JSON
    `sourcetype="fgt_utm" subtype="webfilter" action="blocked" | search category="Malicious Websites" | stats count BY src_ip, url`
```

7. **Detection of Anomalous Traffic Patterns**
    
    **Detection Logic:** Detect significant deviations from typical traffic patterns, such as unusual spikes in traffic volume from a particular IP.

```JSON
    `sourcetype="fgt_traffic" | timechart span=1h sum(bytes_sent) AS bytes_sent BY src_ip | eventstats avg(bytes_sent) AS avg_bytes_sent stdev(bytes_sent) AS stdev_bytes_sent BY src_ip | where bytes_sent > avg_bytes_sent + 3 * stdev_bytes_sent`
```

1. **Detection of VPN Anomalies**
    
    **Detection Logic:** Identify VPN logins from unusual locations or during atypical hours, which may indicate compromised credentials.

```JSON
    `sourcetype="fgt_event" subtype="vpn" action="login" status="success" | lookup user_location_lookup user OUTPUT location | search location!="expected_location"`
```

2. **Detection of Intrusion Prevention System (IPS) Alerts**
    
    **Detection Logic:** Monitor for triggered IPS signatures that indicate attempted exploits or reconnaissance activities.

```JSON
   `sourcetype="fgt_utm" subtype="ips" severity="high" | stats count BY src_ip, dst_ip, signature`
```
 

3. **Detection of Unusual Outbound Connections**
    
    **Detection Logic:** Identify outbound connections to IP addresses or countries that are not typical for the organization, which may indicate command and control communication.

```JSON
    `sourcetype="fgt_traffic" direction="outgoing" | lookup geoip_lookup dst_ip OUTPUT country | search country!="expected_country" | stats count BY src_ip, dst_ip, country`
```

