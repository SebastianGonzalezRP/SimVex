import customtkinter as ctk



class Application():
    def __init__(self):
        self.root = ctk.CTk()

        self.root.geometry("400x400")
        self.root.title("VexSim")
        self.root.resizable(False, False)
        self.frame = None

    def swap_view(self):

        pass

    def load_create_new(self):
        self.root.destroy()
        self.root.mainloop()


    def load_main_view(self):
        
        self.frame = ctk.CTkFrame(self.root)

        button1 = ctk.CTkButton(master=self.root, width=250, height=150, text="Create New Simulation",command=self.load_create_new)
        button2 = ctk.CTkButton(master=self.root, width=250, height=150, text="Re-Use File",)
        button3 = ctk.CTkButton(master=self.root, width=250, height=150, text="Load Files",)


        button1.grid(row=0, column=0, padx=10, pady=10)
        button2.grid(row=1, column=0, padx=10, pady=10)
        button3.grid(row=2, column=0, padx=10, pady=10)
        
        

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

        self.root.grid_columnconfigure(0, weight=1, pad=15)

        

        self.root.mainloop()

    


app = Application()
app.load_main_view()
        