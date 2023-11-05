import tkinter as tk
from tkinter.ttk import *
from time import strftime

class DigitalClock(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stylish Digital Clock")
        self.geometry('400x200')

        self.label = Label(self, font=('Verdana', 40), background='#333', foreground='#FFD700')
        self.label.pack(expand=True, fill='both')

        self.update_time()

    def update_time(self):
        string = strftime('%H:%M:%S %p')
        self.label.config(text=string)
        self.after(1000, self.update_time)

if __name__ == "__main__":
    app = DigitalClock()
    app.mainloop()
