import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import configparser


grey1 = "#D4D4D4"
grey2 = "#B4B4B4"
grey3 = "#909090"
grey4 = "#636363"

window_width = 1280
window_height = 800


def destroy_frame_children(frame):
    for child in frame.winfo_children():
        child.destroy()
 
def load_exponencial_template(container):
    distribution_label = tk.Label(container,text="Distribution", bg=grey3, font=('Segoe 12'))
    distribution_label.grid(row=0, column=0, padx=5, pady=5, sticky='nswe')

    distribution_selector = ttk.Combobox(container, values=["Exponential","Uniform","Normal","Fixed"], width=1)
    distribution_selector.set("Exponential")
    distribution_selector.bind('<<ComboboxSelected>>', lambda event: distribution_selector_change(container,distribution_selector))
    distribution_selector.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

    rate_label = tk.Label(container,text="Distribution Rate (seconds)", bg=grey3, font=('Segoe 12'))
    rate_label.grid(row=0, column=1, padx=5, pady=5, sticky='nswe')

    rate_field = tk.Entry(container)
    rate_field.grid(row=1, column=1, padx=5, pady=5, sticky='nswe')

    container.columnconfigure(0, weight=2)
    container.columnconfigure(1, weight=1)

def load_uniform_template(container):
    distribution_label = tk.Label(container,text="Distribution", bg=grey3, font=('Segoe 12'))
    distribution_label.grid(row=0, column=0, padx=5, pady=5, sticky='nswe')

    distribution_selector = ttk.Combobox(container, values=["Exponential","Uniform","Normal","Fixed"], width=1)
    distribution_selector.set("Uniform")
    distribution_selector.bind('<<ComboboxSelected>>', lambda event: distribution_selector_change(container,distribution_selector))
    distribution_selector.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

    a_label = tk.Label(container,text="A", bg=grey3, font=('Segoe 12'))
    a_label.grid(row=0, column=1, padx=5, pady=5, sticky='nswe')

    a_field = tk.Entry(container)
    a_field.grid(row=1, column=1, padx=5, pady=5, sticky='nswe')

    b_label = tk.Label(container,text="B", bg=grey3, font=('Segoe 12'))
    b_label.grid(row=0, column=2, padx=5, pady=5, sticky='nswe')

    b_field = tk.Entry(container)
    b_field.grid(row=1, column=2, padx=5, pady=5, sticky='nswe')

    container.columnconfigure(0, weight=2)
    container.columnconfigure(1, weight=1)
    container.columnconfigure(2, weight=1)

def load_normal_template(container):
    distribution_label = tk.Label(container,text="Distribution", bg=grey3, font=('Segoe 12'))
    distribution_label.grid(row=0, column=0, padx=5, pady=5, sticky='nswe')

    distribution_selector = ttk.Combobox(container, values=["Exponential","Uniform","Normal","Fixed"], width=1)
    distribution_selector.set("Normal")
    distribution_selector.bind('<<ComboboxSelected>>', lambda event: distribution_selector_change(container,distribution_selector))
    distribution_selector.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

    mu_label = tk.Label(container,text="Mean", bg=grey3, font=('Segoe 12'))
    mu_label.grid(row=0, column=1, padx=5, pady=5, sticky='nswe')

    mu_field = tk.Entry(container)
    mu_field.grid(row=1, column=1, padx=5, pady=5, sticky='nswe')

    stdv_label = tk.Label(container,text="Standard Deviation", bg=grey3, font=('Segoe 12'))
    stdv_label.grid(row=0, column=2, padx=5, pady=5, sticky='nswe')

    stdv_field = tk.Entry(container)
    stdv_field.grid(row=1, column=2, padx=5, pady=5, sticky='nswe')

    container.columnconfigure(0, weight=2)
    container.columnconfigure(1, weight=1)
    container.columnconfigure(2, weight=1)

