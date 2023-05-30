import json
import csv
from factory.node_factory import *
from models.transit_network import TransitNetwork as TN
from models.route import Route
from factory.bus_factory import *
from factory.passenger_factory import * 

class Sim_Controller:
    def __init__(self,generator_path,passenger_dispatch_path,bus_dispatch_path):
        self.generator = self.load_json(generator_path)
        self.passenger_data = self.load_csv(passenger_dispatch_path)
        self.bus_data = self.load_csv(bus_dispatch_path)

        self.transit_network = []
        self.routes = []

        self.bus_hyperparameter = {}

        self.bus_dispatcher = []
        self.passenger_dispatcher = []

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

    def get_route_by_id(self,route_id):
        for route in self.routes:
            if route.id == route_id:
                return route
            
    def set_bus_hyperparameter(self):
        self.bus_hyperparameter = self.generator["Buses"]

    def create_passenger_construction_params(self,passenger_data):
        #construction_params = [origin, destiny, route, boarding_t, alighting_t]
        origin = passenger_data[1]
        destiny = passenger_data[2]
        route = self.get_route_by_id(passenger_data[3])
        boarding_time = int(passenger_data[4])
        alighting_time = int(passenger_data[5])
        return [origin, destiny, route, boarding_time, alighting_time]

    def create_passenger_dispatcher(self):
        for passenger_data in self.passenger_data:
            arrival_time = passenger_data[0]
            new_passenger_params = self.create_passenger_construction_params(passenger_data)
            new_passenger = construct_passenger(new_passenger_params)
            self.passenger_dispatcher.append((arrival_time,new_passenger))

    def remove_processed_bus_passengers(self,index_list):
        for index in sorted(index_list, reverse=True):
            del self.passenger_data[index]

    def get_boarded_passengers(self,bus_id):
        boarded_passengers = []
        remove_index = []
        for passenger_data in self.passenger_data:
            if passenger_data[1] == bus_id:
                new_passenger_params = self.create_passenger_construction_params(passenger_data)
                new_passenger = construct_passenger(new_passenger_params)
                boarded_passengers.append(new_passenger)
                remove_index.append(self.passenger_data.index(passenger_data))
        self.remove_processed_bus_passengers(remove_index)
        return boarded_passengers

    def create_bus_construction_params(self,bus_data):
        #construction_params = [id, route, passengers,door_n, top_speed,acc, desc]
        bus_id = bus_data[1]
        bus_route = self.get_route_by_id(bus_data[2])
        boarded_passengers = self.get_boarded_passengers(bus_id)
        door_n = int(bus_data[3])
        top_speed = int(self.bus_hyperparameter["top_speed"])
        acc = int(self.bus_hyperparameter["acc"])
        desc = int(self.bus_hyperparameter["desc"])
        return [bus_id,bus_route,boarded_passengers,door_n,top_speed,acc,desc]

    def create_bus_dispatcher(self):
        for bus_data in self.bus_data:
            arrival_time = bus_data[0]
            new_bus_params = self.create_bus_construction_params(bus_data)
            new_bus = construct_bus(new_bus_params)
            self.bus_dispatcher.append((arrival_time,new_bus))


    def initialize_sim(self):
        self.create_nodes()
        self.create_routes()
        self.set_bus_hyperparameter()
        self.create_bus_dispatcher()
        self.create_passenger_dispatcher()


    def debug(self):
        for node in self.transit_network.network:
            print(node)
        for route in self.routes:
            print(route)
    
            
        
    