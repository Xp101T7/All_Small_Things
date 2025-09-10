import csv

with open("./Parser/ugly_logs.txt", "r") as infile, open("outfile.csv", "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow({"timestamp", "level", "message"}) #headerw
    
    for line in infile:
        
        parts = line.strip().split()
        if len(parts) >= 1: 
            timestamp = parts[0]
            level     = parts[1]
            message = " ".join(parts[2:])
            writer.writerow([timestamp,level, message])
