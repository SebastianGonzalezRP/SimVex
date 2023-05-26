import json
import csv
from factory.node_factory import *
from models.transit_network import TransitNetwork as TN

class Sim_Controller:
    def __init__(self,generator_path,psngr_dispatch_path,bus_dispatch_path):
        self.generator = self.load_json(generator_path)
        self.psngr_dispatcher = self.load_csv(psngr_dispatch_path)
        self.bus_dispatcher = self.load_csv(bus_dispatch_path)

        self.nodes = []
        

        pass

    def load_json(self, path):
        with open(path, 'r') as file:
            data = json.load(file)
        return data

    def load_csv(self, path):
        data = []
        with open(path, 'r') as file:
            csv_reader = csv.reader(file)
            for line in csv_reader:
                data.append(line)
        return data
    
    def debug(self):
        for element in self.bus_dispatcher:
            print (element)

    def create_nodes(self):
        for node in self.generator["Node"]:
            new_node = node_generator(node)
            new_node.print_node()
            self.nodes.append(new_node)
        self.nodes = TN(self.nodes)
    