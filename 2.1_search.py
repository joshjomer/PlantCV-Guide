#We use Trefle to search for the identified plant
import json
import requests

token = ' ' #API Key
plant_scientific_name = "Epipremnum aureum" #Scientific name of the plant to search for
r = requests.get('https://trefle.io/api/v1/plants/search?token={}&q={}'.format(token,plant_scientific_name)) #search for the plant in Trefle by passing the token and the plant name along with API url.

print("Raw json result")
print(json.dumps(r.json(),indent=2))

data = r.json()
print("Filtered Search results") #Similar to the previous program we can filter out the data we require
for i in range(0,len(data["data"])): 
    print("\nScientific name: ",data["data"][i]["scientific_name"])
    print("slug: ",data["data"][i]["slug"])
    print("link: ",data["data"][i]["links"]["plant"]) #the link can be used to find the details about the plant, which is done in the next program
