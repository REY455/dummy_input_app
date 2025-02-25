from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov'}

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    text_content = None
    file_url = None
    error = None

    if request.method == 'POST':
        # Handle text input
        if 'text_input' in request.form:
            text_content = request.form['text_input']
        
        # Handle file upload
        if 'file_input' in request.files:
            file = request.files['file_input']
            if file.filename != '':
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    file_url = url_for('static', filename=f'uploads/{filename}')
                else:
                    error = "Invalid file type. Allowed types: images (png, jpg, jpeg, gif) and videos (mp4, mov)"

    return render_template('index.html', 
                          text_content=text_content,
                          file_url=file_url,
                          error=error)

if __name__ == '__main__':
    app.run(debug=True)