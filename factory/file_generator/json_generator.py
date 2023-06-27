from factory.file_generator.utils import generate_serial
from factory.file_generator.utils import write_json

class JSONGenerator:
    def __init__(self, generator):
        self.generator = generator

        serial = generate_serial()
        self.generate_json_file(serial)

    def generate_json_file(self,serial):
        write_json(self.generator,serial,"generator.json")
