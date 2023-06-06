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

        self.duration = self.generator["Time"]["Duration"]
        self.tick = self.generator["Time"]["Tick"]

        self.transit_network = []
        self.routes = []

        self.bus_hyperparameter = {}

        self.bus_dispatcher = []
        self.passenger_dispatcher = []

        self.bus_in_transit = []
        self.bus_in_stops = []
        self.bus_in_intersection = []

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
            
    def get_stop_by_id(self,stop_id):
        for node in self.transit_network.network:
            if type(node) == Stop:
                if node.id == stop_id:
                    return node
            
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
            arrival_time = int(passenger_data[0])
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
            arrival_time = int(bus_data[0])
            new_bus_params = self.create_bus_construction_params(bus_data)
            new_bus = construct_bus(new_bus_params)
            self.bus_dispatcher.append((arrival_time,new_bus))


    def populate_stops(self):
        print(len(self.passenger_dispatcher))
        arrived_passengers = [psng_arrival[1] for psng_arrival in self.passenger_dispatcher if psng_arrival[0] == 0]
        self.passenger_dispatcher = [psng_arrival for psng_arrival in self.passenger_dispatcher if psng_arrival[0] != 0]
        for node in self.transit_network.network:
            if type(node) == Stop:
                passengers = []
                for passenger in arrived_passengers:
                    if passenger.origin == node.id:
                        passengers.append(passenger) 
                        arrived_passengers.remove(passenger)  
                node.build_passenger_boarding_queue(passengers) 

    def initialize_queue_length(self):
        for node in self.transit_network.network:
            if type(node) == Stop:
                node.calculate_queue_length()
            if type(node) == Intersection:
                node.calculate_queue_length()
        
    def set_bus_star_mark(self):
        for bus_arrival in self.bus_dispatcher:
            bus_arrival[1].location = self.transit_network.network[0]
            bus_arrival[1].next_node = bus_arrival[1].location.next_node

    def update_intersections(self):
        for node in self.transit_network.network:
            if type(node) == Intersection:
                node.update_timer(self.tick)

    def check_bus_dispatcher(self):
        arriving_buses = [bus_arrival[1] for bus_arrival in self.bus_dispatcher if bus_arrival[0] <= self.simulated_time]
        self.bus_dispatcher = [bus_arrival[1] for bus_arrival in self.bus_dispatcher if bus_arrival[0] > self.simulated_time]
        for bus in arriving_buses:
            self.dispatch_bus(bus)
        
    def check_passenger_dispatcher(self):
        arriving_passengers = [psng_arrival[1] for psng_arrival in self.passenger_dispatcher if psng_arrival[0] <= self.simulated_time]
        self.passenger_dispatcher = [psng_arrival for psng_arrival in self.passenger_dispatcher if psng_arrival[0] > self.simulated_time]
        for passenger in arriving_passengers:
            self.dispatch_passenger(passenger)


    def dispatch_bus(self, dispatched_bus):
        self.bus_in_transit.append(dispatched_bus)
        dispatched_bus.enter_simulation()

    def dispatch_passenger(self, dispatched_passenger):
        objective_stop = self.get_stop_by_id(dispatched_passenger.origin)
        objective_stop.arriving_passenger(dispatched_passenger)

    def update_buses_in_transit(self):
        for bus in self.bus_in_transit:
            bus.update_speed(self.tick)
            bus.update_position(self.tick)
            bus.update_stop_flag()
            bus.update_breaking_point()
            bus.should_brake()

    def update_buses_in_stop(self):
        pass

    def check_bus_node_transfer(self):
        for bus in self.bus_in_transit:
            position = bus.position
            node_length = bus.location.length
            if position >= node_length:
                bus.node_transition()



#MainLoop Functions
    def initialize_sim(self):
        self.create_nodes()
        self.create_routes()
        self.set_bus_hyperparameter()
        self.create_bus_dispatcher()
        self.create_passenger_dispatcher()
        self.populate_stops()
        self.initialize_queue_length()
        self.set_bus_star_mark() 

    def run_sim(self):
        self.simulated_time = self.tick
        while self.simulated_time < self.duration:
            self.update_intersections()
            self.check_bus_dispatcher()
            self.check_passenger_dispatcher()
            self.update_buses_in_transit()
            self.check_bus_node_transfer()
            self.check_passenger_transfer()
            pass
            self.simulated_time += self.tick


    def debug(self):
        for bus in self.bus_dispatcher:
            bus[1].enter_simulation()
