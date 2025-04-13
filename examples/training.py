import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.utils import class_weight
import seaborn as sns
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import BatchNormalization, Activation
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from tensorflow.keras.utils import to_categorical
import collections

def load_images(filename):
    with open(filename, 'rb') as f:
        magic, num, rows, cols = np.fromfile(f, dtype='>i4', count=4)
        images = np.fromfile(f, dtype=np.uint8).reshape(num, rows, cols)
    return images

def load_labels(filename):
    with open(filename, 'rb') as f:
        magic, num = np.fromfile(f, dtype='>i4', count=2)
        labels = np.fromfile(f, dtype=np.uint8)
    return labels

images = load_images("../gzip/emnist-byclass-train-images-idx3-ubyte")
labels = load_labels("../gzip/emnist-byclass-train-labels-idx1-ubyte")

counts = collections.Counter(labels)
print("Class Distribution:")
for label, count in sorted(counts.items()):
    print(f"Label {label}: {count} samples")

images = images / 255.0
X_dense = images.reshape(images.shape[0], -1)
X_cnn = images.reshape(images.shape[0], 28, 28, 1)
num_classes = 62
y_cat = to_categorical(labels, num_classes=num_classes)

class_weights = class_weight.compute_class_weight(
    class_weight='balanced',
    classes=np.unique(labels[:60000]),
    y=labels[:60000]
)
class_weights_dict = dict(enumerate(class_weights))

X_train_dense, X_val_dense = X_dense[:60000], X_dense[60000:]
X_train_cnn, X_val_cnn = X_cnn[:60000], X_cnn[60000:]
y_train, y_val = y_cat[:60000], y_cat[60000:]

# dense
print("Dense Model:\n")
dense_model = Sequential([
    Dense(512, input_shape=(784,)), BatchNormalization(), Activation('relu'), Dropout(0.4),
    Dense(256), BatchNormalization(), Activation('relu'), Dropout(0.4),
    Dense(128), BatchNormalization(), Activation('relu'), Dropout(0.3),
    Dense(num_classes, activation='softmax')
])
dense_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
dense_model.fit(X_train_dense, y_train, epochs=20, batch_size=128, validation_data=(X_val_dense, y_val), class_weight=class_weights_dict)

# cnn
print("CNN Model:\n")
cnn_model = Sequential([
    Conv2D(32, (3, 3), padding='same', input_shape=(28, 28, 1)), BatchNormalization(), Activation('relu'), MaxPooling2D((2, 2)), Dropout(0.25),
    Conv2D(64, (3, 3), padding='same'), BatchNormalization(), Activation('relu'), MaxPooling2D((2, 2)), Dropout(0.25),
    Conv2D(128, (3, 3), padding='same'), BatchNormalization(), Activation('relu'), MaxPooling2D((2, 2)), Dropout(0.25),
    Flatten(), Dense(256), BatchNormalization(), Activation('relu'), Dropout(0.5),
    Dense(num_classes, activation='softmax')
])
cnn_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
cnn_model.fit(X_train_cnn, y_train, epochs=20, batch_size=128, validation_data=(X_val_cnn, y_val), class_weight=class_weights_dict)

# evaluation
dense_loss, dense_accuracy = dense_model.evaluate(X_val_dense, y_val, verbose=2)
cnn_loss, cnn_accuracy = cnn_model.evaluate(X_val_cnn, y_val, verbose=2)
print(f"Dense Model Accuracy: {dense_accuracy:.4f}")
print(f"CNN Model Accuracy: {cnn_accuracy:.4f}")

# confusion matrix
def plot_confusion_matrix(model, X_val, y_val, title):
    preds = np.argmax(model.predict(X_val), axis=-1)
    true = np.argmax(y_val, axis=-1)
    cm = confusion_matrix(true, preds)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=False, cmap="Blues")
    plt.title(title)
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.show()

plot_confusion_matrix(dense_model, X_val_dense, y_val, "Dense Model Confusion Matrix")
plot_confusion_matrix(cnn_model, X_val_cnn, y_val, "CNN Model Confusion Matrix")

# save models
dense_model.save('dense_model.h5')
cnn_model.save('cnn_model.h5')

true_label = np.argmax(y_val, axis=1)
print(f"True labels: {true_label[:20]}")

predictions_dense = dense_model.predict(X_val_dense)
predicted_labels_dense = np.argmax(predictions_dense, axis=1)

predictions_cnn = cnn_model.predict(X_val_cnn)
predicted_labels_cnn = np.argmax(predictions_cnn, axis=1)

print(f"First 20 predictions from Dense Model: {predicted_labels_dense[:20]}")
print(f"First 20 predictions from CNN Model: {predicted_labels_cnn[:20]}")
