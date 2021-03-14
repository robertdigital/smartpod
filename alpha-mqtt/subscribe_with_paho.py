from config import *
from datetime import datetime
import paho.mqtt.client as mqtt
def on_connect(client, userdata, flags, rc):
    print("Result from connect: {}".format(
        mqtt.connack_string(rc)))


# Subscribe to the vehicles/vehiclepi01/tests topic filter
    client.subscribe("sensor/gauge", qos=2)
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
                                             database='sensors',
                                             user='root',
                                             password='MY$QL_R00t65')
        mySql_insert_query = """INSERT INTO gauge (temp, humidity, barometric, windSpeed) 
                               VALUES 
                               (?, ?, ?, ?) """

        cursor = connection.cursor(prepared=True)
        cursor.execute(mySql_insert_query, insert_tuple)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into python sensors")
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into python sensors {}".format(error))

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
