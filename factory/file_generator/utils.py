from numpy import random
from factory.node_factory import *
from models.route import Route
from models.transit_network import TransitNetwork as TN
import datetime

import csv
import json
import os

def random_value(distribution, attributes):            
        if distribution == "Exponential":
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

#region File Manipulation
def create_path(serial):
    if not os.path.exists(f'files/{serial}'):
        os.makedirs(f'files/{serial}')

def write_json(data,serial,file_name):
    create_path(serial)
    with open(f'files/{serial}/{file_name}', 'a') as json_file:
        json.dump(data, json_file)

def write_csv(data,serial,file_name):
    create_path(serial)
    with open(f'files/{serial}/{file_name}', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)

def load_json(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data

def load_csv(path):
    data = []
    with open(path, 'r') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            data.append(line)
    return data

#endregion

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

def generate_serial():
        current_datetime = datetime.datetime.now()
        year = current_datetime.year
        month = current_datetime.month
        day = current_datetime.day
        hour = current_datetime.hour
        minutes = current_datetime.minute
        serial = f'{year}_{month}_{day}_{hour}{minutes}'
        return serial