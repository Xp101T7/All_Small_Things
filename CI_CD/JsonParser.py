import json
import re
import csv
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# File paths
json_file_path = 'dummy_data_simple.json'
csv_file_path = 'event_data_output.csv'

# Load the JSON data
try:
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    logging.info(f"Successfully loaded data from {json_file_path}")
    logging.debug(f"Type of loaded data: {type(data)}")
    logging.debug(f"First item of data: {data[0] if isinstance(data, list) else data}")
except Exception as e:
    logging.error(f"Error loading JSON file: {e}")
    raise

# Extract "Detection" values
detection_values = []
if isinstance(data, list):
    for item in data:
        if isinstance(item, dict):
            if "Detection" in item:
                detection_values.append(item["Detection"])
            else:
                logging.warning(f"'Detection' key not found in item: {item}")
        else:
            logging.warning(f"Unexpected item type: {type(item)}. Full item: {item}")
elif isinstance(data, dict) and "Detection" in data:
    detection_values.append(data["Detection"])
else:
    logging.error(f"Unexpected data type or structure: {type(data)}")

logging.info(f"Number of detection values found: {len(detection_values)}")

# Updated regex patterns for EventID
event_id_patterns = [
    re.compile(r'EventID\s*(?:=|==|:|\bin\b)\s*(?:\'|\")?\s*(\d{1,6})\s*(?:\'|\")?', re.IGNORECASE),
    re.compile(r'EventID\s+in\s*\((\'|\")?\s*(\d{1,6})(?:\s*,\s*(?:\'|\")?\d{1,6}(?:\'|\")?\s*)*\)', re.IGNORECASE),
    re.compile(r'EventID:?\s*\n\s*-\s*(\d{1,6})(?:\s*\n\s*-\s*\d{1,6})*', re.IGNORECASE),
    re.compile(r'EventID:?\s*(\d{1,6})', re.IGNORECASE),
    re.compile(r'\bevent_id\s*[=:]\s*(\d{1,6})', re.IGNORECASE)
]

# Regex patterns for EventCode
event_code_patterns = [
    re.compile(r'EventCode\s*(?:=|==|:|\bin\b)\s*(?:\'|\")?\s*(\d{1,6})\s*(?:\'|\")?', re.IGNORECASE),
    re.compile(r'EventCode\s+in\s*\((\'|\")?\s*(\d{1,6})(?:\s*,\s*(?:\'|\")?\d{1,6}(?:\'|\")?\s*)*\)', re.IGNORECASE),
    re.compile(r'EventCode:?\s*\n\s*-\s*(\d{1,6})(?:\s*\n\s*-\s*\d{1,6})*', re.IGNORECASE),
    re.compile(r'EventCode:?\s*(\d{1,6})', re.IGNORECASE),
    re.compile(r'\bevent_code\s*[=:]\s*(\d{1,6})', re.IGNORECASE)
]

def extract_values(detection, patterns):
    for pattern in patterns:
        matches = pattern.findall(detection)
        if matches:
            logging.debug(f"Matches found with pattern: {pattern.pattern}")
            logging.debug(f"Matches: {matches}")
            return [match[0] if isinstance(match, tuple) else match for match in matches]
    logging.debug(f"No match found for detection: {detection}")
    return []

all_matches = []

for i, detection in enumerate(detection_values):
    logging.debug(f"Processing detection {i+1}/{len(detection_values)}")
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
        else:
            logging.warning(f"No EventID or EventCode found in detection: {detection}")
        
        logging.debug(f"Detection string: {detection}")
        logging.debug(f"Extracted data: {event_data}")
    else:
        logging.warning(f"Unexpected detection type: {type(detection)}. Full detection: {detection}")

logging.info(f"Number of matches found: {len(all_matches)}")

# Determine fieldnames dynamically
fieldnames = sorted(set(key for match in all_matches for key in match.keys()))

# Write to CSV
try:
    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_matches)
    logging.info(f"Data has been written to {csv_file_path}")
except Exception as e:
    logging.error(f"Error writing to CSV file: {e}")
    raise

logging.info("Script execution completed")