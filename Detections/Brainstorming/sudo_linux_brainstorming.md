# Linux Sudo Log Detection Rules

## 1. Monitoring All `sudo` Command Executions

This detection captures all instances where a user executes a command with `sudo`.

### **Bash Command**

```bash
grep 'sudo:' /var/log/auth.log
```

### **Splunk Query**

```spl
sourcetype=linux_secure process=sudo COMMAND=*
| rex "COMMAND=(?<command>.*)"
| table _time host user command
```

---

## 2. Detecting Failed `sudo` Attempts

Failed `sudo` attempts indicate possible unauthorized privilege escalation attempts.

### **Bash Command**

```bash
grep 'sudo:' /var/log/auth.log | grep 'authentication failure'
```

### **Splunk Query**

```spl
sourcetype=linux_secure "sudo" "authentication failure"
| table _time host user message
```

---

## 3. Identifying `sudo` Commands Executed Without a Password

`NOPASSWD` directives in `sudo` commands could indicate a security risk.

### **Bash Command**

```bash
grep 'sudo:' /var/log/auth.log | grep 'NOPASSWD'
```

### **Splunk Query**

```spl
sourcetype=linux_secure "sudo" "NOPASSWD"
| table _time host user message
```

---

## 4. Detecting Attempts to Edit the `sudoers` File

Modifying the `/etc/sudoers` file could allow unauthorized privilege escalation.

### **Bash Command**

```bash
grep 'sudo:' /var/log/auth.log | grep -E 'visudo|/etc/sudoers'
```

### **Splunk Query**

```spl
sourcetype=linux_secure "sudo" ("visudo" OR "/etc/sudoers")
| table _time host user message
```

---

## 5. Monitoring for the Baron Samedit Vulnerability (CVE-2021-3156)

Detects potential exploitation attempts of the `sudoedit` vulnerability.

### **Bash Command**

```bash
grep 'sudoedit -s \\' /var/log/auth.log
```

### **Splunk Query**

```spl
sourcetype=linux_secure "sudoedit -s \\\"
| table _time host user process
```

---

## 6. Detecting Sudden Privilege Escalation

Identifies cases where a non-root user suddenly switches to root.

### **Splunk Query**

```spl
sourcetype=linux_secure "sudo" "root"
| stats count by user host
| where count > 3
```

---

## 7. Monitoring Sudo Command Enumeration (`sudo -l`)

Attackers may use `sudo -l` to check allowed commands.

### **Splunk Query**

```spl
sourcetype=linux_secure "sudo -l"
| table _time host user message
```

---

## 8. Detecting Unusual Sudo Usage by a Low-Privileged User

Flags users executing `sudo` for the first time or with unusual frequency.

### **Splunk Query**

```spl
sourcetype=linux_secure "sudo"
| stats count by user host
| eventstats avg(count) as avg_count stdev(count) as stdev_count by host
| where count > (avg_count + 2*stdev_count)
```

---

These **detection rules** will help **monitor, detect, and alert on suspicious sudo activities** in a Linux environment.

