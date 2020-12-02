from tkinter import Button, PhotoImage
import tkinter.constants as TkC
from tkinter import *  # Note: lower case "t" in tkinter
from tkinter import font as tkFont  # for convenience
from PIL import Image


class FlatButton(Button):
    """ 
    Custom button created from the tkinter Button class
    """
    def __init__(self, imagePath, parent, color, **kw):
        self.image = None
        if imagePath != None:
            # keep reference of PhotoImage to prevent destruction of the object
            self.image = PhotoImage(file=imagePath)
            self.image = self.image.zoom(2, 2)
            # self.image = self.image.resize((34, 26), Image.ANTIALIAS)
            # self.image = Image.open(imagePath)
            # self.image  = self.image.resize((34, 26), Image.ANTIALIAS)
            # self.photoImage = PhotoImage(self.image)


        super().__init__(parent, image=self.image, **kw)

        helv36 = tkFont.Font(family='Helvetica', size=20, weight='bold')
        self['font'] = helv36
        
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
