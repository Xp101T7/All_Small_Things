import re
from datetime import datetime

# File path
file_path = r"C:\Users\hecki\Downloads\windows-sysmon.txt"

# Read the log file
with open(file_path, 'r') as file:
    logs = file.readlines()

# Get today's date
today_str = datetime.today().strftime('%Y-%m-%d')

# Function to update the date in SystemTime and UtcTime
def update_date(log_line):
    # Update SystemTime
    systemtime_match = re.search(r"SystemTime='([0-9-T:.]+)Z'", log_line)
    if systemtime_match:
        original_time_str = systemtime_match.group(1)
        try:
            time_part = original_time_str.split('T')[1]
            updated_time_str = f"{today_str}T{time_part}"
            log_line = log_line.replace(original_time_str, updated_time_str)
        except ValueError as e:
            print(f"Error parsing SystemTime date: {e}")

    # Update UtcTime
    utctime_match = re.search(r"UtcTime'>([0-9-: .]+)</Data>", log_line)
    if utctime_match:
        original_time_str = utctime_match.group(1)
        try:
            date_part, time_part = original_time_str.split(' ')
            updated_time_str = f"{today_str} {time_part}"
            log_line = log_line.replace(original_time_str, updated_time_str)
        except ValueError as e:
            print(f"Error parsing UtcTime date: {e}")

    return log_line

# Update the logs
updated_logs = [update_date(log) for log in logs]

# Save the updated logs
output_file_path = r"C:\Users\hecki\Downloads\updated_windows-sysmon.txt"
with open(output_file_path, 'w') as file:
    file.writelines(updated_logs)

print(f"Logs have been updated and saved to '{output_file_path}'")
