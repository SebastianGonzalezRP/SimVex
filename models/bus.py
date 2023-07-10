from models.nodes.start import Start
from models.nodes.stop import Stop
from models.nodes.intersection import Intersection
from models.nodes.street import Street
from models.route import Route
from models.passenger import Passenger
from typing import List


class Bus:
    def __init__(self,
                 arrival_time:int, 
                 id: str,
                 route: Route, 
                 door_n: int, 
                 top_speed: float, 
                 acc: float, 
                 desc: float):
    
        self.arrival_time = arrival_time

        self.id = id
        self.route = route
        
        self.door_n = door_n
        self.top_speed =top_speed
        self.acc = acc #acc > 0 in m/s2
        self.desc = desc #dec > 0 in m/s2

        self.next_node = None
        self.stop_flag = False
        self.check_stop_flag = True
        self.alighting_queues = []
        self.status = None #[Stationary, Accelerating, Decelerating, Cruising]
        self.speed = None # speed > 0 in m/s
        self.location = None #Node
        self.position = None  #Relative to Node/Location First Position is Node Start
        self.traveled_distance = 0

        self.passengers = []

        self.breaking_point = None

        self.speed_log = []
        self.time_log = 0

    
    def board_passenger(self, passenger):
        self.passengers.append(passenger)

    def disembark_passenger(self, passenger):
        self.passengers.remove(passenger)
        for alighting_queue in self.alighting_queues:
            if passenger in alighting_queue:
                alighting_queue.remove(passenger)

    def generate_alighting_queues(self):
        #Isolate all passengers descending in next node (Stop)
        alighting_passengers = []
        for passenger in self.passengers:
            if passenger.destiny == self.next_node.id:
                alighting_passengers.append(passenger)

        if (self.door_n <= 2):
            self.alighting_queues = [alighting_passengers]
        else:
            quotient, remainder = divmod(len(alighting_passengers), self.door_n - 1)
            parts = []
            index = 0
            for i in range(self.door_n - 1):
                if i < remainder:
                    size = quotient + 1
                else:
                    size = quotient
                parts.append(alighting_passengers[index:index + size])
                index += size
            self.alighting_queues = parts

#region Street Circulation Methods

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
        self.speed = round(self.speed,2)

    def update_position(self, tick):
        self.position += self.speed * tick
        self.traveled_distance += self.speed * tick

    def update_stop_flag(self):
        if type(self.next_node) == Stop:
            if self.route in self.next_node.serving_routes:
                if len(self.next_node.passengers_boarding_queue[self.route.id])>0:
                    self.stop_flag = True
                elif len(self.alighting_queues) > 0:
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
        if type(self.next_node) in [Stop, Intersection]:
            breaking_distance = (self.speed**2)/(2*self.desc)
            last_stationary_bus_position = self.next_node.last_occupied_queue_spot()

            self.breaking_point = self.location.length - (breaking_distance + (15 * last_stationary_bus_position))
        else:
            self.breaking_point = 0


    def should_brake(self):
        if self.stop_flag and self.position >= self.breaking_point:
            self.status = "Decelerating"

#endregion

#region Stop Operations Methods
    def passenger_transfer(self, tick):
        stop = self.location
        route = self.route.id

        if len(stop.passengers_boarding_queue[route]) == 0:
            if sum(len(queue) for queue in self.alighting_queues) == 0:
                stop.departing_bus(self)
                self.node_transition()
                
        #Boarding Passengers
        if len(stop.passengers_boarding_queue[route]) > 0:
            passenger = stop.passengers_boarding_queue[route][0]
            if passenger.boarding_time - tick <=0:
                self.board_passenger(passenger)
                stop.leaving_passenger(passenger)
            else:
                passenger.boarding_time -= tick

        #Alighting Passenger 
        for alighting_q in self.alighting_queues[:]:
            if len(alighting_q) > 0:
                passenger = alighting_q[0]
                if passenger.alighting_time - tick <=0:
                    self.disembark_passenger(passenger)
                else:
                    passenger.alighting_time -= tick

    def check_queue_departure_conditions(self):
        #assert (type(self.location),Stop)
        stop = self.location
        position = stop.bus_operational_queue.index(self)
        if position == 0:
            return True
        else:
            if stop.bus_operational_queue[0] == None:
                return True 
            elif self.next_node.tracks > 1:
                return True
            else:
                return False
            
    def check_operation_completion(self,tick):
        stop = self.location
        route = self.route.id
        if len(stop.passengers_boarding_queue[route]) == 0:
            if sum(len(queue) for queue in self.alighting_queues) == 0:
                if self.check_queue_departure_conditions():
                    stop.departing_bus(self)
                    self.node_transition()
        else:
            self.passenger_transfer(tick)

    def check_operational_position_in_queue(self,tick):
        stop = self.location
        if self in stop.bus_operational_queue:
            self.check_operation_completion(tick)
        elif self in stop.bus_waiting_queue:
            pass
        else:
            stop.arriving_bus(self)

#endregion

#region Log
    def update_log_speed(self):
        self.speed_log.append(self.speed)

    def update_log_time(self, tick):
        self.time_log += tick

    def update_log(self,tick):
        self.update_log_speed()
        self.update_log_time(tick)
#endregion

#region Transfer Node Block

    #Node Transition Should be callable by controllers in conditions
    def node_transition(self):
        if type(self.location) == Street:
            if self.stop_flag:
                self.go_next_node()
            else:
                self.go_next_node()
                self.go_next_node()
        else:
            self.go_next_node()
        
    
    def go_next_node(self):
        if type(self.next_node) in [Stop, Intersection]: #Case Node is at Stop or Intersection
            if self.stop_flag:
                self.status = "Stationary"
                self.speed = 0
                self.next_node.arriving_bus(self)
        else:                                       #Case Node is at Street
            self.status = "Accelerating"
        self.position = 0
        self.breaking_point = 0
        self.stop_flag = False
        self.check_stop_flag = True
        self.update_reference_nodes()

    def update_reference_nodes(self):
        if type(self.location) in [Start, Street,Stop,Intersection]:
            self.location = self.next_node
            self.next_node = self.location.next_node
            if type(self.next_node) == Stop:
                self.generate_alighting_queues()

#endregion Transfer Node Block

    def enter_simulation(self):
        self.node_transition()
        self.status = "Cruising"
        self.speed = self.top_speed
        self.update_breaking_point()
        self.update_stop_flag()


#region Debug
    def print_status(self):
        print(f"==================================")
        print(f"Current Location: {self.location}")
        print(f"Current Position: {self.position}")
        print(f"Alighting Queue: {self.alighting_queues}")
        print(f"Current Status: {self.status}")
        print(f"Current Speed: {self.speed}")
        print(f"Next Destination: {self.next_node}")
        print(f"==================================")

#endregion
        
    
        
    