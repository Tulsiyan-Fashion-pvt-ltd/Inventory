from PIL import Image
import io

def compress_image(file) -> bytes:
    img = Image.open(io.BytesIO(file))   # making the file binary object treating as file in the memory
    return_file = io.BytesIO()
    img.thumbnail((420, 420))
    img.save(return_file, format='JPEG', quality=90, optimize=True)
    return return_file.getvalue()