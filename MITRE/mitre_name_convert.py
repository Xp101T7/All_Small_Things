import re

def convert_mitre_names(input_text):
    # Dictionary to map MITRE technique names to numbers
    mitre_mapping = {
        # Tactics (TA)
        "reconnaissance": "TA0043",
        "resource development": "TA0042",
        "initial access": "TA0001",
        "execution": "TA0002",
        "persistence": "TA0003",
        "privilege escalation": "TA0004",
        "defense evasion": "TA0005",
        "credential access": "TA0006",
        "discovery": "TA0007",
        "lateral movement": "TA0008",
        "collection": "TA0009",
        "command and control": "TA0011",
        "exfiltration": "TA0010",
        "impact": "TA0040",

        # Techniques (T)
        "active scanning": "T1595",
        "gather victim host information": "T1592",
        "gather victim identity information": "T1589",
        "gather victim network information": "T1590",
        "gather victim organization information": "T1591",
        "search open technical databases": "T1596",
        "search open websites or domains": "T1593",
        "search victim-owned websites": "T1594",
        "send spearphishing email": "T1566",
        "social engineering": "T1598",
        "compromise infrastructure": "T1584",
        "establish accounts": "T1585",
        "obtain capabilities": "T1587",
        "obtain victim information": "T1586",
        "develop capabilities": "T1588",
        "test capabilities": "T1589",
        "establish accounts": "T1585",
        "compromise accounts": "T1586",
        "social engineering": "T1598",
        "drive-by compromise": "T1189",
        "exploit public-facing application": "T1190",
        "hardware additions": "T1200",
        "phishing": "T1566",
        "supply chain compromise": "T1195",
        "valid accounts": "T1078",
        "command and scripting interpreter": "T1059",
        "deployment tools": "T1072",
        "exploitation for client execution": "T1203",
        "inter-process communication": "T1559",
        "native api": "T1106",
        "scheduled task/job": "T1053",
        "user execution": "T1204",
        "account manipulation": "T1098",
        "boot or logon initialization scripts": "T1037",
        "create account": "T1136",
        "create or modify system process": "T1543",
        "event triggered execution": "T1546",
        "implant internal image": "T1205",
        "modify authentication process": "T1556",
        "modify cloud compute infrastructure": "T1578",
        "modify registry": "T1112",
        "pre-OS boot": "T1542",
        "server software component": "T1505",
        "traffic signaling": "T1205",
        "validate capability": "T1580",
        "abuse elevation control mechanism": "T1548",
        "access token manipulation": "T1134",
        "boot or logon initialization scripts": "T1037",
        "create or modify system process": "T1543",
        "event triggered execution": "T1546",
        "exploitation for privilege escalation": "T1068",
        "process injection": "T1055",
        "access token manipulation": "T1134",
        "abuse elevation control mechanism": "T1548",
        "account manipulation": "T1098",
        "bypass user account control": "T1088",
        "cloud service dashboard": "T1538",
        "compromise accounts": "T1586",
        "disable or modify tools": "T1562",
        "exploitation for defense evasion": "T1211",
        "implant internal image": "T1205",
        "indicator blocking": "T1563",
        "indicator removal on host": "T1070",
        "masquerading": "T1036",
        "modify authentication process": "T1556",
        "modify cloud compute infrastructure": "T1578",
        "modify registry": "T1112",
        "network boundary bridging": "T1599",
        "obfuscated files or information": "T1027",
        "pre-OS boot": "T1542",
        "process injection": "T1055",
        "rootkit": "T1014",
        "subvert trust controls": "T1553",
        "system binary proxy execution": "T1218",
        "traffic signaling": "T1205",
        "valid accounts": "T1078",
        "brute force": "T1110",
        "credentials from password stores": "T1555",
        "exploitation for credential access": "T1212",
        "input capture": "T1056",
        "man-in-the-middle": "T1557",
        "network sniffing": "T1040",
        "steal application access token": "T1528",
        "steal or forge kerberos tickets": "T1558",
        "steal web session cookie": "T1539",
        "account discovery": "T1087",
        "application window discovery": "T1010",
        "browser information discovery": "T1217",
        "cloud infrastructure discovery": "T1580",
        "cloud service dashboard": "T1538",
        "cloud service discovery": "T1526",
        "cloud storage object discovery": "T1619",
        "container and resource discovery": "T1613",
        "device driver discovery": "T1652",
        "domain trust discovery": "T1482",
        "file and directory discovery": "T1083",
        "group policy discovery": "T1615",
        "log enumeration": "T1654",
        "network service discovery": "T1046",
        "network share discovery": "T1135",
        "password policy discovery": "T1201",
        "peripheral device discovery": "T1120",
        "permission groups discovery": "T1069",
        "process discovery": "T1057",
        "query registry": "T1012",
        "remote system discovery": "T1018",
        "software discovery": "T1518",
        "system information discovery": "T1082",
        "system location discovery": "T1614",
        "system network configuration discovery": "T1016",
        "system network connections discovery": "T1049",
        "system owner/user discovery": "T1033",
        "system service discovery": "T1007",
        "system time discovery": "T1124",
        "exploitation of remote services": "T1210",
        "internal spearphishing": "T1534",
        "lateral tool transfer": "T1570",
        "remote service session hijacking": "T1563",
        "remote services": "T1021",
        "taint shared content": "T1080",
        "archive collected data": "T1560",
        "audio capture": "T1123",
        "automated collection": "T1119",
        "browser session hijacking": "T1185",
        "clipboard data": "T1115",
        "data from cloud storage": "T1530",
        "data from configuration repository": "T1602",
        "data from information repositories": "T1213",
        "data from local system": "T1005",
        "data from network shared drive": "T1039",
        "data from removable media": "T1025",
        "data staged": "T1074",
        "email collection": "T1114",
        "screen capture": "T1113",
        "video capture": "T1125",
        "automated exfiltration": "T1020",
        "data transfer size limits": "T1030",
        "exfiltration over alternative protocol": "T1048",
        "traffic duplication": "T1020.001",
        "exfiltration over asymmetric encrypted non-c2 protocol": "T1048.002",
        "exfiltration over symmetric encrypted non-c2 protocol": "T1048.001",
        "exfiltration over unencrypted non-c2 protocol": "T1048.003",
        "exfiltration over bluetooth": "T1011.001",
        "exfiltration over usb": "T1052.001",
        "exfiltration over webhook": "T1567.004",
        "exfiltration to cloud storage": "T1567.002",
        "exfiltration to code repository": "T1567.001",
        "exfiltration to text storage sites": "T1567.003",
        "runtime data manipulation": "T1565.003",
        "stored data manipulation": "T1565.001",
        "transmitted data manipulation": "T1565.002",
        "external defacement": "T1491.002",
        "internal defacement": "T1491.001",
        "disk content wipe": "T1561.001",
        "disk structure wipe": "T1561.002",
        "application exhaustion flood": "T1499.003",
        "application or system exploitation": "T1499.004",
        "os exhaustion flood": "T1499.001",
        "service exhaustion flood": "T1499.002",
        "direct network flood": "T1498.001",
        "reflection amplification": "T1498.002",
        
        #SubTechniques
        "scanning ip blocks": "T1595.001",
        "vulnerability scanning": "T1595.002",
        "wordlist scanning": "T1595.003",
        "client configurations": "T1592.004",
        "firmware": "T1592.003",
        "botnet": "T1583.005",
        "dns server": "T1583.002",
        "domains": "T1583.001",
        "malvertising": "T1583.008",
        "apple script": "T1059.002",
        "autohotkey & autoit": "T1059.010",
        "cloud api": "T1059.009",
        "javascript": "T1059.007",
        "additional cloud credentials": "T1098.001",
        "dns": "T1071.004",
        "file transfer protocols": "T1071.002",
        "mail protocols": "T1071.003",
        "web protocols": "T1071.001",
        "non-standard encoding": "T1132.002",
        "standard encoding": "T1132.001",
        "junk data": "T1001.001",
        "protocol impersonation": "T1001.003",
        "steganography": "T1001.002",
        "dns calculation": "T1568.003",
        "domain generation algorithms": "T1568.002",
        "fast flux dns": "T1568.001",
        "asymmetric cryptography": "T1573.002",
        "symmetric cryptography": "T1573.001",
        "domain fronting": "T1090.004",
        "external proxy": "T1090.002",
        "internal proxy": "T1090.001",
        "multi-hop proxy": "T1090.003",
        "bidirectional communication": "T1102.002",
        "dead drop resolver": "T1102.001",
        "one-way communication": "T1102.003",
        "traffic duplication": "T1020.001",
        "exfiltration over asymmetric encrypted non-c2 protocol": "T1048.002",
        "exfiltration over symmetric encrypted non-c2 protocol": "T1048.001",
        "exfiltration over unencrypted non-c2 protocol": "T1048.003",
        "exfiltration over bluetooth": "T1011.001",
        "exfiltration over usb": "T1052.001",
        "exfiltration over webhook": "T1567.004",
        "exfiltration to cloud storage": "T1567.002",
        "exfiltration to code repository": "T1567.001",
        "exfiltration to text storage sites": "T1567.003",
        "runtime data manipulation": "T1565.003",
        "stored data manipulation": "T1565.001",
        "transmitted data manipulation": "T1565.002",
        "external defacement": "T1491.002",
        "internal defacement": "T1491.001",
        "disk content wipe": "T1561.001",
        "disk structure wipe": "T1561.002",
        "application exhaustion flood": "T1499.003",
        "application or system exploitation": "T1499.004",
        "os exhaustion flood": "T1499.001"
        }


    def replace_mitre(item):
        item = item.strip().lower()
        if item.startswith('t') or item.startswith('ta'):
            return item.upper()
        return mitre_mapping.get(item, item)
    
    items = [item.strip() for item in input_text.split(',')]
    converted_items = [replace_mitre(item) for item in items]
    converted_text = ', '.join(converted_items)
    
    return converted_text

