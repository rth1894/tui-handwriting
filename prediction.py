import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

EMNIST_CLASSES = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

USE_CNN = True
MODEL_PATH = "./examples/cnn_model.h5" if USE_CNN else "./examples/dense_model.h5"

model = load_model(MODEL_PATH)

def preprocess_image(image_path):
    img = Image.open(image_path).convert('L')
    img = img.resize((28, 28))
    # img = ImageOps.invert(img)
    img = img.transpose(Image.ROTATE_270)
    img_array = np.array(img).astype("float32") / 255.0

    plt.imshow(img_array.reshape(28, 28), cmap="gray")
    plt.title("Final Input to Model")
    plt.axis("off")
    plt.show()

    if USE_CNN:
        return img_array.reshape(1, 28, 28, 1)
    else:
        return img_array.reshape(1, 784)

def predict(image_path):
    try:
        processed = preprocess_image(image_path)
        prediction = model.predict(processed)[0]
        sorted_indices = np.argsort(prediction)[::-1]
        top_preds = []

        for i in sorted_indices[:5]:
            prob = float(prediction[i])
            top_preds.append((EMNIST_CLASSES[i], prob))

        print(f"\nTop 5 Predictions:")
        for char, prob in top_preds:
            print(f"{char}: {prob:.4f}")

        return top_preds

    except Exception as e:
        print(f"Error during prediction: {e}")
        return []


predict("./image.png")
