from models.nodes.start import Start
from models.nodes.end import End


#nodes =  list of nodes of type [Street, Stop, Intersection], initially unlinked

class TransitNetwork():
    def __init__(self, nodes):
        self.network =  TransitNetwork.create_network(nodes)

    # Links the node elements and adds a Start and End node to the nodes list
    @staticmethod
    def create_network(nodes):
        start = Start()
        end = End()
        start.assign_next_node(nodes[0])
        for i, node in enumerate(nodes):
            if i == 0:
                node.assign_prev_node(start)
                node.assign_next_node(nodes[i+1])
            if i > 0:
                node.assign_prev_node(nodes[i-1])
            if i < len(nodes) - 1:
                node.assign_next_node(nodes[i+1])
            if i == len(nodes) - 1:
                node.assign_next_node(end)
                end.assign_prev_node(node)

        nodes.insert(0,start)
        nodes.append(end)
        return nodes
            