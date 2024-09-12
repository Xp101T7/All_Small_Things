import json
import re
import csv

# File paths
json_file_path = 'dummy_data_simple.json'
csv_file_path = 'event_data_output.csv'

# Load the JSON data
with open(json_file_path, 'r') as file:
    data = json.load(file)

print(f"Type of loaded data: {type(data)}")
print(f"Structure of loaded data: {data[:2] if isinstance(data, list) else data}")

# Extract "Detection" values
detection_values = []
if isinstance(data, list):
    for item in data:
        if isinstance(item, dict) and "Detection" in item:
            detection_values.append(item["Detection"])
        else:
            print(f"Unexpected item structure: {item}")
elif isinstance(data, dict) and "Detection" in data:
    detection_values.append(data["Detection"])
else:
    print(f"Unexpected data type or structure: {type(data)}")

print(f"Number of detection values found: {len(detection_values)}")

# Updated regex patterns for EventID
event_id_patterns = [
    re.compile(r'EventID\s*(?:=|==|in)\s*(?:\'|\")?\s*(\d{1,6})\s*(?:\'|\")?'),
    re.compile(r'EventID\s+in\s*\((\'|\")?\s*(\d{1,6})(?:\s*,\s*(?:\'|\")?\d{1,6}(?:\'|\")?\s*)*\)'),
    re.compile(r'EventID:\s*\n\s*-\s*(\d{1,6})(?:\s*\n\s*-\s*\d{1,6})*'),
    re.compile(r'EventID:\s*(\d{1,6})')
]

# Regex patterns for EventCode
event_code_patterns = [
    re.compile(r'EventCode\s*(?:=|==|in)\s*(?:\'|\")?\s*(\d{1,6})\s*(?:\'|\")?'),
    re.compile(r'EventCode\s+in\s*\((\'|\")?\s*(\d{1,6})(?:\s*,\s*(?:\'|\")?\d{1,6}(?:\'|\")?\s*)*\)')
]

def extract_values(detection, patterns):
    for pattern in patterns:
        match = pattern.search(detection)
        if match:
            # If it's a list pattern, return all matched numbers
            if '-' in pattern.pattern:
                return [num.strip() for num in re.findall(r'-\s*(\d+)', detection)]
            return [match.group(1)]
    return []

all_matches = []

for detection in detection_values:
    if isinstance(detection, str):
        event_data = {}
        
        event_ids = extract_values(detection, event_id_patterns)
        event_codes = extract_values(detection, event_code_patterns)
        
        if event_ids:
            event_data['EventID'] = ', '.join(event_ids)
        if event_codes:
            event_data['EventCode'] = ', '.join(event_codes)
        
        if event_data:
            all_matches.append(event_data)
        
        print(f"\nDetection string: {detection}")
        print(f"Extracted data: {event_data}")

print(f"\nNumber of matches found: {len(all_matches)}")

# Determine fieldnames dynamically
fieldnames = sorted(set(key for match in all_matches for key in match.keys()))

# Write to CSV
with open(csv_file_path, mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_matches)

print(f"Data has been written to {csv_file_path}")