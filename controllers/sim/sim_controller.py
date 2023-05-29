import json
import csv
from factory.node_factory import *
from models.transit_network import TransitNetwork as TN
from models.route import Route

class Sim_Controller:
    def __init__(self,generator_path,psngr_dispatch_path,bus_dispatch_path):
        self.generator = self.load_json(generator_path)
        self.psngr_dispatcher = self.load_csv(psngr_dispatch_path)
        self.bus_dispatcher = self.load_csv(bus_dispatch_path)

        self.transit_network = []
        self.routes = []

        self.initialize_sim()


    def load_json(self, path):
        with open(path, 'r') as file:
            data = json.load(file)
        return data

    def load_csv(self, path):
        data = []
        with open(path, 'r') as file:
            csv_reader = csv.reader(file)
            for line in csv_reader:
                data.append(line)
        return data

    def create_nodes(self):
        for node in self.generator["Node"]:
            new_node = node_generator(node)
            self.transit_network.append(new_node)
        self.transit_network = TN(self.transit_network)

    def create_routes(self):
        route_data = self.generator["Route"]
        for route_id, route_info in route_data.items():
            stops = list(route_info["stops"].keys())
            serving_stops = []
            for node in self.transit_network.network:
                if type(node) == Stop:
                    if node.id in stops:
                        serving_stops.append(node)
            new_route = Route(route_id, serving_stops)
            self.routes.append(new_route)

    def update_stops_routes(self):
        pass

    def initialize_sim(self):
        self.create_nodes()
        self.create_routes()


    def debug1(self):
        route_data = self.generator["Route"]
        for route_id, route_info in route_data.items():
            stops = list(route_info["stops"].keys())
            serving_stops = []
            for node in self.transit_network.network:
                if type(node) == Stop:
                    if node.id in stops:
                        serving_stops.append(node)
            new_route = Route(route_id, serving_stops)
            self.routes.append(new_route)
    
    def debug2(self):
        for route in self.routes:
            print(route.id)

            
        
    