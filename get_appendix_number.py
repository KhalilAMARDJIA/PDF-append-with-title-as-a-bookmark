from PyPDF2 import PdfReader, PdfWriter
import os
import glob

def generate_toc_and_merge_pdfs(input_folder: str, output_folder: str, main_document_name: str = "00_template.pdf"):
    # Ensure output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Define paths for the main document and output files
    main_document = os.path.join(input_folder, main_document_name)
    output_pdf_path = os.path.join(output_folder, "final_document_with_toc.pdf")
    toc_txt_path = os.path.join(output_folder, "table_of_contents.txt")

    # Step 1: Count pages in the main document
    main_reader = PdfReader(main_document)
    main_page_count = len(main_reader.pages)

    # Step 2: Get all appendix PDFs (excluding main document) and prepare TOC entries
    appendix_paths = sorted(glob.glob(os.path.join(input_folder, "*.pdf")))
    appendix_paths = [path for path in appendix_paths if os.path.basename(path) != main_document_name]
    toc_entries = []

    current_page = main_page_count + 1  # Start TOC from the first page after main document

    # Calculate starting pages and titles based on appendix file names
    for appendix_path in appendix_paths:
        appendix_reader = PdfReader(appendix_path)
        appendix_page_count = len(appendix_reader.pages)
        
        # Create title from filename (e.g., "01_caprani2017.pdf" -> "Appendix A")
        appendix_title = f"Appendix {chr(65 + len(toc_entries))}"  # Convert to letters A, B, C, etc.
        toc_entries.append(f"{appendix_title} ............................ Page {current_page}")
        
        current_page += appendix_page_count  # Update for next appendix

    # Step 3: Write TOC entries to a .txt file
    with open(toc_txt_path, "w") as toc_file:
        toc_file.write("Table of Contents\n\n")
        for entry in toc_entries:
            toc_file.write(entry + "\n")
    print(f"Table of Contents written to {toc_txt_path}")

    # Step 4: Compile the final document with main document and appendices
    writer = PdfWriter()

    # Add all pages from the main document
    for page in main_reader.pages:
        writer.add_page(page)

    # Add each appendix PDF, starting a new page for each appendix
    for appendix_path in appendix_paths:
        appendix_reader = PdfReader(appendix_path)
        for page in appendix_reader.pages:
            writer.add_page(page)

    # Step 5: Save final merged PDF
    with open(output_pdf_path, "wb") as output_pdf:
        writer.write(output_pdf)

    print(f"PDF with main document and appendices created successfully at {output_pdf_path}")

# Example usage
generate_toc_and_merge_pdfs(input_folder="input_pdfs", output_folder="output")
