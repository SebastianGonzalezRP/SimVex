import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from models.bus_model import *
from GUI.style import *

grey1 = "#D4D4D4"
grey2 = "#B4B4B4"
grey3 = "#909090"
grey4 = "#636363"

window_width = 1280
window_height = 800

def delete_parent_container(container):
    container.destroy()


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

    rate_label = tk.Label(container,text="Rate (seconds)", bg=grey3, font=('Segoe 12'))
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
    else:
        return None

#region Sim Time Parameters


def submit_time_config(self,time_list):

    try:
        duration = int(time_list.winfo_children()[1].get())
        tick = float(time_list.winfo_children()[3].get())
        
        self.controller.generator["Time"]["Duration"] = duration
        self.controller.generator["Time"]["Tick"] = tick

        self.load_node_creator()
    except:
        tk.messagebox.showinfo(" ",f"Fields may not be empty")

#endregion



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

    length_label = tk.Label(node_container, text="Street Length (m)", bg=grey3)
    length_label.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

    length_field = tk.Entry(node_container)
    length_field.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

    ntracks_label = tk.Label(node_container, text="Number of Tracks", bg=grey3)
    ntracks_label.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

    number_spinbox = ttk.Spinbox(node_container, from_=2, to=2)
    number_spinbox.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

    delete_button = tk.Button(node_container, text="X", bg="red", command=lambda: delete_parent_container(node_container))
    delete_button.grid(row=0,column=3, padx= (0,2), pady=(2,0), sticky='ne')

    node_container.columnconfigure(0, weight=4)
    node_container.columnconfigure(1, weight=4)
    node_container.columnconfigure(2, weight=4)
    node_container.columnconfigure(3, weight=1)

def load_street_node(self,node_container):

    node_label = tk.Label(node_container, text="Node Type", bg=grey3)
    node_label.grid(row=0, column=0, padx=5, pady=5, sticky='nswe')

    node_selector = ttk.Combobox(node_container, values=["Street","Stop","Intersection"])
    node_selector.set("Street")
    node_selector.bind('<<ComboboxSelected>>', lambda event: node_selector_change(self, node_selector))
    node_selector.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

    length_label = tk.Label(node_container, text="Street Length (m)", bg=grey3)
    length_label.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

    length_field = tk.Entry(node_container)
    length_field.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

    ntracks_label = tk.Label(node_container, text="Number of Lanes", bg=grey3)
    ntracks_label.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

    number_spinbox = ttk.Spinbox(node_container, from_=2, to=2)
    number_spinbox.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

    delete_button = tk.Button(node_container, text="X", bg="red", command=lambda: delete_parent_container(node_container))
    delete_button.grid(row=0,column=3, padx= (0,2), pady=(2,0), sticky='ne')

    node_container.columnconfigure(0, weight=4)
    node_container.columnconfigure(1, weight=4)
    node_container.columnconfigure(2, weight=4)
    node_container.columnconfigure(3, weight=1)

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

    delete_button = tk.Button(node_container, text="X", bg="red", command=lambda: delete_parent_container(node_container))
    delete_button.grid(row=0,column=3, padx= (0,2), pady=(2,0), sticky='ne')

    node_container.columnconfigure(0, weight=4)
    node_container.columnconfigure(1, weight=4)
    node_container.columnconfigure(2, weight=4)
    node_container.columnconfigure(3, weight=1)

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

    effective_green_label = tk.Label(node_container, text="Green Ratio", bg=grey3)
    effective_green_label.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

    effective_green = ttk.Spinbox(node_container, from_=0, to=1, increment=0.01)
    effective_green.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

    delete_button = tk.Button(node_container, text="X", bg="red", command=lambda: delete_parent_container(node_container))
    delete_button.grid(row=0,column=3, padx= (0,2), pady=(2,0), sticky='ne')

    node_container.columnconfigure(0, weight=4)
    node_container.columnconfigure(1, weight=4)
    node_container.columnconfigure(2, weight=4)
    node_container.columnconfigure(3, weight=1)

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
        self.controller.generator["Node"] = nodes
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
    for node in self.controller.generator["Node"]:
        if list(node.keys())[0] == "Stop":
            existing_stops.insert(tk.END, node["Stop"]["id"])

    
    add_stop_button = tk.Button(route_container, text="Add Stop",command=lambda: listbox_switch(existing_stops,selected_stops))
    add_stop_button.grid(row=2, column=1, padx=5, pady=5, sticky='nwe')

    selected_stops_label = tk.Label(route_container, text="Selected Stops", bg=grey3)
    selected_stops_label.grid(row=0, column=2, padx=5, pady=5, sticky='nswe')

    selected_stops = tk.Listbox(route_container, selectmode=tk.MULTIPLE, height=5)
    selected_stops.grid(row=1, column=2, padx=5, pady=5, sticky='nwe')
    
    remove_stop_button = tk.Button(route_container, text="Remove Stop",command=lambda: listbox_switch(selected_stops, existing_stops))
    remove_stop_button.grid(row=2, column=2, padx=5, pady=5, sticky='nwe')

    delete_button = tk.Button(route_container, text="X", bg="red", command=lambda: delete_parent_container(route_container))
    delete_button.grid(row=0,column=3, padx= (0,2), pady=(2,0), sticky='ne')

    route_container.columnconfigure(0, weight=4)
    route_container.columnconfigure(1, weight=4)
    route_container.columnconfigure(2, weight=4)
    route_container.columnconfigure(3, weight=1)
    pass

