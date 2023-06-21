import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

grey1 = "#D4D4D4"
grey2 = "#B4B4B4"
grey3 = "#909090"
grey4 = "#636363"

window_width = 1280
window_height = 800


def destroy_frame_children(frame):
    for child in frame.winfo_children():
        child.destroy()


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
        return {node_type: {"length": value1, "tracks": value2}}
    elif node_type == "Stop":
        return {node_type: {"id": value1, "berths": value2}}
    elif node_type == "Intersection":
        return {node_type: {"cicle": value1, "green": value2}}

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
    self.load_stop_conf()

#endregion

#region Stop Configuration
def create_stop_config_container(self,stop_list,_route_id, _stop_id):
    stop_container = tk.Frame(stop_list, height=100, bg=grey3)
    stop_container.pack(anchor='n', fill='x', padx=5, pady=5,)

    route_label = tk.Label(stop_container, text="Route ID:",bg=grey3, font=('Segoe 12') )
    route_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    route_id = tk.Label(stop_container, text=_route_id, bg=grey3, font=('Segoe 12'))
    route_id.grid(row=0, column=1, padx=5, pady=5, sticky='we')

    stop_label = tk.Label(stop_container, text="Stop ID:", bg=grey3, font=('Segoe 12'))
    stop_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')

    stop_id = tk.Label(stop_container, text=_stop_id, bg=grey3, font=('Segoe 12'))
    stop_id.grid(row=1, column=1, padx=5, pady=5, sticky='we')

    distribution_label = tk.Label(stop_container,text="Distribution", bg=grey3, font=('Segoe 12'))
    distribution_label.grid(row=0, column=3, padx=5, pady=5, sticky='nswe')

    distribution_selector = ttk.Combobox(stop_container, values=["Exponencial","Uniform","Normal","Fixed"], width=1)
    distribution_selector.set("Exponencial")
    distribution_selector.bind('<<ComboboxSelected>>', lambda event: distribution_selector_change(self, distribution_selector))
    distribution_selector.grid(row=1, column=3, padx=5, pady=5, sticky='nsew')

    rate_label = tk.Label(stop_container,text="Distribution Rate exp(rate)", bg=grey3, font=('Segoe 12'))
    rate_label.grid(row=0, column=4, padx=5, pady=5, sticky='nswe')

    rate_field = tk.Entry(stop_container)
    rate_field.grid(row=1, column=4, padx=5, pady=5, sticky='nswe')

    stop_container.columnconfigure(0, weight=0)
    stop_container.columnconfigure(1, weight=0)
    stop_container.columnconfigure(2, weight=1)
    stop_container.columnconfigure(3, weight=2)
    stop_container.columnconfigure(4, weight=1)

def load_exponencial_stop_config_container(self,stop_container,_route_id, _stop_id):

    route_label = tk.Label(stop_container, text="Route ID:",bg=grey3, font=('Segoe 12') )
    route_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    route_id = tk.Label(stop_container, text=_route_id, bg=grey3, font=('Segoe 12'))
    route_id.grid(row=0, column=1, padx=5, pady=5, sticky='we')

    stop_label = tk.Label(stop_container, text="Stop ID:", bg=grey3, font=('Segoe 12'))
    stop_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')

    stop_id = tk.Label(stop_container, text=_stop_id, bg=grey3, font=('Segoe 12'))
    stop_id.grid(row=1, column=1, padx=5, pady=5, sticky='we')

    distribution_label = tk.Label(stop_container,text="Distribution", bg=grey3, font=('Segoe 12'))
    distribution_label.grid(row=0, column=3, padx=5, pady=5, sticky='nswe')

    distribution_selector = ttk.Combobox(stop_container, values=["Exponencial","Uniform","Normal","Fixed"], width=1)
    distribution_selector.set("Exponencial")
    distribution_selector.bind('<<ComboboxSelected>>', lambda event: distribution_selector_change(self, distribution_selector))
    distribution_selector.grid(row=1, column=3, padx=5, pady=5, sticky='nsew')

    rate_label = tk.Label(stop_container,text="Distribution Rate exp(rate)", bg=grey3, font=('Segoe 12'))
    rate_label.grid(row=0, column=4, padx=5, pady=5, sticky='nswe')

    rate_field = tk.Entry(stop_container)
    rate_field.grid(row=1, column=4, padx=5, pady=5, sticky='nswe')

    stop_container.columnconfigure(0, weight=0)
    stop_container.columnconfigure(1, weight=0)
    stop_container.columnconfigure(2, weight=1)
    stop_container.columnconfigure(3, weight=2)
    stop_container.columnconfigure(4, weight=1)

