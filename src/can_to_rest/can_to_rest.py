import threading
import can
import time
import argparse
import json
from canstruct import pycanstruct
import yaml


from flask import (
    Flask,
    jsonify
)

class Valve:
    def __init__(self, name, description, addr, value_index):
        self.name = name
        self.description = description
        self.address = addr
        self.valve_index = value_index
        self.is_on = False
        self.turn_on_time = 0

    def status(self):
        return {
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "relay": self.valve_index,
            "is_on": self.is_on
        }

class State:
    def __init__(self):
        self.valves = None
        self.lock = threading.RLock()
    
    def populate_from_config(self, fn):
        print('Loading %s' % fn)
        json_cfg = json.load(open(fn, 'r'))
        self.valves = {}
        for name, valve_def in json_cfg['valves'].items():
            self.valves[name] = Valve(name,
                    valve_def["description"],
                    int(valve_def["address"]),
                    int(valve_def["relay"])
                )
    def set_valve_state(self, name, state):
        with self.lock:
            for _, valve in self.valves.items():
                valve.is_on = False
            self.valves[name].is_on = state == 1
            self.valves[name].turn_on_time = time.time()

    def status(self):
        valves = {}
        for valve_name, valve in self.valves.items():
            valves[valve.name] = valve.status()
        return {
            "valves": valves
        }
    
    def stations(self):
        stations_map = {}
        for name, valve_def in self.valves.items():
            if valve_def.address not in stations_map:
                stations_map[valve_def.address] = {
                    "Sprinkler1": 0,
                    "Sprinkler2": 0,
                    "Sprinkler3": 0,
                    "Sprinkler4": 0,
                }
            if valve_def.is_on:
                stations_map[valve_def.address]["Sprinkler" + str(valve_def.valve_index)] = 1
        return stations_map
    

state = State()
app = Flask(__name__)

@app.route("/")
def root():
    return jsonify(
        state.status()
    )

@app.route("/control/valve/<valve>/<control_state>")
def control(valve, control_state):
    control_state = int(control_state)
    if not (valve in state.valves):
        return jsonify({
                "code": -1,
                "message": "No such valve (%s)" % valve
            }
        )

    if not (control_state in [1,0]): 
        return jsonify({
                "code": -1,
                "message": "Control state need to be 1 or 0"
            }
        )
    
    print(time.time," : ", valve, " = ", control_state)
    state.set_valve_state(valve, control_state)

    return jsonify({
            "code": 1,
            "message": "ok"
        }
    )

@app.route("/stations")
def stations():
    return jsonify(state.stations())

def check_time_valves():
    while 1:
        time.sleep(1.0)
        with state.lock:
            for valve_name, valve in state.valves.items():
                if valve.is_on:
                    if abs(time.time() - valve.turn_on_time) > (60 * 3):
                        print("Safety shutoff valve", valve_name)
                        valve.is_on = 0


def command_can_bus():
    canstruct_cfg = yaml.load(open(args.canstruct, 'r'))
    canstruct = pycanstruct.CANStruct(canstruct_cfg[list(canstruct_cfg.keys())[0]]);
    bus = can.interface.Bus(channel=args.interface , bustype='socketcan_ctypes')

    while 1:
        time.sleep(1.0)
        MY_ADDR = 0
        for addr_str, sprinklers in state.stations().items():
            addr = int(addr_str)

            arbid = canstruct.encode_arbid({
                            'source_address': MY_ADDR,
                            'destination': addr,
                            'function_code':  0x10, # SprinkleCommand
                            'priority':  0x7,
                            'reserved':  0x0,
                            'data_page':  0x0,
                        }
                    )
            data = canstruct.encode_message('SprinkleCommand', sprinklers)
            #print("sending over can ", data)
            canmsg = can.Message(arbitration_id=arbid, data=data, extended_id=True)
            bus.send(canmsg)



#if __name__ == "__main__":
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Persephone CAN Bus sprinkler System')
    parser.add_argument('canstruct', help='canstruct config filename')
    parser.add_argument('interface', help='SocketCAN interface')
    parser.add_argument('config', help='Sprinkler configuration')
    args = parser.parse_args()
    state.populate_from_config(args.config)
    
    can_control_worker = threading.Thread(target=command_can_bus)
    can_control_worker.setDaemon(True)
    can_control_worker.start()
    
    safety_worker = threading.Thread(target=check_time_valves)
    safety_worker.setDaemon(True)
    safety_worker.start()
    
    app.run(debug=False, host="0.0.0.0")

#http://192.168.1.182:5000/control/valve/sprinkler3/1 (malenkaya)


'''
def receiver():
    while 1:
        bus = can.interface.Bus(channel=args.interface , bustype='socketcan_ctypes')
        message = bus.recv()
        message_timestamp = time.time()
        msg_rec = None
        if message.arbitration_id in walker.msgs:
            msg_rec = walker.msgs[message.arbitration_id]
        else:
            msg_rec = MsgRecord()
            walker.msgs[message.arbitration_id] = msg_rec

        msg_rec.update(message)
'''
