"""
Name: Dhaval Shrishrimal
Description: This file holds all the functions required for 
applying make onto the image passed in
File : 'makeup.py'
"""

import numpy as np
import cv2

# colors of all the different makeup elements
LIPSTICK = (32, 0, 128)
LINER = (1, 1, 1)
SHADOW = (255, 0, 0)
BLUSH = (128, 0, 128)

def lips(img, landmarks):
    """
    This function takes the image and the landmarks file and applies
    lipstick to it
    @param img: the image passed in
    @param landmarks: the list of all the dlib face points
    @return img: the picture with lipstick applied
    """
    mask = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    outer = landmarks[48:60]    # outer edge of the lips
    inner = landmarks[60:68]    # inner edge of the lips
    # fill the outer edges with white and then the inner edges with black
    mask = cv2.fillPoly(mask, np.array([outer]), (255, 255, 255))
    mask = cv2.fillPoly(mask, np.array([inner]), (0, 0, 0))
    color_mask = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    color_mask[:] = LIPSTICK
    # add the masks together for the right color
    mask = cv2.bitwise_and(mask, color_mask)
    mask = cv2.GaussianBlur(mask, (11, 11), 10)
    # add the mask to the image
    img = cv2.addWeighted(img, 1, mask, 0.6, 0)
    return img

def eye_liner_loop(mask, eye, brow, kernel, isleft, thick):
    """
    This function loops over the upper edge of the eye to apply eyeliner
    @param mask: the empty mask image
    @param eye: list of points in the upper edge of eye
    @param brow: the outer coroner of the brow
    @param kernel: the kernel used by the erode func
    @param isLeft: is this the lefy eye?
    @param thick: the starting thickenss.
    @return mask: return the mask of eye liner image
    """
    i = int(mask.shape[1]/100)
    for idx in range(len(eye) - 1):
        start = tuple([eye[idx][0], eye[idx][1]-i])
        end = tuple([eye[idx+1][0], eye[idx+1][1] - i])
        # draw a line around the 
        cv2.line(mask, start, end, (255, 255, 255), thick)
        if isleft: thick-=1
        else: thick+=1
    # erode to make the edges look sharper
    mask = cv2.erode(mask, kernel, iterations=1)
    return mask

def eye_liner(img, landmarks):
    """
    This function applies eye liner on the the img on both eyes
    @param img: the image passed in
    @param landmarks: list of all the landmarks
    @return img: image with eyeliner applied
    """
    kernel = np.ones((5,5), np.uint8)
    # create black mask images
    mask_left = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    mask_right = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    # update the mask with eye liner areas
    mask_left = eye_liner_loop(mask_left, landmarks[36:40], landmarks[17], kernel, True, 10)
    mask_right = eye_liner_loop(mask_right, landmarks[42:46], landmarks[26], kernel, False, 8)
    # combine the masks together
    mask = cv2.bitwise_or(mask_left, mask_right)
    color_mask = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    color_mask[:] = (0,0,0)
    valMask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    valMask = cv2.bitwise_not(valMask)
    mask = cv2.GaussianBlur(mask, (5, 5), 1)
    # add the images together
    img = cv2.bitwise_xor(img, color_mask, mask=valMask)
    return img

