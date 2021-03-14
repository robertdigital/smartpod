import flask
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/lights',methods=['GET'])
def lights():
    """
    Insert call listDevices(type="light")
    """
    return json.dumps([{"id":1,"status":True, "desc": "Middle Hallway", "type":"strip","group":"hallways", "color": 0x000000},
        {"id":2,"status":False, "desc": "Living Room Center Console", "type": "bulb", "group":"Living Room", "color":0xffffff}])

@app.route('/light', methods=['POST'])
def add_light():
    """
    Insert call to addDevice()
    """
    return json.dumps({"msg":"Device added successfully","id":5})

@app.route('/light',methods=['PUT'])
def update_light():
    """
    Insert call to updateDevice(id=x)
    """
    return json.dumps({"msg":"Device updated successfully","id":3})

@app.route('/light',methods=["GET"])
def get_light():
    """
    Insert call to getDevice(id=x) here
    """
    return json.dumps({"id":2,"status":False, "desc": "Living Room Center Console", "type": "bulb", "group":"Living Room", "color":0xffffff})

@app.route('/light',methods=["DELETE"])
def delete_light():
    """
    deleteDevice(id=x) why would you want to delete a device?
    """
    return json.dumps({"id":2, "msg":"Device deleted successfully"})





app.run()
