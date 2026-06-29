from PIL import Image
import numpy as np
from io import BytesIO

IMG_SIZE = (224, 224)


def preprocess_image(uploaded_file):
    """
    Converts uploaded image into model input.
    """

    if isinstance(uploaded_file, bytes):
        image = Image.open(BytesIO(uploaded_file))
    else:
        image = Image.open(uploaded_file)

    image = image.convert("RGB")

    image = image.resize(IMG_SIZE)

    image = np.array(image)

    image = image.astype("float32")

    image = np.expand_dims(image, axis=0)

    return image