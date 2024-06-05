import sys
import re
from collections import defaultdict

# Define the score mapping
score_mapping = {
    'Easy': 1,
    'Hard': 2,
    'Extreme': 4,
    'Hardcore': 8
}

# Function to calculate the total score for a week
def calculate_week_score(week_items):
    total_score = 0
    for item in week_items:
        match = re.search(r'\[(Easy|Hard|Extreme|Hardcore)\]', item)
        if match:
            total_score += score_mapping[match.group(1)]
    return total_score

# Function to filter items to meet the 24 point limit
def filter_week_items(week_items, max_points):
    filtered_items = []
    total_score = 0
    overflow_items = []

    for item in week_items:
        match = re.search(r'\[(Easy|Hard|Extreme|Hardcore)\]', item)
        if match:
            item_score = score_mapping[match.group(1)]
            if total_score + item_score <= max_points:
                filtered_items.append(item)
                total_score += item_score
            else:
                overflow_items.append(item)
        else:
            filtered_items.append(item)
    
    return filtered_items, overflow_items, total_score

def main(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    weeks = defaultdict(list)
    current_week = None

    # Organize lines into weeks
    for line in lines:
        week_match = re.match(r'### (Week \d+)', line)
        if week_match:
            current_week = week_match.group(1)
        if current_week:
            weeks[current_week].append(line)

    max_points_per_week = 18
    week_numbers = sorted(weeks.keys(), key=lambda x: int(x.split()[1]))
    all_items = []
    overflow_items = []

    for week in week_numbers:
        week_items = weeks[week]
        tasks = [item for item in week_items if re.search(r'- \[ \]', item)]
        non_tasks = [item for item in week_items if not re.search(r'- \[ \]', item)]

        filtered_items, overflow, week_score = filter_week_items(tasks, max_points_per_week)
        all_items.append(non_tasks + filtered_items)
        overflow_items.extend(overflow)
        
        # Append current week's score to the week heading
        for i in range(len(all_items[-1])):
            if re.match(r'### Week \d+', all_items[-1][i]):
                all_items[-1][i] = f"{all_items[-1][i].strip()} (Current score: {week_score})\n"

    # Stack all overflow items into week 10
    if overflow_items:
        if '### Week 10' in weeks:
            week_10_items = weeks['### Week 10']
            week_10_non_tasks = [item for item in week_10_items if not re.search(r'- \[ \]', item)]
            week_10_tasks = [item for item in week_10_items if re.search(r'- \[ \]', item)]
            all_items[-1] = week_10_non_tasks + week_10_tasks + overflow_items
        else:
            all_items.append([f'### Week 10 (Current score: {calculate_week_score(overflow_items)})\n'] + overflow_items)

    # Write the new organized weeks to the output file
    with open(output_file, 'w') as f:
        for week, items in zip(week_numbers + (['### Week 10'] if overflow_items else []), all_items):
            f.write(f"{week}\n")
            f.writelines(items)
            f.write('\n')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script.py input_file.md output_file.md")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)
