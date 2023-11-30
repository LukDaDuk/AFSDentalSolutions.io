from flask import Flask, request, render_template, redirect, url_for, session
from UpdatedPythonTest import check_teeth_condition, allowed_file
import os

app = Flask(__name__)
app.secret_key = 'DentalTartarStrip'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Handle regular file upload
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            result_key, processed_image_path, saturation_graph_path = check_teeth_condition(file)
            session['result_key'] = result_key
            session['processed_image'] = processed_image_path
            session['saturation_graph'] = saturation_graph_path
            return redirect(url_for('result'))
        else:
            return "File not allowed or no file selected", 400
    return render_template('upload.html')

@app.route('/result')
def result():
    result_key = session.get('result_key', 'condition1')
    processed_image = session.get('processed_image', 'default_processed_image.jpg')
    saturation_graph = session.get('saturation_graph', 'default_saturation_graph.jpg')
    return render_template('result.html', 
                           result_key=result_key,
                           processed_image=processed_image,
                           saturation_graph=saturation_graph)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
