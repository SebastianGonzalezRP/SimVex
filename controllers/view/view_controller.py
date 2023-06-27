import configparser
from factory.file_generator.utils import load_json

class ViewController:
    def __init__(self):
        self.complete = False
        self.app_mode = None

        config = configparser.ConfigParser()
        config.read(".config")
        self.generator = {
        "Time":{
            "Duration": int(config.get('SimTime', 'sim_duration')),
            "Tick": float(config.get('SimTime', 'sim_tick'))},
        "Node":[],
        "Route":{},
        "Buses":{"top_speed": float(config.get('Buses', 'top_speed')), 
                 "acc":float(config.get('Buses', 'acceleration')),
                 "desc":float(config.get('Buses', 'deceleration'))},
        "Passenger":{}}

        self.passenger_dispatcher = None
        self.bus_dispatcher = None

        self.generator_path = None
        self.passenger_dispatcher_path = None
        self.bus_dispatcher_path = None

    def load_generator_from_path(self,path):
        self.generator = load_json(path)
