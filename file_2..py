from PIL import Image
import numpy as np
import pandas as pd

# Open the image using Pillow
image_path = 'your_image.png'
img = Image.open(image_path)

# Convert the image to grayscale
gray_img = img.convert('L')

# Convert the Pillow image to a NumPy array
img_array = np.array(gray_img)

# Apply thresholding to the grayscale image
threshold = 200  # Adjust the threshold value as needed
binary_img = img_array > threshold
binary_img = binary_img.astype(np.uint8) * 255

# Find contours in the thresholded image
contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter out small contours (adjust the area threshold as needed)
min_contour_area = 500
table_contours = [contour for contour in contours if cv2.contourArea(contour) > min_contour_area]

# Sort contours by their Y-coordinate to arrange them in rows
table_contours.sort(key=lambda contour: cv2.boundingRect(contour)[1])

# Initialize a list to hold the table data
table_data = []

for contour in table_contours:
    x, y, w, h = cv2.boundingRect(contour)

    # Crop each cell from the original image using Pillow
    cell_image = img.crop((x, y, x + w, y + h))

    # Use OCR (Tesseract or another OCR library) to extract text from each cell
    cell_text = "Your_OCR_Function(cell_image)"  # Replace with your OCR function
    cell_text = cell_text.strip()

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
