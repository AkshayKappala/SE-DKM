import numpy as np
from skimage import io, color, feature, img_as_float
from skimage.transform import resize

def _get_edges(image):
    # Convert image to grayscale if it has more than 2 dimensions
    if image.ndim == 3:
        image = color.rgb2gray(image)
    # Apply Canny edge detection
    edges = feature.canny(image)
    return edges

def compute_iou(edges1, edges2):
    # Compute intersection and union
    intersection = np.logical_and(edges1, edges2)
    union = np.logical_or(edges1, edges2)
    # Compute IoU
    iou = np.sum(intersection) / np.sum(union)
    return iou

def compare_images(image1, image2):
    # Convert images to float
    image1 = img_as_float(image1)
    image2 = img_as_float(image2)

    # Resize images to the same dimensions
    image2 = resize(image2, image1.shape)

    # Get edges of both images
    edges1 = _get_edges(image1)
    edges2 = _get_edges(image2)

    # Compute IoU
    iou = compute_iou(edges1, edges2)
    return iou

if __name__ == "__main__":
    # Load images
    image1 = io.imread('images/cropl.jpg')
    image2 = io.imread('images/cropr.jpg')

    # Compare images
    iou_index = compare_images(image1, image2)
    print(f"IoU Index: {iou_index}")