import numpy as np
from skimage import io, img_as_float, color
from skimage.metrics import structural_similarity as ssim
from skimage.transform import resize
from dwt import dwt2d

def _get_2d_array(image):
    # Convert image to grayscale if it has more than 2 dimensions
    if image.ndim == 3:
        image = color.rgb2gray(image)
    # Convert image to uint8
    image = (image * 255).astype(np.uint8)
    # Flatten the image and reshape it into a 2D array with the original dimensions
    return np.reshape(image.flatten(), image.shape[:2])

def compare_images(image1, image2):
    # Convert images to float
    image1 = img_as_float(image1)
    image2 = img_as_float(image2)

    image2 = resize(image2, image1.shape)

    # Convert images to 2D byte arrays
    image1_2d = _get_2d_array(image1)
    image2_2d = _get_2d_array(image2)

    # Perform DWT on both images
    ll1, hl1, lh1, hh1 = dwt2d(image1_2d)
    ll2, hl2, lh2, hh2 = dwt2d(image2_2d)

    # Compute SSIM for each pair of corresponding coefficients
    ssim_ll = ssim(ll1, ll2)
    ssim_hl = ssim(hl1, hl2)
    ssim_lh = ssim(lh1, lh2)
    ssim_hh = ssim(hh1, hh2)

    # Return the average SSIM
    return (ssim_ll + ssim_hl + ssim_lh + ssim_hh) / 4

if __name__ == "__main__":
    # Load images
    image1 = io.imread('images/crop.jpg')
    image2 = io.imread('images/cropf.jpg')

    # Compare images
    ssim_index = compare_images(image1, image2)
    print(f"SSIM Index: {ssim_index}")