from numpy import random
import csv

class Passenger_Dispatcher():
    def __init__(self,generator_file):
        self.file = generator_file
        self.duration = generator_file["Time"]["Duration"]
        self.route_stop_passenger_rate = []
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

    def generate_passenger_arrival(self):
        for params in self.route_stop_passenger_rate:
            time = self.duration
            cumulative_arrival = 0
            while time > 0:
                id = len(self.to_file)
                route = params[0]
                stop = params[1]
                arrival_distribution = list(params[2])[0]
                arrival_dist_attributes = params[2][arrival_distribution]
                arrival = self.random_value(arrival_distribution, arrival_dist_attributes)
                cumulative_arrival += arrival

                boarding_distribution = list(self.passenger_hyperparameter[0])[0]
                boarding_dist_attributes = self.passenger_hyperparameter[0][boarding_distribution]

                boarding_t = self.random_value(boarding_distribution,boarding_dist_attributes)

                alighting_distribution = list(self.passenger_hyperparameter[1])[0]
                alighting_dist_attributes = self.passenger_hyperparameter[1][alighting_distribution]

                alighting_t = self.random_value(alighting_distribution,alighting_dist_attributes)

                passenger = [id,stop," ",route, cumulative_arrival,boarding_t,alighting_t]
                self.to_file.append(passenger)

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
        

    def write_csv(self):
        with open('passenger_dispatcher_serial.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for row in self.to_file:
                    writer.writerow(row)

    def generate_dispatcher_file(self):
        self.get_passenger_route_rates()
        self.get_passenger_hyperparameter()
        self.generate_passenger_arrival()
        self.write_csv()
