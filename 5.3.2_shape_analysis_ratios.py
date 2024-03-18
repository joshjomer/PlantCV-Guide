#We perform shape analysis on the plant and find its ratio with respect to the plant pot similar to the previous program.
from plantcv import plantcv as pcv
from plantcv.plantcv import params
import cv2

params.line_thickness = 2
img, path, filename = pcv.readimage(filename="Images/potato17Oct2020.jpg")
s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')
s_thresh = pcv.threshold.binary(gray_img=s, threshold=81, max_value=255, object_type='light')
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
analysis_image = pcv.analyze_object(img=img, obj=obj, mask=mask)

plantheight = pcv.outputs.observations['height']['value']
plantwidth = pcv.outputs.observations['width']['value']
cv2.imshow('img',mask)

print("Plant Height: ",plantheight)
print("Plant Width: ",plantwidth)

#Finding the pot dimension using region of interest similar to the previously done program
rpot = cv2.selectROI(img)
potheight = rpot[3]
potwidth = rpot[2]

print("Pot Height: ",potheight)
print("Pot Width: ",potwidth)

print("\nHeight Ratio: ",plantheight/potheight)
print("Width Ratio: ",plantwidth/potwidth)

#Printing the plant height and width in cm (this might not be very accurate) after finding the ratio similar to the previously done program
potheightcm = 18
potwidthcm = 21

plant_height_cm = potheightcm*(plantheight/potheight)
plant_width_cm = potwidthcm*(plantwidth/potwidth)
print("Plant height: {} cm \nPlant width: {} cm".format(plant_height_cm,plant_width_cm))
