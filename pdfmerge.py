def main():
    import os
    os.chdir("H:\\AFF-CLINIQUE\\Produits\\NEOMIS Percutaneous\\2022_CER V00 MDR Burrs\\ANNEXES\\ANNEX D\\all_articles")
    import glob
    from PyPDF2 import PdfFileMerger
    from PyPDF2.generic import Bookmark
    def merger(output_path, input_paths):
        pdf_merger = PdfFileMerger()
        file_handles = []
        
        for path in input_paths:
            bookmark = os.path.basename(path)
            pdf_merger.append(fileobj= path,bookmark=None, pages=None, import_bookmarks=False)
            
        with open(output_path, 'wb') as fileobj:
            pdf_merger.write(fileobj)
            
    if __name__ == '__main__':
        paths = glob.glob('*.pdf')
        paths.sort()
        merger(output_path= 'pdf_merger.pdf', input_paths= paths)

if __name__ == "__main__":
    main()
