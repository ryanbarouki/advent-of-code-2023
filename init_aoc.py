import os

def create_aoc_folder(base_path):
    # Find the highest numbered existing day folder
    existing_days = [d for d in os.listdir(base_path) if d.startswith('day_') and os.path.isdir(os.path.join(base_path, d))]
    highest_day = max([int(day.split('_')[1]) for day in existing_days], default=0)

    # Determine the next day's folder name
    next_day = highest_day + 1
    next_day_folder = f"day_{next_day:02d}"
    next_day_path = os.path.join(base_path, next_day_folder)

    # Create the next day's folder
    os.makedirs(next_day_path, exist_ok=True)

    # Create the Python file with initial code
    python_file_path = os.path.join(next_day_path, f"day_{next_day:02d}.py")
    with open(python_file_path, 'w') as python_file:
        python_file.write("with open('input.txt') as f:\n    for line in f.readlines():\n        print(line)")

    # Create an empty input.txt file
    input_file_path = os.path.join(next_day_path, 'input.txt')
    open(input_file_path, 'w').close()

    return next_day_path

if __name__ == "__main__":
    create_aoc_folder(os.getcwd())

