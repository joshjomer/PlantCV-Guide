#We seperate colours in the HSV colour space. This program lets us find the threshold value to seperate green plants from the backgaround
from plantcv import plantcv as pcv
import cv2

img, path, filename = pcv.readimage(filename="Images/potato3Nov2020.jpg") #Open the image using plantcv
s = pcv.rgb2gray_hsv(rgb_img=img, channel='s') #convert the rgb imge to HSV and only select the saturation channel(this returns a grayscale image of the saturation channel), the saturation channel is selected as it helps us spererate colours such as green easier. But Hue 'h' and value 'v' can also be selected.

def nothing(x): #We need an empty function to pass as an argument for the trackbar. This function is called when the slider value changes, this functionality can be useful but not required for us
    pass

cv2.namedWindow('Slider Window') #Create a new window for the slider

cv2.createTrackbar('Sat','Slider Window',0,255, nothing) #Create slider


while True:
    sat = cv2.getTrackbarPos('Sat', 'Slider Window') #get the trackbar value

    # Threshold the saturation image

    # Inputs:
    #   gray_img - Grayscale image data 
    #   threshold- Threshold value (between 0-255)
    #   max_value - Value to apply above threshold (255 = white) 
    #   object_type - 'light' (default) or 'dark'. If the object is lighter than the 
    #                 background then standard threshold is done. If the object is 
    #                 darker than the background then inverse thresholding is done. 
    s_thresh = pcv.threshold.binary(gray_img=s, threshold=sat, max_value=255, object_type='light')

    cv2.imshow('img',s_thresh) #show the thresholded image
    
    if cv2.waitKey(1) == ord('q'): #exit the program by pressing 'q
        break

cv2.destroyAllWindows() #close all the opened windows after exiting the loop
