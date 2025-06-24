from skimage.feature import hog
from skimage.color import rgb2gray
import numpy as np

def extract_features(image):
    if len(image.shape) == 3:
        image = rgb2gray(image)

    try:
        features = hog(
            image,
            pixels_per_cell=(8, 8),
            cells_per_block=(2, 2),
            feature_vector=True
        )
        print("HOG features extracted. Shape:", features.shape)
        return features
    except Exception as e:
        print("HOG extraction failed:", e)
        return np.zeros((1,))  # or any fallback vector that keeps shape consistent
