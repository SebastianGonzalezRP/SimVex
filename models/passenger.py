class Passenger:
    def __init__(self, id, route, t_in, origin, destiny):
        self.id = id
        self.route = route
        self.t_in = t_in
        self.origin = origin
        self.destiny = destiny
        self.position = None

    

    #TODO: Update class for it to build possible route option based on the origin and destiny attributes