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
        self.simulation_distance = 0
        self.simulation_length = self.sim_c.generator['Time']['Duration']
        self.buses_data = []
        self.generate_document()
    
    def get_simulated_distance(self):
        distance = 0
        for node in self.sim_c.streets:
            distance += node.length
        self.simulation_distance = distance

    

    def get_bus_commercial_speed(self):
        data = []
        for bus in self.sim_c.completed_buses:
            buf_list = []
            buf_list.append(bus.id)
            buf_list.append(bus.route.id)
            buf_list.append(round(self.simulation_distance/bus.time_log,2))
            data.append(buf_list)
        data =  sorted(data, key=lambda x: x[2], reverse=True)
        return data
    

    def build_simulated_data_table(self):
        data = []
        data.append(["Simulated Time: ",f"{self.simulation_length} seconds"])
        data.append(["Nº Stops Simulated: ",f"{len(self.sim_c.stops_ids)}",f"{self.sim_c.stops_ids}"])
        data.append(["Nº Intersections Simulated: ",f"{len(self.sim_c.intersections)}"])
        data.append(["Nº Routes Simulated: ",f"{len(self.sim_c.routes_ids)}",f"{self.sim_c.routes_ids}"])
        data.append(["Simulated Distance: ",f"{self.simulation_distance} [m]"])
        data.append(["Bus Flow: ",f"{round(len(self.sim_c.buses)/3600*self.sim_c.duration)} [bus/h]" ])
        data.append(["Total Passengers Simulated",f"{round(len(self.sim_c.passengers)/3600*self.sim_c.duration)} [pax/h]"])
        data.append(["Boarding Demand",f"{round(len(self.sim_c.boarding_passengers)/3600*self.sim_c.duration)} [pax/h]"])
        data.append(["Alighting Demand",f"{round(len(self.sim_c.alighting_passengers)/3600*self.sim_c.duration)} [pax/h]"])
        
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

    def get_buses_stats(self):
        #[["Bus Id","Route","Comercial Speed(km/h)","Travel Time(s)","Stop Q Time(s)","Dwell Time(s)","Intersection Time(s)","Total Delay(s)"]]
        data = []
        for bus in self.sim_c.buses:
            buff = []
            buff.append(bus.id)
            buff.append(bus.route.id)
            buff.append(round((self.simulation_distance*3.6)/(bus.time_log),2))
            buff.append(round(bus.travel_time_log/60,2))
            buff.append(bus.stop_queue_time_log)
            buff.append(bus.stop_dwell_time_log)
            buff.append(bus.intersection_queue_time_log)
            buff.append(bus.stop_dwell_time_log + bus.stop_queue_time_log + bus.intersection_queue_time_log)
            data.append(buff)
        data =  sorted(data, key=lambda x: x[2], reverse=True)
        self.buses_data= data

    def build_bus_data_table(self):
        data = [["Bus Id","Route","Comercial Speed[km/h]","Travel Time[min]","Stop Q Time[s]","Dwell Time[s]","Intersection Time[s]","Total Delay[s]"]]
        data += self.buses_data
        self.PDFG.append_table(data,"Bus Data Sheet")

    def get_stop_stats(self):
        pass

    def build_stop_data_table(self):
        data = [["Stop ID","Capacity[bus/h]","Queue Length"]]
        for stop in self.sim_c.stops:
            buff = []
            buff.append(stop.id)
            buff.append(stop.served_buses_count*self.simulation_length/3600)
            buff.append(f"Max: {max(stop.bus_count_at_queue_log)}")
            buff.append(f"Mean: {round(np.mean(stop.bus_count_at_queue_log),2)}")
            buff.append(f"Std: {round(np.std(stop.bus_count_at_queue_log),2)}")
            data.append(buff)
        self.PDFG.append_table(data,"Stop Data")

    def build_passenger_data_table(self):
        data = [["Stop ID","Passenger Waiting Time[s]","","","Passengers At Stop","",""]]
        for stop in self.sim_c.stops:
            passenger_waiting_time = []
            buff = []
            buff.append(stop.id)
            for passenger in self.sim_c.boarding_passengers:
                if passenger.origin == stop.id:
                    passenger_waiting_time.append(passenger.waiting_time_log)
            buff.append(f"Max: {max(passenger_waiting_time)}")
            buff.append(f"Mean: {round(np.mean(passenger_waiting_time),2)}")
            buff.append(f"Std: {round(np.std(passenger_waiting_time),2)}")
            buff.append(f"Max: {max(stop.passengers_count_in_platform_log)}")
            buff.append(f"Mean: {round(np.mean(stop.passengers_count_in_platform_log),2)}")
            buff.append(f"Std: {round(np.std(stop.passengers_count_in_platform_log),2)}")
            data.append(buff)
        self.PDFG.append_table(data,None)


    def build_general_simulation_data_table(self):
        data = [["Total Travel Time[min]","Comercial Speed[km/h]","Signal Delay[s]","Bus Stop Delay[s]"]]
        buff = []
        total_trave_time = 0
        comercial_speed = 0
        signal_delay = 0
        bus_stop_delay = 0
        for bus in self.sim_c.buses:
            total_trave_time += round(bus.time_log/60,2)
            comercial_speed += self.simulation_distance*3.6/bus.time_log
            signal_delay += bus.intersection_queue_time_log
            bus_stop_delay += bus.stop_queue_time_log + bus.stop_dwell_time_log
        buff.append(total_trave_time)
        buff.append(round(comercial_speed/len(self.sim_c.buses),2))
        buff.append(signal_delay)
        buff.append(bus_stop_delay)
        data.append(buff)

        self.PDFG.append_table(data,"Arterial Road Data")



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
        self.get_buses_stats()

    def generate_document(self):
        self.generate_data()
        self.build_simulated_data_table()
        self.build_intersection_data_table()
        self.build_bus_data_table()
        self.build_stop_data_table()
        self.build_passenger_data_table()
        self.build_general_simulation_data_table()
        #self.build_speed_by_route_graph()
        #self.debug()

        self.PDFG.build_document()

    def debug(self):
        for bus in self.sim_c.buses:
            bus.print_times_log()