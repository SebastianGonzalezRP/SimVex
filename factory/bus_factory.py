from models.bus import Bus

#construction_params = [arrival_time, id, route,door_n, top_speed,acc, desc]

def construct_bus(construction_params):
    new_bus = Bus(arrival_time= construction_params[0], #Integer (Seconds)
                  id=construction_params[1],            #String
                  route = construction_params[2],       #Object.Route
                  door_n= construction_params[3],       #Integer
                  top_speed=construction_params[4],     #Float (m/s2)
                  acc=construction_params[5],           #Float (m/s2)
                  desc=construction_params[6])         #Float (m/s)

    return new_bus
