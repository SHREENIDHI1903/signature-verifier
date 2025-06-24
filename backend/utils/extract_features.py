from skimage.feature import hog

def extract_features(image):
    features = hog(image, pixels_per_cell=(8, 8), cells_per_block=(2, 2), feature_vector=True)
    return features
