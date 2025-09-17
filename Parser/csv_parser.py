import csv
import re

with open("./Parser/ugly_logs.txt", "r") as infile, open("./Parser/outfile.csv", "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["timestamp", "level", "ip", "message"])

    for line in infile:
        line = line.strip()
        if not line:
            continue

        # --- Case: [timestamp],message ---
        if line.startswith("[") and "]," in line:
            ts = line.split("],", 1)[0].strip("[]")            # remove [ ]
            msg = line.split("],", 1)[1].strip()               # rest of message
            ip_match = re.search(r"\d+\.\d+\.\d+\.\d+", msg)   # find IPv4
            ip = ip_match.group(0) if ip_match else ""
            writer.writerow([ts, "", ip, msg])

        # --- Default case: space-split style ---
        else:
            parts = line.split()
            if len(parts) >= 2:
                timestamp = parts[0]
                level     = parts[1]
                message   = " ".join(parts[2:])
                writer.writerow([timestamp, level, "", message])
