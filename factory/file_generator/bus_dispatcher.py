from factory.file_generator.utils import *

from factory.file_generator.dispatcher import Dispatcher


#BUS: [t_in, ID, route, model]


class Bus_Dispatcher(Dispatcher):
    def __init__(self,generator_file):
        super().__init__(generator_file)
        self.route_bus_rate = []
        self.bus_hyperparameter = []
        self.to_file = []
        self.boarded_passenger = []
        self.passenger_hyperparameter = []

    
    def add_to_file(self, bus):
        self.to_file.append(bus)


    def get_bus_route_rates(self):
        for route_key, route_val in self.generator['Route'].items():
            bus_rate_info = route_val['bus_rate']
            self.route_bus_rate.append((route_key, bus_rate_info))

    def generate_bus_arrival(self):
        for params in self.route_bus_rate:
            time = self.duration
            
            cumulative_arrival = 0
            route = params[0]
            bus_arrival_distribution = list(params[1])[0]
            bus_arrival_attributes = params[1][bus_arrival_distribution]
            while time > 0:
                id = len(self.to_file)
                arrival = random_value(bus_arrival_distribution, bus_arrival_attributes)
                cumulative_arrival += arrival
                model_list = list(self.generator["Route"][route]["bus_model"].keys())
                model = random.choice(model_list)
                
                bus = [cumulative_arrival,f"b-{id}",route,model]
                if cumulative_arrival<time:
                    self.to_file.append(bus)
            
                time -= arrival
    
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

    def generate_boarded_passengers(self):
        self.passenger_hyperparameter.append(self.generator['Passenger']['boarding_time_dist'])
        self.passenger_hyperparameter.append(self.generator['Passenger']['alighting_time_dist'])
        for bus in self.to_file:
            bus_arrival = bus[0]
            bus_id = bus[1]
            bus_route = bus[2]

            occupancy_distribution = list(self.generator["Route"][bus_route]["initial_occupancy"])[0]
            occupancy_rate = self.generator["Route"][bus_route]["initial_occupancy"][occupancy_distribution]

            passenger_count = random_value(occupancy_distribution,occupancy_rate)

            for i in range(passenger_count):
                boarding_distribution = list(self.passenger_hyperparameter[0])[0]
                boarding_dist_attributes = self.passenger_hyperparameter[0][boarding_distribution]

                destination = self.random_posible_destination(bus_route,"start")

                boarding_t = random_value(boarding_distribution,boarding_dist_attributes)

                alighting_distribution = list(self.passenger_hyperparameter[1])[0]
                alighting_dist_attributes = self.passenger_hyperparameter[1][alighting_distribution]

                alighting_t = random_value(alighting_distribution,alighting_dist_attributes)

                #PASSENGER:  [t_in, origin, destiny, route,  boarding_t, alighting_t]
                passenger = [bus_arrival,bus_id,destination,bus_route,boarding_t,alighting_t]
                self.boarded_passenger.append(passenger)
        

    def generate_dispatcher_file(self,serial):
        self.get_bus_route_rates()
        self.generate_bus_arrival()
        self.generate_boarded_passengers()
        write_csv(self.boarded_passenger,serial,"passenger_dispatcher.csv")
        self.to_file = sort_file(self.to_file,0)
        write_csv(self.to_file,serial,"bus_dispatcher.csv")