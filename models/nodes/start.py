from node import Node

class Start(Node):

    def assign_prev_node(self, node):
        raise NotImplementedError("Class Start can't have a previous Node")