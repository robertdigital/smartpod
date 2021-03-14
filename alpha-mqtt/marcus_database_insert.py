import os.path

mqtt_server_host = "localhost"
mqtt_server_port = 1883
mqtt_keepalive = 60


from datetime import datetime
import paho.mqtt.client as mqtt
def on_connect(client, userdata, flags, rc):
    print("Result from connect: {}".format(
        mqtt.connack_string(rc)))


# Subscribe to the SeaPod0001/Bathroom/InfinityShower/Sensor000Test topic filter
    client.subscribe("SeaPod0001/Bathroom/InfinityShower/Sensor000Test", qos=2)
def on_subscribe(client, userdata, mid, granted_qos):
    print("I've subscribed with QoS: {}".format(
        granted_qos[0]))
        
def on_message(client, userdata, msg):
    print("")
    print("Message received. Topic: {}. Payload: {}".format(
        msg.topic, 
        str(msg.payload)))
    
    
    now = datetime.now()
    current_time = now.strftime("%Y/%m/%d %H:%M:%S")
    print("Current Time =", current_time)
    
    msg.payload = msg.payload.decode("utf-8")
    print(msg.payload)
    x = msg.payload.split(", ")
    insert_tuple = (x)
    

    import mysql.connector
    from mysql.connector import Error
    from mysql.connector import errorcode

    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='SeaPod0001',
                                             user='iotGroup',
                                             password='@WSX2wsxok')
        mySql_insert_query = """INSERT INTO DataSensor000Test (Temperature) 
                               VALUES 
                               (?) """

        cursor = connection.cursor(prepared=True)
        cursor.execute(mySql_insert_query, insert_tuple)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into iotGroup DataSensor000Test")
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into iotGroup DataSensor000Test {}".format(error))

    finally:
        if (connection.is_connected()):
            connection.close()
            print("MySQL connection is closed")
    print("")        
if __name__ == "__main__":
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    
    client.connect(host=mqtt_server_host,
        port=mqtt_server_port,
        keepalive=mqtt_keepalive)


client.loop_forever()
