from node import Node

class End(Node):

    def assign_next_node(self, node):
        raise NotImplementedError("Class End can't have a next Node")