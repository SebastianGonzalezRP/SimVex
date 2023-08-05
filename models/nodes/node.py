class Node:
    def __init__(self):
        self.prev_node = None
        self.next_node = None

    def assign_prev_node(self, node):
        self.prev_node = node

    def assign_next_node(self, node):
        self.next_node = node

    def print_node(self):
        pass

    def print_adjacent_nodes(self):
        print(f"{self.prev_node}|{self}|{self.next_node}")