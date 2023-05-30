from factory.file_generator.utils import *
from factory.file_generator.dispatcher import Dispatcher


#PASSENGER:  [t_in, origin, destiny, route,  boarding_t, alighting_t]

class Passenger_Dispatcher(Dispatcher):
    def __init__(self,generator_file):
        super().__init__(generator_file)

        self.route_stop_passenger_rate = []
        self.bus_dispatch_rate = {}
        self.passenger_hyperparameter = []
        self.to_file = []

    def get_passenger_route_rates(self):
        for route_key, route_val in self.generator['Route'].items():
            for stop_key, stop_val in route_val['stops'].items():
                passenger_rate_info = stop_val['passenger_rate']
                self.route_stop_passenger_rate.append([route_key, stop_key, passenger_rate_info])

    def get_passenger_hyperparameter(self):
        self.passenger_hyperparameter.append(self.generator['Passenger']['boarding_time_dist'])
        self.passenger_hyperparameter.append(self.generator['Passenger']['alighting_time_dist'])

    def get_possible_destinations(self,route,origin):
        possible_destinations = []
        for _route in self.routes:
            if _route.id == route:
                possible_destinations = _route.get_remaining_stops_id(origin)
        possible_destinations.append("end")
        return possible_destinations

    def random_posible_destination(self,route,origin):
        possible_destinations = self.get_possible_destinations(route,origin)
        return random.choice(possible_destinations)

    def get_bus_dispatch_rates(self):
        for route_id, route_data in self.generator["Route"].items():
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
                arrival = random_value(passenger_arrival_distribution, passenger_arrival_dist_attributes)
                cumulative_arrival += arrival

                destination = self.random_posible_destination(route,stop)

                boarding_distribution = list(self.passenger_hyperparameter[0])[0]
                boarding_dist_attributes = self.passenger_hyperparameter[0][boarding_distribution]

                boarding_t = random_value(boarding_distribution,boarding_dist_attributes)

                alighting_distribution = list(self.passenger_hyperparameter[1])[0]
                alighting_dist_attributes = self.passenger_hyperparameter[1][alighting_distribution]

                alighting_t = random_value(alighting_distribution,alighting_dist_attributes)

                passenger = [cumulative_arrival,stop,destination,route,boarding_t,alighting_t]
                self.to_file.append(passenger)

                time -= arrival

            bus_arrival_distribution = list(self.bus_dispatch_rate[route])[0]
            bus_arrival_attributes = self.bus_dispatch_rate[route][bus_arrival_distribution]
            virtual_time = random_value(bus_arrival_distribution, bus_arrival_attributes)

            while virtual_time > 0:
                arrival = random_value(passenger_arrival_distribution, passenger_arrival_dist_attributes)

                destination = self.random_posible_destination(route,stop)

                boarding_distribution = list(self.passenger_hyperparameter[0])[0]
                boarding_dist_attributes = self.passenger_hyperparameter[0][boarding_distribution]

                boarding_t = random_value(boarding_distribution,boarding_dist_attributes)

                alighting_distribution = list(self.passenger_hyperparameter[1])[0]
                alighting_dist_attributes = self.passenger_hyperparameter[1][alighting_distribution]

                alighting_t = random_value(alighting_distribution,alighting_dist_attributes)

                passenger = [0,stop,destination,route,boarding_t,alighting_t]
                self.to_file.append(passenger)

                virtual_time -= arrival
                

    def generate_dispatcher_file(self,serial):
        self.get_passenger_route_rates()
        self.get_bus_dispatch_rates()
        self.get_passenger_hyperparameter()
        self.generate_passenger_stop_arrival()
        self.to_file = sort_file(self.to_file,0)
        write_csv(self.to_file,serial,"passenger_dispatcher.csv")

    
