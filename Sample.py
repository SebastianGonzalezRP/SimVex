import json
from numpy import random
from factory.file_generator.passenger_dispatcher import Passenger_Dispatcher
from factory.file_generator.bus_dispatcher import Bus_Dispatcher
import json
from factory.file_generator.file_generator import FileGenerator
from controllers.sim.sim_controller import Sim_Controller
from factory.node_factory import *
from models.transit_network import TransitNetwork
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd



FILE = {
    "Time":{
        "Duration": 3600,
        "Tick": 0.5
    },
    "Node":[
        {"Street": {"length": 200, "tracks": 2}},
        {"Stop": {"id": "p-103", "berths": 2}},
        {"Street": {"length": 300, "tracks": 2}},
        {"Intersection": {"cicle": 110, "green": 0.6}},
        {"Street": {"length": 500, "tracks": 2}},
        {"Stop": {"id": "p-104", "berths": 2}},
        {"Street": {"length": 200, "tracks": 2}},
    ],
    "Route":{
        "101":{
            "stops":{"p-103":{"passenger_rate":{"Exp":{"rate":40}}},
                     "p-104":{"passenger_rate":{"Exp":{"rate":50}}}},
            "bus_rate":{"Exp":{"rate":720}},
            "initial_occupancy":{"Fixed":{"rate":20}}},
        "102":{
            "stops":{"p-103":{"passenger_rate":{"Exp":{"rate":30}}}},
            "bus_rate":{"Fixed":{"rate":600}},
            "initial_occupancy":{"Normal":{"mu":20,"stdv":3}}},
        "103":{
            "stops":{"p-104":{"passenger_rate":{"Exp":{"rate":30}}}},
            "bus_rate":{"Uniform":{"a":540,"b":720}},
            "initial_occupancy":{"Uniform":{"a":15,"b":25}}}
    },  
    "Buses":{"top_speed": 14, "acc":1,"desc":1},
    "Passenger":{
        "boarding_time_dist":{"Normal":{"mu":3,"stdv":1}},
        "alighting_time_dist":{"Uniform":{"a":2,"b":4}}
    }
}

#print(random.exponential())

#with open("generator.json", "w") as outfile:
#    json.dump(FILE, outfile)

#PASSENGER:  [t_in, ID, origin, destiny, route,  boarding_t, alighting_t]
#BUS: [t_in, ID, route, door_n]

#PD = Passenger_Dispatcher(FILE)
#PD.generate_dispatcher_file("TEST_SERIAL")

#BD = Bus_Dispatcher(FILE)
#BD.generate_dispatcher_file("TEST_SERIAL")

#FG = FileGenerator(FILE)

#json_data = json.dumps(FILE, indent=4)
## Write JSON string to a file
#with open("generator.json", "w") as file:
#    file.write(json_data)

generator_path = 'files\generator.json' 
passenger_file_path  = r'files\2023_5_30_1253\passenger_dispatcher.csv'
bus_file_path = r'files\2023_5_30_1253\bus_dispatcher.csv'


SC = Sim_Controller(generator_path=generator_path,
                    passenger_dispatch_path= passenger_file_path,
                    bus_dispatch_path = bus_file_path)

SC.debug()

results = SC.get_results()

sns.boxplot(data=results)
plt.show()

for line in results:
    plt.plot(line)
plt.show()

df = pd.DataFrame(results)

sns.lineplot(data=df.T)
plt.show()


