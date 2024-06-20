import os

# Paths to the input and output files
input_file = '/home/ubuntu/EasyOCR/results_val.txt'
output_file = '/home/ubuntu/EasyOCR/results_val_converted.txt'

# Function to convert coordinates
def convert_coordinates(x_min, y_min, width, height):
    x_center = x_min + width / 2
    y_center = y_min + height / 2
    return x_center, y_center, width, height

# Function to process the file
def process_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            try:
                # Split the line based on the initial known parts
                parts = line.split('Bounding Box: ')
                image_part = parts[0].strip().replace('Image: ', '').strip()
                remaining = parts[1]

                parts = remaining.split('Confidence: ')
                bbox_part = parts[0].strip('(), ').strip()
                remaining = parts[1]

                parts = remaining.split('Text: ')
                confidence_part = parts[0].strip().strip()
                text_part = parts[1].strip().strip()

                # Parse the bounding box values
                bbox_parts = bbox_part.split(', ')
                x_min = float(bbox_parts[0].split('=')[1])
                y_min = float(bbox_parts[1].split('=')[1])
                width = float(bbox_parts[2].split('=')[1])
                height = float(bbox_parts[3].split('=')[1])

                # Convert coordinates
                x_center, y_center, width, height = convert_coordinates(x_min, y_min, width, height)

                # Write the converted coordinates to the new file
                outfile.write(f'Image: {image_part}, Bounding Box: (x_center={x_center:.4f}, y_center={y_center:.4f}, width={width:.4f}, height={height:.4f}), Confidence: {confidence_part}, Text: {text_part}\n')
            except IndexError as e:
                print(f"Error processing line: {line.strip()}")
                print(f"Error details: {e}")
            except ValueError as e:
                print(f"Value error: Line format is incorrect: {line.strip()}")
                print(f"Error details: {e}")
            except Exception as e:
                print(f"Unexpected error processing line: {line.strip()}")
                print(f"Error details: {e}")

# Process the file
process_file(input_file, output_file)