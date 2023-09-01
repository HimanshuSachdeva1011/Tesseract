from PIL import Image
import pandas as pd

# Path to your input image
image_path = 'your_image.png'

# Open the image using Pillow
img = Image.open(image_path)

# Convert the image to grayscale
gray_img = img.convert('L')

# Apply thresholding to create a binary image
threshold = 200  # Adjust the threshold value as needed
binary_img = gray_img.point(lambda p: p > threshold and 255)

# Perform connected component labeling to identify objects (potential table cells)
from scipy import ndimage
label_objects, num_labels = ndimage.label(binary_img)

# Find bounding boxes of labeled objects
objects_boxes = ndimage.find_objects(label_objects)

# Initialize a list to hold the table data
table_data = []

# Text extraction method (based on pixel intensity)
def extract_text_from_roi(roi):
    # Simple method: Count white pixels and assume them as text
    white_pixel_count = sum(1 for pixel in roi.getdata() if pixel == 255)
    if white_pixel_count > 0:
        return "Text Detected"
    else:
        return ""

# Iterate through detected objects (potential table cells)
for obj_box in objects_boxes:
    obj = binary_img[obj_box]

    # Extract the region of interest (ROI) for the potential table cell
    roi = gray_img.crop(obj_box)

    # Use the text extraction method for the ROI
    cell_text = extract_text_from_roi(roi).strip()

    # Split cell text by tab or comma to identify columns
    cell_data = [cell.strip() for cell in cell_text.split('\t')]  # Assuming tab as column separator

    if len(cell_data) > 1:
        table_data.append(cell_data)

# Convert the table data to a Pandas DataFrame
table_df = pd.DataFrame(table_data)

# Save the DataFrame as a CSV file
csv_file_path = 'table_data.csv'
table_df.to_csv(csv_file_path, index=False)

print(f"Table extracted and saved as {csv_file_path}")