def shadow_loop(mask, eye, brow, start, stop, step):
    """
    This fucntion returns the mask required by the eye shadow
    @param mask: the black mask image
    @param eye: list of all the points in eye_upper
    @param brow: list of all the points in brow
    @param start: where to start looping
    @param end: where to stop looping
    @param step: go forward or backward
    @return mask: the updated mask image
    """
    thick = 15
    # loop from start to stop
    for i in range(start, stop, step):
        # calc the points 1/3 way between eye and brows
        xdist = abs((eye[i][0] - brow[i][0]) // 3)
        ydist = abs((eye[i][1] - brow[i][1]) // 3)
        xdistnext = abs((eye[i+step][0] - brow[i+step][0]) // 3)
        ydistnext = abs((eye[i+step][1] - brow[i+step][1]) // 3)
        start = tuple([ -xdist + eye[i][0], -ydist + eye[i][1]])
        end = tuple([ -xdistnext+ eye[i+step][0], -ydistnext +eye[i+step][1] ])
        # draw a line through those points
        cv2.line(mask, start, end, (255, 255, 255), thick)
        thick-=2
    if step == 1: idx = -1
    else: idx = 0
    # draw the final line near the nose
    xdistnext = abs(eye[idx][0] - brow[idx][0]) // 2
    ydistnext = abs(eye[idx][1] - brow[idx][1]) // 2
    cv2.line(mask, end, (-xdistnext + eye[-1][0], -ydistnext + eye[-1][1]), (255, 255, 255), thick)
    return mask

def eye_shadow(img, landmarks):
    """
    This function applied eye shadow to both the eyes in the image passed in
    @param img: the image passed in
    @param landmarks: the list of the landmarks file
    @return img: the image with applied eye shadow
    """
    arr_len = len(landmarks[36:40]) - 1 
    # make the mask for left eye
    mask_left = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    mask_left = shadow_loop(mask_left, landmarks[36:40], landmarks[17:22], 0, arr_len, 1)
    # make the mask for right eys
    mask_right = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    mask_right = shadow_loop(mask_right, landmarks[42:46], landmarks[22:27], arr_len, 0 ,-1)
    # combine the masks together
    mask = cv2.bitwise_or(mask_left, mask_right)
    color_mask = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    color_mask[:] = SHADOW
    # Blurr to make it look realistic
    mask = cv2.GaussianBlur(mask, (11, 11), 3)
    mask = cv2.bitwise_and(mask, color_mask)
    img = cv2.addWeighted(img, 1, mask, 0.6, 0)
    return img

def perp(a):
    """
    This is a helper function used by find_intersect
    """
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

def find_intersect(a1,a2, b1,b2) :
    """
    Finds the intersection between the lines (a1, a2) and (b1,b2)
    """
    da = np.array(a2)-np.array(a1)
    db = np.array(b2)-np.array(b1)
    dp = np.array(a1)-np.array(b1)
    dap = perp(da)
    denom = np.dot( dap, db)
    num = np.dot( dap, dp )
    ans = (num / denom.astype(float))*db + b1
    return [int(ans[0]), int(ans[1])]

def get_area_left_blush(cheek, nose, edge, eye, mask):
    """
    Create the mask for the left cheek
    @param cheek: the points on the cheek
    @param nose: the points on the nose
    @param edge: outer edge of the nose
    @param eye: inner edge of the eye
    @param mask: the black mask image
    @return mask: the updated mask image
    """
    # get the edge points near nose area
    upper_bound = find_intersect(cheek[0], nose[0], edge, eye)
    lower_bound = find_intersect(cheek[4], nose[0], edge, eye)
    offy = abs(cheek[0][1] - cheek[-1][1]) // 4
    offx = abs(cheek[0][0] - upper_bound[0]) // 4 
    new = list()
    # add all the points to the list, while reducing the area of the polygon formed
    new.append([cheek[0][0] + offx, cheek[0][1] + offy])
    new.append([cheek[-1][0] + offx, cheek[-1][1] - offy])
    new.append([lower_bound[0] - offx//2, lower_bound[1]-offy//2])
    new.append([upper_bound[0] -offx//2, upper_bound[1]+offy//2])
    # fill the polygon
    mask = cv2.fillPoly(mask, np.array([new]), (255, 255, 255))
    return mask

def left_blush(img, landmarks):
    """
    This function takes in the image and the landmarks points and applies blush on the
    left side.
    @param img: the image passed in
    @param landmarks: the list of the landmarks on the face
    @return img: the image file with left blush applied
    """
    # create the mask
    mask_left = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    mask_left = get_area_left_blush(landmarks[0:5], landmarks[28:30], \
        landmarks[31], landmarks[39], mask_left)
    # restruct the mask
    dilatation_size = 15
    dilatation_type = cv2.MORPH_CROSS
    element = cv2.getStructuringElement(dilatation_type,(2*dilatation_size + 1, \
        2*dilatation_size+1),(dilatation_size, dilatation_size))
    # dilate the mask
    mask_left = cv2.dilate(mask_left, element)
    color_mask = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    color_mask[:] = BLUSH
    mask = mask_left.copy()
    # blurr the mask for realism
    mask = cv2.GaussianBlur(mask, (11, 11), 5)
    mask = cv2.bitwise_and(mask, color_mask)
    mask = cv2.blur(mask, (81, 81))
    img = cv2.addWeighted(img, 1, mask, 0.6, 0)
    return img

def get_area_right_blush(cheek, nose, edge, eye, mask):
    """
    Create the mask for the right cheek
    @param cheek: the points on the cheek
    @param nose: the points on the nose
    @param edge: outer edge of the nose
    @param eye: inner edge of the eye
    @param mask: the black mask image
    @return mask: the updated mask image
    """
    # get the edge points near nose area
    upper_bound = find_intersect(cheek[-1], nose[0], edge, eye)
    lower_bound = find_intersect(cheek[0], nose[0], edge, eye)
    offy = abs(cheek[-1][1] - cheek[0][1]) // 4
    offx = abs(cheek[-1][0] - upper_bound[0]) // 4 
    new = list()
    # add all the points to the list, while reducing the area of the polygon formed
    new.append([cheek[-1][0] - offx, cheek[-1][1] + offy])
    new.append([cheek[0][0] - offx, cheek[0][1] - offy])
    new.append([lower_bound[0] + offx//2, lower_bound[1] - offy//2])
    new.append([upper_bound[0] + offx//2, upper_bound[1] + offy//2])
    # fill the polygon
    mask = cv2.fillPoly(mask, np.array([new]), (255, 255, 255))
    return mask

def right_blush(img, landmarks):
    """
    This function takes in the image and the landmarks points and applies blush on the
    right side.
    @param img: the image passed in
    @param landmarks: the list of the landmarks on the face
    @return img: the image file with left blush applied
    """
    # create the mask
    mask_right = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    mask_right = get_area_right_blush(landmarks[12:17], landmarks[28:30], \
        landmarks[35], landmarks[42], mask_right)
    # restruct the mask
    dilatation_size = 15
    dilatation_type = cv2.MORPH_CROSS
    element = cv2.getStructuringElement(dilatation_type,(2*dilatation_size + 1, \
        2*dilatation_size+1),(dilatation_size, dilatation_size))
    # dilate the mask
    mask_right = cv2.dilate(mask_right, element)
    color_mask = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    color_mask[:] = BLUSH
    mask = mask_right.copy()
    # blurr the mask for realism
    mask = cv2.GaussianBlur(mask, (11, 11), 5)
    mask = cv2.bitwise_and(mask, color_mask)
    mask = cv2.blur(mask, (81, 81))
    img = cv2.addWeighted(img, 1, mask, 0.6, 0)
    return img