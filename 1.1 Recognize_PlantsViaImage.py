#Identifying a plant from an image
import requests
import json 

url = 'https://my-api.plantnet.org/v2/identify/all?'  #This the url to which we can upload an image to the plantnet server and get the response of the identified plant 
api_key = 'api-key=  ' #We need to pass our API-Key along with the url which can be found in the plantnet account settings after loging in
imagefile = open('Images/moneyplant.jpg','rb')#We open the image file of the plant we want to identify by passing its location and open in read binary mode.
data = {'organs':'leaf'} #We specify the part of the plant we want to identify


files = {'images':imagefile} #We create a dictionary with the key 'image' and the value as the image we have opened.

result = requests.post(url+api_key, data=data, files=files) #We make a HTTP POST request by concatenating the url with the api-key, we also pass the plant image and also the data of the part of the plant we are trying to identify.


#Printing the result which is in JSON
print("Raw json data")
print(result.json())

print("The same date indented:")
print(json.dumps(result.json(), indent=1)) #We can use the json library to print an indented version of the result, we can obsereve that the indented version appears similar to that of a dictionary.


data = result.json() #we can load the json result to a variable, the json result will be stored as a dictionary(dictionaries with dictionaries and also list) in python. Thus we can access data similar to a python dictionary.

#Print the recognized plant with the highest score
print("\n\nOnly the plant with the higest score")
print("Score: ",data['results'][0]['score']) #To print the plant with the highest similarity score, we can access the "results" key in the dictionary. The result keys value is a list which contains all the recognized plants. The first element of the list is the plant with the higest similarity score, with its details as a dictionary. Inside that dictionay we see the key 'score' and thus we can print its value.  
print('Scientific name: ',data['results'][0]['species']['scientificNameWithoutAuthor']) #similary we can access the scientific name and commonNames
print('Common names: ',data['results'][0]['species']['commonNames'])


#Access the data and print all of it in loop
#We can also write a loop which prints out all the plants which were recognized.
print("\n\nAll data")
for result in data['results']: #here we loop through the list of all recognized plants
    print("Score: ",result['score'])
    print("Scientific name: ",result['species']['scientificNameWithoutAuthor'])
    print("Common names: ",result['species']['commonNames'])
    print("\n")

