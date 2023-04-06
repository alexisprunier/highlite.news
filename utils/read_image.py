from PIL import Image
import numpy as np


def read_webp(path):
    im = Image.open(path)
    images = []
    try:
        while 1:
            im.seek(im.tell( ) +1)
            image_png = im.convert("RGBA")
            image_png = image_png.resize((80, 80))
            image_ndarray = np.array(image_png)

            for i in range(0, len(image_ndarray)):
                for j in range(0, len(image_ndarray[0])):
                    if not np.array_equal(image_ndarray[i, j], (0, 0, 0, 0)):
                        image_ndarray[i, j] = (243, 242, 151, 255)

            images.append(image_ndarray)
    except EOFError:
        pass

    return images
