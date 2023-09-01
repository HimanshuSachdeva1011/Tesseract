from PIL import Image
import pytesseract
import pandas as pd

# Path to your Tesseract executable (change this to your Tesseract installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Open the image using Pillow
image_path = 'your_image.png'
img = Image.open(image_path)

# Convert the image to grayscale for better OCR accuracy
gray_img = img.convert('L')

# Use Tesseract to perform OCR on the preprocessed image
table_text = pytesseract.image_to_string(gray_img)

# Split the OCR result into lines to identify rows
table_lines = table_text.split('\n')

# Create a list to hold the table data
table_data = []

# Iterate through the lines and split them by tab or comma to identify columns
for line in table_lines:
    row = [cell.strip() for cell in line.split('\t')]  # Assuming tab as column separator
    if len(row) > 1:
        table_data.append(row)

# Convert the table data to a Pandas DataFrame
table_df = pd.DataFrame(table_data)

# Save the DataFrame as a CSV file
csv_file_path = 'table_data.csv'
table_df.to_csv(csv_file_path, index=False)

print(f"Table extracted and saved as {csv_file_path}")
