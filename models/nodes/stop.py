from models.nodes.node import Node
BUS_DIMENSION = 15

class Stop(Node):
    def __init__(self,id: str,n_platform: int):
        self.id = id
        self.serving_routes = []
        self.n_platform = n_platform

        self.passengers_boarding_queue = {} #Dictionary with the Route Label, and passengers queue
        self.bus_operational_queue =[None for i in range(n_platform)]
        self.bus_waiting_queue = []


    #Passengers entering the simulation at the this Stop
    def arriving_passenger(self,passenger):
        self.add_passenger_boarding_queue(passenger)

    #Passenger in this Stop boarding a Bus
    def leaving_passenger(self,passenger):
        passenger_route = passenger.route.id
        self.passengers_boarding_queue[passenger_route].remove(passenger)


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
        size = (street_length // BUS_DIMENSION) - self.n_platform
        self.bus_waiting_queue = [None for i in range(size - 1)]

    def arriving_bus(self, bus):
        if None in self.bus_operational_queue:
            for index, spot in enumerate(self.bus_operational_queue):
                if spot == None:
                    self.bus_operational_queue[index] = bus
                    break
        else:
            for index, spot in enumerate(self.bus_waiting_queue):
                if spot == None:
                    self.bus_waiting_queue[index] = bus
                    break
        
    def departing_bus(self, bus):
        try:
            index = self.bus_operational_queue.index(bus)
            self.bus_operational_queue[index] = None
        except ValueError:
            print("Bus Is Not In The Stop Operational Queue")

    def reorganize_queues(self):
        if sum(1 for spot in self.bus_waiting_queue if spot is not None) > 0:
            spaces_operational_queue = self.bus_operational_queue.count(None)
            if spaces_operational_queue > 0:
                split_index = self.first_available_operational_queue_spot()

                slice1 = self.bus_operational_queue[:split_index]
                slice2 = self.bus_operational_queue[split_index:]

                slice3 = self.bus_waiting_queue[len(slice2):]
                slice4 = self.bus_waiting_queue[:len(slice2)]

                self.bus_operational_queue = slice1 + slice3
                self.bus_waiting_queue = slice4 + slice2


    def first_available_operational_queue_spot(self):
        for i, item in reversed(list(enumerate(self.bus_operational_queue))):
            if item is not None:
                return i + 1
        return 0
    
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


        