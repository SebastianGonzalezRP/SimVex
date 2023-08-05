from controllers.view.view_controller import ViewController
from controllers.sim.sim_controller import SimController
from GUI.main_view import MainView
from factory.file_generator.csv_generator import CSVGenerator
from factory.file_generator.json_generator import JSONGenerator
from factory.file_generator.utils import generate_serial
from output.data_analyzer import DataAnalyzer

class SimVex():
    def __init__(self):
        self.view_controller = ViewController()
        self.gui = MainView(self.view_controller)
        self.sim_controller = SimController()
        

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

    def setup_sim_controller(self):
        self.sim_controller.load_files_data(self.generator_path,
                                            self.passenger_dispatcher_path,
                                            self.bus_dispatcher_path)
        self.sim_controller.initialize_sim()
        self.sim_controller.run_sim()

if __name__ == "__main__":
    SV = SimVex()
    SV.run()
    
    if SV.gui.controller.complete:
        app_mode = SV.gui.controller.app_mode
        if app_mode == "new":
            SV.build_from_generator()
            SV.setup_sim_controller()
        elif app_mode == "regenerate":
            SV.build_from_generator()
            SV.setup_sim_controller()
        elif app_mode == "reuse": 
            SV.sim_controller.load_files_data(SV.view_controller.generator_path,
                                            SV.view_controller.passenger_dispatcher_path,
                                            SV.view_controller.bus_dispatcher_path)
            SV.serial = SV.view_controller.generator_path.split('/')[-2]
            SV.sim_controller.initialize_sim()
            SV.sim_controller.run_sim()

    DataAnalyzer(SV.sim_controller, SV.serial)
