from models.bus import Bus

#construction_params = [id, route, passengers,door_n, top_speed,acc, desc]

def construct_bus(construction_params):
    new_bus = Bus(id=construction_params[0],            #String
                  route = construction_params[1],       #Object.Route
                  passengers= construction_params[2],   #List[Object.Passenger]
                  door_n= construction_params[3],       #Integer
                  acc=construction_params[4],           #Integer (m/s2)
                  desc=construction_params[5],          #Integer (m/s2)
                  top_speed=construction_params[6],)    #Integer (m/s)

    return new_bus
