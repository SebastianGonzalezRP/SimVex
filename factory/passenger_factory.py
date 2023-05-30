from models.passenger import Passenger

#construction_params = [origin, destiny, route, boarding_t, alighting_t]

def construct_passenger(construction_params):
    new_passenger = Passenger(origin=construction_params[0],        #String
                              destiny=construction_params[1],       #String
                              route=construction_params[2],         #Object.Route
                              boarding_t=construction_params[3],    #Integer (seconds)
                              alighting_t=construction_params[4])   #Integer (Seconds)
    
    return new_passenger