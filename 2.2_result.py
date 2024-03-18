#Using Trefle we get information regarding the identified plant
import json
import requests

token = 'SnEyMTc0UVJmQ1ZYK1pNLzljV2dUUT09'
plant_link = '/api/v1/plants/epipremnum-aureum'
r = requests.get('https://trefle.io/{}?token={}'.format(plant_link,token))

#print(json.dumps(r.json(),indent=2) #raw json result

#Filtered json result
data = r.json()
print("scientific name: ",data["data"]["scientific_name"],end='\n\n')
print("image url: ",data["data"]["image_url"],end='\n\n')
print("vegetable: ",data["data"]["vegetable"],end='\n\n')
try: #some plants do not have the following information available so we use error handling
    print("edible: ",data["data"]["main_species"]["edible"],end='\n\n')
    print("distribution: ",data["data"]["main_species"]["distribution"],end='\n\n')
    print("Flower: ",data["data"]["main_species"]["flower"],end='\n\n')
    print("Foliage: ",data["data"]["main_species"]["foliage"],end='\n\n')
    print("Fruit or seed: ",data["data"]["main_species"]["fruit_or_seed"],end='\n\n')

    print("\nSpecifications: ")
    for specifications in data["data"]["main_species"]["specifications"]:
        print("{}: {}".format(specifications,data["data"]["main_species"]["specifications"][specifications]))

    print("\nGrowth: ")
    for growth in data["data"]["main_species"]["growth"]:
        print("{}: {}".format(growth,data["data"]["main_species"]["growth"][growth]))
except:
    print("Information for the given plant is not available")
