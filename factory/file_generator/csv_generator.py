from factory.file_generator.bus_dispatcher import Bus_Dispatcher as BD
from factory.file_generator.passenger_dispatcher import Passenger_Dispatcher as PD
from factory.file_generator.utils import generate_serial

class CSVGenerator():
    def __init__(self,generator):

        self.generator = generator
        self.passenger_generator = PD(self.generator)
        self.bus_generator = BD(self.generator)

        serial = generate_serial()
        
        self.generate_csv_files(serial)
        
    def generate_csv_files(self, serial):
        self.passenger_generator.generate_dispatcher_file(serial)
        self.bus_generator.generate_dispatcher_file(serial)

    