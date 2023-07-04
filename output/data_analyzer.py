from factory.file_generator.pdf_generator import PDFGenerator
from models.nodes.street import Street
from models.nodes.stop import Stop
from models.nodes.intersection import Intersection
import matplotlib.pyplot as plt


class DataAnalyzer:
    def __init__(self, sim_controller,serial):
        self.sim_c = sim_controller
        self.PDFG = PDFGenerator(serial)


        #metadata
        self.stop_list = []
        self.route_list = []
        self.simulated_buses_id = []
        self.simulation_length = 0
        self.simulated_buses = 0

        self.boarding_demand = 0
        self.alight_demand = 0

        self.generate_document()
    
    def get_simulated_stops_ids(self):
        stops_ids = []
        for node in self.sim_c.transit_network.network:
            if type(node) == Stop:
                stops_ids.append(node.id)
        self.stop_list =  stops_ids

    def get_simulated_routes_number(self):
        return len(self.sim_c.routes)

    def get_simulated_routes_ids(self):
        route_ids = []
        for route in self.sim_c.routes:
            route_ids.append(route.id)
        self.route_list = route_ids

    def get_simulated_distance(self):
        distance = 0
        for node in self.sim_c.transit_network.network:
            if type(node) == Street:
                distance += node.length
        self.simulation_length = distance

    def get_simulated_buses(self):
        self.simulated_buses = len(self.sim_c.simulated_buses) + len(self.sim_c.completed_buses)

    def get_simulated_buses_ids(self):
        for bus in self.sim_c.bus_data:
            self.simulated_buses_id.append(bus[1])

    def get_bus_commercial_speed(self):
        data = []
        for bus in self.sim_c.completed_buses:
            buf_list = []
            buf_list.append(bus.id)
            buf_list.append(bus.route.id)
            buf_list.append(round(self.simulation_length/bus.time_log,2))
            data.append(buf_list)
        data =  sorted(data, key=lambda x: x[2], reverse=True)
        return data
    
    def get_boarding_demand(self):
        for passenger in self.sim_c.passenger_data:
            if passenger[1] in self.stop_list:
                self.boarding_demand += 1
        
    def build_commercial_speed_by_route(self):
        pass


    def build_simulated_data_table(self):
        data = []
        data.append(["Simulated Time: ",f"{self.sim_c.generator['Time']['Duration']} seconds"])
        data.append(["Nº Stops Simulated: ",f"{len(self.stop_list)}",f"{self.stop_list}"])
        data.append(["Nº Routes Simulated: ",f"{len(self.route_list)}",f"{self.route_list}"])
        data.append(["Simulated Distance: ",f"{self.simulation_length} Meters"])
        data.append(["Nº Simulated Buses: ",f"{self.simulated_buses}"])
        data.append(["Boarding Demand",f"{self.boarding_demand}"])


        self.PDFG.append_table(data,"Simulated Data")

    def build_comercial_speed_table(self):
        data = [["Bus Id","Route","Comercial Speed(m/s)"]]
        data += self.get_bus_commercial_speed()

        self.PDFG.append_table(data,"Bus Commercial Speed")

    def build_simulated_distributions_table(self):
        pass

    def build_graph_test(self):
        plt.plot([1, 2, 3, 4, 5], [1, 4, 9, 16, 25])
        plt.plot([1, 2, 3, 4, 5], [1, 4, 9, 16, 25])
        self.PDFG.append_graph(plt,"test")


    def generate_data(self):
        self.get_simulated_stops_ids()
        self.get_simulated_routes_ids()
        self.get_simulated_distance()
        self.get_simulated_buses()
        self.get_simulated_buses_ids()
        self.get_boarding_demand()

    def generate_document(self):
        self.generate_data()
        self.build_simulated_data_table()
        self.build_comercial_speed_table()
        self.build_commercial_speed_by_route()
        self.build_graph_test()

        self.PDFG.build_document()