def load_fixed_template(container):
    distribution_label = tk.Label(container,text="Distribution", bg=grey3, font=('Segoe 12'))
    distribution_label.grid(row=0, column=0, padx=5, pady=5, sticky='nswe')

    distribution_selector = ttk.Combobox(container, values=["Exponential","Uniform","Normal","Fixed"], width=1)
    distribution_selector.set("Fixed")
    distribution_selector.bind('<<ComboboxSelected>>', lambda event: distribution_selector_change(container,distribution_selector))
    distribution_selector.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

    rate_label = tk.Label(container,text="Arrival Rate (seconds)", bg=grey3, font=('Segoe 12'))
    rate_label.grid(row=0, column=1, padx=5, pady=5, sticky='nswe')

    rate_field = tk.Entry(container)
    rate_field.grid(row=1, column=1, padx=5, pady=5, sticky='nswe')

    container.columnconfigure(0, weight=2)
    container.columnconfigure(1, weight=1)

def distribution_selector_change(container, distribution_selector):
    selection = distribution_selector.get()
    update_existing_distribution_container(container, selection)
    
def update_existing_distribution_container(distribution_container, distribution):
    destroy_frame_children(distribution_container)
    if distribution == "Exponential":
        load_exponencial_template(distribution_container)
    elif distribution == "Uniform":
        load_uniform_template(distribution_container)
    elif distribution == "Normal":
        load_normal_template(distribution_container)
    elif distribution == "Fixed":
        load_fixed_template(distribution_container)

def distribution_parser(container):
    distribution  = container.winfo_children()[1].get()
    if distribution == "Exponential":
        rate = float(container.winfo_children()[3].get())
        return {distribution:{"rate":rate}}
    elif distribution == "Uniform":
        a_value = int(container.winfo_children()[3].get())
        b_value = int(container.winfo_children()[5].get())
        return {distribution:{"a":a_value,"b":b_value}}
    elif distribution == "Normal":
        mu = float(container.winfo_children()[3].get())
        stdv = float(container.winfo_children()[5].get())
        return {distribution:{"mu":mu,"stdv":stdv}}
    elif distribution == "Fixed":
        rate = int(container.winfo_children()[3].get())
        return {distribution:{"rate":rate}}

#region Node Creator
def create_street_node(self,node_list):

    node_container = tk.Frame(node_list, height=100, bg=grey3)
    node_container.pack(anchor='n', fill='x', padx=5, pady=5)

    node_label = tk.Label(node_container, text="Node Type", bg=grey3)
    node_label.grid(row=0, column=0, padx=5, pady=5, sticky='nswe')

    node_selector = ttk.Combobox(node_container, values=["Street","Stop","Intersection"])
    node_selector.set("Street")
    node_selector.bind('<<ComboboxSelected>>', lambda event: node_selector_change(self, node_selector))
    node_selector.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

    length_label = tk.Label(node_container, text="Street Length", bg=grey3)
    length_label.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

    length_field = tk.Entry(node_container)
    length_field.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

    ntracks_label = tk.Label(node_container, text="Number of Tracks", bg=grey3)
    ntracks_label.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

    number_spinbox = ttk.Spinbox(node_container, from_=2, to=2)
    number_spinbox.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

    node_container.columnconfigure(0, weight=1)
    node_container.columnconfigure(1, weight=1)
    node_container.columnconfigure(2, weight=1)

def load_street_node(self,node_container):

    node_label = tk.Label(node_container, text="Node Type", bg=grey3)
    node_label.grid(row=0, column=0, padx=5, pady=5, sticky='nswe')

    node_selector = ttk.Combobox(node_container, values=["Street","Stop","Intersection"])
    node_selector.set("Street")
    node_selector.bind('<<ComboboxSelected>>', lambda event: node_selector_change(self, node_selector))
    node_selector.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

    length_label = tk.Label(node_container, text="Street Length", bg=grey3)
    length_label.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

    length_field = tk.Entry(node_container)
    length_field.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

    ntracks_label = tk.Label(node_container, text="Number of Tracks", bg=grey3)
    ntracks_label.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

    number_spinbox = ttk.Spinbox(node_container, from_=2, to=2)
    number_spinbox.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

    node_container.columnconfigure(0, weight=1)
    node_container.columnconfigure(1, weight=1)
    node_container.columnconfigure(2, weight=1)

