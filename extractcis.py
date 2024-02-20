import fitz  # PyMuPDF

def extract_remediations(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    remediations = []
    
    # Iterate through each page
    for page in doc:
        text = page.get_text("text")
        start_idx = 0
        
        # Search for the text "Remediation:" and extract until the next likely section start or end of content
        while True:
            start_idx = text.find("Remediation:", start_idx)
            if start_idx == -1:  # If "Remediation:" is not found
                break
            
            # Attempt to find the end of the section, which we'll assume for this example could be the start of another "Remediation:" section
            # or the end of the page. This is a simplified approach and might need adjustment for different document structures.
            end_idx = text.find("Remediation:", start_idx + 1)
            if end_idx == -1:  # If no further "Remediation:" is found, go till the end of the page text
                end_idx = len(text)
            
            # Extract the remediation text
            remediation_text = text[start_idx:end_idx].strip()
            remediations.append(remediation_text)
            
            # Update start_idx to search for the next occurrence
            start_idx = end_idx
    
    return remediations

# Path to the uploaded PDF file
pdf_path = 'C:\\Users\\Joel\\Desktop\\apktest\\latestapks\\CIS_Microsoft_Windows_10_Stand-alone_Benchmark_v2.0.0.pdf'

# Extract remediations
remediations = extract_remediations(pdf_path)

# Now, write the extracted remediations to a file, specifying UTF-8 encoding
output_file_path = 'C:\\Users\\Joel\\Desktop\\apktest\\latestapks\\results.txt'
with open(output_file_path, 'w', encoding='utf-8') as f:
    for remediation in remediations:
        f.write(remediation + "\n\n")

# Provide the path to the output file as confirmation
print(f"Remediations have been written to {output_file_path}")
