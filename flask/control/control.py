"""
control.py - Flask control server APP that talks to hardware device
             modules and presents a REST API for devices
Copyright (C) 2021  Ocean Builders LLC

Author: scott@deardorff.org 

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import flask
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/lights',methods=['GET'])
def lights():
    """
    Insert call listDevices(type="light")
    """
    return json.dumps([{"id":1,"status":True, "desc": "Middle Hallway", "type":"strip","group":"hallways", "color": 0x000000, "ata":"ATA 32 00-100-125"},
        {"id":2,"status":False, "desc": "Living Room Center Console", "type": "bulb", "group":"Living Room", "color":0xffffff, "ata":"ATA 32 00-200-126"}])

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
    return json.dumps({"id":2,"status":False, "desc": "Living Room Center Console", "type": "bulb", "group":"Living Room", "color":0xffffff, "ata":"ATA 32 00-200-126"})

@app.route('/light',methods=["DELETE"])
def delete_light():
    """
    deleteDevice(id=x) why would you want to delete a device?
    """
    return json.dumps({"id":2, "msg":"Device deleted successfully"})





app.run()