def listbox_switch(origin,target):
    selections = []
    for index in reversed(origin.curselection()):
        selections.append(origin.get(index))
        origin.delete(index)
    for stop in reversed(selections):
        target.insert(tk.END, stop)

def submit_routes(self, route_list):
    route_parsed_count = 0
    for route in route_list.winfo_children():
        route_id = route.winfo_children()[1].get()
        stops_id_list = list(route.winfo_children()[6].get(0,"end"))
        if route_id != "" and len(stops_id_list) > 0:
            self.controller.generator["Route"][route_id]= {"stops": {},
                                                    "bus_rate": {},
                                                    "initial_occupancy":{},
                                                    "bus_model":{}}
            for stop_id in stops_id_list:
                self.controller.generator["Route"][route_id]["stops"][stop_id]= {"passenger_rate":{}}
            route_parsed_count += 1
        else:
            route_parsed_count = 0
            tk.messagebox.showinfo(" ",f"Route Attributes Can Not Be Empty")
            break
    if route_parsed_count > 0:
        self.load_route_bus_config()

#endregion

#region Route-Bus Configuration

def create_bus_model_card(bus_card_container,model_key,model_stats):

    bus_card = tk.Frame(bus_card_container, bg=grey3)
    bus_card.pack(side="left",expand=True ,fill="both", padx=5, pady=5)

    model_label = tk.Label(bus_card, bg=grey3, text=model_key, font=('Helvetica 10 underline'))
    model_label.grid(row=0, column=0, sticky="W", padx=(5,0))

    door_number_label = tk.Label(bus_card, bg=grey3, text="Door Number: ")
    door_number_label.grid(row=1,column=0, sticky="W", padx=(5,0))

    door_number_value = tk.Label(bus_card, bg=grey3, text=model_stats["door_n"])
    door_number_value.grid(row=1,column=1, sticky="W", padx=(0,2))

    top_speed_label = tk.Label(bus_card, bg=grey3, text="Top Speed: ")
    top_speed_label.grid(row=2,column=0, sticky="W", padx=(5,0))

    top_speed_value = tk.Label(bus_card, bg=grey3, text=f"{model_stats["top_speed"]} (m/s)")
    top_speed_value.grid(row=2,column=1, sticky="W", padx=(0,2))

    acceleration_label = tk.Label(bus_card, bg=grey3, text="Acceleration Rate: ")
    acceleration_label.grid(row=3,column=0, sticky="W", padx=(5,0))

    acceleration_value = tk.Label(bus_card, bg=grey3, text=f"{model_stats["acc"]} (m/s2)")
    acceleration_value.grid(row=3,column=1, sticky="W", padx=(0,2))

    desceleration_label = tk.Label(bus_card, bg=grey3, text="Deceleration Rate: ")
    desceleration_label.grid(row=4,column=0, sticky="W", padx=(5,0))

    desceleration_value = tk.Label(bus_card, bg=grey3, text=f"{model_stats["desc"]} (m/s2)")
    desceleration_value.grid(row=4,column=1, sticky="W", padx=(0,2))

    bus_card.grid_rowconfigure(0,weight=1)
    bus_card.grid_rowconfigure(1,weight=1)
    bus_card.grid_rowconfigure(2,weight=1)
    bus_card.grid_rowconfigure(3,weight=1)

    bus_card.grid_columnconfigure(0,weight=2)
    bus_card.grid_columnconfigure(1,weight=1)


