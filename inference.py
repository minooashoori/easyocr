import os
import easyocr
import math
from PIL import Image

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

# Path to the directory containing images
image_dir = '/home/ubuntu/dev/data/whole/images/val'
batch_size = 256  # Define your batch size

# Function to process a batch of images
def process_batch(image_paths, output_file):
    with open(output_file, 'a') as f:
        for image_path in image_paths:
            try:
                # Read the text from the image
                results = reader.readtext(image_path)

                # Load the image using PIL
                image = Image.open(image_path)
                image_width, image_height = image.size

                # Process each detected text
                for (bbox, text, prob) in results:
                    print(f"Detected text: '{text}' with confidence {prob} at {bbox}")  # Debug print

                    # Calculate the relative coordinates
                    x_min = min(point[0] for point in bbox) / image_width
                    y_min = min(point[1] for point in bbox) / image_height
                    x_max = max(point[0] for point in bbox) / image_width
                    y_max = max(point[1] for point in bbox) / image_height
                    width = x_max - x_min
                    height = y_max - y_min

                    # Save the results to the file
                    f.write(f'Image: {os.path.basename(image_path)}, Bounding Box: (x={x_min:.4f}, y={y_min:.4f}, width={width:.4f}, height={height:.4f}), Confidence: {prob:.4f}, Text: "{text}"\n')

                print(f'Processed image: {image_path}')

            except Exception as e:
                print(f'Error processing image {image_path}: {e}')

# Get the list of image paths
image_paths = [os.path.join(image_dir, filename) for filename in os.listdir(image_dir) if filename.endswith(".jpg")]

# Output file to save the results
output_file = os.path.join('/home/ubuntu/EasyOCR', 'results_val.txt')

# Process images in batches
num_batches = math.ceil(len(image_paths) / batch_size)
for i in range(num_batches):
    batch_start = i * batch_size
    batch_end = batch_start + batch_size
    batch = image_paths[batch_start:batch_end]
    process_batch(batch, output_file)