def load_stop_node(self,node_container):

    node_label = tk.Label(node_container, text="Node Type", bg=grey3)
    node_label.grid(row=0, column=0, padx=5, pady=5, sticky='nswe')

    node_selector = ttk.Combobox(node_container, values=["Street","Stop","Intersection"])
    node_selector.set("Stop")
    node_selector.bind('<<ComboboxSelected>>', lambda event: node_selector_change(self, node_selector))
    node_selector.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

    id_label = tk.Label(node_container, text="Stop ID", bg=grey3)
    id_label.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

    id_field = tk.Entry(node_container)
    id_field.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

    n_berths_label = tk.Label(node_container, text="Number of Berths", bg=grey3)
    n_berths_label.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

    number_spinbox = ttk.Spinbox(node_container, from_=1, to=3)
    number_spinbox.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

    node_container.columnconfigure(0, weight=1)
    node_container.columnconfigure(1, weight=1)
    node_container.columnconfigure(2, weight=1)

def load_intersection_node(self,node_container):

    node_label = tk.Label(node_container, text="Node Type", bg=grey3)
    node_label.grid(row=0, column=0, padx=5, pady=5, sticky='nswe')

    node_selector = ttk.Combobox(node_container, values=["Street","Stop","Intersection"])
    node_selector.set("Intersection")
    node_selector.bind('<<ComboboxSelected>>', lambda event: node_selector_change(self, node_selector))
    node_selector.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

    cicle_label = tk.Label(node_container, text="Cicle Duration (Seconds)", bg=grey3)
    cicle_label.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

    cicle_spinbox = ttk.Spinbox(node_container, from_=1, to=120)
    cicle_spinbox.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

    effective_green_label = tk.Label(node_container, text="Effective Green (%)", bg=grey3)
    effective_green_label.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

    effective_green = ttk.Spinbox(node_container, from_=0, to=1, increment=0.01)
    effective_green.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

    node_container.columnconfigure(0, weight=1)
    node_container.columnconfigure(1, weight=1)
    node_container.columnconfigure(2, weight=1)

def node_selector_change(self, node_selector):
        selection = node_selector.get()
        node_container_path = node_selector.winfo_parent()
        node_container = self.root.nametowidget(node_container_path)
        update_existing_node(self, node_container, selection)

def update_existing_node(self, node_container, node_type):
    destroy_frame_children(node_container)
    if node_type == "Street":
        load_street_node(self, node_container)
    elif node_type == "Stop":
        load_stop_node(self, node_container)
    elif node_type == "Intersection":
        load_intersection_node(self, node_container)
    pass

def node_parser(node_type, value1, value2):
    if node_type == "Street":
        return {node_type: {"length": int(value1), "tracks": int(value2)}}
    elif node_type == "Stop":
        return {node_type: {"id": value1, "berths": int(value2)}}
    elif node_type == "Intersection":
        return {node_type: {"cicle": int(value1), "green": float(value2)}}

def submit_nodes(self, nodes_list):
    nodes = []
    for node in nodes_list.winfo_children():
        node_type = node.winfo_children()[1].get()
        node_attribute_1 = node.winfo_children()[3].get()
        node_attribute_2 = node.winfo_children()[5].get()
        if node_attribute_1 != "" and node_attribute_2 != "":
                nodes.append(node_parser(node_type, node_attribute_1, node_attribute_2))
        else:
            tk.messagebox.showinfo(" ",f"{node_type} Attribute may not be Empty")
            break
        
    if (len(nodes) == len(nodes_list.winfo_children())):
        self.generator["Node"] = nodes
        self.load_route_creator()

#endregion

