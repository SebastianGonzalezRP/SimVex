from controllers.view.view_controller import ViewController
from controllers.sim.sim_controller import SimController
from GUI.main_view import MainView
from factory.file_generator.csv_generator import CSVGenerator
from factory.file_generator.json_generator import JSONGenerator
from factory.file_generator.utils import generate_serial
from output.data_analyzer import DataAnalyzer

class VexSim():
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
    VS = VexSim()
    VS.run()

    if VS.gui.controller.complete:
        app_mode = VS.gui.controller.app_mode
        if app_mode == "new":
            VS.build_from_generator()
            VS.setup_sim_controller()
        elif app_mode == "regenerate":
            VS.build_from_generator()
            VS.setup_sim_controller()
        elif app_mode == "reuse": 
            VS.sim_controller.load_files_data(VS.view_controller.generator_path,
                                            VS.view_controller.passenger_dispatcher_path,
                                            VS.view_controller.bus_dispatcher_path)
            VS.serial = VS.view_controller.generator_path.split('/')[-2]
            VS.sim_controller.initialize_sim()
            VS.sim_controller.run_sim()

    DataAnalyzer(VS.sim_controller, VS.serial)
