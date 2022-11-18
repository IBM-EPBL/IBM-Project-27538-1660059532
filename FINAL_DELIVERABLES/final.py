import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import requests
a="https://api.openweathermap.org/data/2.5/weather?lat=9.939093&lon=78.121719&appid=774e289f963ae64e2b43500df7bd1053"
r = requests.get(url=a)
data = r.json()

temp = data["main"]["temp"]
hum = data["main"]["humidity"]
print("Temperature is :",temp)
print("Humidity is :",hum)

#Provide your IBM Watson Device Credentials
organization = "zdo1c1"
deviceType = "123"
deviceId = "ibm"
authMethod = "token"
authToken = "12345678"

# Initialize GPIO
def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data['command'])
    status=cmd.data['command']
    if status=="lighton":
        print ("led is on")
    elif status == "lightoff":
        print ("led is off")
    else :
        print ("please send proper command")

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        #Get Sensor Data from DHT11
        
        temp = data["main"]["temp"]
        Humid = data["main"]["humidity"]
        speed =  random.randint(10,100)
        if speed < 50 :
            speed = 80
        else :
            speed = 60
        traffic =random.randint(50,100)
        road = random.randint(50,100)
        if(road<75):
            road="Blocked"
        else :
            road="Clear"
        if(traffic<75):
            traffic="Go Straight"
        else :
            traffic="Take Diversion"
        

        
        data = { 'temp' : temp, 'Humid': Humid, 'speed': speed, 'traffic' : traffic, 'road': road}
        #print data
        def myOnPublishCallback():
            print ("Published Temperature = %s C" % temp, "Humidity = %s %%" % Humid,"Speed = %s km/hr" % speed, "traffic = %s " % traffic, "Road status = %s " % road, "to IBM Watson")

        success = deviceCli.publishEvent("IoTSensor", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(10)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