def split_techniques(text):
    items = [item.strip().upper() for item in text.split(',')]
    ta_items = [item for item in items if item.startswith('TA')]
    t1_items = [item for item in items if item.startswith('T') and not item.startswith('TA')]
    return ta_items, t1_items

def generate_mitre_metadata(input_text):
    # Remove 'mitre = ' prefix if present
    input_text = re.sub(r'^mitre\s*=\s*', '', input_text.strip())
    # Remove surrounding quotes if present
    input_text = input_text.strip('"')
    
    converted_text = convert_mitre_names(input_text)
    ta_items, t1_items = split_techniques(converted_text)
    
    mitre_TA = f'"{", ".join(ta_items)}"' if ta_items else '"No TA values found"'
    mitre_T1 = f'"{", ".join(t1_items)}"' if t1_items else '"No T1 values found"'
    
    first_t1 = t1_items[0] if t1_items else "No T1 value found"
    mitre_url = f'"https://attack.mitre.org/techniques/{first_t1}/"' if first_t1 != "No T1 value found" else '"No T1 value found"'
    
    return f"""
Converted text: {converted_text}

mitre_TA = {mitre_TA}
mitre_T1 = {mitre_T1}
mitre_url = {mitre_url}
"""

# Example usage
input_text = 'mitre = "discovery, t1217, initial access, ta0002, Command and Scripting Interpreter, path interception by path environment variable"'

result = generate_mitre_metadata(input_text)
print(result)