#Python code to request sensor data 
import serial
import time


ser = serial.Serial('COM10',baudrate = 9600, timeout=3)

#ser = serial.Serial('/dev/rfcomm0',baudrate = 9600, timeout=3) #For Raspberry Pi

time.sleep(3)

totalvolume = 0

while True:
    userInput = input('Get data point?')

    if userInput == 'l': #LDR
        ser.write(b'l')
        lightval = ser.readline().decode('utf-8')
        if len(lightval) > 0:
            if lightval[0] == 'l':
                lightval = int(lightval[1:])
                print("Light sensor val: ",lightval)
            
    elif userInput == 't': #Temperature
        ser.write(b't')
        tempval = ser.readline().decode('utf-8')
        if len(tempval) > 0:
            if tempval[0] == 't':
                tempval = int(tempval[1:])
                print("\nTemperature val: ",tempval)

    elif userInput == 'm': #Soil moisture
        ser.write(b'm')
        moistureval = ser.readline().decode('utf-8')
        if len(moistureval) > 0:
            if moistureval[0] == 'm':
                moistureval = int(moistureval[1:])
                print("Soil moisture val: ",moistureval)

    elif userInput == 'w': #Pump
        ser.write(b'w')

    elif userInput == 'v': #Volume
        ser.write(b'v')
        volume = ser.readline().decode('utf-8')
        if len(volume) > 0:
            if volume[0] == 'v':
                volume = int(volume[1:])
                totalvolume = totalvolume + volume #Add the volume to the total volume
                print("Total volume of water poured: ",totalvolume)

    elif userInput == 'h': #humidity sensor
        ser.write(b'h')
        humidityval = ser.readline().decode('utf-8')
        if len(humidityval) > 0:
            if humidityval[0] == 'h':
                humidityval = int(humidityval[1:])
                print("Humidity sensor val: ",humidityval)
