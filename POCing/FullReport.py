import os
import re
import argparse

def extract_and_score_refined(base_path):
    """
    Extract and score markdown files based on grades within a given base path.
    
    Args:
        base_path (str): The base directory path to start the search.
    
    Returns:
        tuple: Contains total score, prospective max score, number of ungraded files, 
               total number of files, current score rating, and grades content.
    """
    score_mapping = {'Poor': 1, 'Good': 2, 'Excellent': 3}
    total_score = 0
    max_possible_score = 0
    ungraded_files = 0
    total_files = 0
    exclude_files = ['Vendor_Questionnaire_Summary.md', 'Grading_Layout_Report.md']
    grades_content = {}

    # Walk through the directory structure starting from the base path
    for root, dirs, files in os.walk(base_path):
        for file in files:
            # Process only markdown files excluding specified files
            if file.endswith(".md") and file not in exclude_files:
                total_files += 1
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as md_file:
                    content = md_file.read()
                
                # Look for specific grades within the markdown content
                grades = re.findall(r'\*\*Grade:\*\* \[(Poor|Good|Excellent)\]', content)
                if grades:
                    scores = [score_mapping[grade] for grade in grades if grade in score_mapping]
                    total_score += sum(scores)
                    max_possible_score += 3
                    grades_content[file_path] = f"- Grade: [{grades[0]}]"
                else:
                    ungraded_files += 1

    # Calculate the prospective maximum score assuming ungraded files are rated 'Excellent'
    prospective_max_score = total_files * 3
    current_score_rating = f"{total_score} out of {max_possible_score} possible points."

    return total_score, prospective_max_score, ungraded_files, total_files, current_score_rating, grades_content

def extract_sections_content(base_path, section_names, grades_content):
    """
    Extract specific sections from markdown files and organize the content by folder.
    
    Args:
        base_path (str): The base directory path to start the search.
        section_names (list): List of section names to extract.
        grades_content (dict): Dictionary containing grading information for each file.
    
    Returns:
        dict: Dictionary containing the organized content by folder paths.
    """
    content_dict = {}

    # Traverse the directory structure starting from the base path
    for root, dirs, files in os.walk(base_path):
        for file in files:
            # Process only markdown files
            if file.endswith(".md"):
                # Construct the hierarchical path as markdown headings
                relative_path = os.path.relpath(root, base_path)
                heading_structure = "## " + relative_path.replace(os.sep, '\\') + "\n"

                file_path = os.path.join(root, file)
                with open(file_path, 'r') as md_file:
                    md_content = md_file.read()

                    combined_content = ""
                    
                    # Include the grading information first if available
                    if file_path in grades_content:
                        combined_content += f"{grades_content[file_path]}\n\n"

                    # Extract specified sections from the markdown content
                    for section_name in section_names:
                        section_info_match = re.search(rf'\*\*{section_name}:\*\*\n((?:\s+- .*\n)+)', md_content)
                        if section_info_match:
                            section_info = section_info_match.group(1)
                            combined_content += f"**{section_name}:**\n{section_info.strip()}\n\n"

                    # Add the combined content to the dictionary, organized by folder paths
                    if combined_content:
                        if relative_path not in content_dict:
                            content_dict[relative_path] = heading_structure
                        content_dict[relative_path] += combined_content

    return content_dict

def generate_output_content(score, prospective_max_score, ungraded_count, total_files, current_score_rating, include_product_feedback, include_shortcomings, include_grade, include_vendor_questionnaire, base_path, group_by_folder, grades_content):
    """
    Generate the final output content for the grading layout report.
    
    Args:
        score (int): Total score.
        prospective_max_score (int): Prospective maximum score.
        ungraded_count (int): Number of ungraded files.
        total_files (int): Total number of files.
        current_score_rating (str): Current score rating.
        include_product_feedback (bool): Flag to include product feedback section.
        include_shortcomings (bool): Flag to include shortcomings section.
        include_grade (bool): Flag to include grade section.
        include_vendor_questionnaire (bool): Flag to include vendor questionnaire section.
        base_path (str): The base directory path.
        group_by_folder (bool): Flag to group content by sublevel folder.
        grades_content (dict): Dictionary containing grading information for each file.
    
    Returns:
        str: The final output content for the grading layout report.
    """
    output_content = f"# Grading Layout Report\n\n"
    if include_grade:
        score_percentage = (score / prospective_max_score) * 100 if prospective_max_score > 0 else 0
        output_content += f"Total Score: {score} out of {prospective_max_score} possible points ({score_percentage:.2f}%).\n\n"
        output_content += f"Prospective Total Score (if ungraded files are rated 'Excellent'): {score} out of {prospective_max_score} possible points.\n"
        output_content += f"Number of ungraded files: {ungraded_count} out of {total_files} total files.\n"
        output_content += f"Current Score rating: {current_score_rating}\n\n"
        output_content += f"# Evaluation Summary\n\n"

    section_names = []
    if include_product_feedback:
        section_names.append("Product Feedback")
    if include_shortcomings:
        section_names.append("Shortcomings")
    if include_vendor_questionnaire:
        section_names.append("Vendor Questionnaire")

    # Extract and organize the specified sections' content
    if section_names:
        sections_content_dict = extract_sections_content(base_path, section_names, grades_content)
        for key in sections_content_dict:
            output_content += sections_content_dict[key]

    return output_content

if __name__ == "__main__":
    # Set up argument parser for command-line arguments
    parser = argparse.ArgumentParser(description="Extract and score markdown files.")
    parser.add_argument("base_path", type=str, help="Path to the base directory")
    parser.add_argument("--product_feedback", action="store_true", help="Include Product Feedback section")
    parser.add_argument("--shortcomings", action="store_true", help="Include Shortcomings section")
    parser.add_argument("--grade", action="store_true", help="Include Grade section")
    parser.add_argument("--vendor_questionnaire", action="store_true", help="Include Vendor Questionnaire section")
    parser.add_argument("--group_by_folder", action="store_true", help="Group content by sublevel folder")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Extract and score the markdown files
    score, prospective_max_score, ungraded_count, total_files, current_score_rating, grades_content = extract_and_score_refined(args.base_path)

    # Generate the final output content
    output_content = generate_output_content(
        score,
        prospective_max_score,
        ungraded_count,
        total_files,
        current_score_rating,
        args.product_feedback,
        args.shortcomings,
        args.grade,
        args.vendor_questionnaire,
        args.base_path,
        args.group_by_folder,
        grades_content
    )

    # Write the output content to the Grading Layout Report markdown file
    output_file = os.path.join(args.base_path, "Grading_Layout_Report.md")
    with open(output_file, 'w') as file:
        file.write(output_content)

    print(f"Results have been written to {output_file}.")
