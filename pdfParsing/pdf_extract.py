import fitz  # PyMuPDF

# Load the 'fir-3.pdf' document
file_path = '/mnt/data/fir-3.pdf'
document = fitz.open(file_path)

# Extract text from each page
extracted_text = ""
for page in document:
    extracted_text += page.get_text()

document.close()
extracted_text

