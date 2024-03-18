#In the next method we find the length of the leaf and stem
from plantcv import plantcv as pcv
from plantcv.plantcv import params
import cv2

#pcv.params.debug = "print" #We set debugging to "print" to display the image result after each function, the image will be present in the same folder as the program, default value is "None"

#There are lines displayed on the output image, the line_thickness sets the thickness of the line
params.line_thickness = 2

#The below lines of code are the same as the shape analysis program
img, path, filename = pcv.readimage(filename="Images/plant15.jpg")
s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')
s_thresh = pcv.threshold.binary(gray_img=s, threshold=51, max_value=255, object_type='light')

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

#We can perform the below 3 commands to remove holes within a plant, so that a leaf with a hole will only be detected as a single leaf 
mask = pcv.median_blur(mask, 5) #Applies a median blur filter, 5 is the kernel size, greater the kernel size higher the blur
mask = pcv.fill(mask, 200) #Identifies objects and fills objects that are less than specified size
mask = pcv.fill_holes(mask) #Cleans black holes, https://plantcv.readthedocs.io/en/stable/fill_holes/


#The following lines of code are explained in morphology_tutorial
#https://plantcv.readthedocs.io/en/stable/morphology_tutorial/

# Skeletonize the mask 
#Skeletonizing takes a binary object and reduces it to a 1 pixel wide representations 
    # Inputs:
    #   mask = Binary image data
skeleton = pcv.morphology.skeletonize(mask=mask) 

# Prune the skeleton  
#Generally, skeletonized images will have barbs, representing the width, that need to get pruned off. https://plantcv.readthedocs.io/en/stable/prune/
# Inputs:
    #   skel_img = Skeletonized image
    #   size     = Pieces of skeleton smaller than `size` should get removed. (Optional) Default `size=0`. 
    #   mask     = Binary mask for debugging (optional). If provided, debug images will be overlaid on the mask.
img1, seg_img, edge_objects = pcv.morphology.prune(skel_img=skeleton, size=10, mask=mask) 


# Identify branch points   
#The plantcv.morphology.find_branch_pts function returns a binary mask, where the white pixels are the branch points identified
    # Inputs:
    #   skel_img = Skeletonized image
    #   mask     = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.
branch_pts_mask = pcv.morphology.find_branch_pts(skel_img=skeleton, mask=mask) 

# Identify tip points   
#The plantcv.morphology.find_tips function also returns a binary mask of tip points identified
    # Inputs:
    #   skel_img = Skeletonized image
    #   mask     = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.
tip_pts_mask = pcv.morphology.find_tips(skel_img=skeleton, mask=None)

# Sort segments into leaf objects and stem objects  
#The plantcv.morphology.segment_sort function sorts pieces of the skeleton into leaf and "other". It returns the leaf objects separate from the stem objects, and their corresponding hierarchies. 

    # Inputs:
    #   skel_img  = Skeletonized image
    #   objects   = List of contours
    #   mask      = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.
leaf_obj, stem_obj = pcv.morphology.segment_sort(skel_img=skeleton,    
                                                 objects=edge_objects,
                                                 mask=mask)

# Identify leaf segments     
    # Inputs:
    #   skel_img  = Skeletonized image
    #   objects   = List of contours (leaf objects)
    #   mask      = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.
segmented_img, labeled_img = pcv.morphology.segment_id(skel_img=skeleton,
                                                       objects=leaf_obj,
                                                       mask=mask)

# Measure length of leaves   
    # Inputs:
    #   segmented_img = Segmented image to plot lengths on
    #   objects       = List of contours(leaf objects)
labeled_img  = pcv.morphology.segment_path_length(segmented_img=segmented_img, objects=leaf_obj)



# Instead of measuring the length of the leaves we can measure the the distance of the tip of the leaf from the stem, this is the euclidean length
#labeled_img = pcv.morphology.segment_euclidean_length(segmented_img=segmented_img, objects=leaf_obj)

#Display the identified leaves along with their length labeled
cv2.imshow('leaf', labeled_img)

#Print the length of each leaf in pixels
print(pcv.outputs.observations['segment_path_length']['value'])


# Identify stem segments     
    # Inputs:
    #   skel_img  = Skeletonized image
    #   objects   = List of contours (stem objects)
    #   mask      = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.
segmented_img, labeled_img = pcv.morphology.segment_id(skel_img=skeleton,
                                                       objects=stem_obj,
                                                       mask=mask)
# Measure length of the stem  
    # Inputs:
    #   segmented_img = Segmented image to plot lengths on
    #   objects       = List of contours(stem objects)
labeled_img  = pcv.morphology.segment_path_length(segmented_img=segmented_img, objects=stem_obj)

#Print the length of the stem in pixels
print(pcv.outputs.observations['segment_path_length']['value'])

#Display the identified stem along with their length labeled
cv2.imshow('stem', labeled_img)

#As done earlier we can find ratios to the pot 
