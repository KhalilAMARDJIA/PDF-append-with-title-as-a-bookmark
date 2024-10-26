import os
import glob
from PyPDF2 import PdfMerger

def main():
    # Ensure the output directory exists
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Get the current working directory
    cwd = os.getcwd()
    os.chdir(cwd)
    
    def merger(output_path, input_paths):
        pdf_merger = PdfMerger()
        
        for path in input_paths:
            # Use the file name as the bookmark title
            bookmark_title = os.path.basename(path)
            print(f'Adding {bookmark_title} to the merger...')
            try:
                pdf_merger.append(path, outline_item=bookmark_title)
            except Exception as e:
                print(f"Failed to append {bookmark_title}: {e}")
        
        # Write the merged PDF to the specified output path
        if pdf_merger.pages:  # Check if there are pages to write
            with open(output_path, 'wb') as fileobj:
                pdf_merger.write(fileobj)
                print(f'Merged PDF written to {output_path}')
        else:
            print("No pages were merged. The output PDF is empty.")
            
    # Define the main execution for the script
    paths = glob.glob('input_pdfs/*.pdf')  # Updated input directory
    paths.sort()  # Sort paths to ensure the files are merged in order
    
    if not paths:
        print("No PDF files found in the input directory.")
        return
    
    merger(output_path=os.path.join(output_dir, 'pdf_merger.pdf'), input_paths=paths)

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
