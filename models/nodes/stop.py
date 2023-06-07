from models.nodes.node import Node
BUS_DIMENSION = 15

class Stop(Node):
    def __init__(self,id: str,n_platform: int):
        self.id = id
        self.serving_routes = []
        self.n_platform = n_platform

        self.passengers_boarding_queue = {} #Dictionary with the Route Label, and passengers queue
        self.bus_waiting_queue = None

        self.break_signal = True

    #Passengers entering the simulation at the this Stop
    def arriving_passenger(self,passenger):
        self.add_passenger_boarding_queue(passenger)

    #Passenger in this Stop boarding a Bus
    def leaving_passenger(self,passenger):
        passenger_route = passenger.route.id
        del self.passengers_boarding_queue[passenger_route][passenger]


    def build_passenger_boarding_queue(self, passenger_list):
        for passenger in passenger_list:
            self.add_passenger_boarding_queue(passenger)

    def add_passenger_boarding_queue(self,passenger):
        route_id = passenger.route.id
        if route_id not in self.passengers_boarding_queue:
            self.passengers_boarding_queue[route_id] = []
        self.passengers_boarding_queue[route_id].append(passenger)

    def calculate_queue_length(self):
        street_length = self.prev_node.length
        #TODO: BUS_DIMENSION meters as in the dimension of a bus + some clearance space
        size = street_length // BUS_DIMENSION
        self.bus_waiting_queue = [None for i in range(size - 1)]

    def arriving_bus(self, bus):
        #TODO
        pass

    def departing_bus(self, bus):
        #TODO
        pass

    def last_occupied_queue_spot(self):
        for i, item in reversed(list(enumerate(self.bus_waiting_queue))):
            if item is not None:
                return i
        return 0

    def add_route(self,route):
        self.serving_routes.append(route)
        self.passengers_boarding_queue[route.id]= []

    def print_node(self):
        print("========STOP=========")
        print(f"Stop ID: {self.id}")
        print(f"Serving Routes: {self.serving_routes}")
        print(f"Berth Numbers: {self.n_platform}")
        print("======================")


        