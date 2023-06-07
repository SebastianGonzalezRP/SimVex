from models.nodes.node import Node

class Street(Node):
    def __init__(self, tracks: int, length: int):
        self.tracks = tracks #Number of tracks controls if buses can "overtake"
        self.length = length

        self.breaking_point = None #Distance from the start of node where Bus Should Start To Brake
        self.breaking_point_active = False #Breaking Point Always Active Before Stop. Not Always Active Before Intersection.


    def print_node(self):
        print("======Street===========")
        print(f"Tracks Numbers: {self.tracks}")
        print(f"Street Length: {self.length}")
        print("======================")