def create_route_bus_container(route_list,_route_id):

    main_container = tk.Frame(route_list, height=110, width=200, bg=grey3)
    main_container.pack(side="top", fill='x', padx=5, pady=5)

    route_container = tk.Frame(main_container,  bg=grey3) 
    route_container.pack(side="left", fill="y",anchor="w",padx=5, pady=5)

    route_label = tk.Label(route_container, text="Route ID:",bg=grey3, font=('Segoe 12') )
    route_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    route_id = tk.Label(route_container, text=_route_id, bg=grey3, font=('Segoe 12'))
    route_id.grid(row=0, column=1, padx=5, pady=5, sticky='we')

    model_container = tk.Frame(main_container,bg=grey3,)
    model_container.pack(side="left", fill="both",expand=True, anchor="w",padx=5, pady=5)

    available_models_label = tk.Label(model_container, text="Available Models", bg=grey3)
    available_models_label.grid(row=0, column=0, padx=10, pady=5, sticky='nswe')

    available_models = tk.Listbox(model_container, selectmode=tk.MULTIPLE, height=5)
    available_models.grid(row=1, column=0, padx=10, pady=5, sticky='nwe')
    for model in bus_models:
        available_models.insert(tk.END, model)

    add_model_button = tk.Button(model_container, text="Add Model",command=lambda: listbox_switch(available_models,selected_models))
    add_model_button.grid(row=2, column=0, padx=10, pady=5, sticky='nwe')

    selected_models_label = tk.Label(model_container, text="Selected Models", bg=grey3)
    selected_models_label.grid(row=0, column=1, padx=10, pady=5, sticky='nswe')

    selected_models = tk.Listbox(model_container, selectmode=tk.MULTIPLE, height=5)
    selected_models.grid(row=1, column=1, padx=10, pady=5, sticky='nwe')
    
    remove_models_button = tk.Button(model_container, text="Remove Model",command=lambda: listbox_switch(selected_models, available_models))
    remove_models_button.grid(row=2, column=1, padx=10, pady=5, sticky='nwe')

    model_container.columnconfigure(0, weight=1)
    model_container.columnconfigure(1, weight=1)

def parse_route_bus(self,route_id, selected_models):
    for model in selected_models:
        self.controller.generator["Route"][route_id]["bus_model"][model] = bus_models[model]



def submit_route_bus_config(self,route_list):

    route_parsed_count = 0
    route_count  = len(route_list.winfo_children())
    for main_container in route_list.winfo_children():
        route_container = main_container.winfo_children()[0]
        route_id = route_container.winfo_children()[1].cget("text")

        model_container = main_container.winfo_children()[1]
        selected_models = list(model_container.winfo_children()[4].get(0,"end"))

        if len(selected_models) > 0:
            parse_route_bus(self,route_id,selected_models)
            route_parsed_count +=1
        else:
            route_parsed_count = 0
            tk.messagebox.showinfo(" ",f"Route {route_id} is missing Bus Model")
            break
        if route_parsed_count == route_count:
            self.load_route_arrival_config()

        
#endregion

#region Route Arrival Configuration
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
        self.controller.generator["Route"][route_id]["bus_rate"] = distribution
    self.load_passenger_arrival_config()
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
        self.controller.generator["Route"][route_id]["stops"][stop_id]["passenger_rate"] = distribution
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
    self.controller.generator["Passenger"]["boarding_time_dist"] = distribution_parser(boarding_container)
    self.controller.generator["Passenger"]["alighting_time_dist"] = distribution_parser(alighting_container)
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
        if distribution != None and route_id != "":
            self.controller.generator["Route"][route_id]["initial_occupancy"] = distribution
    self.load_overview()
#endregion

def submit_generator_file(self):
    self.controller.complete = True
    self.root.destroy()

def submit_regeneration_file(self,container):
    self.controller.complete = True
    path = container.get()
    if path != "":
        self.controller.generator_path = path
        self.controller.load_generator_from_path(path)
        self.root.destroy()
    else:
        tk.messagebox.showinfo(" ","Missing Path")

