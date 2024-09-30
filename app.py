import json

from flask import Flask, send_from_directory, request, flash, redirect, url_for, session
import pypdf
from utils import Utils
import os

app = Flask(__name__, static_folder='./static')
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['SPLIT_FOLDER'] = './split/'
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/')
def index():  # put application's code here
    return send_from_directory('static', 'index.html')

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

        output_path = app.config['SPLIT_FOLDER'] + Utils.extract_name_from_file_path(filename) + '/'
        Utils.ensure_directory_exists(output_path)

        # Split fax
        Utils.split_pdf(app, filename, file_path, output_path)
        # Generate pngs out of pdfs

        # Merge each page on each subdirectory

        flash('PDF uploaded and split successfully.')
        messages = json.dumps({"fax_file_path": output_path})
        session['messages'] = messages
        return redirect(url_for('split_selection'), message=messages)

    flash('Allowed file type is PDF only.')
    return redirect(request.url)

@app.route('/download_pdf', methods=['GET'])
def download_pdf():
    return send_from_directory('static', 'download.html')

@app.route('/split_selection', methods=['GET'])
def split_selection():
    messages = session['messages']       # counterpart for session
    return send_from_directory('static', 'split_selection.html', messages=json.loads(messages))


if __name__ == '__main__':
    app.run()
