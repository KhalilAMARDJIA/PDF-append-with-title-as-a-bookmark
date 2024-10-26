import os
import glob
from PyPDF2 import PdfMerger
from typing import List

def main():
    # Ensure the output directory exists
    output_dir = 'output'
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    except Exception as e:
        print(f"Error creating output directory '{output_dir}': {e}")
        return

    # Ensure input directory exists and fetch PDF files
    input_dir = 'input_pdfs'
    if not os.path.exists(input_dir):
        print(f"Input directory '{input_dir}' does not exist.")
        return

    paths = glob.glob(os.path.join(input_dir, '*.pdf'))
    paths.sort()  # Sort paths to ensure the files are merged in order

    if not paths:
        print("No PDF files found in the input directory.")
        return

    # Define the main execution for the script
    try:
        merger(output_path=os.path.join(output_dir, 'pdf_merger.pdf'), input_paths=paths)
    except Exception as e:
        print(f"An error occurred during the PDF merging process: {e}")

def merger(output_path: str, input_paths: List[str]) -> None:
    pdf_merger = PdfMerger()
    pages_added = False  # Flag to track if any pages were successfully added

    for path in input_paths:
        # Use the file name as the bookmark title
        bookmark_title = os.path.basename(path)
        print(f'Adding {bookmark_title} to the merger...')
        
        if not os.path.isfile(path):
            print(f"Warning: '{path}' is not a valid file and will be skipped.")
            continue
        
        try:
            pdf_merger.append(path, outline_item=bookmark_title)
            pages_added = True
        except Exception as e:
            print(f"Failed to append {bookmark_title}: {e}")

    # Write the merged PDF to the specified output path if pages were added
    if pages_added:
        try:
            with open(output_path, 'wb') as fileobj:
                pdf_merger.write(fileobj)
                print(f'Merged PDF written to {output_path}')
        except Exception as e:
            print(f"Error writing the merged PDF to '{output_path}': {e}")
    else:
        print("No pages were merged. The output PDF is empty.")

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
