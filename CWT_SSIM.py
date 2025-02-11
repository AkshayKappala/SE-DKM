import numpy as np
from skimage import io, img_as_float, color, transform as sk_transform
from skimage.metrics import structural_similarity as ssim
from dtcwt.numpy import Transform2d

def _get_2d_array(image):
    # Convert image to float
    image = img_as_float(image)
    # Convert image to grayscale if it has more than 2 dimensions
    if image.ndim == 3:
        image = color.rgb2gray(image)
    # Convert image to uint8
    image = (image * 255).astype(np.uint8)
    # Flatten the image and reshape it into a 2D array with the original dimensions
    return np.reshape(image.flatten(), image.shape[:2])

def compare_images(image1, image2):
    # Resize images to the same dimensions
    image2 = sk_transform.resize(image2, image1.shape)

    # Convert images to 2D byte arrays
    image1_2d = _get_2d_array(image1)
    image2_2d = _get_2d_array(image2)

    # Perform CWT on both images
    cwt_transform = Transform2d()
    cwt1 = cwt_transform.forward(image1_2d)
    cwt2 = cwt_transform.forward(image2_2d)

    # Compute SSIM 
    ssim_index, _ = ssim(cwt1.lowpass, cwt2.lowpass, data_range=cwt1.lowpass.max() - cwt1.lowpass.min(), full=True)
    return ssim_index

if __name__ == "__main__":
    # Load images
    image1 = io.imread('images/cropl.jpg')
    image2 = io.imread('images/cropr.jpg')

    # Compare images
    ssim_index = compare_images(image1, image2)
    print(f"SSIM Index: {ssim_index}")