def submit_reuse_file(self,json_container,passenger_container,bus_container):
    
    self.controller.complete = True
    json_path = json_container.get()
    passenger_path = passenger_container.get()
    bus_path = bus_container.get()
    if json_path != "" and passenger_path != "" and bus_path != "":
        self.controller.generator_path = json_path
        self.controller.passenger_dispatcher_path = passenger_path
        self.controller.bus_dispatcher_path = bus_path
        self.root.destroy()
    else:
        tk.messagebox.showinfo(" ","Missing Paths")

def open_json_file_dialog(field):
    file_path = filedialog.askopenfilename(initialdir="files", title="Select File", filetypes=[("Json Files", "*.json")])
    if file_path:
        field.delete(0,tk.END)        
        field.insert(0,file_path)

def open_csv_file_dialog(field):
    file_path = filedialog.askopenfilename(initialdir="files", title="Select File", filetypes=[("CSV", "*.csv")])
    if file_path:
        field.delete(0,tk.END)        
        field.insert(0,file_path)

#=================================App Class=======================================#
#region MainView Class
class MainView():
    def __init__(self,controller):
        self.root = tk.Tk()
        self.root.geometry("400x400")
        self.root.title("SimVex")
        self.root.configure(bg=grey1)
        self.root.resizable(False,False)
        self.frame = None

        self.controller = controller
        self.load_main_view()

#region Main View
    def load_main_view(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        button1 = tk.Button(master=self.frame, width=250, height=150, 
                            text="Create New Simulation",command=self.load_create_new)
        button2 = tk.Button(master=self.frame, width=250, height=150, 
                            text="Re-Use File", command=self.load_reuse)
        button3 = tk.Button(master=self.frame, width=250, height=150, 
                            text="Load Files", command=self.load_existing_file)

        button1.grid(row=0, column=0, padx=5, pady=(5,5))
        button2.grid(row=1, column=0, padx=5, pady=(0,5))
        button3.grid(row=2, column=0, padx=5, pady=(0,5))

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)

        self.frame.grid_columnconfigure(0, weight=1, pad=15)
#endregion
#region Create New
    def load_create_new(self):
        self.controller.app_mode = "new"
        self.frame.destroy()
        self.root.geometry(f"{window_width}x{window_height}")

        self.frame = tk.Frame(self.root, background=grey1)
        self.frame.pack(padx = 5, pady = 5, fill = 'both', expand = True)

        self.load_side_panel()
        self.load_time_config()
        
