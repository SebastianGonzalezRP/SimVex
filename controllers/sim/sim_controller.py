from factory.node_factory import *
from models.transit_network import TransitNetwork as TN
from models.route import Route
from factory.bus_factory import *
from factory.passenger_factory import * 

from factory.file_generator.utils import load_csv, load_json

class SimController:
    def __init__(self):
        self.generator = None
        self.passenger_data = None
        self.bus_data = None

        self.duration = None
        self.tick = None

        self.transit_network = []
        self.routes = []

        self.streets = []
        self.intersections = []
        self.stops = []

        self.routes_ids = []
        self.stops_ids = []

        self.passengers = []
        self.passenger_dispatcher = []
        self.boarding_passengers = []
        self.alighting_passengers = []

        self.buses = []
        self.bus_dispatcher = []

        self.buses_in_simulation = []
        self.completed_buses = []
    
    def load_files_data(self,generator_path,passenger_dispatch_path,bus_dispatch_path):
        self.generator = load_json(generator_path)
        self.passenger_data = load_csv(passenger_dispatch_path)
        self.bus_data = load_csv(bus_dispatch_path)

    def load_time_config(self):
        self.duration = self.generator["Time"]["Duration"]
        self.tick = self.generator["Time"]["Tick"]

    def create_nodes(self):
        for node in self.generator["Node"]:
            new_node = node_generator(node)
            self.transit_network.append(new_node)
            if type(new_node) == Street:
                self.streets.append(new_node)
            elif type(new_node) == Intersection:
                self.intersections.append(new_node)
            elif type(new_node) == Stop:
                self.stops.append(new_node)
                self.stops_ids.append(new_node.id)
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
            self.routes_ids.append(new_route.id)

    def assign_operating_routes(self):
        for node in self.transit_network.network:
            if type(node) == Stop:
                for route in self.routes:
                    for stop in route.serving_stops:
                        if stop == node:
                            node.serving_routes.append(route)

    def get_route_by_id(self,route_id):
        for route in self.routes:
            if route.id == route_id:
                return route
            
    def get_stop_by_id(self,stop_id):
        for node in self.transit_network.network:
            if type(node) == Stop:
                if node.id == stop_id:
                    return node

    def generate_passengers(self):
        for passenger_data in self.passenger_data:
            new_passenger_params = self.create_passenger_construction_params(passenger_data)
            new_passenger = construct_passenger(new_passenger_params)
            self.passengers.append(new_passenger)

    def determine_passenger_action(self):
        self.determine_boarding_passengers()
        self.determine_alighting_passengers()

    def determine_boarding_passengers(self):
        for passenger in self.passengers:
            if passenger.origin in self.stops_ids:
                self.boarding_passengers.append(passenger)

    def determine_alighting_passengers(self):
        for passenger in self.passengers:
            if passenger.destiny in self.stops_ids:
                self.alighting_passengers.append(passenger)
        

    def generate_buses(self):
        for bus_data in self.bus_data:
            new_bus_params = self.create_bus_construction_params(bus_data)
            new_bus = construct_bus(new_bus_params)
            self.buses.append(new_bus)

    def create_passenger_construction_params(self,passenger_data):
        #construction_params = [arrival_time, origin, destiny, route, boarding_t, alighting_t]
        arrival_time = int(passenger_data[0])
        origin = passenger_data[1]
        destiny = passenger_data[2]
        route = self.get_route_by_id(passenger_data[3])
        boarding_time = int(passenger_data[4])
        alighting_time = int(passenger_data[5])
        return [arrival_time,origin, destiny, route, boarding_time, alighting_time]

    def create_passenger_dispatcher(self):
        self.passenger_dispatcher = self.passengers[:]

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
        #bus_Data: [t_in, ID, route, model]
        #construction_params = [arrival_time, id, route, door_n, top_speed,acc, desc]
        
        arrival_time = int(bus_data[0])
        bus_id = bus_data[1]
        route_id = bus_data[2]
        bus_model = bus_data[3]

        bus_route_object = self.get_route_by_id(route_id)
        bus_model_specs = self.generator["Route"][route_id]["bus_model"][bus_model]

        door_n = int(bus_model_specs["door_n"])
        top_speed = float(bus_model_specs["top_speed"])
        acc = float(bus_model_specs["acc"])
        desc = float(bus_model_specs["desc"])

        return [arrival_time,bus_id,bus_route_object,door_n,top_speed,acc,desc]

    def create_bus_dispatcher(self):
        self.bus_dispatcher = self.buses[:]

    def populate_stops(self):
        arrived_passengers = [passenger for passenger in self.passenger_dispatcher if passenger.arrival_time == 0]
        self.passenger_dispatcher = [passenger for passenger in self.passenger_dispatcher if passenger.arrival_time != 0]
        for stop in self.stops:
            passengers = []
            for passenger in arrived_passengers:
                if passenger.origin == stop.id:
                    passengers.append(passenger) 
                    arrived_passengers.remove(passenger)  
            stop.build_passenger_boarding_queue(passengers) 

    def initialize_queue_length(self):
        for node in self.transit_network.network:
            if type(node) == Stop:
                node.calculate_queue_length()
            if type(node) == Intersection:
                node.calculate_queue_length()
        
    def set_bus_star_mark(self):
        for bus in self.buses:
            bus.location = self.transit_network.network[0]
            bus.next_node = bus.location.next_node


    def update_intersections(self):
        for node in self.transit_network.network:
            if type(node) == Intersection:
                node.update_timer(self.tick)

    def load_boarded_passengers_in_bus(self,bus:Bus):
        for passenger in reversed(self.passenger_dispatcher):
            if passenger.origin == bus.id:
                bus.board_passenger(passenger)
                self.passenger_dispatcher.remove(passenger)

    def check_bus_dispatcher(self):
        arriving_buses = [bus for bus in self.bus_dispatcher if bus.arrival_time <= self.simulated_time]
        self.bus_dispatcher = [bus for bus in self.bus_dispatcher if bus.arrival_time > self.simulated_time]
        for bus in arriving_buses:
            self.load_boarded_passengers_in_bus(bus)
            self.dispatch_bus(bus)
        
    def check_passenger_dispatcher(self):
        arriving_passengers = [passenger for passenger in self.passenger_dispatcher if passenger.arrival_time <= self.simulated_time]
        self.passenger_dispatcher = [passenger for passenger in self.passenger_dispatcher if passenger.arrival_time > self.simulated_time]
        for passenger in arriving_passengers:
            self.dispatch_passenger(passenger)

    def dispatch_bus(self, dispatched_bus):
        self.buses_in_simulation.append(dispatched_bus)
        dispatched_bus.enter_simulation()

    def dispatch_passenger(self, dispatched_passenger):
        objective_stop = self.get_stop_by_id(dispatched_passenger.origin)
        objective_stop.arriving_passenger(dispatched_passenger)

    def update_buses_in_transit(self):
        for bus in self.buses_in_simulation:
            if type(bus.location) == Street:
                bus.update_breaking_point()
                bus.update_position(self.tick)
                bus.update_speed(self.tick)
                bus.update_stop_flag()
                bus.should_brake()

    def update_buses_at_stops(self):
        for bus in self.buses_in_simulation:
            if type(bus.location) == Stop:
                bus.check_operational_position_in_queue(self.tick)
        for node in self.transit_network.network:
            if type(node) == Stop:
                node.reorganize_queues()
    
    def update_buses_at_intersections(self):
        for node in self.transit_network.network:
            if type(node) == Intersection:
                if node.semaphore == 'G':
                    node.broadcast_green()

    def check_bus_node_transfer(self):
        for bus in self.buses_in_simulation: 
            if type(bus.location) == Street:
                position = bus.position
                node_length = bus.location.length
                if position >= node_length:
                    bus.node_transition()

    def update_simulated_buses_log(self):
        for bus in self.buses_in_simulation:
            bus.update_log(self.tick)

    def update_simulated_stops_log(self):
        for stop in self.stops:
            stop.update_stop_log()

    def update_simulated_passenger_log(self):
        for stop in self.stops:
            for route in stop.passengers_boarding_queue.keys():
                for passenger in stop.passengers_boarding_queue[route]:
                    passenger.update_waiting_time_log(self.tick)
        pass

    def remove_exited_buses(self):
        for bus in self.buses_in_simulation[:]:
            if bus.location == self.transit_network.network[-1]:
                self.buses_in_simulation.remove(bus)
                self.completed_buses.append(bus)

