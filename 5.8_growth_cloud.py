#We first retrive the image from adafruitIO, then we perform landmark points growth analysis and finally we upload the result to adafruitio. The growth result data can be plotted in a graph block
from Adafruit_IO import Client, RequestError, Feed
import base64
from plantcv import plantcv as pcv
from plantcv.plantcv import params
import cv2

ADAFRUIT_IO_KEY = '' #Adafruit IO Key

ADAFRUIT_IO_USERNAME = '' #Adafruit IO username

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

#Feed objects
img_feed = aio.feeds('image')
avgh_feed = aio.feeds('avgh-dist') #New feeds were created for averge vertical and horizontal distances
avgv_feed = aio.feeds('avgv-dist')


#Retriving the base64string and decoding it back to an image                      
base64_img = aio.receive(img_feed.key)
base64_img = base64_img.value
base64_img_bytes = base64_img.encode('utf-8')

with open('decoded_image.jpg', 'wb') as file_to_save:
    decoded_image_data = base64.decodebytes(base64_img_bytes)
    file_to_save.write(decoded_image_data)


#Perform land mark points analysis
params.line_thickness = 2
img, path, filename = pcv.readimage(filename="decoded_image.jpg")
s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')
s_thresh = pcv.threshold.binary(gray_img=s, threshold=69, max_value=255, object_type='light')
masked = pcv.apply_mask(img=img, mask=s_thresh, mask_color='white')
id_objects, obj_hierarchy = pcv.find_objects(img=masked, mask=s_thresh)
r = cv2.selectROI(img)
roi1, roi_hierarchy= pcv.roi.rectangle(img=masked, x=r[0], y=r[1], h=r[3], w=r[2])
roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img=img, roi_contour=roi1, 
                                                               roi_hierarchy=roi_hierarchy, 
                                                               object_contour=id_objects, 
                                                               obj_hierarchy=obj_hierarchy,
                                                               roi_type='partial')
obj, mask = pcv.object_composition(img=img, contours=roi_objects, hierarchy=hierarchy3)
cv2.imshow('img',mask)
#top, bottom, center_v  = pcv.x_axis_pseudolandmarks(img, obj, mask)

#pcv.params.debug = "print"
left, right, center_h  = pcv.y_axis_pseudolandmarks(img, obj, mask)
#pcv.params.debug = None

landmarks = left + right + center_h 

r = cv2.selectROI(img)
boundary_image = pcv.analyze_bound_horizontal(img, obj, mask, r[1])
#cv2.imshow('img',boundary_image)

points_rescaled, centroid_rescaled, base_rescaled = pcv.scale_features(obj, mask, landmarks, r[1])
pcv.landmark_reference_pt_dist(points_rescaled, centroid_rescaled, base_rescaled)

avg_vert_distance = pcv.outputs.observations['vert_ave_c']['value']
print("average vertical distance: ",avg_vert_distance)
avg_hor_distance = pcv.outputs.observations['hori_ave_c']['value']
print("average horizontal distance: ",avg_hor_distance)


#Ask the user if they want to publish the growth data to AdafruitIO
response = input("Do you want to publish these values to the cloud? (y/n)")

#Publish growth data
if response == 'y':
       aio.send_data(avgv_feed.key, avg_vert_distance)
       aio.send_data(avgh_feed.key, avg_hor_distance)

