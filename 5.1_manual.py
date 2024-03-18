#We estimate the plant growth by drawing bounding boxes around the plant and pot. We find the length and breadth ratios of both the bounding boxes. These ratios will vary as the plant grows bigger and its bounding box also has to get bigger.
#Instead of findind the ratios to the pot we can also find the ratio to a sticker which can be stuck to the pot
#The purpose for finding ratios to a standard object(pot/sticker) is that some photos taken might be more zoomed in or out, to account for this we divide plant lengths by pot lengths
import cv2

img = cv2.imread('Images/potato17Oct2020.jpg') #Open the image of the plant

rplant = cv2.selectROI(img) #draw the bounding box around the plant such that the height of the box stretches from the base to the top of the plant. The width of box should be from the leftmost to rightmost point of the plant.

plantheight = rplant[3] 
plantwidth = rplant[2]

rpot = cv2.selectROI(img) #draw the bounding box around the pot

potheight = rpot[3]
potwidth = rpot[2]

plant_height_ratio = (plantheight/potheight) #compute the ratios
plant_width_ratio = (plantwidth/potwidth)

print("Plant height ratio: {}  \nPlant width ratio: {} ".format(plant_height_ratio,plant_width_ratio))


#Based on the calculated ratios and pot dimensions we can calculate the plant heigh and width. This might not be very accurate, to improve accuracy all the photos have to be taken parallel to the plant.
potheightcm = 18
potwidthcm = 21

plant_height_cm = potheightcm*(plantheight/potheight)
plant_width_cm = potwidthcm*(plantwidth/potwidth)

print("Plant height: {} cm \nPlant width: {} cm".format(plant_height_cm,plant_width_cm))


