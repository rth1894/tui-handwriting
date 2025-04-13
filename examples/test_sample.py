import collections
import numpy as np


def load_labels(filename):
    with open(filename, 'rb') as f:
        magic, num = np.fromfile(f, dtype='>i4', count=2)
        labels = np.fromfile(f, dtype=np.uint8)
    return labels

labels = load_labels("../gzip/emnist-byclass-train-labels-idx1-ubyte")
mapping = {}

with open("../gzip/emnist-byclass-mapping.txt") as f:
    for line in f:
        key, val = line.strip().split()
        mapping[int(key)] = chr(int(val))


counts = collections.Counter(labels)
print("Class Distribution (Label ID → Character → Sample Count):")
for label, count in sorted(counts.items()):
    print(f"Label {label:2d} → '{mapping[label]}' → {count} samples")
