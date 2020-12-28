import os
os.chdir("I:\\Python_merge_pdf")
import glob
from PyPDF2 import PdfFileMerger
from PyPDF2.generic import Bookmark
def merger(output_path, input_paths):
    pdf_merger = PdfFileMerger()
    file_handles = []
    
    for path in input_paths:
        bookmark = os.path.basename(path)
        pdf_merger.append(path,import_bookmarks=False, bookmark = bookmark)
        
    with open(output_path, 'wb') as fileobj:
        pdf_merger.write(fileobj)
        
if __name__ == '__main__':
    paths = glob.glob('*.pdf')
    paths.sort()
    merger('pdf_merger2.pdf', paths)