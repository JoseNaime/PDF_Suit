import shutil
import zipfile
import os

from flask import Flask, send_from_directory, request, flash, redirect, url_for, session, render_template, send_file
from PyPDF2 import PdfMerger
from utils import Utils

app = Flask(__name__, static_folder='./static')
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['MERGED_FOLDER'] = 'merged_pdfs/'
app.config['SPLIT_FOLDER'] = 'split/'
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
@app.route('/')
def index():  # put application's code here
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def process_pdf():
    if 'pdfFile' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['pdfFile']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and Utils.allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        output_path = os.path.join('static', app.config['SPLIT_FOLDER'], Utils.extract_name_from_file_path(filename))
        Utils.ensure_directory_exists(output_path)

        # Split the PDF and get the filenames
        pdf_filenames, png_filenames = Utils.split_pdf(app, filename, file_path, output_path)

        # Store filenames in session or pass them along for further processing
        session['pdf_filenames'] = pdf_filenames
        session['png_filenames'] = png_filenames
        session['original_pdf_filename'] = filename  # Store original filename

        flash('PDF uploaded and split successfully.')
        return redirect(url_for('split_selection', fax_file_path=output_path))

    flash('Allowed file type is PDF only.')
    return redirect(request.url)

# Route to display the PNG files and form
@app.route('/split_selection', methods=['GET'])
def split_selection():
    output_path = request.args.get('fax_file_path')

    if output_path and os.path.exists(output_path):
        png_files = [f for f in os.listdir(output_path) if f.endswith('.png')]
        png_files.sort(key=Utils.extract_page_number)
    else:
        png_files = []

    relative_output_path = os.path.relpath(output_path, 'static').replace('\\', '/')

    return render_template('split_selection.html', png_files=png_files, output_path=relative_output_path, original_pdf_filename=session.get('original_pdf_filename'))

# Route to handle form submission, merge PDFs, and create folders
@app.route('/group_pdf', methods=['POST'])
def group_pdf():
    original_pdf_filename = request.form.get('original_filename')

    pdf_filenames = session.get('pdf_filenames', [])
    png_filenames = session.get('png_filenames', [])

    output_path = os.path.join('static', app.config['SPLIT_FOLDER'], Utils.extract_name_from_file_path(original_pdf_filename))

    print(f"Output path: {output_path}")
    groups = {}

    # Organize PDF pages into groups based on the user input
    for key, value in request.form.items():
        if key.startswith('page_'):  # Ensure it's a page input
            page_number = int(key.split('_')[1])
            group_number = int(value)

            # Append the page number to the respective group
            if group_number not in groups:
                groups[group_number] = []
            groups[group_number].append(page_number)


    # Create folders for each group and merge PDFs
    merged_folder_path = os.path.join(app.config['MERGED_FOLDER'])
    os.makedirs(merged_folder_path, exist_ok=True)

    for group, pages in groups.items():
        group_folder = os.path.join(merged_folder_path, f'group_{group}')
        os.makedirs(group_folder, exist_ok=True)

        merger = PdfMerger()

        for page_number in sorted(pages):
            pdf_filename = pdf_filenames[page_number - 1]
            png_filename = png_filenames[page_number - 1]

            pdf_path = os.path.join(output_path, pdf_filename).replace('\\', '/')
            png_path = os.path.join(output_path, png_filename).replace('\\', '/')

            print(f"PDF Path: {pdf_path}")
            print(f"PNG Path: {png_path}")

            if os.path.exists(pdf_path):
                shutil.copy(pdf_path, os.path.join(group_folder, pdf_filename))
            else:
                print(f"Error: PDF file not found: {pdf_filename}")
                flash(f"PDF file not found: {pdf_filename}")
                return redirect(request.url)

            if os.path.exists(png_path):
                shutil.copy(png_path, os.path.join(group_folder, png_filename))
            else:
                print(f"Error: PNG file not found: {png_filename}")
                flash(f"PNG file not found: {png_filename}")
                return redirect(request.url)

            merger.append(pdf_path)

        merged_pdf_path = os.path.join(group_folder, f'merged_group_{group}.pdf')
        with open(merged_pdf_path, 'wb') as merged_pdf_file:
            merger.write(merged_pdf_file)
        merger.close()

        print(f"Merged PDF created for group {group}: {merged_pdf_path}")

    # Dynamic zip file name based on the original PDF filename (without extension)
    zip_filename = f"{os.path.splitext(original_pdf_filename)[0]}_grouped_pdfs.zip"
    zip_path = os.path.join(app.config['UPLOAD_FOLDER'], zip_filename)
    print(f"ZIP file path: {zip_path}")

    # Create the ZIP file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(merged_folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, merged_folder_path)
                zipf.write(full_path, relative_path)
                print(f"Added to ZIP: {relative_path}")

    # Debug: Ensure ZIP file is not empty
    if os.path.exists(zip_path):
        print(f"ZIP file created: {zip_path}")
    else:
        print(f"Error: Failed to create ZIP file.")
        flash(f"Failed to create ZIP file.")
        return redirect(request.url)

    # Return the ZIP file as a downloadable response
    return send_file(zip_path, as_attachment=True)

# Utility function to clean up (optional)
@app.teardown_appcontext
def cleanup(exception=None):
    # Clean up merged folder if needed
    if os.path.exists(app.config['MERGED_FOLDER']):
        shutil.rmtree(app.config['MERGED_FOLDER'])

if __name__ == '__main__':
    app.run()
