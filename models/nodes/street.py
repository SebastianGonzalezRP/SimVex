from models.nodes.node import Node

class Street(Node):
    def __init__(self, tracks, length):
        self.tracks = tracks #Number of tracks controls if buses can "overtake"
        self.length = length

        self.breaking_point = None #Distance from the start of node where Bus Should Start To Brake
        self.breaking_point_active = False #Breaking Point Always Active Before Stop. Not Always Active Before Intersection.


    def calculate_breaking_point(self):
        #TODO
        pass

    def update_breaking_point(self):
        #TODO
        pass