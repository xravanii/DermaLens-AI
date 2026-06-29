from ml.predict import predict_image

def analyze_skin(uploaded_image):

    print("Type:", type(uploaded_image))
    print("Length:", len(uploaded_image))

    report = predict_image(uploaded_image)

    return report