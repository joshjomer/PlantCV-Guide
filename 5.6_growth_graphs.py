#We can plot the points from the csv file using the module matplotlib
import matplotlib.pyplot as plt #matplotlib is used to plot graphs
import pandas as pd #pandas is used to handle csv files

growth_data = pd.read_csv("growth_data.csv") #Read the csv file

#Lets plot two plots on the same graph
plt.subplot(1,3,1) #specify the subplot positions 1 row, 3 columns and ploting at the 1st position
plt.plot(growth_data["Date"],growth_data["Height_Ratio"],label='height ratio') #plot the date in the x axis and height ratio in the y axis with the label 'height ratio'
plt.plot(growth_data["Date"],growth_data["Width_Ratio"],label='width ratio') #plot the date in the x axis and width ratio in the y axis with the label 'width ratio'
plt.title("Average Ratios") #give a title
plt.legend()#since we have two plots on the same graph, the legend helps us distinguish between the plots
plt.xlabel("Date") #provide an x axis label

#The same plots in seperate graphs
plt.subplot(1,3,2) #specify the subplot positions 1 row, 3 columns and ploting at the 2nd position
plt.plot(growth_data["Date"],growth_data["Height_Ratio"])
plt.title("Average Height Ratio")
plt.xlabel("Date")

plt.subplot(1,3,3) #specify the subplot positions 1 row, 3 columns and ploting at the 3rd position
plt.plot(growth_data["Date"],growth_data["Width_Ratio"])
plt.title("Average Width Ratio")
plt.xlabel("Date")

plt.tight_layout()
plt.show()
