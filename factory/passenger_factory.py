from models.passenger import Passenger

#construction_params = [arrival_time, origin, destiny, route, boarding_t, alighting_t]

def construct_passenger(construction_params):
    new_passenger = Passenger(arrival_time=construction_params[0],  #Integer (Seconds)
                              origin=construction_params[1],        #String
                              destiny=construction_params[2],       #String
                              route=construction_params[3],         #Object.Route
                              boarding_t=construction_params[4],    #Integer (seconds)
                              alighting_t=construction_params[5])   #Integer (Seconds)
    
    return new_passenger