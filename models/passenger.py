class Passenger:
    def __init__(self, id, origin, destiny, boarding_t, alighting_t, location):
        self.id = id
        self.origin = origin
        self.destiny = destiny
        self.boarding_time = boarding_t
        self.alighting_time = alighting_t
        self.location = location

    #TODO: Update class for it to build possible route option based on the origin and destiny attributes