from PIL import Image
import io


def calculate_non_transparent_pixel_density(image):

    try:

        # Get the size of the image
        img = Image.open(io.BytesIO(image))
        width, height = img.size

        # Convert the image to RGBA mode
        img_rgba = img.convert('RGBA')

        # Initialize counters
        total_pixels = width * height
        transparent_pixels = 0
        non_transparent_pixels = 0

        # Loop through each pixel
        for y in range(height):
            for x in range(width):
                # Get the pixel value (RGBA)
                pixel = img_rgba.getpixel((x, y))

                # Check if the pixel is transparent
                if pixel[3] == 0:
                    transparent_pixels += 1
                else:
                    non_transparent_pixels += 1

        # Calculate non-transparent pixel density
        non_transparent_density = (non_transparent_pixels / total_pixels) * 100

        # Display results
        results = {
            "total_pixels": total_pixels,
            "transparent_pixels": transparent_pixels,
            "non_transparent_pixels": non_transparent_pixels,
            "non_transparent_pixel_density": round(non_transparent_density)
        }

        return results

    except Exception as e:
        return {"error": str(e)}
