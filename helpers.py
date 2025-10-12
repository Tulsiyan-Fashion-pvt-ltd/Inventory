from PIL import Image
import io

def compress_image(file) -> bytes:
    print('running compressiong')
    img = Image.open(io.BytesIO(file))   # making the file binary object treating as file in the memory
    return_file = io.BytesIO()
    img.thumbnail((420, 560))
    img.save(return_file, format='JPEG', quality=90, optimize=True)
    return return_file.getvalue()

def compress_main_image(file) -> bytes:
    print('running compressiong')
    img = Image.open(io.BytesIO(file))   # making the file binary object treating as file in the memory
    return_file = io.BytesIO()
    img.thumbnail((800, 800))
    img.save(return_file, format='JPEG', quality=85, optimize=True)
    return return_file.getvalue()