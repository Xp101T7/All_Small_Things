
# The Code


This code will search the SigmaHQ repo using the command line search terms and gets a list of all files. Future use is getting these files yml contents packed into a file to run by sigma_cli


```json
import os
import yaml
import argparse
from typing import Dict, List, Any
from pathlib import Path

def parse_arguments():
    """Parses command-line arguments for search criteria."""
    parser = argparse.ArgumentParser(description="Search for SIGMA YAML files based on criteria.")
    parser.add_argument("--path", required=True, help="Path to the SIGMA repository.")
    parser.add_argument("--title", help="Partial match for the title.")
    parser.add_argument("--date", help="Partial match for the date.")
    parser.add_argument("--product", help="Partial match for the product.")
    parser.add_argument("--tags", nargs="+", help="Partial matches for tags (space-separated).")
    parser.add_argument("--description", help="Partial match for the description.")
    return parser.parse_args()

def safe_yaml_load_all(file_path: str) -> List[Dict[str, Any]]:
    """Safely load all YAML documents with error handling."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return list(yaml.safe_load_all(f))
    except yaml.YAMLError as e:
        print(f"YAML parsing error in {file_path}: {str(e)}")
        return []
    except Exception as e:
        print(f"Error reading file '{file_path}': {str(e)}")
        return []

def normalize_tag(tag: str) -> str:
    """Normalize tag format by removing 'attack.' prefix and converting to lowercase."""
    tag = tag.lower()
    if tag.startswith('attack.'):
        tag = tag[7:]
    return tag

def matches_criteria(content: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
    """Check if YAML content matches the given criteria."""
    if not content:
        return False

    # Check title
    if criteria.get("title"):
        if not content.get("title") or criteria["title"].lower() not in content["title"].lower():
            return False

    # Check date
    if criteria.get("date"):
        if not content.get("date") or criteria["date"] not in str(content["date"]):
            return False

    # Check product
    if criteria.get("product"):
        logsource = content.get("logsource", {})
        if not logsource.get("product") or criteria["product"].lower() not in logsource["product"].lower():
            return False

    # Check description
    if criteria.get("description"):
        if not content.get("description") or criteria["description"].lower() not in content["description"].lower():
            return False

    # Check tags
    if criteria.get("tags"):
        content_tags = content.get("tags", [])
        if not content_tags:
            return False
        
        # Normalize content tags
        content_tags = [normalize_tag(str(tag)) for tag in content_tags]
        
        # Check if any required tag matches (partial matching)
        for required_tag in criteria["tags"]:
            required_tag = normalize_tag(required_tag)
            tag_found = False
            for content_tag in content_tags:
                if required_tag in content_tag:
                    tag_found = True
                    break
            if not tag_found:
                return False

    return True

def search_sigma_detectors(path: str, criteria: Dict[str, Any]) -> List[str]:
    """Searches YAML files in the given directory recursively based on matching criteria."""
    matches = []
    path = Path(path)

    if not path.exists():
        print(f"Error: The path '{path}' does not exist.")
        return matches

    for yaml_file in path.rglob("*.yml"):
        try:
            documents = safe_yaml_load_all(str(yaml_file))
            
            for content in documents:
                if matches_criteria(content, criteria):
                    matches.append(str(yaml_file))
                    print(f"\nMatch found in: {yaml_file}")
                    print(f"Title: {content.get('title', 'N/A')}")
                    print(f"Tags: {content.get('tags', [])}")
                    break
                    
        except Exception as e:
            print(f"Error processing file '{yaml_file}': {e}")
            continue

    return matches

def main():
    args = parse_arguments()
    criteria = {
        "title": args.title,
        "date": args.date,
        "product": args.product,
        "tags": args.tags,
        "description": args.description
    }

    print("\nSearch Parameters:")
    for key, value in criteria.items():
        if value:
            print(f"{key}: {value}")

    print(f"\nSearching in directory: {args.path}")
    results = search_sigma_detectors(args.path, criteria)

    if not results:
        print("\nNo matching detectors found.")
    else:
        print(f"\nFound {len(results)} matching detector(s):")
        for result in results:
            print(result)

if __name__ == "__main__":
    main()
```

### Prime Example for SIGMAHQ:

To search for SIGMA YAML files with detailed arguments (e.g., tags related to MITRE ATT&CK execution), you can use:

```json 
python SigmaHQ_Searcher.py \   
--path "C:\Path\To\SigmaHQ" \   
--tags "attack.execution" "attack.t1059.001" "mitre.attack.execution" \   
--product "windows" \   
--description "execution of commands or scripts"
```

Oneliner 
```json
python SigmaHQ_Searcher.py --path "C:\Users\<user>\Desktop\Code\sigma\sigma" --title "PowerShell" --date "2024" --product "windows" --tags "T1059" --description "alternate PowerShell hosts"
```

