ugly_logs = """ 
   2025-09-09   INFO     User logged in  
2025-09-09   ERROR   Failed login attempt from  192.168.1.50   
2025-09-09 DEBUG   ip=10.0.0.25   user=carol    action=upload 
user=bob ip=172.16.0.5 action=download   timestamp=2025-09-09T15:30:00
[2025-09-09 15:31:22] connection from  8.8.8.8   dropped
garbage 2025-09-09 15:32:10 noise ip=192.168.100.100 action=scan detected
"""

with open("./ugly_logs.txt", "w") as f:
    f.write(ugly_logs)

"/mnt/data/ugly_logs.txt"