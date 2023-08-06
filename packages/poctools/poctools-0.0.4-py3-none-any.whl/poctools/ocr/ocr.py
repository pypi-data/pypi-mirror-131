from io import BytesIO

import cv2
import numpy as np
import pytesseract
from PIL import Image

from .config import NUMBER_OCR_CONFIG


def new_number(image_data: bytes) -> str:
    image = cv2.imdecode(np.asarray(bytearray(image_data), dtype=np.uint8), cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    return pytesseract.image_to_string(image, lang='eng', config=NUMBER_OCR_CONFIG).strip()


def new_ocr(image_data: bytes, charset: str) -> str:
    config = f"--psm 10 --oem 3 -c tessedit_char_whitelist={charset}"
    image = Image.open(BytesIO(image_data)).convert('L')
    table=[0 if i < 150 else 1 for i in range(256)]
    image = image.point(table, "1")
    return pytesseract.image_to_string(image, config=config).strip()
