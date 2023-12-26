import os
from PIL import Image
import pytesseract

# Set the path for tesseract executable if it's not in the system PATH
# For example, on Windows you might need to uncomment the following line:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ['TESSDATA_PREFIX'] = r"C:\Program Files\Tesseract-OCR\tessdata"
# Define the path to the image file

image_path = 'uploads/firss.png'


image = Image.open(image_path)
text = pytesseract.image_to_string(image, lang='hin+eng')

output_file_path = 'output.txt'

# Save the extracted text into a text file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write(text)

# Print a message indicating the file has been saved
print(f"Extracted text saved to {output_file_path}")