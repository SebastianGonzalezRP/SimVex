class Route:
    def __init__ (self,id,serving_stops):
        self.id = id
        self.serving_stops = serving_stops

    def get_remaining_stops_id(self,stop_id):
        remaining_stop_id = []
        if stop_id == "start":
            for stop in self.serving_stops:
                remaining_stop_id.append(stop.id)
            return remaining_stop_id
        for stop in self.serving_stops:
            if stop.id == stop_id:
                index = self.serving_stops.index(stop) + 1
                remaining_stop = self.serving_stops[index:]
                for stop in remaining_stop:
                    remaining_stop_id.append(stop.id)
                return remaining_stop_id
            else:
                return []