from models.nodes.stop import Stop
from models.nodes.intersection import Intersection
from models.nodes.street import Street
from models.passenger import Passenger


class Bus:
    def __init__(self, id, route, passengers,door_n, top_speed,acc, desc, capacity):
        self.id = id
        self.route = route
        self.passengers = passengers
        self.door_n = door_n
        self.top_speed =top_speed
        self.acc = acc #acc > 0 in m/s2
        self.desc = desc #dec > 0 in m/s2
        self.capacity = capacity

        self.next_stop = None
        self.next_destination = None
        self.alighting_queue = self.generate_alighting_queue()
        self.status = None #[Stationary, Accelerating, Decelerating, Cruising]
        self.speed = None # speed > 0 in m/s
        self.location = None #Node
        self.position = None  #Relative to Node/Location First Position is Node Start

        self.breaking_point = None



    def update_position(self, tick):
        #A bus can only be "Stationary" at stops and intersections
        #TODO:BIG TODO!!!!

        if isinstance(self.next_destination,Stop):
            pass
        elif isinstance(self.next_destination,Intersection):

            pass
        else:
            pass

    def update_speed(self, tick):
        if self.status == "Stationary":
            pass
        elif self.status == "Accelerating":
            if (self.speed + self.acc * tick) >= self.top_speed:
                self.speed = self.top_speed
                self.status = "Cruising"
            else:
                self.speed += self.acc * tick
        elif self.status == "Decelerating":
            if (self.speed - self.desc * tick) <= 0:
                self.speed = 0
                self.status = "Stationary"
            else:
                self.speed -= self.desc * tick
        elif self.status == "Cruising":
            pass


    def assign_next_stop(self):
        current_node = self.location
        if current_node != None:
            while not isinstance(current_node.next_node, Stop):
                current_node = current_node.next_node
            self.next_stop = current_node.next_node
        else:
            raise Exception("Bus Locations Unassigned")
        
    def generate_alighting_queue(self):
        #Isolate all passengers descending in next stop
        alighting_passengers = []
        for passenger in self.passengers:
            if passenger.destiny == self.next_stop:
                alighting_passengers.append[passenger]

        if (self.door_n == 1):
            self.alighting_queue = alighting_passengers
        else:
            quotient, remainder = divmod(len(self.passengers), self.door_n - 1)
            parts = []
            index = 0
            for i in range(n):
                if i < remainder:
                    size = quotient + 1
                else:
                    size = quotient
                parts.append(self.passengers[index:index + size])
                index += size
            self.alighting_queue = parts
    
    def board_passenger(self, passenger):
        self.passengers.append(passenger)

    def disembark_passenger(self, passenger):
        self.passengers.remove(passenger)

    def determine_next_stop(self):
        #TODO
        pass

    def update_breaking_point(self):
        breaking_distance = (self.speed**2)/(2*self.desc)
        last_stationary_bus_position = self.next_destination.last_occupied_queue_spot()

        #TODO: 20 meters as in the dimension of a bus + some clearance space
        self.breaking_point = (breaking_distance + (20 * last_stationary_bus_position))

        
    
        
    