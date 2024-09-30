import os
import re
import fitz


class Utils:
    ALLOWED_EXTENSIONS = {'pdf'}

    @staticmethod
    def split_pdf(app, filename, file_path, output_path):
        pdf_filenames = []
        png_filenames = []

        with fitz.open(file_path) as doc:
            if len(doc) == 0:
                raise Exception("No pages found in the document")

            # Ensure the output path exists
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            # Loop through each page in the original document
            for page_num in range(len(doc)):
                # Extract the current page and save it as a separate PDF
                new_pdf = fitz.open()  # Create a new empty PDF
                new_pdf.insert_pdf(doc, from_page=page_num, to_page=page_num)

                # Construct the PDF output filename using os.path.join for correct path formatting
                output_filename = os.path.join(output_path,
                                               f"{Utils.extract_name_from_file_path(filename)}-Page-{page_num + 1}.pdf")

                # Save the extracted page as a new PDF file
                new_pdf.save(output_filename)
                new_pdf.close()  # Close the new PDF file after saving
                pdf_filenames.append(os.path.basename(output_filename))

                # Load the current page to convert to PNG
                page = doc.load_page(page_num)
                pix = page.get_pixmap(dpi=150)  # Use dpi=150 for decent resolution

                # Create the PNG output filename (remove ".pdf" and add ".png")
                output_png_filename = output_filename.replace(".pdf", ".png")
                pix.save(output_png_filename)

                png_filenames.append(os.path.basename(output_png_filename))

                print(f"Saved: {output_filename} and {output_png_filename}")

        return pdf_filenames, png_filenames

    @staticmethod
    def extract_name_from_file_path(file_path):
        # This method should extract the base name (without the extension) from the file path
        return os.path.splitext(os.path.basename(file_path))[0]

    @staticmethod
    def ensure_directory_exists(directory):
        # Ensure that the directory exists, create it if not
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Utils.ALLOWED_EXTENSIONS

    @staticmethod
    def extract_page_number(filename):
        match = re.search(r'Page-(\d+)', filename)
        if match:
            return int(match.group(1))
        return 0  # Default if no number is found

    @staticmethod
    def ensure_directory_exists(folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)


    def pdf_to_png(self):
        print("Test")
