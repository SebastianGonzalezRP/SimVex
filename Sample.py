import json
from numpy import random
from factory.file_generator.passenger_dispatcher import Passenger_Dispatcher



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
            "bus_rate":{"Exp":{"rate":720}}},
        "102":{
            "stops":{"p-103":{"passenger_rate":{"Exp":{"rate":30}}}},
            "bus_rate":{"Fixed":{"rate":600}}},
        "103":{
            "stops":{"p-104":{"passenger_rate":{"Exp":{"rate":30}}}},
            "bus_rate":{"Uniform":{"a":540,"b":720}}}
    },  
    "Buses":{"top_speed": 14, "acc":10,"desc":4},
    "Passenger":{
        "boarding_time_dist":{"Normal":{"mu":3,"stdv":1}},
        "alighting_time_dist":{"Uniform":{"a":2,"b":4}}
    }
}

#print(random.exponential())

#with open("generator.json", "w") as outfile:
#    json.dump(FILE, outfile)

# ID, origin, destiny, route, t_in, boarding_t, alighting_t

PD = Passenger_Dispatcher(FILE)
PD.generate_dispatcher_file()




#print(f"Exponencial: {random.exponential(720)}")
#print(f"Uniforme: {random.uniform(2,4)}")
#print(f"Normal: {round(random.normal(3,1))}")




dict = {"Route": None, "Stop": None, }