#region Route Creator
def create_route_container(self,route_list):

    route_container = tk.Frame(route_list, height=100, bg=grey3)
    route_container.pack(anchor='n', fill='x', padx=5, pady=5,)

    route_label = tk.Label(route_container, text="Route ID", bg=grey3)
    route_label.grid(row=0, column=0, padx=5, pady=5, sticky='nswe')

    id_field = tk.Entry(route_container)
    id_field.grid(row=1, column=0, padx=5, pady=5, sticky='new')

    existing_stops_label = tk.Label(route_container, text="Available Stops", bg=grey3)
    existing_stops_label.grid(row=0, column=1, padx=5, pady=5, sticky='nswe')

    existing_stops = tk.Listbox(route_container, selectmode=tk.MULTIPLE, height=5)
    existing_stops.grid(row=1, column=1, padx=5, pady=5, sticky='nwe')
    for node in self.generator["Node"]:
        if list(node.keys())[0] == "Stop":
            existing_stops.insert(tk.END, node["Stop"]["id"])

    
    add_stop_button = tk.Button(route_container, text="Add Stop",command=lambda: switch_stop(existing_stops,selected_stops))
    add_stop_button.grid(row=2, column=1, padx=5, pady=5, sticky='nwe')

    selected_stops_label = tk.Label(route_container, text="Selected Stops", bg=grey3)
    selected_stops_label.grid(row=0, column=2, padx=5, pady=5, sticky='nswe')

    selected_stops = tk.Listbox(route_container, selectmode=tk.MULTIPLE, height=5)
    selected_stops.grid(row=1, column=2, padx=5, pady=5, sticky='nwe')
    
    remove_stop_button = tk.Button(route_container, text="Remove Stop",command=lambda: switch_stop(selected_stops, existing_stops))
    remove_stop_button.grid(row=2, column=2, padx=5, pady=5, sticky='nwe')


    route_container.columnconfigure(0, weight=1)
    route_container.columnconfigure(1, weight=1)
    route_container.columnconfigure(2, weight=1)
    pass

def switch_stop(origin,target):
    selections = []
    for index in reversed(origin.curselection()):
        selections.append(origin.get(index))
        origin.delete(index)
    for stop in reversed(selections):
        target.insert(tk.END, stop)

def submit_routes(self, route_list):
    route = []
    for route in route_list.winfo_children():
        route_id = route.winfo_children()[1].get()
        stops_id_list = list(route.winfo_children()[6].get(0,"end"))
        self.generator["Route"][route_id]= {"stops": {},
                                                "bus_rate": {},
                                                "initial_occupancy":{}}
        for stop_id in stops_id_list:
            self.generator["Route"][route_id]["stops"][stop_id]= {"passenger_rate":{}}
    self.load_stop_config()

#endregion

#region Stop Configuration
def create_stop_config_container(stop_list,_route_id, _stop_id,):
    main_container = tk.Frame(stop_list, height=110, width=200, bg=grey3)
    main_container.pack(side="top", fill='x', padx=5, pady=5)

    main_container.columnconfigure(0, weight=1)
    main_container.columnconfigure(1, weight=2)

    stop_container = tk.Frame(main_container, height=110, width=200, bg=grey3)
    stop_container.grid(row=0, column=0, padx=(5,0), pady=5, sticky='we')

    stop_container.columnconfigure(0, weight=0)
    stop_container.columnconfigure(1, weight=0)

    route_label = tk.Label(stop_container, text="Route ID:",bg=grey3, font=('Segoe 12') )
    route_label.grid(row=0, column=0, padx=5, pady=2.5, sticky='w')

    route_id = tk.Label(stop_container, text=_route_id, bg=grey3, font=('Segoe 12'))
    route_id.grid(row=0, column=1, padx=5, pady=2.5, sticky='we')

    stop_label = tk.Label(stop_container, text="Stop ID:", bg=grey3, font=('Segoe 12'))
    stop_label.grid(row=1, column=0, padx=5, pady=2.5, sticky='w')

    stop_id = tk.Label(stop_container, text=_stop_id, bg=grey3, font=('Segoe 12'))
    stop_id.grid(row=1, column=1, padx=5, pady=2.5, sticky='we')

    distribution_container = tk.Frame(main_container, height=110, bg=grey3)
    distribution_container.grid(row=0, column=1, padx=5, pady=5, sticky='we') 

    load_exponencial_template(distribution_container)

def submit_stop_config(self, stop_list):
    for main_container in stop_list.winfo_children():
        data_container = main_container.winfo_children()[0]
        distribution_container = main_container.winfo_children()[1]
        route_id = data_container.winfo_children()[1]["text"]
        stop_id = data_container.winfo_children()[3]["text"]
        distribution = distribution_parser(distribution_container)
        self.generator["Route"][route_id]["stops"][stop_id]["passenger_rate"] = distribution
    self.load_route_config()
