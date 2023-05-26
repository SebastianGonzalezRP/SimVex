from models.nodes.node import Node

class Stop(Node):
    def __init__(self,id,n_platform,):
        self.id = id
        self.serving_routes = []
        self.n_platform = n_platform
        self.passengers = []

        self.passengers_boarding_queue = None #Dictionary with the Route Label, and passengers queue
        self.bus_waiting_queue = None

        self.break_signal = True

    def arriving_passenger(self,passenger):
        self.passengers.append(passenger)
        self.add_passenger_boarding_queue(passenger)

    def leaving_passenger(self,passenger):
        self.passengers.remove(passenger)

    def build_passenger_boarding_queue(self):
        for passenger in self.passengers:
            self.add_passenger_boarding_queue(passenger)

    def add_passenger_boarding_queue(self,passenger):
        #Passenger q is determined by passenger route, but multiple routes can be useful
        route_id = passenger.route.id
        if route_id not in self.passengers_boarding_queue:
            self.passengers_boarding_queue[route_id] = []
        self.passengers_boarding_queue[route_id].append(passenger)

    def calculate_queue_length(self):
        street_length = self.prev_node.length
        #TODO: 20 meters as in the dimension of a bus + some clearance space
        size = street_length // 20
        self.bus_waiting_queue = [None for i in range(size - 1)]

    def last_occupied_queue_spot(self):
        for i, item in reversed(list(enumerate(self.bus_waiting_queue))):
            if item is not None:
                return i

    def print_node(self):
        print("========STOP=========")
        print(f"Stop ID: {self.id}")
        print(f"Berth Numbers: {self.n_platform}")
        print("======================")


        