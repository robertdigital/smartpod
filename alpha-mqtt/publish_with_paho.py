import paho.mqtt.client as mqtt #import the client1
broker_address="localhost" 

client = mqtt.Client("P1") #create new instance
client.connect(broker_address) #connect to broker
client.publish("house/bulb1","ON")#publish