import matplotlib.pyplot as plt
import numpy as np

def load_images(filename):
    with open(filename, 'rb') as f:
        magic, num, rows, cols = np.fromfile(f, dtype=np.dtype('>i4'), count=4)
        images = np.fromfile(f, dtype=np.uint8).reshape(num, rows, cols)
    return images


def load_labels(filename):
    with open(filename, 'rb') as f:
        magic, num = np.fromfile(f, dtype=np.dtype('>i4'), count=2)
        labels = np.fromfile(f, dtype=np.uint8)
    return labels


images = load_images("../gzip/emnist-balanced-train-images-idx3-ubyte")
print(f"Loaded {images.shape[0]} images of size {images.shape[1]}x{images.shape[2]}")

labels = load_labels("../gzip/emnist-balanced-train-labels-idx1-ubyte")
print(f"Loaded {len(labels)} labels")


plt.imshow(images[10], cmap='gray')
plt.title(f"Label: {labels[10]}")
plt.savefig("sample_image.png")  # Saves the image
print("Image saved as sample_image.png")
