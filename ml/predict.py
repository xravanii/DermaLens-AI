import numpy as np

from ml.model_loader import model
from ml.preprocess import preprocess_image


CLASS_NAMES = [
    "Acne",
    "Healthy",
    "Pigmentation",
    "Wrinkles"
]


def predict_image(uploaded_file):

    image = preprocess_image(uploaded_file)

    prediction = model.predict(image, verbose=0)

    confidence = float(np.max(prediction))

    class_index = int(np.argmax(prediction))

    predicted_class = CLASS_NAMES[class_index]

    return {
        "condition": predicted_class,
        "confidence": round(confidence * 100, 2),
        "all_predictions": [
            {
                "condition": CLASS_NAMES[i],
                "confidence": round(float(prediction[0][i]) * 100, 2)
            }
            for i in range(len(CLASS_NAMES))
        ]
    }
    