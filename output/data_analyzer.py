from factory.file_generator.pdf_generator import PDFGenerator
from models.nodes.street import Street
from models.nodes.stop import Stop
from models.nodes.intersection import Intersection


class DataAnalyzer:
    def __init__(self, sim_controller,serial):
        self.sim_c = sim_controller
        self.PDFG = PDFGenerator(serial)


        #metadata
        self.stop_list = []
        self.route_list = []
        self.simulation_length = 0
        self.simulated_buses = 0

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

    def build_simulated_data_table(self):
        data = []
        data.append(["Simulated Time: ",f"{self.sim_c.generator['Time']['Duration']} seconds"])
        data.append(["Nº Stops Simulated: ",f"{len(self.stop_list)}",f"{self.stop_list}"])
        data.append(["Nº Routes Simulated: ",f"{len(self.route_list)}",f"{self.route_list}"])
        data.append(["Simulated Distance: ",f"{self.simulation_length} Meters"])
        data.append(["Nº Simulated Buses: ",f"{self.simulated_buses}"])

        self.PDFG.append_table(data)

    def build_comercial_speed_table(self):
        data = [["Bus Id","Route","Comercial Speed(m/s)"]]
        data += self.get_bus_commercial_speed()

        self.PDFG.append_table(data)

    def build_simulated_distributions_table(self):
        pass

    def generate_data(self):
        self.get_simulated_stops_ids()
        self.get_simulated_routes_ids()
        self.get_simulated_distance()
        self.get_simulated_buses()

    def generate_document(self):
        self.generate_data()
        self.build_simulated_data_table()
        self.build_comercial_speed_table()
        self.PDFG.build_document()