from numpy import random
from factory.node_factory import *
from models.route import Route
from models.transit_network import TransitNetwork as TN
import csv
import os

def random_value(distribution, attributes):            
        if distribution == "Exp":
            value = random.exponential(attributes["rate"])
        elif distribution == "Uniform":
            value = random.uniform(attributes["a"],attributes["b"])
        elif distribution == "Normal":
            value = random.normal(attributes["mu"],attributes["stdv"])
        elif distribution == "Fixed":
            value = attributes["rate"]
        return round(value)

def sort_file(data,sort_index):
        data = sorted(data, key=lambda x: x[sort_index])
        return data

def write_csv(data,serial,file_name):
        if not os.path.exists(f'files/{serial}'):
            os.makedirs(f'files/{serial}')
        with open(f'files/{serial}/{file_name}', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in data:
                writer.writerow(row)

def create_nodes(generator):
    transit_network  = []
    for node in generator["Node"]:
        new_node = node_generator(node)
        transit_network.append(new_node)
        transit_network = TN(transit_network)
    return transit_network

def create_routes(generator):
        routes = []
        route_data = generator["Route"]
        for route_id, route_info in route_data.items():
            stops = list(route_info["stops"].keys())
            serving_stops = []
            for node in create_nodes(generator):
                if type(node) == Stop:
                    if node.id in stops:
                        serving_stops.append(node)
            new_route = Route(route_id, serving_stops)
            routes.append(new_route)
        return routes


def generate_route_object():
    pass