from factory.file_generator.utils import load_json

class ViewController:
    def __init__(self):
        self.complete = False
        self.app_mode = None

        self.generator = {
        "Time":{
            "Duration": None,
            "Tick": None},
        "Node":[],
        "Route":{},
        "Passenger":{}}

        self.passenger_dispatcher = None
        self.bus_dispatcher = None

        self.generator_path = None
        self.passenger_dispatcher_path = None
        self.bus_dispatcher_path = None

    def load_generator_from_path(self,path):
        self.generator = load_json(path)
