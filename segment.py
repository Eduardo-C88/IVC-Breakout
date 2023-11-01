import cv2
import numpy as np

def update_segmentation(image_hsv):
    if hmin < hmax:
        ret, mask_hmin = cv2.threshold(src=image_hsv[:, :, 0], thresh=hmin,
                                       maxval=1, type=cv2.THRESH_BINARY)
        ret, mask_hmax = cv2.threshold(src=image_hsv[:, :, 0], thresh=hmax,
                                       maxval=1, type=cv2.THRESH_BINARY_INV)
        mask_h = mask_hmin * mask_hmax
    else:
        ret, mask_hmin = cv2.threshold(src=image_hsv[ :, :, 0], thresh=hmin,
                                       maxval=1, type=cv2.THRESH_BINARY_INV)
        ret, mask_hmax = cv2.threshold(src=image_hsv[:, :, 0], thresh=hmax,
                                       maxval=1, type=cv2.THRESH_BINARY)

        mask_h = cv2.bitwise_or(mask_hmin, mask_hmax)

    ret, mask_smin = cv2.threshold(src=image_hsv[ :, :, 1], thresh=smin,
                maxval=1, type=cv2.THRESH_BINARY)
    ret, mask_smax = cv2.threshold(src=image_hsv[ :, :, 1], thresh=smax,
                maxval=1, type=cv2.THRESH_BINARY_INV)
    mask_s = mask_smin * mask_smax

    ret, mask_vmin = cv2.threshold(src=image_hsv[ :, :, 2], thresh=vmin,
                maxval=1, type=cv2.THRESH_BINARY)
    ret, mask_vmax = cv2.threshold(src=image_hsv[ :, :, 2], thresh=vmax,
                maxval=1, type=cv2.THRESH_BINARY_INV)
    mask_v = mask_vmin * mask_vmax

    mask = mask_h * mask_s * mask_v

    kernel = np.ones((5, 5), np.uint8)

    mask_close = cv2.dilate(src=mask, kernel=kernel, iterations=1)
    mask_close = cv2.erode(src=mask_close, kernel=kernel, iterations=1)

    cv2.imshow("Mask Closed", mask_close * 255)
    return mask

def create_trackbar():
    hmin = 65
    hmax = 90
    smin = 79
    smax = 255
    vmin = 54
    vmax = 214

    def on_change_hmin(val):
        global hmin
        hmin = val

    def on_change_hmax(val):
        global hmax
        hmax = val

    def on_change_smin(val):
        global smin
        smin = val

    def on_change_smax(val):
        global smax
        smax = val

    def on_change_vmin(val):
        global vmin
        vmin = val

    def on_change_vmax(val):
        global vmax
        vmax = val

    cv2.namedWindow("Image")
    cv2.createTrackbar("Hmin", "Image", hmin, 180, on_change_hmin)
    cv2.createTrackbar("Hmax", "Image", hmax, 180, on_change_hmax)
    cv2.createTrackbar("Smin", "Image", smin, 255, on_change_smin)
    cv2.createTrackbar("Smax", "Image", smax, 255, on_change_smax)
    cv2.createTrackbar("Vmin", "Image", vmin, 255, on_change_vmin)
    cv2.createTrackbar("Vmax", "Image", vmax, 255, on_change_vmax)

def find_countour_direction(mask, image_width):
    contours, hierarchy = cv2.findContours(image=mask,
                                           mode=cv2.RETR_TREE,
                                           method=cv2.CHAIN_APPROX_NONE)

    # If there is more than one contour, choose the biggest to follow
    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)

        # Get the center of the contour
        M = cv2.moments(largest_contour)
        if M['m00'] != 0:
            Cx = int(np.round(M['m10'] / M['m00']))

            # Calculate the position relative to the image width
            position = Cx / image_width

            # Determine the direction based on position
            if position < 1 / 3:
                return -1  # Contour is closer to 1/3
            elif position > 2 / 3:
                return 1  # Contour is closer to 2/3
    return None

"""" Tracking  """
def find_countour_center(mask):
    contours, hierarchy = cv2.findContours(image=mask,
                                           mode=cv2.RETR_TREE,
                                           method=cv2.CHAIN_APPROX_NONE)

    # If there is more than one contour, choose the biggest to follow
    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)

        # Get the center of the contour
        M = cv2.moments(largest_contour)
        if M['m00'] != 0:
            Cx = int(np.round(M['m10'] / M['m00']))
            Cy = int(np.round(M['m01'] / M['m00']))
            return Cx, Cy
    return None