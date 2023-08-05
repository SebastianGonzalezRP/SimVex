from models.route import Route

class Passenger:
    def __init__(self, 
                 arrival_time: int,
                 origin: str, 
                 destiny: str, 
                 route: Route, 
                 boarding_t: int, 
                 alighting_t: int):
        
        self.arrival_time = arrival_time
        self.origin = origin
        self.destiny = destiny
        self.route = route
        self.boarding_time = boarding_t
        self.alighting_time = alighting_t

        self.waiting_time_log = 0

    def update_waiting_time_log(self,tick):
        self.waiting_time_log += tick

    def print_self(self):
        print("====================================")
        print(f"Arriving Time: {self.arrival_time}")
        print(f"Origin: {self.origin}")
        print(f"Destiny: {self.destiny}")
        print(f"Route: {self.route.id}")
        print(f"Boarding T: {self.boarding_time}")
        print(f"Alighting T: {self.alighting_time}")
        print("====================================\n")



