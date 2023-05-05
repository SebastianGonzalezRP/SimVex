from models.nodes.node import Node

class Intersection(Node):
    def __init__(self,semaphore, cicle_duration, effective_green):
        self.semaphore = semaphore #["G","Y","R"]
        self.cicle_duration = cicle_duration #Seconds
        self.effective_green = effective_green #Percentage (0,1) ej: 0.75

        self.g_timer = self.calculate_g_timer()
        self.y_timer = 3
        self.r_timer = self.calculate_r_timer()
        self.current_timer_left = self.g_timer
        
        self.bus_waiting_queue = None
        self.break_signal = False

    def calculate_g_timer(self):
        self.g_timer = self.cicle_duration * self.effective_green

    def calculate_r_timer(self):
        self.r_timer = self.cicle_duration - self.g_timer - self.y_timer

    def activate_g_light(self):
        self.current_timer_left = self.g_timer
        self.semaphore = "G"
        self.break_signal = False

    def activate_y_light(self):
        self.current_timer_left = self.y_timer
        self.semaphore = "Y"
        self.break_signal = True

    def activate_r_light(self):
        self.current_timer_left = self.r_timer
        self.semaphore = "R"
        self.break_signal = True

    def update_timer(self,tick):
        if self.current_timer_left - tick <= 0:
            time_remaining = tick - self.current_timer_left
            if self.semaphore == "G":
                self.activate_y_light
            elif self.semaphore == "Y":
                self.activate_r_light
            elif self.semaphore == "R":
                self.activate_g_light
            self.current_timer_left - time_remaining
        else:
            self.current_timer_left - tick

    def calculate_queue_length(self):
        street_length = self.prev_node.length
        #TODO: 20 meters as in the dimension of a bus + some clearance space
        size = street_length // 20
        self.bus_waiting_queue = [None for i in range(size - 1)]
        

    def last_occupied_queue_spot(self):
        for i, item in reversed(list(enumerate(self.bus_waiting_queue))):
            if item is not None:
                return i