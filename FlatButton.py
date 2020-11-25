from tkinter import Button, PhotoImage
import tkinter.constants as TkC


class FlatButton(Button):
    """ 
    Custom button created from the tkinter Button class
    """
    def __init__(self, imagePath, master=None, cnf=None, **kw):
        self.image = None
        if imagePath != None:
            # keep reference of PhotoImage to prevent destruction of the object
            print(imagePath)
            self.image = PhotoImage(file=imagePath)

        Button.__init__(self, master, cnf, image=self.image, **kw)

        self.config(
            compound=TkC.TOP,
            relief=TkC.FLAT,
            bd=0,
            bg="#b91d47",  # dark-red
            fg="white",
            activebackground="#b91d47",  # dark-red
            activeforeground="white",
            highlightthickness=0
        )

    def set_color(self, color):
        self.configure(
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white"
        )
