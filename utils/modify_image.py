import cv2


def resize_image(img, ratio):
    width = int(img.shape[1] * ratio)
    height = int(img.shape[0] * ratio)
    return cv2.resize(img, (width, height))


def crop_image_in_center(img, w, h):
    start_height = int(len(img) / 2 - h / 2)
    end_height = int(len(img) / 2 + h / 2)
    start_width = int(len(img[0]) / 2 - w / 2)
    end_width = int(len(img[0]) / 2 + w / 2)
    return img[start_height:end_height, start_width:end_width]


def make_white_pixels_transparent(img):
    has_channel = len(img[0, 0, :]) == 4

    for i in range(0, len(img)):
        for j in range(0, len(img[0])):
            if not has_channel:
                if img[i][j][0] == img[i][j][1] == img[i][j][2] == 255:
                    img[i][j] = img[i][j] + (0,)
                else:
                    img[i][j] = img[i][j] + (1,)
            else:
                if img[i][j][0] == img[i][j][1] == img[i][j][2] == 255:
                    img[i][j][3] = 0

    return img


def apply_dark_effect(img):
    """Modify an image to add a dark shade

    Keyword arguments:
    img 		-- numpy.ndarray created with cv2.imread('')
    """

    height, width, channels = img.shape

    for r in range(0, height):
        for c in range(0, width):
            img[r, c] = [img[r, c][0] / 4, img[r, c][1] / 4, img[r, c][2] / 4]

    return img