#MainLoop Functions
    def initialize_sim(self):
        if self.generator != None and self.passenger_data != None and self.bus_data != None:
            self.load_time_config()
            self.create_nodes()
            self.create_routes()
            self.assign_operating_routes()
            self.generate_passengers()
            self.determine_passenger_action()
            self.generate_buses()
            self.create_passenger_dispatcher()
            self.create_bus_dispatcher()
            self.populate_stops()
            self.initialize_queue_length()
            self.set_bus_star_mark() 
        else:
            raise Exception("Missing Sim Controller Data")

    def run_sim(self):
        self.simulated_time = self.tick
        while self.simulated_time < self.duration:
            self.update_intersections()
            self.check_bus_dispatcher()
            self.check_passenger_dispatcher()
            self.update_buses_in_transit()
            self.update_buses_at_stops()
            self.update_buses_at_intersections()
            self.check_bus_node_transfer()
            self.update_simulated_buses_log()
            self.update_simulated_stops_log()
            self.update_simulated_passenger_log()
            self.remove_exited_buses()
            self.simulated_time += self.tick


    def run(self):
        self.initialize_sim()
        self.run_sim()
#region Debug
    def debug(self):
        print(self.passengers[0].waiting_time_log)
        pass

    def get_results(self):
        speeds = []
        for bus in self.completed_buses:
            speeds.append(bus.speed_log)
        return speeds
#endregion Debug
