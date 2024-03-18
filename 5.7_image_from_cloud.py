#This code is to retrive the base64 string stored in the image feed of AdafritIO and reconstruct it back as jpg image.
from Adafruit_IO import Client, RequestError, Feed
import base64 #import the base64 module to decode the base64 string to image

ADAFRUIT_IO_KEY = '' #Adafruit IO Key

ADAFRUIT_IO_USERNAME = '' #Adafruit IO Username

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

img_feed = aio.feeds('image') 

base64_img = aio.receive(img_feed.key)
base64_img = base64_img.value
base64_img_bytes = base64_img.encode('utf-8') #we first convert our Base64 string data into a bytes-like object that can be decoded. This means encoding the to UTF-8.

with open('decoded_image.jpg', 'wb') as file_to_save: #Using with context we create a new jpg file in write binary mode
    decoded_image_data = base64.decodebytes(base64_img_bytes) #We decode the bytes to an image
    file_to_save.write(decoded_image_data) #Save the image


