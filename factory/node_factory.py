from models.nodes.node import Node  
from models.nodes.start import Start
from models.nodes.street import Street
from models.nodes.stop import Stop
from models.nodes.intersection import Intersection
from models.nodes.end import End

def node_generator(node):
    new_node = Node()
    node_type = list(node)[0]
    if node_type == 'Street':
        new_node = Street(length=node[node_type]["length"],
                          tracks=node[node_type]["tracks"])
    elif node_type == 'Stop':
        new_node = Stop(id=node[node_type]["id"],
                        n_platform=node[node_type]["berths"])
    elif node_type == 'Intersection':
        new_node = Intersection(cicle_duration=node[node_type]["cicle"],
                                effective_green=node[node_type]["green"])
    return new_node

