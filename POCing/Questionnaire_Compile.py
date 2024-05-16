import os
import re

def extract_vendor_questionnaire(base_path):
    # Define the path for the summary markdown file
    vendor_questionnaire_path = os.path.join(base_path, "Vendor_Questionnaire_Summary.md")
    content = ""

    # Traverse the directory structure
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".md"):
                # Construct the hierarchical path as markdown headings
                relative_path = os.path.relpath(root, base_path)
                path_parts = relative_path.split(os.sep)
                heading_structure = "\n".join([f"{'#' * (i+2)} {part}" for i, part in enumerate(path_parts)])

                file_path = os.path.join(root, file)
                with open(file_path, 'r') as md_file:
                    md_content = md_file.read()
                    # Extract the Vendor Questionnaire content using regular expression
                    vendor_info_match = re.search(r'\*\*Vendor Questionnaire:\*\*\n((?:\s+- .*\n)+)', md_content)
                    if vendor_info_match:
                        vendor_info = vendor_info_match.group(1)
                        # Debugging statement to check captured vendor info
                        print(f"Captured Vendor Questionnaire in {file}:\n{vendor_info}")
                        # Format and add the extracted content to the overall summary
                        content += f"{heading_structure}\n**Vendor Questionnaire:**\n{vendor_info.strip()}\n\n"

    # Write or overwrite the extracted content to the summary file
    with open(vendor_questionnaire_path, 'w') as outfile:
        outfile.write(content)

    return vendor_questionnaire_path

# Specify the path to the base directory where the markdown files are stored
base_path = "SnapAttack_PoC_Evaluation"

# Call the function and print the location of the created summary file
vendor_questionnaire_file = extract_vendor_questionnaire(base_path)
print(f"Vendor Questionnaire information written to '{vendor_questionnaire_file}'.")
