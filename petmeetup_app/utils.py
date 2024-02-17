# utils.py
from PIL import Image


def crop_square_image(image_path, size=300):
    original_image = Image.open(image_path)
    width, height = original_image.size

    # Calculate the crop box (left, top, right, bottom)
    left = (width - min(width, height)) / 2
    top = (height - min(width, height)) / 2
    right = (width + min(width, height)) / 2
    bottom = (height + min(width, height)) / 2

    # Crop the image
    cropped_image = original_image.crop((left, top, right, bottom))

    # Resize the image to the desired size
    cropped_image = cropped_image.resize((size, size))

    return cropped_image
