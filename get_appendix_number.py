from PyPDF2 import PdfReader
import os
import glob

def generate_appendix_toc(input_folder: str, output_folder: str, main_document_name: str = "00_template.pdf"):
    # Ensure output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Define paths for the main document and output TOC file
    main_document = os.path.join(input_folder, main_document_name)
    toc_txt_path = os.path.join(output_folder, "table_of_contents.txt")

    # Step 1: Count pages in the main document
    main_reader = PdfReader(main_document)
    main_page_count = len(main_reader.pages)

    # Step 2: Get all appendix PDFs (excluding the main document) and prepare TOC entries
    appendix_paths = sorted(glob.glob(os.path.join(input_folder, "*.pdf")))
    appendix_paths = [path for path in appendix_paths if os.path.basename(path) != main_document_name]
    toc_entries = []

    # Start TOC page numbering for appendices after the last page of the main document
    current_page = main_page_count + 1

    # Calculate starting pages and titles based on appendix file names
    for appendix_path in appendix_paths:
        appendix_reader = PdfReader(appendix_path)
        appendix_page_count = len(appendix_reader.pages)
        
        # Create title from filename (e.g., "01_caprani2017.pdf" -> "Appendix A")
        appendix_title = f"Appendix {chr(65 + len(toc_entries))}"  # Convert to letters A, B, C, etc.
        toc_entries.append(f"{appendix_title} ............................ Page {current_page}")
        
        current_page += appendix_page_count  # Update for the next appendix

    # Step 3: Write TOC entries to a .txt file
    with open(toc_txt_path, "w") as toc_file:
        toc_file.write("Table of Contents\n\n")
        for entry in toc_entries:
            toc_file.write(entry + "\n")
    
    print(f"Table of Contents for appendices written to {toc_txt_path}")

# Example usage
generate_appendix_toc(input_folder="input_pdfs", output_folder="output")