def load_uniform_stop_config_container(self,stop_container,_route_id, _stop_id):

    route_label = tk.Label(stop_container, text="Route ID:",bg=grey3, font=('Segoe 12') )
    route_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    route_id = tk.Label(stop_container, text=_route_id, bg=grey3, font=('Segoe 12'))
    route_id.grid(row=0, column=1, padx=5, pady=5, sticky='we')

    stop_label = tk.Label(stop_container, text="Stop ID:", bg=grey3, font=('Segoe 12'))
    stop_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')

    stop_id = tk.Label(stop_container, text=_stop_id, bg=grey3, font=('Segoe 12'))
    stop_id.grid(row=1, column=1, padx=5, pady=5, sticky='we')

    distribution_label = tk.Label(stop_container,text="Distribution", bg=grey3, font=('Segoe 12'))
    distribution_label.grid(row=0, column=3, padx=5, pady=5, sticky='nswe')

    distribution_selector = ttk.Combobox(stop_container, values=["Exponencial","Uniform","Normal","Fixed"], width=1)
    distribution_selector.set("Uniform")
    distribution_selector.bind('<<ComboboxSelected>>', lambda event: distribution_selector_change(self, distribution_selector))
    distribution_selector.grid(row=1, column=3, padx=5, pady=5, sticky='nsew')

    a_label = tk.Label(stop_container,text="A", bg=grey3, font=('Segoe 12'))
    a_label.grid(row=0, column=4, padx=5, pady=5, sticky='nswe')

    a_field = tk.Entry(stop_container)
    a_field.grid(row=1, column=4, padx=5, pady=5, sticky='nswe')

    b_label = tk.Label(stop_container,text="B", bg=grey3, font=('Segoe 12'))
    b_label.grid(row=0, column=5, padx=5, pady=5, sticky='nswe')

    b_field = tk.Entry(stop_container)
    b_field.grid(row=1, column=5, padx=5, pady=5, sticky='nswe')

    stop_container.columnconfigure(0, weight=0)
    stop_container.columnconfigure(1, weight=0)
    stop_container.columnconfigure(2, weight=1)
    stop_container.columnconfigure(3, weight=2)
    stop_container.columnconfigure(4, weight=1)
    stop_container.columnconfigure(5, weight=1)

def load_normal_stop_config_container(self,stop_container,_route_id, _stop_id):

    route_label = tk.Label(stop_container, text="Route ID:",bg=grey3, font=('Segoe 12') )
    route_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    route_id = tk.Label(stop_container, text=_route_id, bg=grey3, font=('Segoe 12'))
    route_id.grid(row=0, column=1, padx=5, pady=5, sticky='we')

    stop_label = tk.Label(stop_container, text="Stop ID:", bg=grey3, font=('Segoe 12'))
    stop_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')

    stop_id = tk.Label(stop_container, text=_stop_id, bg=grey3, font=('Segoe 12'))
    stop_id.grid(row=1, column=1, padx=5, pady=5, sticky='we')

    distribution_label = tk.Label(stop_container,text="Distribution", bg=grey3, font=('Segoe 12'))
    distribution_label.grid(row=0, column=3, padx=5, pady=5, sticky='nswe')

    distribution_selector = ttk.Combobox(stop_container, values=["Exponencial","Uniform","Normal","Fixed"], width=1)
    distribution_selector.set("Normal")
    distribution_selector.bind('<<ComboboxSelected>>', lambda event: distribution_selector_change(self, distribution_selector))
    distribution_selector.grid(row=1, column=3, padx=5, pady=5, sticky='nsew')

    mu_label = tk.Label(stop_container,text="Mean", bg=grey3, font=('Segoe 12'))
    mu_label.grid(row=0, column=4, padx=5, pady=5, sticky='nswe')

    mu_field = tk.Entry(stop_container)
    mu_field.grid(row=1, column=4, padx=5, pady=5, sticky='nswe')

    stdv_label = tk.Label(stop_container,text="Standard Deviation", bg=grey3, font=('Segoe 12'))
    stdv_label.grid(row=0, column=5, padx=5, pady=5, sticky='nswe')

    stdv_field = tk.Entry(stop_container)
    stdv_field.grid(row=1, column=5, padx=5, pady=5, sticky='nswe')

    stop_container.columnconfigure(0, weight=0)
    stop_container.columnconfigure(1, weight=0)
    stop_container.columnconfigure(2, weight=1)
    stop_container.columnconfigure(3, weight=2)
    stop_container.columnconfigure(4, weight=1)
    stop_container.columnconfigure(5, weight=1)

def load_fixed_stop_config_container(self,stop_container,_route_id, _stop_id):

    route_label = tk.Label(stop_container, text="Route ID:",bg=grey3, font=('Segoe 12') )
    route_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    route_id = tk.Label(stop_container, text=_route_id, bg=grey3, font=('Segoe 12'))
    route_id.grid(row=0, column=1, padx=5, pady=5, sticky='we')

    stop_label = tk.Label(stop_container, text="Stop ID:", bg=grey3, font=('Segoe 12'))
    stop_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')

    stop_id = tk.Label(stop_container, text=_stop_id, bg=grey3, font=('Segoe 12'))
    stop_id.grid(row=1, column=1, padx=5, pady=5, sticky='we')

    distribution_label = tk.Label(stop_container,text="Distribution", bg=grey3, font=('Segoe 12'))
    distribution_label.grid(row=0, column=3, padx=5, pady=5, sticky='nswe')

    distribution_selector = ttk.Combobox(stop_container, values=["Exponencial","Uniform","Normal","Fixed"], width=1)
    distribution_selector.set("Fixed")
    distribution_selector.bind('<<ComboboxSelected>>', lambda event: distribution_selector_change(self, distribution_selector))
    distribution_selector.grid(row=1, column=3, padx=5, pady=5, sticky='nsew')

    rate_label = tk.Label(stop_container,text="Arrival Rate", bg=grey3, font=('Segoe 12'))
    rate_label.grid(row=0, column=4, padx=5, pady=5, sticky='nswe')

    rate_field = tk.Entry(stop_container)
    rate_field.grid(row=1, column=4, padx=5, pady=5, sticky='nswe')

    stop_container.columnconfigure(0, weight=0)
    stop_container.columnconfigure(1, weight=0)
    stop_container.columnconfigure(2, weight=1)
    stop_container.columnconfigure(3, weight=2)
    stop_container.columnconfigure(4, weight=1)

