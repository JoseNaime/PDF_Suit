import os

import pymupdf # PyMuPDF


class Utils:
    ALLOWED_EXTENSIONS = {'pdf'}

    @staticmethod
    def split_pdf(app, filename, file_path, output_path):
        with pymupdf.open(file_path) as doc:
            if len(doc) == 0:
                raise Exception("No pages found in the document")

            for page_num in range(len(doc)):
                with pymupdf.open() as new_pdf:
                    new_pdf.insert_pdf(doc, from_page=page_num, to_page=page_num)
                    output_filename = f"{output_path}{Utils.extract_name_from_file_path(filename)}-Page-{page_num + 1}.pdf"
                    new_pdf.save(output_filename)

                    # Convert png and save
                    page = doc.load_page(page_num)
                    pix = page.get_pixmap()
                    output_file = f"{output_filename[:-4]}.png" # Remove .pdf and add .png
                    pix.save(output_file)

    @staticmethod
    def extract_name_from_file_path(file_path):
        """ Extracts and returns the file name without extension from a file path. """
        return os.path.splitext(os.path.basename(file_path))[0]

    @staticmethod
    def ensure_directory_exists(folder_path):
        """ Ensures the output folder exists, creates it if it doesn't. """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Utils.ALLOWED_EXTENSIONS

    @staticmethod
    def ensure_directory_exists(folder_path):
        """ Ensures the output folder exists, creates it if it doesn't. """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)


    def pdf_to_png(self):
        print("Test")
