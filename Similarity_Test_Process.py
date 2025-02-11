from ID_MSE import compare_images as compare_id_mse
from ED_IOU import compare_images as compare_ed_iou
from DWT_SSIM import compare_images as compare_dwt_ssim
from CWT_SSIM import compare_images as compare_cwt_ssim

def compare_images(image1, image2):
    id_mse = compare_id_mse(image1, image2) * 100
    ed_iou = compare_ed_iou(image1, image2) * 100
    dwt_ssim = compare_dwt_ssim(image1, image2) * 100
    cwt_ssim = compare_cwt_ssim(image1, image2) * 100

    ID_MSE_Threshold = 80
    ED_IOU_Threshold = 80
    DWT_SSIM_Threshold = 80
    CWT_SSIM_Threshold = 80

    similarities = [id_mse, ed_iou, dwt_ssim, cwt_ssim]
    thresholds = [ID_MSE_Threshold, ED_IOU_Threshold, DWT_SSIM_Threshold, CWT_SSIM_Threshold]
    change_keys = [id_mse < ID_MSE_Threshold, ed_iou < ED_IOU_Threshold, dwt_ssim < DWT_SSIM_Threshold, cwt_ssim < CWT_SSIM_Threshold]

    return similarities, thresholds, change_keys