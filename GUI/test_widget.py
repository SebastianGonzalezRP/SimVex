import customtkinter as ctk



class Application():
    def __init__(self):
        self.root = ctk.CTk()

        self.root.geometry("400x400")
        self.root.title("VexSim")
        self.root.resizable(False, False)
        self.frame = None
        self.load_main_view()


    def load_main_view(self):
        self.frame = ctk.CTkFrame(self.root, bg_color="grey")
        self.frame.pack()


        button1 = ctk.CTkButton(self.frame, width=250, height=150, text="Create New Simulation",command=self.destroy)
        button1.pack()

    def destroy(self):
        self.frame.destroy()



app = Application()
app.root.mainloop()
        