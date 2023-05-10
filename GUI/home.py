import tkinter as tk
from tkinter import ttk

grey1 = "#D4D4D4"
grey2 = "#B4B4B4"
grey3 = "#909090"
grey4 = "#636363"

node_container_config = {
    "Street": {},
    "Stop": {},
    "Intersection":{}
}

def destroy_frame_children(frame):
    for child in frame.winfo_children():
        child.destroy()

def update_existing_node(self, node_container, node_type):
    destroy_frame_children(node_container)
    if node_type == "Street":
        load_street_node(self, node_container)
    elif node_type == "Stop":
        load_stop_node(self, node_container)
    elif node_type == "Intersection":
        load_intersection_node(self, node_container)
    pass



def selector_change(self, node_selector):
        selection = node_selector.get()
        node_container_path = node_selector.winfo_parent()
        node_container = self.root.nametowidget(node_container_path)
        update_existing_node(self, node_container, selection)

def create_street_node(self,node_list):

    node_container = tk.Frame(node_list, height=100, bg=grey3)
    node_container.pack(anchor='n', fill='x', padx=5, pady=5)

    node_label = tk.Label(node_container, text="Node Type", bg=grey3)
    node_label.grid(row=0, column=0, padx=5, pady=5, sticky='nswe')

    node_selector = ttk.Combobox(node_container, values=["Street","Stop","Intersection"])
    node_selector.set("Street")
    node_selector.bind('<<ComboboxSelected>>', lambda event: selector_change(self, node_selector))
    node_selector.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

    length_label = tk.Label(node_container, text="Street Length", bg=grey3)
    length_label.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

    length_field = tk.Entry(node_container)
    length_field.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

    ntracks_label = tk.Label(node_container, text="Number of Tracks", bg=grey3)
    ntracks_label.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

    number_spinbox = ttk.Spinbox(node_container, from_=1, to=2, textvariable=1)
    number_spinbox.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')


    node_container.columnconfigure(0, weight=1)
    node_container.columnconfigure(1, weight=1)
    node_container.columnconfigure(2, weight=1)



def load_street_node(self,node_container):

    node_label = tk.Label(node_container, text="Node Type", bg=grey3)
    node_label.grid(row=0, column=0, padx=5, pady=5, sticky='nswe')

    node_selector = ttk.Combobox(node_container, values=["Street","Stop","Intersection"])
    node_selector.set("Street")
    node_selector.bind('<<ComboboxSelected>>', lambda event: selector_change(self, node_selector))
    node_selector.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

    length_label = tk.Label(node_container, text="Street Length", bg=grey3)
    length_label.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

    length_field = tk.Entry(node_container)
    length_field.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

    ntracks_label = tk.Label(node_container, text="Number of Tracks", bg=grey3)
    ntracks_label.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

    number_spinbox = ttk.Spinbox(node_container, from_=1, to=2, textvariable=1)
    number_spinbox.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')


    node_container.columnconfigure(0, weight=1)
    node_container.columnconfigure(1, weight=1)
    node_container.columnconfigure(2, weight=1)




def load_stop_node(self,node_container):

    node_label = tk.Label(node_container, text="Node Type", bg=grey3)
    node_label.grid(row=0, column=0, padx=5, pady=5, sticky='nswe')

    node_selector = ttk.Combobox(node_container, values=["Street","Stop","Intersection"])
    node_selector.set("Stop")
    node_selector.bind('<<ComboboxSelected>>', lambda event: selector_change(self, node_selector))
    node_selector.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')



    node_container.columnconfigure(0, weight=1)
    node_container.columnconfigure(1, weight=1)
    node_container.columnconfigure(2, weight=1)

def load_intersection_node(self,node_container):

    node_label = tk.Label(node_container, text="Node Type", bg=grey3)
    node_label.grid(row=0, column=0, padx=5, pady=5, sticky='nswe')

    node_selector = ttk.Combobox(node_container, values=["Street","Stop","Intersection"])
    node_selector.set("Intersection")
    node_selector.bind('<<ComboboxSelected>>', lambda event: selector_change(self, node_selector))
    node_selector.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')


    node_container.columnconfigure(0, weight=1)
    node_container.columnconfigure(1, weight=1)
    node_container.columnconfigure(2, weight=1)


    



class Application():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("400x400")
        self.root.title("VexSim")
        self.root.resizable(False,False)
        self.frame = None
        self.load_main_view()

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

    def load_create_new(self):
        self.frame.destroy()
        window_width = 1280
        window_height = 800
        self.root.geometry(f"{window_width}x{window_height}")

        self.frame = tk.Frame(self.root, background=grey1)
        self.frame.pack(padx = 5, pady = 5, fill = 'both', expand = True)

        side_panel = tk.Frame(self.frame, width= window_width//6, bg=grey2)
        side_panel.pack(side="left",fill='y', padx=5, pady=5)

        main_panel = tk.Frame(self.frame, bg=grey2)
        main_panel.pack(side="right", fill="both", padx=5, pady=5, expand=True)

        node_creator_button = tk.Button(side_panel, text="Nodes Creator")
        node_creator_button.pack(side="top", pady=5, padx=5)

        Stops_editor_button = tk.Button(side_panel, text="Stops Editor")
        Stops_editor_button.pack(side="top", pady=5, padx=5)

        generate_button = tk.Button(side_panel, text="Generate Files")
        generate_button.pack(side="bottom", pady=5, padx=5)

        nodes_list = tk.Frame(main_panel)
        
        generate_button = tk.Button(main_panel, text="Add Node",command=lambda: create_street_node(self, nodes_list))
        generate_button.pack(side="top", fill="x", pady=5, padx=5)   

        nodes_list.pack(side='left', fill='both', expand=True, padx=5, pady=5)


    def load_reuse(self):
        pass

    def load_existing_file(self):
        pass


    

    

app = Application()
app.root.mainloop()