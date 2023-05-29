from numpy import random
import csv
import os

#BUS: [t_in, ID, route, door_n]

class Bus_Dispatcher():
    def __init__(self,generator_file):
        self.file = generator_file
        self.duration = generator_file["Time"]["Duration"]
        self.route_bus_rate = []
        self.bus_hyperparameter = []
        self.to_file = []

        self.boarded_passenger = []
        self.passenger_hyperparameter = []

    
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
                
                bus = [cumulative_arrival,f"b-{id}",route,door_n]
                self.to_file.append(bus)
            
                time -= arrival
    
    def generate_boarder_passengers(self):
        self.passenger_hyperparameter.append(self.file['Passenger']['boarding_time_dist'])
        self.passenger_hyperparameter.append(self.file['Passenger']['alighting_time_dist'])
        for bus in self.to_file:
            bus_arrival = bus[0]
            bus_id = bus[1]
            bus_route = bus[2]

            occupancy_distribution = list(self.file["Route"][bus_route]["initial_occupancy"])[0]
            occupancy_rate = self.file["Route"][bus_route]["initial_occupancy"][occupancy_distribution]

            passenger_count = self.random_value(occupancy_distribution,occupancy_rate)

            for i in range(passenger_count):
                id = "TEST_ID"
                boarding_distribution = list(self.passenger_hyperparameter[0])[0]
                boarding_dist_attributes = self.passenger_hyperparameter[0][boarding_distribution]

                boarding_t = self.random_value(boarding_distribution,boarding_dist_attributes)

                alighting_distribution = list(self.passenger_hyperparameter[1])[0]
                alighting_dist_attributes = self.passenger_hyperparameter[1][alighting_distribution]

                alighting_t = self.random_value(alighting_distribution,alighting_dist_attributes)

                passenger = [bus_arrival,id,bus_id," ",bus_route,boarding_t,alighting_t]
                self.boarded_passenger.append(passenger)
        

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

    def write_boarded_passengers(self, serial):
        if not os.path.exists(f'files/{serial}'):
            os.makedirs(f'files/{serial}')
        with open(f'files/{serial}/passenger_dispatcher.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for row in self.boarded_passenger:
                    writer.writerow(row)

    def generate_dispatcher_file(self,serial):
        self.get_bus_route_rates()
        self.get_bus_hyperparameter()
        self.generate_bus_arrival()
        self.generate_boarder_passengers()
        self.write_boarded_passengers(serial)
        self.sort_file()
        self.write_csv(serial)