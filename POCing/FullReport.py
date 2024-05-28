import os
import re
import argparse

class FileProcessor:
    def __init__(self, base_path):
        self.base_path = base_path

    def extract_sections(self, section_names, grades_content):
        content_dict = {}
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                if file.endswith(".md"):
                    relative_path = os.path.relpath(root, self.base_path)
                    heading_structure = "## " + relative_path.replace(os.sep, '\\') + "\n"
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as md_file:
                        md_content = md_file.read()
                        combined_content = ""
                        if file_path in grades_content:
                            combined_content += f"{grades_content[file_path]}\n\n"
                        for section_name in section_names:
                            section_info_match = re.search(rf'\*\*{section_name}:\*\*\n((?:\s+- .*\n)+)', md_content)
                            if section_info_match:
                                section_info = section_info_match.group(1)
                                combined_content += f"**{section_name}:**\n{section_info.strip()}\n\n"
                        if combined_content:
                            if relative_path not in content_dict:
                                content_dict[relative_path] = heading_structure
                            content_dict[relative_path] += combined_content
        return content_dict

class Grader:
    def __init__(self, base_path):
        self.base_path = base_path
        self.score_mapping = {'Poor': 1, 'Good': 2, 'Excellent': 3}
        self.total_score = 0
        self.max_possible_score = 0
        self.ungraded_files = 0
        self.total_files = 0
        self.grades_content = {}

    def extract_and_score(self):
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                if file.endswith(".md") and file not in ['Vendor_Questionnaire_Summary.md', 'Grading_Layout_Report.md']:
                    self.total_files += 1
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as md_file:
                        content = md_file.read()
                    grades = re.findall(r'\*\*Grade:\*\* \[(Poor|Good|Excellent)\]', content)
                    if grades:
                        scores = [self.score_mapping[grade] for grade in grades if grade in self.score_mapping]
                        self.total_score += sum(scores)
                        self.max_possible_score += 3
                        self.grades_content[file_path] = f"- **Grade:** [{grades[0]}]"
                    else:
                        self.ungraded_files += 1
        prospective_max_score = self.total_files * 3
        current_score_rating = f"{self.total_score} out of {self.max_possible_score} possible points."
        return self.total_score, prospective_max_score, self.ungraded_files, self.total_files, current_score_rating, self.grades_content

class ReportGenerator:
    def __init__(self, score, prospective_max_score, ungraded_count, total_files, current_score_rating, grades_content, base_path):
        self.score = score
        self.prospective_max_score = prospective_max_score
        self.ungraded_count = ungraded_count
        self.total_files = total_files
        self.current_score_rating = current_score_rating
        self.grades_content = grades_content
        self.base_path = base_path

    def generate(self, include_product_feedback, include_shortcomings, include_grade, include_vendor_questionnaire, group_by_folder):
        output_content = f"# Grading Layout Report\n\n"
        if include_grade:
            score_percentage = (self.score / self.prospective_max_score) * 100 if self.prospective_max_score > 0 else 0
            output_content += f"Total Score: {self.score} out of {self.prospective_max_score} possible points ({score_percentage:.2f}%).\n\n"
            output_content += f"Prospective Total Score (if ungraded files are rated 'Excellent'): {self.score} out of {self.prospective_max_score} possible points.\n"
            output_content += f"Number of ungraded files: {self.ungraded_count} out of {self.total_files} total files.\n"
            output_content += f"Current Score rating: {self.current_score_rating}\n\n"
            output_content += f"# Evaluation Summary\n\n"

        section_names = []
        if include_product_feedback:
            section_names.append("Product Feedback")
        if include_shortcomings:
            section_names.append("Shortcomings")
        if include_vendor_questionnaire:
            section_names.append("Vendor Questionnaire")

        if section_names:
            processor = FileProcessor(self.base_path)
            sections_content_dict = processor.extract_sections(section_names, self.grades_content)
            for key in sections_content_dict:
                output_content += sections_content_dict[key]

        return output_content

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract and score markdown files.")
    parser.add_argument("base_path", type=str, help="Path to the base directory")
    parser.add_argument("--product_feedback", action="store_true", help="Include Product Feedback section")
    parser.add_argument("--shortcomings", action="store_true", help="Include Shortcomings section")
    parser.add_argument("--grade", action="store_true", help="Include Grade section")
    parser.add_argument("--vendor_questionnaire", action="store_true", help="Include Vendor Questionnaire section")
    parser.add_argument("--group_by_folder", action="store_true", help="Group content by sublevel folder")
    args = parser.parse_args()

    grader = Grader(args.base_path)
    score, prospective_max_score, ungraded_count, total_files, current_score_rating, grades_content = grader.extract_and_score()

    report_generator = ReportGenerator(
        score,
        prospective_max_score,
        ungraded_count,
        total_files,
        current_score_rating,
        grades_content,
        args.base_path
    )
    output_content = report_generator.generate(
        args.product_feedback,
        args.shortcomings,
        args.grade,
        args.vendor_questionnaire,
        args.group_by_folder
    )

    output_file = os.path.join(args.base_path, "Grading_Layout_Report.md")
    with open(output_file, 'w') as file:
        file.write(output_content)

    print(f"Results have been written to {output_file}.")
