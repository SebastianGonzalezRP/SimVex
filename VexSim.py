from GUI.main_view import MainView
from factory.file_generator.csv_generator import CSVGenerator
from factory.file_generator.json_generator import JSONGenerator
from factory.file_generator.utils import generate_serial

class VexSim():
    def __init__(self):
        self.gui = MainView()

        self.generator_path = None
        self.bus_dispatcher_path = None
        self.passenger_dispatcher_path = None

        self.serial = None
        
    def run(self):
        self.gui.root.mainloop()

    

if __name__ == "__main__":
    VS = VexSim()
    VS.run()

    if VS.gui.complete:
        app_mode = VS.gui.app_mode
        if app_mode == "new":
            generator = VS.gui.generator
            VS.serial = generate_serial()
            JSONGenerator(generator)
            CSVGenerator(generator)
            VS.generator_path = f"files/{VS.serial}/generator.json"
            VS.bus_dispatcher_path = f"files/{VS.serial}/bus_dispatcher.csv"
            VS.passenger_dispatcher_path = f"files/{VS.serial}/passenger_dispatcher.csv"
        elif app_mode == "regenerate":
            generator = VS.gui.generator
            pass
        elif app_mode == "reuse":
            pass
