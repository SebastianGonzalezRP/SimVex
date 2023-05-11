class Passenger:
    def __init__(self, origin, destiny, route, boarding_t, alighting_t):
        self.origin = origin
        self.destiny = destiny
        self.route = route
        self.boarding_time = boarding_t
        self.alighting_time = alighting_t
        self.location = None

    #TODO: Update class for it to build possible route option based on the origin and destiny attributes