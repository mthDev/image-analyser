# Image Analysis Web Application

This is a Python Flask web application designed to allow users to upload images and analyze them to determine various image properties such as size, pixels, transparency percentage, and other metadata.

## Features

- **Image Upload**: Users can upload images of various file types.
- **Image Analysis**: Uploaded images are analyzed to extract the following information:
  - Size: The file size of the image.
  - Pixels: The dimensions of the image in pixels.
  - Transparency Percentage: The percentage of transparent pixels in the image.
  - Other Image Metadata: Additional metadata such as color mode, resolution, etc.
- **Multiple File Type Support**: The application supports multiple image file types including JPEG, PNG, GIF, etc.
- **User-friendly Interface**: The web interface is designed to be intuitive and easy to use.

## Requirements

- Python 3.x
- Flask
- Pillow (Python Imaging Library)

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/mthDev/image-analyser.git
    ```

2. Navigate to the project directory:

    ```bash
    cd image-analysis
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Start the Flask server:

    ```bash
    python application.py
    ```

2. Open your web browser and navigate to `[http://localhost:3000](http://localhost:3000)`.
3. Use the web interface to upload images and view their analysis results.

## Contributing

Contributions are welcome! If you have any ideas for improvements or new features, feel free to open an issue or submit a pull request.

## License

TBC
