import io
import traceback

from error_handler import generate_error_response, CustomError
from flask import jsonify, Response
from json2html import json2html
from PIL import Image

OUTPUT_FORMATS = ["JSON", "HTML"]


def analyse_image_api(request, output_format):

    if output_format not in OUTPUT_FORMATS:
        error_invalid_output_format()

    if 'file' not in request.files:
        error_no_file_attached_to_request()

    file = request.files['file']

    if file.filename == '':
        error_filename_cannot_be_determined()

    if not file.content_type.startswith('image'):
        error_not_an_image()

    analysis_results = calculate_non_transparent_pixel_density(file)
    response = ''

    if output_format == "JSON":
        response = jsonify(analysis_results)
    elif output_format == "HTML":
        analysis_results = json2html.convert(json=analysis_results, table_attributes="id=\"results-table\" class=\"table\"")
        response = Response(analysis_results, mimetype='text/HTML')

    return response


def calculate_non_transparent_pixel_density(file):

    try:
        image = file.read()
        img = Image.open(io.BytesIO(image))
        width, height = img.size
        img_rgba = img.convert('RGBA')
        total_pixels = width * height
        transparent_pixels = 0
        non_transparent_pixels = 0

        for y in range(height):
            for x in range(width):
                pixel = img_rgba.getpixel((x, y))
                if pixel[3] == 0:
                    transparent_pixels += 1
                else:
                    non_transparent_pixels += 1

        non_transparent_density = (non_transparent_pixels / total_pixels) * 100

        results = {
            "image_type": file.mimetype,
            "non_transparent_pixels": non_transparent_pixels,
            "non_transparent_pixel_density": round(non_transparent_density, 2),
            "resolution": {
                "width": width,
                "height": height
            },
            "total_pixels": total_pixels,
            "transparent_pixels": transparent_pixels
        }

        return results

    except Exception as e:
        error_unhandled_exception(e, traceback)


# -----------------------------------
# Exception handlers
# -----------------------------------

def error_invalid_output_format():
    """ Where the user has provided an invalid output format enum """
    generate_error_response(
        CustomError(
            message="The output format is invalid.",
            code=400,
            instruction=f'Available values are: {", ".join(OUTPUT_FORMATS)}',
            traceback="N/A"
        )
    )


def error_no_file_attached_to_request():
    """ Where no file is attached to the request """
    generate_error_response(
        CustomError(
            message="No file object has not been attached to the request",
            code=400,
            instruction="Please attach a file and retry",
            traceback="N/A"
        )
    )


def error_filename_cannot_be_determined():
    """ Where the filename cannot be determined from the request """
    generate_error_response(
        CustomError(
            message="The filename cannot be determined",
            code=400,
            instruction="Please attach a file and retry",
            traceback="N/A"
        )
    )


def error_not_an_image():
    """ Where the provided file is not of an image type """
    generate_error_response(
        CustomError(
            message="The attached file is not an image",
            code=400,
            instruction="Please re-attach an image file and retry",
            traceback="N/A"
        )
    )


def error_unhandled_exception(exception, trace):
    """ Where an unhandled exception has been thrown """
    generate_error_response(
        CustomError(
            message=f'An unhandled exception has occurred -- {exception}',
            code=500,
            instruction="Please contact your administrator",
            traceback=trace.format_exc()
        )
    )
