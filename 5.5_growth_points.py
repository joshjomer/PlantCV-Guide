#In this method we will plot landmark points on the plant and see how these points spread out as the plant grows
from plantcv import plantcv as pcv
from plantcv.plantcv import params
import cv2

#pcv.params.debug = "print" #We set debugging to "print" to display the image result after each function, the images will be present in the same folder as the program, default value is "None"
#Since there are many functions in this program there will be many output images

params.line_thickness = 2
img, path, filename = pcv.readimage(filename="Images/potato3Nov2020.jpg")
s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')
s_thresh = pcv.threshold.binary(gray_img=s, threshold=75, max_value=255, object_type='light')
masked = pcv.apply_mask(img=img, mask=s_thresh, mask_color='white')
id_objects, obj_hierarchy = pcv.find_objects(img=masked, mask=s_thresh)
rplant = cv2.selectROI(img)
roi1, roi_hierarchy= pcv.roi.rectangle(img=masked, x=rplant[0], y=rplant[1], h=rplant[3], w=rplant[2])
roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img=img, roi_contour=roi1, 
                                                               roi_hierarchy=roi_hierarchy, 
                                                               object_contour=id_objects, 
                                                               obj_hierarchy=obj_hierarchy,
                                                               roi_type='partial')
obj, mask = pcv.object_composition(img=img, contours=roi_objects, hierarchy=hierarchy3)
#The above lines of code are similar to the previous methods

cv2.imshow('img',mask)#The plant mask is displayed so that we can see if the plant has been acurately isolated



#To see the result of one method we can turn debugging to "print" and then set it back None
pcv.params.debug = "print"
#top, bottom, center_v  = pcv.x_axis_pseudolandmarks(img, obj, mask) #Divide plant object into twenty equidistant bins along the x-axis https://plantcv.readthedocs.io/en/stable/x_axis_pseudolandmarks/
left, right, center_h  = pcv.y_axis_pseudolandmarks(img, obj, mask) #Divide plant object into twenty equidistant bins along the y-axis https://plantcv.readthedocs.io/en/stable/y_axis_pseudolandmarks/
pcv.params.debug = None

landmarks = left + right + center_h #We consider all the landmark points along the y axis

rpot = cv2.selectROI(img) #Draw a bounding box around the pot
boundary_image = pcv.analyze_bound_horizontal(img, obj, mask, rpot[1]) #Set boundary line with boundary tool, this allows the user to find the extent-y ('height') above the pot https://plantcv.readthedocs.io/en/stable/analyze_bound_horizontal/
#cv2.imshow('img',boundary_image)

                                                                                              #A vertical coordinate (int) that denotes the height of the plant pot
points_rescaled, centroid_rescaled, base_rescaled = pcv.scale_features(obj, mask, landmarks, rpot[1]) #This is a function to to transform the coordiantes of landmark points onto a common scale (0-1.0) Scaling is used to remove the influence of size on shape parameters. https://plantcv.readthedocs.io/en/stable/scale_features/ 

pcv.landmark_reference_pt_dist(points_rescaled, centroid_rescaled, base_rescaled) #This is a function to measure the distance from user defined points to the centroid and a point defined by the centroid coordinate along the x-axis and baseline coordinate (top of pot) along the y-axis. https://plantcv.readthedocs.io/en/stable/landmark_reference_pt_dist/#landmark_reference_pt_dist

#The result of the above method gives us the average euclidean, vertical and horizontal distances of all the landmark points
avg_euc_c_distance = pcv.outputs.observations['euc_ave_c']['value']
print("average euclidean distance from centroid: ",avg_euc_c_distance)
avg_euc_b_distance = pcv.outputs.observations['euc_ave_b']['value']
print("average euclidean distance from pot base: ",avg_euc_b_distance)

avg_vert_c_distance = pcv.outputs.observations['vert_ave_c']['value']
print("average vertical distance from centroid: ",avg_vert_c_distance)
avg_vert_b_distance = pcv.outputs.observations['vert_ave_b']['value']
print("average vertical distance from pot base: ",avg_vert_b_distance)

avg_hori_c_distance = pcv.outputs.observations['hori_ave_c']['value']
print("average horizontal distance: ",avg_hori_c_distance)


