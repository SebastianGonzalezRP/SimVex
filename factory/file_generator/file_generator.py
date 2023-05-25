from factory.file_generator.bus_dispatcher import Bus_Dispatcher as BD
from factory.file_generator.passenger_dispatcher import Passenger_Dispatcher as PD
import datetime

class FileGenerator():
    def __init__(self,generator):

        self.generator = generator
        self.passenger_generator = PD(self.generator)
        self.bus_generator = BD(self.generator)


        ##TODO: Replace Serial with Generator File Serial(INPUT MODULE)
        current_datetime = datetime.datetime.now()
        year = current_datetime.year
        month = current_datetime.month
        day = current_datetime.day
        hour = current_datetime.hour
        minutes = current_datetime.minute
        serial = f'{year}_{month}_{day}_{hour}{minutes}'
        self.generate_files(serial)
        
    def generate_files(self, serial):
        self.passenger_generator.generate_dispatcher_file(serial)
        self.bus_generator.generate_dispatcher_file(serial)