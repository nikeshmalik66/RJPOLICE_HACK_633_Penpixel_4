import fitz  # PyMuPDF
import re

def extract_fields(text):
    """
    Extracts key fields and their values from the given text.
    The regular expressions in the 'patterns' dictionary may need to be adjusted
    based on the specific format of the FIR PDFs.
    """
    extracted_fields = {}

    # Regular expressions for the fields
    patterns = {
        'District': r'1\. District\s*\n\(िजला\):\s*([^\n]*)',
        'PS': r'P\.S\.\s*\n\(थाना\):\s*([^\n]*)',
        'FIR No.': r'FIR No\.\s*\n\(.*?\):\s*([^\n]*)',
        'Year': r'Year\n\(वष�\):\s*([^\n]*)',
        'Acts': r'Acts\s*\n\s*\(अिधिनयम\)\s*([^\n]*)(?=\n\D)',
        'Sections': r'Sections\s*\n\s*\(धाराएँ\)\s*([^\n]*)(?=\n\D)',
        'Time From': r'Time From\s*\n\(समय से\):\s*([^\n]*)',
        'Date From': r'Date From\s*\n\(�दनांक से\):\s*([^\n]*)',
        'Occurrence of Offence': r'Occurrence of offence\s*\(अपराध क� घटना\):\s*([^\n]*)',
        'Information received at P.S.': r'Information received at P.S\.\s*\(थाना जहाँ सूचना �ा� �ई\):\s*([^\n]*)',
        'General Diary Reference': r'General Diary Reference\s*\(रोजनामचा संदभ�\)\s*:\s*([^\n]*)',
        'Beat No.': r'Beat No\.\s*\(बीट सं\.\)\s*:\s*([^\n]*)',
        'Address': r'Address\(पता\):\s*([^\n]*)(?=\n\D)',
    }

    # Extracting fields using regex patterns
    for field, pattern in patterns.items():
        match = re.search(pattern, text, re.MULTILINE)
        if match:
            extracted_fields[field] = match.group(1).strip()

    return extracted_fields

def main(file_path, output_file_path):
    """
    Main function to open a PDF file, extract text from the first page,
    and save the extracted fields and their values to a text file.
    """
    # Open the PDF file
    doc = fitz.open(file_path)

    # Extract text from the first page
    page = doc[0]
    text = page.get_text()

    # Extract fields from the text
    extracted_data = extract_fields(text)

    # Save the extracted data to a text file
    with open(output_file_path, 'w') as output_file:
        for field, value in extracted_data.items():
            output_file.write(f"{field}: {value}\n")

# Example usage
file_path = 'uploads\fir-2.pdf'  # Replace with your FIR PDF file path
output_file_path = 'output.txt'  # Replace with the desired output file path
main(file_path, output_file_path)
