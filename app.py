from flask import Flask, render_template, request, send_file
import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pydicom

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join('uploads', uploaded_file.filename)
        uploaded_file.save(file_path)
        try:
            png_filename = dicom_to_png(file_path)
            return render_template('index.html', png_filename=png_filename)
        except Exception as e:
            error_message = f"Error converting DICOM to PNG: {str(e)}"
            return render_template('index.html', error=error_message)
    return render_template('index.html')

@app.route('/show_image/<path:filename>')
def show_image(filename):
    image_path = os.path.join('static', filename)
    return send_file(image_path, mimetype='image/png')

def dicom_to_png(dicom_file):
    ds = pydicom.dcmread(dicom_file)
    pixel_array = ds.pixel_array
    plt.imshow(pixel_array, cmap=cm.gray)
    plt.axis('off')
    png_filename = f"{os.path.splitext(os.path.basename(dicom_file))[0]}.png"
    png_path = os.path.join('static', png_filename)
    plt.savefig(png_path, bbox_inches='tight', pad_inches=0)
    plt.close()
    return png_filename

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)
