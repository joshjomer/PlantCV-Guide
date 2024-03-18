#Identifying a plant from the camera
import requests
import json
import cv2

video_capture = cv2.VideoCapture(0) #Create a video capture object in opencv.There might be multiple webcam attached, 0 selects the first one 

#By default opencv  uses a lower resolution for the camera, so we manually provide a higher resolution
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True: #run the loop continously to access frames from the webcam
    ret, frame = video_capture.read() #getting a single frame(an image) from the video

    cv2.imshow('Video',frame) #show the frame in a new window, the name of the window is Video

    if cv2.waitKey(1) == ord('q'): #the last frame before exiting will be used for detection
        break

video_capture.release()  #Release the camera
cv2.destroyAllWindows() #Close the new window that was opened

#The selectROI method allows us to crop a specific part of an Image(which contains text), this is done by drawing rectangle with the mouse. Once completed we can press enter
r = cv2.selectROI(frame) #r conatins the x,y,width and height of the cropped rectangle

#We crop the tplant image with the cropped rectangle x,y,width and height values
#r[0] is the cropped rectangle x value, r[2] is the width, r[1] is the y value and r[3] is the height
imgCrop = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

cv2.imshow('CroppedImg',imgCrop) #display the cropped image 

cv2.imwrite('Images/planttest.jpg',imgCrop) #Save the image

url = 'https://my-api.plantnet.org/v2/identify/all?'
api_key = 'api-key=  '
data = {'organs':'leaf'}
imagefile = open('Images/planttest.jpg','rb')

files = {'images':imagefile}

result = requests.post(url+api_key, data=data, files=files)

data = result.json()

print("\n\nOnly the plant with the higest score")
print("Score: ",data['results'][0]['score'])
print('Scientific name: ',data['results'][0]['species']['scientificNameWithoutAuthor'])
print('Common names: ',data['results'][0]['species']['commonNames'])
