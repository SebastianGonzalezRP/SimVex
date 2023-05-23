from numpy import random
import csv

class Passenger_Dispatcher():
    def __init__(self,generator_file):
        self.file = generator_file
        self.duration = generator_file["Time"]["Duration"]
        self.route_stop_passenger_rate = []
        self.bus_dispatch_rate = {}
        self.passenger_hyperparameter = []
        self.to_file = []

    def get_passenger_route_rates(self, ):
        for route_key, route_val in self.file['Route'].items():
            for stop_key, stop_val in route_val['stops'].items():
                passenger_rate_info = stop_val['passenger_rate']
                self.route_stop_passenger_rate.append([route_key, stop_key, passenger_rate_info])

    def get_passenger_hyperparameter(self):
        self.passenger_hyperparameter.append(self.file['Passenger']['boarding_time_dist'])
        self.passenger_hyperparameter.append(self.file['Passenger']['alighting_time_dist'])

    def get_bus_dispatch_rates(self):
        for route_id, route_data in self.file["Route"].items():
            bus_rate = route_data["bus_rate"]
            self.bus_dispatch_rate[route_id] = bus_rate

    def generate_passenger_stop_arrival(self):
        for params in self.route_stop_passenger_rate:
            time = self.duration
            
            cumulative_arrival = 0
            route = params[0]
            stop = params[1]
            passenger_arrival_distribution = list(params[2])[0]
            passenger_arrival_dist_attributes = params[2][passenger_arrival_distribution]

            while time > 0:
                id = len(self.to_file)
                
                arrival = self.random_value(passenger_arrival_distribution, passenger_arrival_dist_attributes)
                cumulative_arrival += arrival

                boarding_distribution = list(self.passenger_hyperparameter[0])[0]
                boarding_dist_attributes = self.passenger_hyperparameter[0][boarding_distribution]

                boarding_t = self.random_value(boarding_distribution,boarding_dist_attributes)

                alighting_distribution = list(self.passenger_hyperparameter[1])[0]
                alighting_dist_attributes = self.passenger_hyperparameter[1][alighting_distribution]

                alighting_t = self.random_value(alighting_distribution,alighting_dist_attributes)

                passenger = [cumulative_arrival,id,stop," ",route,boarding_t,alighting_t]
                self.to_file.append(passenger)

                time -= arrival

            bus_arrival_distribution = list(self.bus_dispatch_rate[route])[0]
            bus_arrival_attributes = self.bus_dispatch_rate[route][bus_arrival_distribution]
            virtual_time = self.random_value(bus_arrival_distribution, bus_arrival_attributes)

            while virtual_time > 0:
                id = len(self.to_file)
                
                arrival = self.random_value(passenger_arrival_distribution, passenger_arrival_dist_attributes)

                boarding_distribution = list(self.passenger_hyperparameter[0])[0]
                boarding_dist_attributes = self.passenger_hyperparameter[0][boarding_distribution]

                boarding_t = self.random_value(boarding_distribution,boarding_dist_attributes)

                alighting_distribution = list(self.passenger_hyperparameter[1])[0]
                alighting_dist_attributes = self.passenger_hyperparameter[1][alighting_distribution]

                alighting_t = self.random_value(alighting_distribution,alighting_dist_attributes)

                passenger = [0,id,stop," ",route,boarding_t,alighting_t]
                self.to_file.append(passenger)

                virtual_time -= arrival
                
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

    def write_csv(self):
        with open('passenger_dispatcher_serial.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for row in self.to_file:
                    writer.writerow(row)

    def generate_dispatcher_file(self):
        self.get_passenger_route_rates()
        self.get_bus_dispatch_rates()
        self.get_passenger_hyperparameter()
        self.generate_passenger_stop_arrival()
        self.sort_file()
        self.write_csv()

    