#region Side Panel
    def load_side_panel(self):
        side_panel = tk.Frame(self.frame, width= window_width//6, bg=grey2)
        side_panel.pack(side="left",fill='y', padx=5, pady=5)

        time_config_button = tk.Button(side_panel,text="Time Configuration",command=self.load_time_config)
        time_config_button.config(state="disabled")
        time_config_button.pack(side="top",fill="both", pady=5, padx=5)

        node_creator_button = tk.Button(side_panel, text="Nodes Creator", command=self.load_node_creator)
        node_creator_button.config(state="disabled")
        node_creator_button.pack(side="top",fill="both", pady=5, padx=5)

        route_creator_button = tk.Button(side_panel, text="Route Creator", command=self.load_route_creator)
        route_creator_button.config(state="disabled")
        route_creator_button.pack(side="top",fill="both", pady=5, padx=5)

        route_bus_button = tk.Button(side_panel, text="Route-Bus Configuration", command=self.load_route_bus_config)
        route_bus_button.config(state="disabled")
        route_bus_button.pack(side="top",fill="both", pady=5, padx=5)

        route_arrival_button = tk.Button(side_panel, text="Route-Arrival Configuration", command= self.load_route_arrival_config)
        route_arrival_button.config(state="disabled")
        route_arrival_button.pack(side="top",fill="both", pady=5, padx=5)

        passanger_arrival_config_button = tk.Button(side_panel, text="Passanger Arrival Configuration", command=self.load_passenger_arrival_config)
        passanger_arrival_config_button.config(state="disabled")
        passanger_arrival_config_button.pack(side="top",fill="both", pady=5, padx=5)

        passenger_action_configuration_button = tk.Button(side_panel, text="Passenger Action Configuration", command=self.load_passenger_action_config)
        passenger_action_configuration_button.config(state="disabled")
        passenger_action_configuration_button.pack(side="top",fill="both", pady=5, padx=5)

        passenger_occupancy_configuration_button = tk.Button(side_panel, text="Passenger Occupancy Configuration",command= self.load_passenger_occupancy_config)
        passenger_occupancy_configuration_button.config(state="disabled")
        passenger_occupancy_configuration_button.pack(side="top",fill="both", pady=5, padx=5)

        generate_button = tk.Button(side_panel, text="Generate Files",command=lambda: submit_generator_file(self))
        generate_button.config(state="disabled")
        generate_button.pack(side="bottom",fill="both", pady=5, padx=5)
        
    def update_side_panel_activity(self, index):
        side_buttons = self.frame.winfo_children()[0].winfo_children()
        for i, button in enumerate(side_buttons):
            if i <= index:
                button.config(state="active")
            else:
                button.config(state="disable")
            
    def enable_generator_file_button(self):
        generator_file_button = self.frame.winfo_children()[0].winfo_children()[-1]
        generator_file_button.config(state="active")
#endregion

#region Main Panel

    def load_time_config(self):

        self.controller.generator["Time"]["Duration"] = None
        self.controller.generator["Time"]["Tick"] = None

        self.update_side_panel_activity(0)

        try:
            self.frame.winfo_children()[1].destroy()
        except:
            pass

        main_panel = tk.Frame(self.frame, bg=grey2)
        main_panel.pack(side="right", fill="both", padx=5, pady=5, expand=True)

        title_label = tk.Label(main_panel, bg=grey1, text="Simulation Time Configuration", font=('Segoe 14'))
        title_label.pack(side="top", fill="x", padx=5, pady=5)

        time_list = tk.Frame(main_panel, bg=grey1)
        time_list.pack(fill='both', expand=True, padx=5, pady=5)

        duration_label = tk.Label(time_list, text="Simulation Duration (s)", bg=grey1)
        duration_label.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        duration_field = tk.Entry(time_list)
        duration_field.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

        tick_label = tk.Label(time_list, text="Tick Duration (s)", bg=grey1)
        tick_label.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

        tick_spinbox = ttk.Spinbox(time_list, from_=0, to=1,increment=0.05)
        tick_spinbox.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

        time_list.columnconfigure(0, weight=1)
        time_list.columnconfigure(1, weight=1)
        time_list.columnconfigure(2, weight=1)
        time_list.columnconfigure(3, weight=1)

        submit_time_config_button = tk.Button(main_panel, text="Submit Time Configuration",command=lambda: submit_time_config(self, time_list))
        submit_time_config_button.pack(side="bottom", fill="x", pady=5, padx=5)  
        pass

    def load_node_creator(self):
        
        self.controller.generator["Node"] = []

        self.update_side_panel_activity(1)
        self.frame.winfo_children()[1].destroy()

        main_panel = tk.Frame(self.frame, bg=grey2)
        main_panel.pack(side="right", fill="both", padx=5, pady=5, expand=True)

        nodes_list = tk.Frame(main_panel)
        
        generate_button = tk.Button(main_panel, text="Add Node",command=lambda: create_street_node(self, nodes_list))
        generate_button.pack(side="top", fill="x", pady=5, padx=5)   

        nodes_list.pack(fill='both', expand=True, padx=5, pady=5)

        submit_nodes_button = tk.Button(main_panel, text="Submit Nodes",command=lambda: submit_nodes(self, nodes_list))
        submit_nodes_button.pack(side="bottom", fill="x", pady=5, padx=5)   

    def load_route_creator(self):

        self.controller.generator["Route"]= {}

        self.update_side_panel_activity(2)
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
        
    def load_route_bus_config(self):

        for route in self.controller.generator["Route"]:
            self.controller.generator["Route"][route]["bus_rate"]= {}
            self.controller.generator["Route"][route]["initial_occupancy"]= {}
            self.controller.generator["Route"][route]["bus_model"]= {}

        self.update_side_panel_activity(3)
        self.frame.winfo_children()[1].destroy()

        main_panel = tk.Frame(self.frame, bg=grey2)
        main_panel.pack(side="right", fill="both", padx=5, pady=5, expand=True)

        title_label = tk.Label(main_panel, bg=grey2, text="Route Bus Model Configuration", font=('Segoe 14'))
        title_label.pack(side="top", fill="x", padx=5, pady=5)

        bus_card_list = tk.Frame(main_panel)
        bus_card_list.pack(side="top",fill="x", padx=5)

        for model in bus_models:
            create_bus_model_card(bus_card_list,model,bus_models[model])


        route_list = tk.Frame(main_panel)
        route_list.pack(side="top",fill='both', expand=True, padx=5, pady=5)

        for route_id in self.controller.generator["Route"].keys():
            create_route_bus_container(route_list,route_id)

        submit_route_bus_button = tk.Button(main_panel, text="Submit Route-Bus Configuration",command=lambda: submit_route_bus_config(self, route_list))
        submit_route_bus_button.pack(side="bottom", fill="x", pady=5, padx=5)

    def load_route_arrival_config(self):

        for route in self.controller.generator["Route"]:
            self.controller.generator["Route"][route]["bus_rate"]= {}

        self.update_side_panel_activity(4)
        self.frame.winfo_children()[1].destroy()

        main_panel = tk.Frame(self.frame, bg=grey2)
        main_panel.pack(side="right", fill="both", padx=5, pady=5, expand=True)

        title_label = tk.Label(main_panel, bg=grey2, text="Route Bus Arrival Configuration", font=('Segoe 14'))
        title_label.pack(side="top", fill="x", padx=5, pady=5)

        route_list = tk.Frame(main_panel)
        route_list.pack(side="top",fill='both', expand=True, padx=5, pady=5)

        for route_id in self.controller.generator["Route"].keys():
            create_route_config_container(route_list,route_id)

        submit_route_config_button = tk.Button(main_panel, text="Submit Bus Arrival Rate",command=lambda: submit_route_config(self, route_list))
        submit_route_config_button.pack(side="bottom", fill="x", pady=5, padx=5)

    def load_passenger_arrival_config(self):

        for route in self.controller.generator["Route"]:
            for stop in self.controller.generator["Route"][route]["stops"]:
                self.controller.generator["Route"][route]["stops"][stop]["passenger_rate"] = {}

        self.update_side_panel_activity(5)
        self.frame.winfo_children()[1].destroy()

        main_panel = tk.Frame(self.frame, bg=grey2)
        main_panel.pack(side="right", fill="both", padx=5, pady=5, expand=True)

        title_label = tk.Label(main_panel, bg=grey2, text="Stop Passenger Arrival Configuration", font=('Segoe 14'))
        title_label.pack(side="top", fill="x", padx=5, pady=5)

        stop_list = tk.Frame(main_panel)
        stop_list.pack(side="top",fill='both', expand=True, padx=5, pady=5)

        stop_list.columnconfigure(0, weight=1)
        stop_list.columnconfigure(1, weight=3)

        for route_id, route_data in self.controller.generator["Route"].items():
            stops = route_data["stops"]    
            for stop_id in stops:
                create_stop_config_container(stop_list,route_id,stop_id)

        submit_stop_config_button = tk.Button(main_panel, text="Submit Passenger Arrival Rate",command=lambda: submit_stop_config(self, stop_list))
        submit_stop_config_button.pack(side="bottom", fill="x", pady=5, padx=5)

    def load_passenger_action_config(self):

        self.controller.generator["Passenger"] = {}

        self.update_side_panel_activity(6)
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

        for route in self.controller.generator["Route"]:
            self.controller.generator["Route"][route]["initial_occupancy"]= {}

        self.update_side_panel_activity(7)
        self.frame.winfo_children()[1].destroy()

        main_panel = tk.Frame(self.frame, bg=grey2)
        main_panel.pack(side="right", fill="both", padx=5, pady=5, expand=True)

        title_label = tk.Label(main_panel, bg=grey2, text="Passenger Occupancy Configuration", font=('Segoe 14'))
        title_label.pack(side="top", fill="x", padx=5, pady=5)

        route_list = tk.Frame(main_panel)
        route_list.pack(side="top",fill='both', expand=True, padx=5, pady=5)

        for route_id in self.controller.generator["Route"].keys():
            create_passenger_occupancy_config_container(route_list,route_id)

        submit_passenger_occupancy_config_button = tk.Button(main_panel, text="Submit Passenger Occupancy Rate",command=lambda: submit_passenger_occupancy_config(self, route_list))
        submit_passenger_occupancy_config_button.pack(side="bottom", fill="x", pady=5, padx=5)
     
    def load_overview(self):
        self.update_side_panel_activity(99)
        self.enable_generator_file_button()
        self.frame.winfo_children()[1].destroy()
        pass
#endregion
#endregion
#region Reuse Generator File 

    def load_reuse(self):
        self.controller.app_mode = "regenerate"
        self.frame.destroy()
        self.root.geometry("400x400")

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx = 5, pady = 5, fill = 'both', expand = True)

        title_label = tk.Label(self.frame ,text="Regenerate Files", font=('Segoe 12 underline'))
        title_label.pack(pady=(5,60), padx=5)

        path_container = tk.Frame(self.frame)
        path_container.pack(fill="x")

        file_path_label = tk.Label(path_container ,text="Generator File Path:", font=('Segoe 10'))
        file_path_label.pack(padx=0, side="top",anchor="w")

        file_path_entry = tk.Entry(path_container)
        file_path_entry.pack(side="left", pady=5, padx=5,fill="x", expand=True)

        path_button = tk.Button(path_container, text="...", command=lambda: open_json_file_dialog(file_path_entry))
        path_button.pack(side="right")

        regenerate_button = tk.Button(self.frame, text="Generate Files", command=lambda:submit_regeneration_file(self, file_path_entry))
        regenerate_button.pack(side="bottom", anchor="s", padx=5, pady=5)

        