#endregion

#region Route Configuration
def create_route_config_container(route_list,_route_id):
    main_container = tk.Frame(route_list, height=110, width=200, bg=grey3)
    main_container.pack(side="top", fill='x', padx=5, pady=5)

    main_container.columnconfigure(0, weight=1)
    main_container.columnconfigure(1, weight=2)

    route_container = tk.Frame(main_container, height=110, width=200, bg=grey3)
    route_container.grid(row=0, column=0, padx=(5,0), pady=5, sticky='we')

    route_container.columnconfigure(0, weight=0)

    route_label = tk.Label(route_container, text="Route ID:",bg=grey3, font=('Segoe 12') )
    route_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    route_id = tk.Label(route_container, text=_route_id, bg=grey3, font=('Segoe 12'))
    route_id.grid(row=0, column=1, padx=5, pady=5, sticky='we')

    distribution_container = tk.Frame(main_container, height=110, bg=grey3)
    distribution_container.grid(row=0, column=1, padx=5, pady=5, sticky='we') 

    load_exponencial_template(distribution_container)


def submit_route_config(self, route_list):
    for main_container in route_list.winfo_children():
        data_container = main_container.winfo_children()[0]
        distribution_container = main_container.winfo_children()[1]
        route_id = data_container.winfo_children()[1]["text"]
        distribution = distribution_parser(distribution_container)
        self.generator["Route"][route_id]["bus_rate"] = distribution
    self.load_passenger_action_config()
#endregion

#region Passenger Action Configuration
def create_passenger_action_config_container(passenger_list,title):
    main_container = tk.Frame(passenger_list, height=110, width=200, bg=grey3)
    main_container.pack(side="top", fill='x', padx=5, pady=5)

    main_container.columnconfigure(0, weight=1)
    main_container.columnconfigure(1, weight=2)

    passenger_container = tk.Frame(main_container, height=110, width=200, bg=grey3)
    passenger_container.grid(row=0, column=0, padx=(5,0), pady=5, sticky='we')

    passenger_container.columnconfigure(0, weight=1)

    passenger_label = tk.Label(passenger_container, text=title,bg=grey3, font=('Segoe 12') )
    passenger_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    distribution_container = tk.Frame(main_container, height=110, bg=grey3)
    distribution_container.grid(row=0, column=1, padx=5, pady=5, sticky='we') 

    load_exponencial_template(distribution_container)

def submit_passenger_action_config(self, passenger_list):
    boarding_container = passenger_list.winfo_children()[0].winfo_children()[1]
    alighting_container = passenger_list.winfo_children()[1].winfo_children()[1]
    self.generator["Passenger"]["boarding_time_dist"] = distribution_parser(boarding_container)
    self.generator["Passenger"]["alighting_time_dist"] = distribution_parser(alighting_container)
    self.load_passenger_occupancy_config()

#endregion

#region Passenger Occupancy Configuration
def create_passenger_occupancy_config_container(route_list,_route_id):
    main_container = tk.Frame(route_list, height=110, width=200, bg=grey3)
    main_container.pack(side="top", fill='x', padx=5, pady=5)

    main_container.columnconfigure(0, weight=1)
    main_container.columnconfigure(1, weight=2)

    route_container = tk.Frame(main_container, height=110, width=200, bg=grey3)
    route_container.grid(row=0, column=0, padx=(5,0), pady=5, sticky='we')

    route_container.columnconfigure(0, weight=1)

    route_label = tk.Label(route_container, text="Route ID:",bg=grey3, font=('Segoe 12') )
    route_label.grid(row=0, column=0, padx=5, pady=2.5, sticky='w')

    route_id = tk.Label(route_container, text=_route_id, bg=grey3, font=('Segoe 12'))
    route_id.grid(row=0, column=1, padx=5, pady=2.5, sticky='w')

    distribution_container = tk.Frame(main_container, height=110, bg=grey3)
    distribution_container.grid(row=0, column=1, padx=5, pady=5, sticky='we') 

    load_exponencial_template(distribution_container)

