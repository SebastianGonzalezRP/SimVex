from models.nodes.node import Node

class Street(Node):
    def __init__(self, tracks: int, length: int):
        self.tracks = tracks #Number of tracks controls if buses can "overtake"
        self.length = length


    def print_node(self):
        print("======Street===========")
        print(f"Tracks Numbers: {self.tracks}")
        print(f"Street Length: {self.length}")
        print("======================")