#endregion
#region Use Existing Files
    def load_existing_file(self):
        self.controller.app_mode = "reuse"
        self.frame.destroy()
        self.root.geometry("400x400")

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx = 5, pady = 5, fill = 'both', expand = True)

        title_label = tk.Label(self.frame ,text="Re-Use Files", font=('Segoe 12 underline'))
        title_label.pack(pady=(5,60), padx=5)

        generator_path_container = tk.Frame(self.frame)
        generator_path_container.pack(fill="x")

        generator_path_label = tk.Label(generator_path_container ,text="Generator File Path:", font=('Segoe 10'))
        generator_path_label.pack(padx=0, side="top",anchor="w")

        generator_path_entry = tk.Entry(generator_path_container)
        generator_path_entry.pack(side="left", pady=5, padx=5,fill="x", expand=True)

        generator_path_button = tk.Button(generator_path_container, text="...", command=lambda: open_json_file_dialog(generator_path_entry))
        generator_path_button.pack(side="right")

        passenger_dispatcher_path_container = tk.Frame(self.frame)
        passenger_dispatcher_path_container.pack(fill="x")

        passenger_dispatcher_path_label = tk.Label(passenger_dispatcher_path_container ,text="Passenger Dispatcher File Path:", font=('Segoe 10'))
        passenger_dispatcher_path_label.pack(padx=0, side="top",anchor="w")

        passenger_dispatcher_path_entry = tk.Entry(passenger_dispatcher_path_container)
        passenger_dispatcher_path_entry.pack(side="left", pady=5, padx=5,fill="x", expand=True)

        passenger_dispatcher_path_button = tk.Button(passenger_dispatcher_path_container, text="...", command=lambda: open_csv_file_dialog(passenger_dispatcher_path_entry))
        passenger_dispatcher_path_button.pack(side="right")

        bus_dispatcher_path_container = tk.Frame(self.frame)
        bus_dispatcher_path_container.pack(fill="x")

        bus_dispatcher_path_label = tk.Label(bus_dispatcher_path_container ,text="Bus Dispatcher File Path:", font=('Segoe 10'))
        bus_dispatcher_path_label.pack(padx=0, side="top",anchor="w")

        bus_dispatcher_path_entry = tk.Entry(bus_dispatcher_path_container)
        bus_dispatcher_path_entry.pack(side="left", pady=5, padx=5,fill="x", expand=True)

        bus_dispatcher_path_button = tk.Button(bus_dispatcher_path_container, text="...", command=lambda: open_csv_file_dialog(bus_dispatcher_path_entry))
        bus_dispatcher_path_button.pack(side="right")

        regenerate_button = tk.Button(self.frame, text="Generate Files", command=lambda:submit_reuse_file(self,generator_path_entry,passenger_dispatcher_path_entry,bus_dispatcher_path_entry))
        regenerate_button.pack(side="bottom", anchor="s", padx=5, pady=5)

#endregion
#endregion