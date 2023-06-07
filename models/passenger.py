from models.route import Route

class Passenger:
    def __init__(self, 
                 origin: str, 
                 destiny: str, 
                 route: Route, 
                 boarding_t: int, 
                 alighting_t: int):
        
        self.origin = origin
        self.destiny = destiny
        self.route = route
        self.boarding_time = boarding_t
        self.alighting_time = alighting_t


