"""
Name: Dhaval Shrishrimal
Description: This is the main file for the progam, It downloads the Nick Cage image
from the google drive using get_image and the applies make up using file makeup
File: 'main.py'
"""

from get_image import *
from makeup import lips, eye_liner, eye_shadow, left_blush, right_blush
import dlib
import cv2

def make_up(img):
    """
    call the functions in the make up file to apply it to different parts of the img
    @param img: the image passed in
    @return img: the image with makeup applied on it
    """
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    # get the coordinates of the face
    face = detector(img)[0]
    landmarks_raw = predictor(img, face)
    landmarks = list()
    # create a regular list of all the landmark points
    for i in range(68):
        landmarks.append([landmarks_raw.part(i).x, landmarks_raw.part(i).y])
    # apply makeup to different parts of the face
    img = lips(img, landmarks)
    img = eye_shadow(img, landmarks)
    img = eye_liner(img, landmarks)
    img = left_blush(img, landmarks)
    img = right_blush(img, landmarks)
    return img

def main():
    """
    This is the main entry point of the program
    """
    fileId = '1ALXmFWrnaV7vhCDMPW2N4sPudTsqpjr-'
    filename = 'nick_img.jpg'
    service = build_service()
    download_nick(service, fileId, filename)
    org = cv2.imread(filename)
    img = org.copy()
    img = make_up(img)
    cv2.imshow("NICK CAGE", img)
    cv2.waitKey(0)
    if 0xFF == 'q':
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