def submit_passenger_occupancy_config(self, route_list):
    for main_container in route_list.winfo_children():
        data_container = main_container.winfo_children()[0]
        distribution_container = main_container.winfo_children()[1]
        route_id = data_container.winfo_children()[1]["text"]
        distribution = distribution_parser(distribution_container)
        self.generator["Route"][route_id]["initial_occupancy"] = distribution
    self.load_overview()
#endregion

def submit_generator_file(self):
    self.complete = True
    self.root.destroy()

def submit_regeneration_file(self,container):
    self.complete = True

def open_file_dialog(field):
    file_path = filedialog.askopenfilename(initialdir="files", title="Select File", filetypes=[("Json Files", "*.json")])
    if file_path:
        field.delete(0,tk.END)        
        field.insert(0,file_path)

#=================================App Class=======================================#
#region MainView
class MainView():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("400x400")
        self.root.title("VexSim")
        self.root.resizable(False,False)
        self.frame = None
        self.app_mode = None #["new","regenerate","reuse"]
        self.complete = False


        config = configparser.ConfigParser()
        config.read(".config")
        self.generator = {
        "Time":{
            "Duration": int(config.get('SimTime', 'sim_duration')),
            "Tick": float(config.get('SimTime', 'sim_tick'))},
        "Node":[],
        "Route":{},
        "Buses":{"top_speed": float(config.get('Buses', 'top_speed')), 
                 "acc":float(config.get('Buses', 'acceleration')),
                 "desc":float(config.get('Buses', 'deceleration'))},
        "Passenger":{}}
        self.passenger_dispatcher = None
        self.bus_dispatcher = None
        self.load_main_view()

#region Main View
    def load_main_view(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        button1 = tk.Button(master=self.frame, width=250, height=150, text="Create New Simulation", command=self.load_create_new)
        button2 = tk.Button(master=self.frame, width=250, height=150, text="Re-Use File", command=self.load_reuse)
        button3 = tk.Button(master=self.frame, width=250, height=150, text="Load Files", command=self.load_existing_file)

        button1.grid(row=0, column=0, padx=10, pady=10)
        button2.grid(row=1, column=0, padx=10, pady=10)
        button3.grid(row=2, column=0, padx=10, pady=10)

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)

        self.frame.grid_columnconfigure(0, weight=1, pad=15)
#endregion
#region Create New
    def load_create_new(self):
        self.app_mode = "new"
        self.frame.destroy()
        self.root.geometry(f"{window_width}x{window_height}")

        self.frame = tk.Frame(self.root, background=grey1)
        self.frame.pack(padx = 5, pady = 5, fill = 'both', expand = True)

        self.load_side_panel()
        self.load_node_creator()
        
