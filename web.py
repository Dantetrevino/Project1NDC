from flask import Flask, request, render_template, send_file, redirect, url_for
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the upload directory exists

@app.route('/')
def home():
    return '''
    <html>
    <head>
        <title>File Transfer App</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background-color: #f4f4f4; }
            .container { background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); width: 50%; margin: auto; }
            input, button { margin: 10px; padding: 10px; }
            button { background-color: #007BFF; color: white; border: none; cursor: pointer; border-radius: 5px; }
            button:hover { background-color: #0056b3; }
            ol { text-align: left; display: inline-block; margin: 0 auto; padding-left: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Welcome to the File Transfer App</h2>
            <p>This website allows users to easily upload and download files. Follow the instructions below:</p>
            <ol>
                <li>Choose a file to upload.</li>
                <li>Click "Upload" to send the file to the server.</li>
                <li>Once uploaded, the file will automatically download.</li>
            </ol>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <button type="submit">Upload</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return redirect(url_for('download_file', filename=file.filename))

@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
    
#In the terminal put python web.py
#After ctrl+click on the link that pops up