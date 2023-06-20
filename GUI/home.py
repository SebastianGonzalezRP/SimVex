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
        if node_type == "Street":
            street_length = node.winfo_children()[3].get()
            street_tracks = node.winfo_children()[5].get()
            if street_length != "" and street_tracks != "":
                nodes.append(node_parser(node_type, street_length, street_tracks))
            else:
                tk.messagebox.showinfo(" ",f"{node_type} Attribute may not be Empty")
                break
        elif node_type == "Stop":
            stop_id = node.winfo_children()[3].get()
            n_berths = node.winfo_children()[5].get()
            if stop_id != "" and n_berths != "":
                nodes.append(node_parser(node_type, stop_id, n_berths))
            else:
                tk.messagebox.showinfo(" ",f"{node_type} Attribute may not be Empty")
                break
        elif node_type == "Intersection":
            cicle = node.winfo_children()[3].get()
            effective_g = node.winfo_children()[5].get()
            if cicle != "" and effective_g != "":
                nodes.append(node_parser(node_type, cicle, effective_g))
            else:
                tk.messagebox.showinfo(" ",f"{node_type} Attribute may not be Empty")
                break
    if (len(nodes) == len(nodes_list.winfo_children())):
        self.generator["Node"] = nodes
        print(self.generator)
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
def create_stop_container(self,stop_list):

    pass

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

        stop_list = tk.Frame(main_panel)
        stop_list.pack(side="top",fill='both', expand=True, padx=5, pady=5)


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