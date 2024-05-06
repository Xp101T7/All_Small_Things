# Further refined function to compute scores, considering prospective scores and current score rating for graded files
def extract_and_score_refined(base_path):
    score_mapping = {'Poor': 1, 'Good': 2, 'Excellent': 3}
    total_score = 0
    max_possible_score = 0
    ungraded_files = 0
    total_files = 0

    # Walk through the directory structure
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".md"):
                total_files += 1
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as md_file:
                    content = md_file.read()
                    grades = re.findall(r'\*\*Grade:\*\* \[(Poor|Good|Excellent)\]', content)
                    if grades:
                        # Calculate the score for files with grades
                        scores = [score_mapping[grade] for grade in grades if grade in score_mapping]
                        total_score += sum(scores)
                        max_possible_score += 3
                    else:
                        # Count ungraded files
                        ungraded_files += 1

    # Prospective score if ungraded files were rated 'Excellent'
    prospective_max_score = total_files * 3
    current_score_rating = f"{total_score} out of {max_possible_score} possible points."

    return total_score, prospective_max_score, ungraded_files, current_score_rating

# Calculate the revised scores
score, prospective_max_score, ungraded_count, current_score_rating = extract_and_score_refined(base_path)

# Output the refined results
print(f"Total Score: {score} out of {prospective_max_score} possible points.")
print(f"Prospective Total Score (if ungraded files are rated 'Excellent'): {score} out of {prospective_max_score} possible points.")
print(f"Number of ungraded files total score: {ungraded_count}")
print(f"Current Score rating: {current_score_rating}")

