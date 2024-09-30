
# PDF_Suit [AZ_PDF]

PDF_Suit [AZ_PDF] is a Flask web application that allows users to upload a PDF file, split it into individual pages, display previews of each page, group the pages according to user input, and download the grouped PDFs as a ZIP file.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Code Overview](#code-overview)
    - [app.py](#apppy)
    - [utils.py](#utilspy)
    - [templates](#templates)
    - [static](#static)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features
- **PDF Upload**: Users can upload a PDF file through the web interface.
- **PDF Splitting**: The uploaded PDF is split into individual pages.
- **Page Preview**: Each page is converted to a PNG image for preview.
- **Page Grouping**: Users can group pages by entering group numbers.
- **PDF Merging**: Pages in each group are merged into a single PDF.
- **Download**: The grouped PDFs are compressed into a ZIP file for download.

## Technologies Used
- **Backend**: Python, Flask, PyPDF2, PyMuPDF (pymupdf)
- **Frontend**: HTML, CSS
- **Other**: zipfile, os, shutil

## Prerequisites
- Python 3.x installed on your machine
- pip (Python package manager)
- Git (to clone the repository)

## Installation
Follow these steps to set up and run the project on your local machine.

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/PDF_Suit.git
cd PDF_Suit
```

### 2. Set Up a Virtual Environment
It's recommended to use a virtual environment to manage dependencies.

On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
If requirements.txt is not provided, install the dependencies manually:

```bash
pip install Flask PyPDF2 PyMuPDF
```

### 4. Set Up Directory Structure
Ensure the following directories exist:
- `uploads/` - For storing uploaded PDF files.
- `static/split/` - For storing split PDF pages and images.
- `merged_pdfs/` - For storing grouped and merged PDFs.

If they don't exist, create them:
```bash
mkdir uploads
mkdir static/split
mkdir merged_pdfs
```

## Project Structure
```plaintext
PDF_Suit [AZ_PDF]
├── static
│   ├── css
│   │   ├── index.css
│   │   └── split_selection.css
│   ├── js
│   └── split
├── templates
│   ├── index.html
│   └── split_selection.html
├── uploads
├── venv (virtual environment)
├── app.py
└── utils.py
```

- **static/**: Contains static files like CSS, JavaScript, and images.
- **templates/**: Contains HTML templates for rendering the web pages.
- **uploads/**: Stores the uploaded PDF files.
- **venv/**: Python virtual environment directory.
- **app.py**: The main Flask application file.
- **utils.py**: Utility functions used by the application.

## Usage

### 1. Run the Application
Ensure your virtual environment is activated and run:
```bash
python app.py
```
The application will start on [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

### 2. Use the Application
#### Step 1: Upload a PDF File
- Navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/).
- Click on "Choose a PDF file" and select a PDF from your computer.
- Click on "Process PDF".

#### Step 2: Preview and Group Pages
- After processing, you'll be redirected to a page showing previews of each page.
- For each page, enter a group number in the input field provided.
- After grouping, click on "Download Groups".

#### Step 3: Download Grouped PDFs
- The application will process your input, merge the pages into grouped PDFs, compress them into a ZIP file, and prompt you to download it.

## Code Overview

### app.py
This is the main Flask application file.

#### Routes:
- `/`: Renders the index page with the upload form.
- `/upload`: Handles the PDF upload and splitting.
- `/split_selection`: Displays page previews and grouping form.
- `/group_pdf`: Handles grouping, merging, and zipping of PDFs.

#### Configurations:
- `UPLOAD_FOLDER`: Directory for uploaded files.
- `MERGED_FOLDER`: Directory for merged PDFs.
- `SPLIT_FOLDER`: Directory for split pages.
- `SECRET_KEY`: Used for session management.

### utils.py
Contains utility functions and classes.

#### Utils Class:
- `split_pdf()`: Splits the uploaded PDF into individual pages and saves them as PDFs and PNGs.
- `extract_name_from_file_path()`: Extracts the base name from a file path.
- `allowed_file()`: Checks if the uploaded file is a PDF.
- `extract_page_number()`: Extracts the page number from the filename.
- `ensure_directory_exists()`: Checks if a directory exists, and creates it if it doesn't.

### templates
Contains HTML templates.

- `index.html`: The home page with the PDF upload form.
- `split_selection.html`: Displays previews of PDF pages and allows grouping.

### static
Contains static files like CSS and JavaScript.

- `css/index.css`: Styles for the index page.
- `css/split_selection.css`: Styles for the split selection page.
- `split/`: Stores split PDF pages and their PNG previews.

## Troubleshooting

### Issue: Uploaded PDF doesn't split properly.
- **Solution**: Ensure that the PDF is not corrupted and has at least one page.

### Issue: Error when downloading grouped PDFs.
- **Solution**: Check the server console for errors. Ensure that the directories have the correct permissions and paths are constructed properly.

### Issue: Application not starting or crashes on start.
- **Solution**: Verify that all dependencies are installed. Check for syntax errors or missing files.

## Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Commit your changes: `git commit -am 'Add your feature'`.
4. Push to the branch: `git push origin feature/your-feature-name`.
5. Submit a pull request.

Please ensure your code adheres to the existing style guidelines and includes appropriate tests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- **Flask**: For providing a simple and powerful web framework.
- **PyPDF2**: For PDF manipulation capabilities.
- **PyMuPDF (pymupdf)**: For handling PDF rendering and conversions.
