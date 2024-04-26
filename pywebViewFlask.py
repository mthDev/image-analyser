from flask import Flask, render_template, request
from image_analyser import calculate_non_transparent_pixel_density

import webview
import sys
import threading
import base64

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def image_analyser():  # put application's code here
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="No file part")

        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error="No selected file")

        # Check if the file is an image
        if file.content_type.startswith('image'):
            image_data = file.read()
            image_type = file.mimetype
            encoded_image_data = base64.b64encode(image_data)
            analysis_results = calculate_non_transparent_pixel_density(image_data)
            return render_template('result.html', results=analysis_results,
                                   image_data=encoded_image_data.decode('utf-8'), image_type=image_type)
        else:
            return render_template('index.html', error="Uploaded file is not an image")

    # GET Method returns main screen
    return render_template('index.html')


def start_server():
    app.run()


if __name__ == '__main__':
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()
    webview.create_window("Image Analyser", "http://127.0.0.1:5000/", min_size=(800, 875))
    webview.start()
    sys.exit()
