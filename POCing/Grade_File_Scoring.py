import os
import re

def extract_and_score_refined(base_path):
    score_mapping = {'Poor': 1, 'Good': 2, 'Excellent': 3}
    total_score = 0
    max_possible_score = 0
    ungraded_files = 0
    total_files = 0
    exclude_files = ['Vendor_Questionnaire_Summary.md', 'Grading_Layout_Report.md']

    # Walk through the directory structure
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".md") and file not in exclude_files:
                total_files += 1
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as md_file:
                    content = md_file.read()
                
                # Check for the ungraded pattern
                if re.search(r'\*\*Grade:\*\* \[Poor/Good/Excellent\]', content):
                    ungraded_files += 1
                else:
                    # Look for specific grades
                    grades = re.findall(r'\*\*Grade:\*\* \[(Poor|Good|Excellent)\]', content)
                    if grades:
                        scores = [score_mapping[grade] for grade in grades if grade in score_mapping]
                        total_score += sum(scores)
                        max_possible_score += 3

    # Prospective score if ungraded files were rated 'Excellent'
    prospective_max_score = total_files * 3
    current_score_rating = f"{total_score} out of {max_possible_score} possible points."

    return total_score, prospective_max_score, ungraded_files, current_score_rating

# Specify the path to the base directory
base_path = "SnapAttack_PoC_Evaluation"

# Calculate the revised scores
score, prospective_max_score, ungraded_count, current_score_rating = extract_and_score_refined(base_path)

# Generate the output content
output_content = f"# Grading Layout Report\n\n"
output_content += f"Total Score: {score} out of {prospective_max_score} possible points.\n"
output_content += f"Prospective Total Score (if ungraded files are rated 'Excellent'): {score} out of {prospective_max_score} possible points.\n"
output_content += f"Number of ungraded files total score: {ungraded_count}\n"
output_content += f"Current Score rating: {current_score_rating}\n"

# Write the output to the Grading_Layout_Report.md file in the SnapAttack_PoC_Evaluation folder
output_file = os.path.join(base_path, "Grading_Layout_Report.md")
with open(output_file, 'w') as file:
    file.write(output_content)

print(f"Results have been written to {output_file}.")