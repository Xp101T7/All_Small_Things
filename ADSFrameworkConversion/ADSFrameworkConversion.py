import re
import yaml

def extract_yara_metadata(yara_file_path):
    """
    Extracts metadata from a YARA rule file.
    """
    metadata = {}
    try:
        with open(yara_file_path, 'r') as file:
            in_metadata = False
            for line in file:
                if line.strip().startswith("meta:"):
                    in_metadata = True
                elif in_metadata and line.strip() == "}":
                    break
                elif in_metadata:
                    key_value_match = re.match(r'\s*(\w+)\s*=\s*"([^"]+)"', line.strip())
                    if key_value_match:
                        key, value = key_value_match.groups()
                        metadata[key] = value
    except Exception as e:
        print(f"Error reading YARA file: {e}")
    return metadata

def convert_to_ads_input(metadata):
    """
    Converts metadata to ADS input format.
    """
    ads_input = {
        "goal": metadata.get("goal"),
        "categorization": metadata.get("categorization"),
        "strategy": metadata.get("strategy"),
        "technical_context": metadata.get("technical_context"),
        "priority": metadata.get("priority")
    }
    return ads_input

def save_to_yaml(data, output_path):
    """
    Saves data to a YAML file.
    """
    try:
        with open(output_path, 'w') as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style=False)
    except Exception as e:
        print(f"Error writing to YAML file: {e}")

def main():
    yara_file_path = input("Enter the path to the YARA file: ")
    metadata = extract_yara_metadata(yara_file_path)
    ads_input = convert_to_ads_input(metadata)
    output_path = input("Enter the path to save the ADS input YAML file: ")
    save_to_yaml(ads_input, output_path)
    print("ADS input has been successfully saved.")

if __name__ == "__main__":
    main()