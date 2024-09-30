document.getElementById('pdfForm').addEventListener('submit', function(event) {
    // Prevent the form from submitting
    event.preventDefault();

    // Get the file input and split range input values
    const fileInput = document.getElementById('pdfFile');
    // Validate the file
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select a PDF file.');
        return;
    }

    // Check if the file is a PDF
    const fileName = file.name.toLowerCase();
    if (!fileName.endsWith('.pdf')) {
        alert('Only PDF files are allowed.');
        return;
    }

    const formData = new FormData();
    formData.append('pdfFile', file);

    // Send the POST request using fetch
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('PDF uploaded and split successfully.');
            } else {
                alert('There was an error: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An unexpected error occurred.');
        });

});