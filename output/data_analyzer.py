from factory.file_generator.pdf_generator import PDFGenerator
from models.nodes.street import Street
from models.nodes.stop import Stop
from models.nodes.intersection import Intersection
from scipy import stats
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics



class DataAnalyzer:
    def __init__(self, sim_controller,serial):
        self.sim_c = sim_controller
        self.PDFG = PDFGenerator(serial)


        #metadata

        self.simulation_length = 0
        self.generate_document()
    
    def get_simulated_distance(self):
        distance = 0
        for node in self.sim_c.streets:
            distance += node.length
        self.simulation_length = distance

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
    
        
    def build_commercial_speed_by_route(self):
        pass


    def build_simulated_data_table(self):
        data = []
        data.append(["Simulated Time: ",f"{self.sim_c.generator['Time']['Duration']} seconds"])
        data.append(["Nº Stops Simulated: ",f"{len(self.sim_c.stops_ids)}",f"{self.sim_c.stops_ids}"])
        data.append(["Nº Intersections Simulated: ",f"{len(self.sim_c.intersections)}"])
        data.append(["Nº Routes Simulated: ",f"{len(self.sim_c.routes_ids)}",f"{self.sim_c.routes_ids}"])
        data.append(["Simulated Distance: ",f"{self.simulation_length} Meters"])
        data.append(["Bus Flow: ",f"{len(self.sim_c.buses)/3600*self.sim_c.duration} [Bus/h]" ])
        data.append(["Total Passengers Simulated",f"{len(self.sim_c.passengers)}"])
        data.append(["Boarding Demand",f"{len(self.sim_c.boarding_passengers)}"])
        data.append(["Alighting Demand",f"{len(self.sim_c.alighting_passengers)}"])
        
        self.PDFG.append_table(data,"Simulation Input Data")

    def build_intersection_data_table(self):
        data = []
        data.append(["Intersection Number","Cycle Duration (s)","Green Ratio"])
        count = 0
        for node in self.sim_c.transit_network.network:
            if type(node)  == Intersection:
                count += 1
                data.append([f"Intersection {count}",node.cicle_duration,node.effective_green])
        if count > 0:
            self.PDFG.append_table(data,None)



    def build_comercial_speed_table(self):
        data = [["Bus Id","Route","Comercial Speed(m/s)"]]
        data += self.get_bus_commercial_speed()

        self.PDFG.append_table(data,"Bus Commercial Speed")

    def build_simulated_distributions_table(self):
        pass


    def build_speed_by_route_graph(self):
        graph_file_path = "files/tmp/graph.png" 
        data = self.get_bus_commercial_speed()
        df = pd.DataFrame(data, columns=['ID', 'Route', 'AvgSpeed'])
        summary = df.groupby('Route')['AvgSpeed'].agg(['mean', 'std']).reset_index()
        summary = summary.sort_values(by=['mean'])
        sns.barplot(x='Route', y='mean', data=summary, yerr=summary["std"])
        plt.xlabel('Route ID')
        plt.ylabel('Average Speed (m/s)')
        plt.savefig(graph_file_path)
        self.PDFG.append_graph("Average Speed by Route")


    def generate_data(self):
        self.get_simulated_distance()

    def generate_document(self):
        self.generate_data()
        self.build_simulated_data_table()
        self.build_intersection_data_table()
        self.build_comercial_speed_table()
        self.build_commercial_speed_by_route()
        self.build_speed_by_route_graph()

        self.PDFG.build_document()

    def debug(self):
        print(f"Self Sim c boarding_passengers len {len(self.sim_c.boarding_passengers)}")
        print(f"Self Sim c boarding_passengers len {len(self.sim_c.alighting_passengers)}")