from tkinter import Button, PhotoImage
import tkinter.constants as TkC


class FlatButton(Button):
    """ 
    Custom button created from the tkinter Button class
    """
    def __init__(self, imagePath, parent, color, **kw):
        self.image = None
        if imagePath != None:
            # keep reference of PhotoImage to prevent destruction of the object
            self.image = PhotoImage(file=imagePath)

        super().__init__(parent, image=self.image, **kw)

        self.config(
            compound=TkC.TOP,
            relief=TkC.FLAT,
            bd=0,
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            highlightthickness=0
        )
