#Let us write a program to save the growth data to a csv file. Make sure to create a csv file in excel with the Columns "Date","Height_Ratio" and "Width_Ratio".
import cv2
import csv
from datetime import datetime

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

#The above lines of code are the same as the first method of growth analysis

date = datetime.now().strftime("%d %m %Y") #get the date in the day, month Year format


with open('growth_data.csv', 'a') as File: #We use the with context manager to append('a') to the file
    FileWriter = csv.writer(File) #csv writer object lets us write to csv file
    FileWriter.writerow([date,plant_height_ratio,plant_width_ratio]) #write the new row which contains date, height ratio and width ratio