#region Side Panel
    def load_side_panel(self):
        side_panel = tk.Frame(self.frame, width= window_width//6, bg=grey2)
        side_panel.pack(side="left",fill='y', padx=5, pady=5)

        node_creator_button = tk.Button(side_panel, text="Nodes Creator")
        node_creator_button.config(state="disabled")
        node_creator_button.pack(side="top",fill="both", pady=5, padx=5)

        route_creator_button = tk.Button(side_panel, text="Route Creator")
        route_creator_button.config(state="disabled")
        route_creator_button.pack(side="top",fill="both", pady=5, padx=5)

        stop_config_button = tk.Button(side_panel, text="Stop Configuration")
        stop_config_button.config(state="disabled")
        stop_config_button.pack(side="top",fill="both", pady=5, padx=5)

        route_configuration_button = tk.Button(side_panel, text="Route Configuration")
        route_configuration_button.config(state="disabled")
        route_configuration_button.pack(side="top",fill="both", pady=5, padx=5)

        passenger_action_configuration_button = tk.Button(side_panel, text="Passenger Action Configuration")
        passenger_action_configuration_button.config(state="disabled")
        passenger_action_configuration_button.pack(side="top",fill="both", pady=5, padx=5)

        passenger_occupancy_configuration_button = tk.Button(side_panel, text="Passenger Occupancy Configuration")
        passenger_occupancy_configuration_button.config(state="disabled")
        passenger_occupancy_configuration_button.pack(side="top",fill="both", pady=5, padx=5)

        generate_button = tk.Button(side_panel, text="Generate Files",command=lambda: submit_generator_file(self))
        generate_button.config(state="disabled")
        generate_button.pack(side="bottom",fill="both", pady=5, padx=5)
        
    def update_side_panel_activity(self, index):
        side_buttons = self.frame.winfo_children()[0].winfo_children()
        for i, button in enumerate(side_buttons):
            if index == i:
                button.config(state="active")
            else:
                button.config(state="disable")
            
    def enable_generator_file_button(self):
        generator_file_button = self.frame.winfo_children()[0].winfo_children()[-1]
        generator_file_button.config(state="active")
#endregion

    def load_node_creator(self):
        
        self.update_side_panel_activity(0)

        main_panel = tk.Frame(self.frame, bg=grey2)
        main_panel.pack(side="right", fill="both", padx=5, pady=5, expand=True)

        nodes_list = tk.Frame(main_panel)
        
        generate_button = tk.Button(main_panel, text="Add Node",command=lambda: create_street_node(self, nodes_list))
        generate_button.pack(side="top", fill="x", pady=5, padx=5)   

        nodes_list.pack(fill='both', expand=True, padx=5, pady=5)

        submit_nodes_button = tk.Button(main_panel, text="Submit Nodes",command=lambda: submit_nodes(self, nodes_list))
        submit_nodes_button.pack(side="bottom", fill="x", pady=5, padx=5)   

    def load_route_creator(self):
        self.update_side_panel_activity(1)
        self.frame.winfo_children()[1].destroy()

        main_panel = tk.Frame(self.frame, bg=grey2)
        main_panel.pack(side="right", fill="both", padx=5, pady=5, expand=True)

        #route_list = tk.Frame(main_panel)
        route_list = tk.Canvas(main_panel)
        
        generate_button = tk.Button(main_panel, text="Add Route",command=lambda: create_route_container(self, route_list))
        generate_button.pack(side="top", fill="x", pady=5, padx=5)   

        route_list.pack(side="top",fill='both', expand=True, padx=5, pady=5)


        submit_routes_button = tk.Button(main_panel, text="Submit Routes",command=lambda: submit_routes(self, route_list))
        submit_routes_button.pack(side="bottom", fill="x", pady=5, padx=5)
        
    def load_stop_config(self):
        self.update_side_panel_activity(2)
        self.frame.winfo_children()[1].destroy()

        main_panel = tk.Frame(self.frame, bg=grey2)
        main_panel.pack(side="right", fill="both", padx=5, pady=5, expand=True)

        title_label = tk.Label(main_panel, bg=grey2, text="Stop Passenger Arrival Configuration", font=('Segoe 14'))
        title_label.pack(side="top", fill="x", padx=5, pady=5)

        stop_list = tk.Frame(main_panel)
        stop_list.pack(side="top",fill='both', expand=True, padx=5, pady=5)

        stop_list.columnconfigure(0, weight=1)
        stop_list.columnconfigure(1, weight=3)

        for route_id, route_data in self.generator["Route"].items():
            stops = route_data["stops"]    
            for stop_id in stops:
                create_stop_config_container(stop_list,route_id,stop_id)

        submit_stop_config_button = tk.Button(main_panel, text="Submit Passenger Arrival Rate",command=lambda: submit_stop_config(self, stop_list))
        submit_stop_config_button.pack(side="bottom", fill="x", pady=5, padx=5)

    def load_route_config(self):
        self.update_side_panel_activity(3)
        self.frame.winfo_children()[1].destroy()

        main_panel = tk.Frame(self.frame, bg=grey2)
        main_panel.pack(side="right", fill="both", padx=5, pady=5, expand=True)

        title_label = tk.Label(main_panel, bg=grey2, text="Route Bus Arrival Configuration", font=('Segoe 14'))
        title_label.pack(side="top", fill="x", padx=5, pady=5)

        route_list = tk.Frame(main_panel)
        route_list.pack(side="top",fill='both', expand=True, padx=5, pady=5)

        for route_id in self.generator["Route"].keys():
            create_route_config_container(route_list,route_id)

        submit_route_config_button = tk.Button(main_panel, text="Submit Bus Arrival Rate",command=lambda: submit_route_config(self, route_list))
        submit_route_config_button.pack(side="bottom", fill="x", pady=5, padx=5)

    def load_passenger_action_config(self):
        self.update_side_panel_activity(4)
        self.frame.winfo_children()[1].destroy()

        main_panel = tk.Frame(self.frame, bg=grey2)
        main_panel.pack(side="right", fill="both", padx=5, pady=5, expand=True)

        title_label = tk.Label(main_panel, bg=grey2, text="Passenger Boarding/Alighting Configuration", font=('Segoe 14'))
        title_label.pack(side="top", fill="x", padx=5, pady=5)

        passenger_list = tk.Frame(main_panel)
        passenger_list.pack(side="top",fill='both', expand=True, padx=5, pady=5)

        create_passenger_action_config_container(passenger_list,"Passenger Boarding Distribution")
        create_passenger_action_config_container(passenger_list,"Passenger Alighting Distribution")

        submit_passenger_action_config_button = tk.Button(main_panel, text="Submit Passenger Configuration",command=lambda: submit_passenger_action_config(self, passenger_list))
        submit_passenger_action_config_button.pack(side="bottom", fill="x", pady=5, padx=5)

    def load_passenger_occupancy_config(self):
        self.update_side_panel_activity(5)
        self.frame.winfo_children()[1].destroy()

        main_panel = tk.Frame(self.frame, bg=grey2)
        main_panel.pack(side="right", fill="both", padx=5, pady=5, expand=True)

        title_label = tk.Label(main_panel, bg=grey2, text="Passenger Occupancy Configuration", font=('Segoe 14'))
        title_label.pack(side="top", fill="x", padx=5, pady=5)

        route_list = tk.Frame(main_panel)
        route_list.pack(side="top",fill='both', expand=True, padx=5, pady=5)

        for route_id in self.generator["Route"].keys():
            create_passenger_occupancy_config_container(route_list,route_id)

        submit_passenger_occupancy_config_button = tk.Button(main_panel, text="Submit Bus Arrival Rate",command=lambda: submit_passenger_occupancy_config(self, route_list))
        submit_passenger_occupancy_config_button.pack(side="bottom", fill="x", pady=5, padx=5)
     
    def load_overview(self):
        self.update_side_panel_activity(99)
        self.enable_generator_file_button()
        self.frame.winfo_children()[1].destroy()
        pass
#endregion
#region Reuse Generator File 

    def load_reuse(self):
        self.app_mode = "regenerate"
        self.frame.destroy()
        self.root.geometry("200x300")

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx = 5, pady = 5, fill = 'both', expand = True)

        title_label = tk.Label(self.frame ,text="Regenerate Files", font=('Segoe 12 underline'))
        title_label.pack(pady=(5,60), padx=5)

        path_container = tk.Frame(self.frame)
        path_container.pack(fill="x")

        file_path_label = tk.Label(path_container ,text="Generator File Path:", font=('Segoe 10'))
        file_path_label.pack(padx=0, side="top",anchor="w")


        # Entry widget for the file path
        file_path_entry = tk.Entry(path_container)
        file_path_entry.pack(side="left", pady=5, padx=5,fill="x", expand=True)

        # Button widget to trigger the file regeneration
        path_button = tk.Button(path_container, text="...", command=lambda: open_file_dialog(file_path_entry))
        path_button.pack(side="right")

        regenerate_button = tk.Button(self.frame, text="Generate Files", command=None)
        regenerate_button.pack(side="bottom", anchor="s", padx=5, pady=5)

        

#endregion
#region Use Existing Files
    def load_existing_file(self):
        self.app_mode = "reuse"
        self.frame.destroy()
        self.root.geometry("400x600")

        self.frame = tk.Frame(self.root, background=grey1)
        self.frame.pack(padx = 5, pady = 5, fill = 'both', expand = True)

        select_button = tk.Button(self.frame, text="Select File", command=open_file_dialog(self))
        select_button.pack(pady=10)

        submit_button = tk.Button(self.frame, text="Submit")
        submit_button.pack(pady=10)
        
#endregion
#endregion
