This Program downloads an image from the google drive using google APIs
and the applies make up on to it.

Changing the file name in the main function, can let the user change the 
input files and apply makeup on to it.

The Program used opencv to manipuulate the images and uses the dlib
shape predictor to get the right landmarks.

REQUIREMENTS:

DOWNLOAD THE SHAPE PREDICTOR FROM THE LINK and UNZIP it:
http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
and put it in with the rest of the files

0.
Remeber to close the image window only using key 'q'
Closing it using the mouse or any other thing wont let the image pop back up
again, until 30s, even if you run it again.

1.
For the google API to work the user needs to put in a credentials.json
in the same file as get_image.py 
credentials.json can be found at this link:
https://developers.google.com/drive/api/v3/quickstart/python

the click on enable API, enter a name and select 'Desktop'

Download the client config and put it in the maindirectory

2.
You need the following packages and libraries in python

(Note that some of these may need cmake and gcc to work preoperly)
pip install cmake
pip install gcc

pip install opencv-python
pip install dlib
pip install numpy
pip install oauth2client
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

Name: Dhaval Shrishrimal
Email: dhavalshrishrimal@gmail.com / drs4554@rit.edu
