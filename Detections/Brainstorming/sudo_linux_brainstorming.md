# Linux Sudo Log Detection Rules (Splunk)

## 1. Monitoring All `sudo` Command Executions
```spl
| tstats count from datamodel=Endpoint.Processes where Processes.process_name="sudo" 
| table _time host user Processes.process_name Processes.process
```

---

## 2. Detecting Failed `sudo` Attempts
```spl
index=linux sourcetype=secure "sudo:" "authentication failure"
| table _time host user message
```

---

## 3. Identifying `sudo` Commands Executed Without a Password
```spl
index=linux sourcetype=secure "sudo:" "NOPASSWD"
| table _time host user message
```

---

## 4. Detecting Attempts to Edit the `sudoers` File
```spl
index=linux sourcetype=secure "sudo:" ("visudo" OR "/etc/sudoers")
| table _time host user message
```

---

## 5. Monitoring for the Baron Samedit Vulnerability (CVE-2021-3156)
```spl
index=linux sourcetype=secure "sudoedit -s \\""
| table _time host user process
```

---

## 6. Detecting Sudden Privilege Escalation
```spl
index=linux sourcetype=secure "sudo" "root"
| stats count by user host
| where count > 3
```

---

## 7. Monitoring Sudo Command Enumeration (`sudo -l`)
```spl
index=linux sourcetype=secure "sudo -l"
| table _time host user message
```

---

## 8. Detecting Unusual Sudo Usage by a Low-Privileged User
```spl
index=linux sourcetype=secure "sudo"
| stats count by user host
| eventstats avg(count) as avg_count stdev(count) as stdev_count by host
| where count > (avg_count + 2*stdev_count)
```

---

These **Splunk rules** will help **monitor, detect, and alert on suspicious sudo activities** in a Linux environment.

