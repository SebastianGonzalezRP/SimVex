class BusModel:
    def __init__(self,
                bus_model: str,
                door_n: int,
                top_speed: float,
                acceleration: float,
                desceleration: float):
        
        self.name = bus_model
        self.door_n = door_n
        self.top_speed = top_speed
        self.acc = acceleration
        self.desc = desceleration


bus_models = {
    "New Flyer": {"door_n":1, "top_speed": 19, "acc":1.2, "desc": 1.8},
    "Nova Bus LFS":{"door_n":2, "top_speed": 17, "acc":1.1, "desc": 1.5},
    "BYD K9":{"door_n":2, "top_speed": 16.5, "acc":1, "desc": 1.5},
    "Dennis Enviro500":{"door_n":3, "top_speed": 15.5, "acc":0.9, "desc": 1.2}}
       