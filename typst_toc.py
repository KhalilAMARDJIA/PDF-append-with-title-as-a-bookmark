from PyPDF2 import PdfReader
import os
import glob

def generate_typst_toc(input_folder: str, output_folder: str, main_document_name: str = "00_template.pdf"):
    # Ensure output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Define paths for the main document and output Typst file
    main_document = os.path.join(input_folder, main_document_name)
    toc_typ_path = os.path.join(output_folder, "table_of_contents.typ")

    # Step 1: Count pages in the main document
    main_reader = PdfReader(main_document)
    main_page_count = len(main_reader.pages)

    # Step 2: Get all appendix PDFs (excluding the main document) and prepare Typst entries
    appendix_paths = sorted(glob.glob(os.path.join(input_folder, "*.pdf")))
    appendix_paths = [path for path in appendix_paths if os.path.basename(path) != main_document_name]

    # Start Typst content with document-wide settings and TOC outline
    typst_content = [
        '#set text(font: ("Times New Roman", "IBM Plex Serif"), size: 11pt)',
        '#outline(title: "Appendices")',
        '#pagebreak()'  # Start appendices on a new page after TOC
    ]

    # Iterate over each appendix to create headers and page breaks based on page count
    current_page = main_page_count + 1
    for appendix_path in appendix_paths:
        appendix_reader = PdfReader(appendix_path)
        appendix_page_count = len(appendix_reader.pages)

        # Extract appendix title from filename without extension
        appendix_title = os.path.splitext(os.path.basename(appendix_path))[0]

        # Add appendix header (Typst will auto-generate TOC from these headers)
        typst_content.append(f"\n= {appendix_title}\n")

        # Add page breaks for each page in the appendix
        typst_content.append(f"#let n_pages = {appendix_page_count}")
        typst_content.append("#let i = 0")
        typst_content.append("#while i < n_pages {\n    pagebreak()\n    i += 1\n}")

        # Update starting page for the next appendix
        current_page += appendix_page_count

    # Write the Typst file content to an output file
    with open(toc_typ_path, "w") as typ_file:
        typ_file.write("\n".join(typst_content))

    print(f"Typst file with TOC and appendices written to {toc_typ_path}")

# Example usage
generate_typst_toc(input_folder="input_pdfs", output_folder="output")
