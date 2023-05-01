from models.nodes.node import Node

class Stop(Node):
    def __init__(self,id,serving_routes,n_platform,passengers,passenger_limit):
        self.id = id
        self.serving_routes = serving_routes
        self.n_platform = n_platform
        self.passengers = passengers

        self.passengers_boarding_queue = None #Dictionary with the Route Label, and passengers queue
        self.bus_waiting_queue = None

    def arriving_passanger(self,passenger):
        self.passengers.append(passenger)

    def leaving_passenger(self,passenger):
        self.passengers.remove(passenger)
        
    def 