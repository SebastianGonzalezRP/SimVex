from controllers.view.view_controller import ViewController
from GUI.main_view import MainView
from factory.file_generator.csv_generator import CSVGenerator
from factory.file_generator.json_generator import JSONGenerator
from factory.file_generator.utils import generate_serial

class VexSim():
    def __init__(self):
        self.controller = ViewController()
        self.gui = MainView(self.controller)

        self.generator_path = None
        self.bus_dispatcher_path = None
        self.passenger_dispatcher_path = None

        self.serial = None
        
    def run(self):
        self.gui.root.mainloop()

    def define_serial(self):
        self.serial = generate_serial()

    def build_from_generator(self):
        self.define_serial()
        generator = self.gui.controller.generator
        JSONGenerator(generator)
        CSVGenerator(generator)
        self.generator_path = f"files/{self.serial}/generator.json"
        self.bus_dispatcher_path = f"files/{self.serial}/bus_dispatcher.csv"
        self.passenger_dispatcher_path = f"files/{self.serial}/passenger_dispatcher.csv"

if __name__ == "__main__":
    VS = VexSim()
    VS.run()

    if VS.gui.controller.complete:
        app_mode = VS.gui.controller.app_mode
        if app_mode == "new":
            VS.build_from_generator()
        elif app_mode == "regenerate":
            VS.build_from_generator()
        elif app_mode == "reuse":
            pass
