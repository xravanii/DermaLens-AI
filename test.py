from ml.preprocess import preprocess_image

img = preprocess_image("test.jpg")

print(img.shape)
print(img.dtype)