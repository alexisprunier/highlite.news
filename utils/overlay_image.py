import numpy
from PIL import ImageFont, ImageDraw, Image
import textwrap
from itertools import chain
import os
from utils.config import PROJECT_PATH


def overlay_highlight_frame(img):
    """Add the Highlite.me styled frame on an image

    Keyword arguments:
    img 		-- numpy.ndarray created with cv2.imread('')
    """

    height, width, channels = img.shape

    for r in range(0, height):
        for c in chain(range(10, 20), range(width - 20, width - 10)):
            img[r, c] = [151, 242, 243]
    for r in chain(range(10, 20), range(height - 20, height - 10)):
        for c in range(0, width):
            img[r, c] = [151, 242, 243]

    for r in range(0, height):
        for c in chain(range(0, 10), range(width - 10, width)):
            img[r, c] = [253, 207, 70]
    for r in chain(range(0, 10), range(height - 10, height)):
        for c in range(0, width):
            img[r, c] = [253, 207, 70]

    return img


def overlay_text(img, text, pos, size, color, max_width=None, pos_type="left", f=None):
    """Add a text to an image

    Keyword arguments:
    img 		-- numpy.ndarray - variable created with cv2.imread('')
    text 		-- str - text to apply to the image -> "Mon texte"
    pos		 	-- tuple of int - position of the text on the image -> (50, 100)
                -- "centered" can be used
    size 		-- int - size of the text on the image
    color 		-- typle of int - color BGR of the text on the image -> (151, 242, 243)
    """

    if max_width is None:
        lines = [text]
    else:
        lines = textwrap.wrap(text, width=max_width)

    img_pil = Image.fromarray(img).convert('RGBA')
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype(os.path.join(PROJECT_PATH, "static/font/bungee/Bungee-Regular.otf"), size)

    if f is not None:
        color = color + (int(f / 20 * 255),)
    else:
        color = color + (255,)

    for i, line in enumerate(lines):
        line_color = (color[0], color[1], color[2], max(0, color[3] - (i * (100 if f is not None else 0))))

        if pos[0] == "centered":
            w, h = draw.textsize(line, font=font)
            calc_pos = (img.shape[1] / 2 - w / 2, pos[1] + (i * size))
        else:
            if pos_type == "middle":
                w, h = draw.textsize(line, font=font)
                calc_pos = (pos[0] - int(w / 2), pos[1] + (i * size))
            elif pos_type == "right":
                w, h = draw.textsize(line, font=font)
                calc_pos = (pos[0] - w, pos[1] + (i * size))
            else:
                calc_pos = (pos[0], pos[1] + (i * size))

        txt = Image.new('RGBA', img_pil.size, (255, 255, 255, 0))
        d = ImageDraw.Draw(txt)
        d.text(calc_pos, line, fill=line_color, font=font)
        img_pil = Image.alpha_composite(img_pil, txt)

    return numpy.array(img_pil.convert('RGB'))


def overlay_image(img1, img2, pos, pos_type="left", f=None):
    """Add an image over another one

    Keyword arguments:
    img1		-- numpy.ndarray - variable created with cv2.imread('')
    img2		-- numpy.ndarray - variable created with cv2.imread('')
    pos			-- tuple of int - position of the img2 -> (50, 100)
    """

    h, w, c = img2.shape
    x, y = pos

    if x != "centered":
        if pos_type == "middle":
            x = int(x - (w / 2))
        elif pos_type == "right":
            x = x - w
    else:
        x = int(img1.shape[1] / 2 - (w / 2))

    if len(img2[0, 0, :]) == 4:
        alpha = img2[:, :, 3] * min(1, (f / 20)) / 255.0 if f is not None else img2[:, :, 3] / 255.0
    else:
        alpha = min(1, (f / 20)) if f is not None else 1

    img1[y:(y + h), x:(x + w), 0] = (1. - alpha) * img1[y:(y + h), x:(x + w), 0] + alpha * img2[:, :, 0]
    img1[y:(y + h), x:(x + w), 1] = (1. - alpha) * img1[y:(y + h), x:(x + w), 1] + alpha * img2[:, :, 1]
    img1[y:(y + h), x:(x + w), 2] = (1. - alpha) * img1[y:(y + h), x:(x + w), 2] + alpha * img2[:, :, 2]

    return img1
