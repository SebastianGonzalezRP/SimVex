from numpy import random
import csv
import os

class Bus_Dispatcher():
    def __init__(self,generator_file):
        self.file = generator_file
        self.duration = generator_file["Time"]["Duration"]
        self.route_bus_rate = []
        self.bus_hyperparameter = []
        self.to_file = []

    
    def add_to_file(self, bus):
        self.to_file.append(bus)


    def get_bus_route_rates(self):
        for route_key, route_val in self.file['Route'].items():
            bus_rate_info = route_val['bus_rate']
            self.route_bus_rate.append((route_key, bus_rate_info))

    def get_bus_hyperparameter(self):
        self.bus_hyperparameter.append(self.file['Buses'])

    def generate_bus_arrival(self):
        for params in self.route_bus_rate:
            time = self.duration
            
            cumulative_arrival = 0
            route = params[0]
            bus_arrival_distribution = list(params[1])[0]
            bus_arrival_attributes = params[1][bus_arrival_distribution]
            while time > 0:
                id = len(self.to_file)
                arrival = self.random_value(bus_arrival_distribution, bus_arrival_attributes)
                cumulative_arrival += arrival
                door_n = random.randint(1,4)
                
                bus = [cumulative_arrival,id,route,door_n]
                self.to_file.append(bus)
            
                time -= arrival

    def random_value(self, distribution, attributes):            
        if distribution == "Exp":
            value = random.exponential(attributes["rate"])
        elif distribution == "Uniform":
            value = random.uniform(attributes["a"],attributes["b"])
        elif distribution == "Fixed":
            value = attributes["rate"]
        elif distribution == "Normal":
            value = random.normal(attributes["mu"],attributes["stdv"])
        return round(value)
    
    def sort_file(self):
        self.to_file = sorted(self.to_file, key=lambda x: x[0])

    def write_csv(self, serial):
        if not os.path.exists(f'files/{serial}'):
            os.makedirs(f'files/{serial}')
        with open(f'files/{serial}/bus_dispatcher.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for row in self.to_file:
                    writer.writerow(row)

    def generate_dispatcher_file(self,serial):
        self.get_bus_route_rates()
        self.get_bus_hyperparameter()
        self.generate_bus_arrival()
        self.sort_file()
        self.write_csv(serial)