def distribution_selector_change(self, distribution_selector):
    selection = distribution_selector.get()
    stop_config_container_path = distribution_selector.winfo_parent()
    stop_config_container = self.root.nametowidget(stop_config_container_path)
    update_existing_stop_config(self, stop_config_container, selection)

def update_existing_stop_config(self, stop_config_container, distribution):
    route_id= stop_config_container.winfo_children()[1]["text"]
    stop_id= stop_config_container.winfo_children()[3]["text"]
    destroy_frame_children(stop_config_container)
    if distribution == "Exponencial":
        load_exponencial_stop_config_container(self, stop_config_container,route_id,stop_id)
    elif distribution == "Uniform":
        load_uniform_stop_config_container(self, stop_config_container,route_id,stop_id)
    elif distribution == "Normal":
        load_normal_stop_config_container(self, stop_config_container,route_id,stop_id)
    elif distribution == "Fixed":
        load_fixed_stop_config_container(self, stop_config_container,route_id,stop_id)

def stop_config_parser(self, stop_list):

    pass


def submit_config(self, stop_list):

    pass

#endregion

#region Route Configuration
#endregion

#region Passenger Configuration
#endregion

#=================================App Class=======================================#
#region InputView
class InputView():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("400x400")
        self.root.title("VexSim")
        self.root.resizable(False,False)
        self.frame = None
        self.generator = {
        "Time":{
            "Duration": 3600,
            "Tick": 0.5},
        "Node":[],
        "Route":{},
        "Buses":{},
        "Passengers":{}}
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
        node_creator_button.pack(side="top", pady=5, padx=5)

        route_creator_button = tk.Button(side_panel, text="Route Creator")
        route_creator_button.config(state="disabled")
        route_creator_button.pack(side="top", pady=5, padx=5)

        stop_config_button = tk.Button(side_panel, text="Stop Configuration")
        stop_config_button.config(state="disabled")
        stop_config_button.pack(side="top", pady=5, padx=5)

        route_configuration_button = tk.Button(side_panel, text="Route Configuration")
        route_configuration_button.config(state="disabled")
        route_configuration_button.pack(side="top", pady=5, padx=5)

        passenger_configuration_button = tk.Button(side_panel, text="Passenger Configuration")
        passenger_configuration_button.config(state="disabled")
        passenger_configuration_button.pack(side="top", pady=5, padx=5)

        generate_button = tk.Button(side_panel, text="Generate Files")
        generate_button.config(state="disabled")
        generate_button.pack(side="bottom", pady=5, padx=5)
        
    def update_side_panel_activity(self, index):
        side_buttons = self.frame.winfo_children()[0].winfo_children()
        for i, button in enumerate(side_buttons):
            if index == i:
                button.config(state="active")
            else:
                button.config(state="disable")
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
        
    def load_stop_conf(self):
        self.update_side_panel_activity(2)
        self.frame.winfo_children()[1].destroy()

        main_panel = tk.Frame(self.frame, bg=grey2)
        main_panel.pack(side="right", fill="both", padx=5, pady=5, expand=True)

        title_label = tk.Label(main_panel, bg=grey2, text="Passenger Arrival Configuration", font=('Segoe 14'))
        title_label.pack(side="top", fill="x", padx=5, pady=5)

        stop_list = tk.Frame(main_panel)
        stop_list.pack(side="top",fill='both', expand=True, padx=5, pady=5)

        for route_id, route_data in self.generator["Route"].items():
            stops = route_data["stops"]    
            for stop_id in stops:
                create_stop_config_container(self,stop_list,route_id,stop_id)

        submit_stop_config_button = tk.Button(main_panel, text="Submit Routes",command=lambda: submit_config(self, stop_list))
        submit_stop_config_button.pack(side="bottom", fill="x", pady=5, padx=5)

        pass

    def load_route_conf(self):
        self.update_side_panel_activity(3)
        self.frame.winfo_children()[1].destroy()
        pass

    def load_passenger_conf(self):
        self.update_side_panel_activity(5)
        self.frame.winfo_children()[1].destroy()
        pass
     
#endregion
#region Reuse Generator File 
    def load_reuse(self):
        pass
#endregion
#region Use Existing Files
    def load_existing_file(self):
        pass
#endregion
#endregion

    

    

app = InputView()
app.root.mainloop()