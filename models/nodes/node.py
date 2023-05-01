class Node:
    def __init__(self):
        self.prev_node = None
        self.next_node = None

    def assign_prev_node(self, node):
        self.prev_node = node

    def assign_next_node(self, node):
        self.next_node = node