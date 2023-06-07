from nodes.stop import Stop
from nodes.intersection import Intersection
from nodes.street import Street
from passenger import Passenger


class Bus:
    def __init__(self, id, route, passengers,door_n, top_speed,acc, desc):
        self.id = id
        self.route = route
        self.passengers = passengers
        self.door_n = door_n
        self.top_speed =top_speed
        self.acc = acc #acc > 0 in m/s2
        self.desc = desc #dec > 0 in m/s2

        self.next_node = None
        self.stop_flag = False
        self.check_stop_flag = True
        self.alighting_queue = []
        self.status = None #[Stationary, Accelerating, Decelerating, Cruising]
        self.speed = None # speed > 0 in m/s
        self.location = None #Node
        self.position = None  #Relative to Node/Location First Position is Node Start

        self.breaking_point = None

        self.speed_log = []
        self.time_log = 0

    
    def board_passenger(self, passenger):
        self.passengers.append(passenger)

    def disembark_passenger(self, passenger):
        self.passengers.remove(passenger)

    def generate_alighting_queue(self):
        #Isolate all passengers descending in next node (Stop)
        alighting_passengers = []
        for passenger in self.passengers:
            if passenger.destiny == self.next_node:
                alighting_passengers.append[passenger]

        if (self.door_n == 1):
            self.alighting_queue = alighting_passengers
        else:
            quotient, remainder = divmod(len(self.passengers), self.door_n - 1)
            parts = []
            index = 0
            for i in range(self.door_n - 1):
                if i < remainder:
                    size = quotient + 1
                else:
                    size = quotient
                parts.append(self.passengers[index:index + size])
                index += size
            self.alighting_queue = parts

#region Sim Update Block

    def update_speed(self, tick):
        if self.status == "Accelerating":
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

    def update_position(self, tick):
        self.position = self.speed * tick

    def update_stop_flag(self):
        if type(self.next_node) == Stop:
            if self.route in self.next_node.serving_routes:
                if len(self.next_node.passengers_boarding_queue[self.route.id])>0:
                    self.stop_flag = True
                elif len(self.alighting_queue) > 0:
                    self.stop_flag = True
        elif type(self.next_node) == Intersection and self.check_stop_flag:
            if self.position < self.breaking_point:        # Pre Breaking Point
                if self.next_node.semaphore in ["Y","R"]:
                    self.stop_flag = True
                else:
                    self.stop_flag = False
            else:                                           # Post Breaking Point
                if self.next_node.semaphore in ["Y","G"]:
                    self.stop_flag = False
                    self.check_stop_flag = False
                else:                                       #Semaphore Red Scenario
                    self.stop_flag = True
                    self.check_stop_flag = True

    def update_breaking_point(self):
        breaking_distance = (self.speed**2)/(2*self.desc)
        last_stationary_bus_position = self.next_node.last_occupied_queue_spot()

        #TODO: 15 meters as in the dimension of a bus + some clearance space
        self.breaking_point = self.location.length - (breaking_distance + (15 * last_stationary_bus_position))


    def should_brake(self):
        if self.stop_flag and self.position >= self.breaking_point:
            self.status = "Decelerating"

#endregion Sim Update Block
#region Transfer Node Block

    #Node Transition Should be callable by controllers in conditions
    def node_transition(self):
        print(f"debug transition")
        if type(self.location) == Street:
            if self.stop_flag:
                self.go_next_node()
            else:
                self.go_next_node()
                self.go_next_node()
        else:
            self.go_next_node()
        
    
    def go_next_node(self):
        if type(self.next_node) != Street: #Case Node is at Stop or Intersection
            self.status = "Stationary"
        else:                                       #Case Node is at Street
            self.status = "Accelerating"
        self.position = 0
        self.breaking_point = 0
        self.stop_flag = False
        self.check_stop_flag = True
        self.update_reference_nodes()

    def update_reference_nodes(self):
        self.location = self.next_node
        self.next_node = self.location.next_node
        if type(self.next_node) == Stop:
            self.generate_alighting_queue()

#endregion Transfer Node Block

    def enter_simulation(self):
        self.node_transition()
        self.status = "Cruising"
        self.speed = self.top_speed
        self.update_breaking_point()
        self.update_stop_flag()



    def print_status(self):
        print(f"==================================")
        print(f"Current Location: {self.location}")
        print(f"Current Position: {self.position}")
        print(f"Current Status: {self.status}")
        print(f"Current Speed: {self.speed}")
        print(f"Next Destination: {self.next_node}")
        print(f"==================================")
        
    
        
    