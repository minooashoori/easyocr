import os
import subprocess
import pyarrow.parquet as pq
import easyocr

# Initialize EasyOCR reader
reader = easyocr.Reader(['en', 'ch_sim'])

# Function to process a single image
def process_image(uri, asset_id, output_file):
    try:
        # Construct S3 URI
        s3_uri = f's3://{uri}'

        # Download object from S3 using aws s3 command
        image_filename = f'/tmp/{asset_id}.jpg'  # Temporary file path
        subprocess.run(['aws', '--profile', 'saml', 's3', 'cp', s3_uri, image_filename], check=True)

        # Read the image using EasyOCR directly from file path
        results = reader.readtext(image_filename)

        # Prepare data to write to file
        lines_to_write = []
        lines_to_write.append(f'Image: {asset_id}\n')
        for bbox, text, prob in results:
            lines_to_write.append(f"Bounding Box: {bbox}, Text: '{text}' with confidence {prob}\n")
        lines_to_write.append('\n')

        # Write to output file
        with open(output_file, 'a') as f:
            f.writelines(lines_to_write)

        print(f'Processed image: {s3_uri}')

        # Delete the downloaded image after processing
        os.remove(image_filename)
        print(f'Deleted image: {image_filename}')

    except Exception as e:
        print(f'Error processing image {asset_id} from {s3_uri}: {e}')

# Read the Parquet file and extract URIs
parquet_file = '/home/ubuntu/EasyOCR/logo05/logo_05_idx_00000.parquet'
parquet_table = pq.read_table(parquet_file)
uri_column = parquet_table['uri']
uris = uri_column.to_pylist()
asset_ids = parquet_table['asset_id'].to_pylist()

# Output file for saving results
output_file = '/home/ubuntu/EasyOCR/logo05/results.txt'

# Process images referenced by URIs one by one
for uri, asset_id in zip(uris, asset_ids):
    process_image(uri, asset_id, output_file)
