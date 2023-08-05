from factory.node_factory import *
from models.transit_network import TransitNetwork as TN
from models.route import Route

class Dispatcher():
    def __init__(self, generator_file):
        self.generator = generator_file
        self.duration = generator_file["Time"]["Duration"]
        self.transit_network = []
        self.nodes = []
        self.routes = []

        self.create_nodes()
        self.create_routes()

    def create_nodes(self):
        for node in self.generator["Node"]:
            new_node = node_generator(node)
            self.transit_network.append(new_node)
        self.transit_network = TN(self.transit_network)

    def create_routes(self):
        route_data = self.generator["Route"]
        for route_id, route_info in route_data.items():
            stops = list(route_info["stops"].keys())
            serving_stops = []
            for node in self.transit_network.network:
                if type(node) == Stop:
                    if node.id in stops:
                        serving_stops.append(node)
            new_route = Route(route_id, serving_stops)
            self.routes.append(new_route)
        