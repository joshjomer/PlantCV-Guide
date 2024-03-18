#We perform shape analysis on a plant to find its dimension
from plantcv import plantcv as pcv
from plantcv.plantcv import params
import cv2

#pcv.params.debug = "print" #We set debugging to "print" to display the image result after each function, the image will be present in the same folder as the program, default value is "None"


img, path, filename = pcv.readimage(filename="Images/potato17Oct2020.jpg")
s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')
s_thresh = pcv.threshold.binary(gray_img=s, threshold=50, max_value=255, object_type='light')

# Apply Mask (for VIS(RGB,HSV) images, mask_color=white)
# Inputs:
#   rgb_img - RGB image data 
#   mask - Binary mask image data 
#   mask_color - 'white' or 'black' 
masked = pcv.apply_mask(img=img, mask=s_thresh, mask_color='white')
cv2.imshow('1 masked',masked)

# Identify objects(contours)
id_objects, obj_hierarchy = pcv.find_objects(img=masked, mask=s_thresh)

#Draw a bounding box around the plant area
r = cv2.selectROI(img)

 # Define ROI
    # Inputs: 
    #   img - RGB or grayscale image to plot the ROI on 
    #   x - The x-coordinate of the upper left corner of the rectangle 
    #   y - The y-coordinate of the upper left corner of the rectangle 
    #   h - The height of the rectangle 
    #   w - The width of the rectangle 
roi1, roi_hierarchy= pcv.roi.rectangle(img=masked, x=r[0], y=r[1], h=r[3], w=r[2])


#Once the region of interest is defined you can decide to keep everything overlapping with the region of interest or cut the objects to the shape of the region of interest.
 # Decide which objects to keep
    # Inputs:
    #    img            = img to display kept objects
    #    roi_contour    = contour of roi, output from any ROI function
    #    roi_hierarchy  = contour of roi, output from any ROI function
    #    object_contour = contours of objects, output from pcv.find_objects function
    #    obj_hierarchy  = hierarchy of objects, output from pcv.find_objects function
    #    roi_type       = 'partial' (default, for partially inside), 'cutto', or 
    #    'largest' (keep only largest contour)
roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img=img, roi_contour=roi1, 
                                                               roi_hierarchy=roi_hierarchy, 
                                                               object_contour=id_objects, 
                                                               obj_hierarchy=obj_hierarchy,
                                                               roi_type='partial')

cv2.imshow('2 kept mask',kept_mask)

#The isolated objects now should all be plant material. There can be more than one object that makes up a plant since sometimes leaves twist making them appear in images as separate objects. Therefore, in order for shape analysis to perform properly the plant objects need to be combined into one object using the combine objects function.
# Object combine kept objects
    # Inputs:
    #   img - RGB or grayscale image data for plotting 
    #   contours - Contour list 
    #   hierarchy - Contour hierarchy array 
obj, mask = pcv.object_composition(img=img, contours=roi_objects, hierarchy=hierarchy3)
cv2.imshow("3 mask",mask)

# Find shape properties, output shape image
    # Inputs:
    #   img - RGB or grayscale image data 
    #   obj- Single or grouped contour object
    #   mask - Binary image mask to use as mask for moments analysis
analysis_image = pcv.analyze_object(img=img, obj=obj, mask=mask)

#Display the analysed image
cv2.imshow('4 analysis img',analysis_image)
# Access data stored out from analyze_object method
#the outputs of methods gets automatically stored in the outputs observation class and they can be accessed by passing the right arguments
#Take a look at https://plantcv.readthedocs.io/en/stable/analyze_shape/ output section for all possible outputs
print("Height: ",pcv.outputs.observations['height']['value'])
print("Width: ",pcv.outputs.observations['width']['value'])
print("Plant Area: ",pcv.outputs.observations['area']['value'])
print("Hull Area: ",pcv.outputs.observations['convex_hull_area']['value'])

