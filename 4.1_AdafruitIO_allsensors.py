#This code is used to upload all sensor data to Adafruit IO
from Adafruit_IO import Client, RequestError, Feed
import threading
import serial
import time

ADAFRUIT_IO_KEY = '' #insert key here

ADAFRUIT_IO_USERNAME = '' #insert username here

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

temp_feed = aio.feeds('temp')#create feed objects for all the created feeds
light_feed = aio.feeds('light')
humidity_feed = aio.feeds('humidity')
moisture_feed = aio.feeds('soil-moisture')
pump_feed = aio.feeds('pump')
totalvolume_feed = aio.feeds('total-volume')

ser = serial.Serial('COM10',baudrate = 9600, timeout=3)

time.sleep(3)

totalvolume = None

def startLogger(): #Thread for logging sensor data
    ser.write(b't') #Temperature
    tempval = ser.readline().decode('utf-8')
    if len(tempval) > 0:
        if tempval[0] == 't':
            tempval = int(tempval[1:])
            print("\nTemperature val: ",tempval)
            aio.send_data(temp_feed.key, tempval)

    ser.write(b'l') #LDR
    lightval = ser.readline().decode('utf-8')
    if len(lightval) > 0:
        if lightval[0] == 'l':
            lightval = int(lightval[1:])
            print("Light sensor val: ",lightval)
            aio.send_data(light_feed.key, lightval)

    ser.write(b'h') #Humidity
    humidityval = ser.readline().decode('utf-8')
    if len(humidityval) > 0:
        if humidityval[0] == 'h':
            humidityval = int(humidityval[1:])
            print("Humidity sensor val: ",humidityval)
            aio.send_data(humidity_feed.key, humidityval)

    totalvolume = aio.receive(totalvolume_feed.key) #Get the total volume of water poured from the,
    #'total volume' feed so we can add to it
    totalvolume = int(totalvolume.value)
    ser.write(b'v')
    volume = ser.readline().decode('utf-8')
    if len(volume) > 0:
        if volume[0] == 'v':
            volume = int(volume[1:])
            totalvolume = totalvolume + volume #Update the total volume
            print("Total volume of water poured: ",totalvolume)
            aio.send_data(totalvolume_feed.key, totalvolume) 

    ser.write(b'm') #Soil moisture
    moistureval = ser.readline().decode('utf-8')
    if len(moistureval) > 0:
        if moistureval[0] == 'm':
            moistureval = int(moistureval[1:])
            print("Soil moisture val: ",moistureval)
            aio.send_data(moisture_feed.key, moistureval)
    
    
    threading.Timer(300,startLogger).start()

startLogger()
    
while True: #Section of code checks if the "Water plant button" in Adafruit IO is pressed
    pumpstatus = aio.receive(pump_feed.key) #Read the pump status, the button block in AdafruitIO
    #is created such that if it is pressed its value is "True" and released is "False"
    if pumpstatus.value == 'True':
        print("Turn on the pump")
        pumpstatus = 'On' #We have to press the "Water plant button" for a few seconds as
        #there will be some delays. Thus we can create an indicator block in adafruitIO to show
        #if the pump has turned On. The indicator changes colour from red to blue if pumpstatus is "On"
        aio.send_data(pump_feed.key, pumpstatus) #Update pump status
        ser.write(b'w') #Send w by bluetooth to Arduino to water the plant
    elif pumpstatus == 'On': #If the pump was previously turned ON
        pumpstatus = 'False' #set pump status back to 'False' so the pump indicator led goes back to Red
        aio.send_data(pump_feed.key, pumpstatus) #Update pump status
    
   
