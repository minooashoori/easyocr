import os
import shutil

# Paths
single_file_path = '/home/ubuntu/EasyOCR/results_converted.txt'
input_dir = '/home/ubuntu/dev/data/whole/labels/train'
output_dir = '/home/ubuntu/dev/data/whole/labels/updated_train'

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to parse single text file into a dictionary
def parse_single_file(single_file_path):
    bbox_dict = {}
    with open(single_file_path, 'r') as file:
        for line in file:
            if line.strip():  # Check if the line is not empty
                parts = line.split(",, ")  # Split by ",, " instead of ", "
                image_name = parts[0].split(": ")[1].strip()
                
                # Extract bounding box information
                bbox_info = parts[1].split(": ")[1].strip().strip('()')
                x_center = None
                y_center = None
                width = None
                height = None
                for item in bbox_info.split(', '):
                    if item.startswith('x_center='):
                        x_center = float(item.split('=')[1])
                    elif item.startswith('y_center='):
                        y_center = float(item.split('=')[1])
                    elif item.startswith('width='):
                        width = float(item.split('=')[1])
                    elif item.startswith('height='):
                        height = float(item.split('=')[1].strip(')'))  # Strip closing parenthesis

                try:
                    confidence = float(parts[2].split(": ")[1].strip().strip(','))  # Remove trailing comma and strip whitespace
                except ValueError:
                    confidence = None  # Handle case where confidence cannot be converted to float

                # Change image_name extension from .jpg to .txt
                image_name = image_name.replace('.jpg', '.txt')
                bbox_dict.setdefault(image_name, []).append(([x_center, y_center, width, height], confidence))
    return bbox_dict

# Parse the single text file
bbox_dict = parse_single_file(single_file_path)

# Function to process individual text files
def process_files(input_dir, output_dir, bbox_dict):
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_file_path = os.path.join(input_dir, filename)
            output_file_path = os.path.join(output_dir, filename)
            
            with open(input_file_path, 'r') as file:
                lines = file.readlines()

            # Remove lines starting with '2'
            lines = [line for line in lines if not line.startswith('2')]

            # Prepare new lines to add at the beginning
            new_lines = []
            if filename in bbox_dict:
                for bbox, confidence in bbox_dict[filename]:
                    if None not in bbox:  # Ensure all bbox values are not None
                        x_center, y_center, width, height = bbox
                        new_line = f'2 {x_center:.4f} {y_center:.4f} {width:.4f} {height:.4f}\n'
                        new_lines.append(new_line)

            # Insert new lines at the beginning of the file
            lines = new_lines + lines

            # Write the modified content to the output file
            with open(output_file_path, 'w') as file:
                file.writelines(lines)

# Process the individual text files
process_files(input_dir, output_dir, bbox_dict)