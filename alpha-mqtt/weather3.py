import urllib.request
import json
import time
from datetime import datetime
starttime = time.time()

import paho.mqtt.client as mqtt #import the client1
broker_address="seapod.technoid.info" 

client = mqtt.Client("P1") #create new instance
#client.username_pw_set("byron", password="ferret")

while True:
    client.connect(broker_address)
    f = urllib.request.urlopen('https://api.weather.com/v2/pws/observations/current?stationId=KMAHANOV10&format=json&units=e&apiKey=d36de6d37ca147edade6d37ca1c7ed4d')
    
    #sample data
    #{"observations":[{"stationID":"KMAHANOV10","obsTimeUtc":"2020-08-18T07:08:44Z","obsTimeLocal":"2020-08-18 03:08:44","neighborhood":"1505Broadway","softwareType":"Rainwise IP-100","country":"US","solarRadiation":null,"lon":-70.864853,"realtimeFrequency":null,"epoch":1597734524,"lat":42.092632,"uv":null,"winddir":112,"humidity":96,"qcStatus":1,"imperial":{"temp":65,"heatIndex":65,"dewpt":63,"windChill":65,"windSpeed":0,"windGust":0,"pressure":29.83,"precipRate":0.18,"precipTotal":0.21,"elev":104}}]}

    json_string = f.read()
    parsed_json = json.loads(json_string)
    location = parsed_json['observations'][0]['stationID']
    humidity = parsed_json['observations'][0]['humidity']
    temp_f = parsed_json['observations'][0]['imperial']['temp']
    pressure = parsed_json['observations'][0]['imperial']['pressure']
    windSpeed = parsed_json['observations'][0]['imperial']['windSpeed']
    
    
    now = datetime.now()
    current_time = now.strftime("%Y/%m/%d %H:%M:%S")
    print("Current Time =", current_time)

    print ("Current Temperature is: %s" % (temp_f))
    print ("Current Humidity is: %s" % (humidity))
    print ("Current Barometric Pressure is: %s" % (pressure))
    print ("Current Wind Speed is: %s" % (windSpeed))
    print ("")
    
    x = str(temp_f)+', '+str(humidity)+', '+str(pressure)+', '+str(windSpeed)
    #print (x)        
    f.close()
    
    client.publish("weather/gauge", x)
    client.disconnect()
    
    time.sleep(600)