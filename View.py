import tkinter.constants as TkC
from tkinter import Frame
from FlatButton import *
from math import floor, sqrt, ceil

class View(Frame):
    """
    Easily configure a tkinter Frame with buttons inside them
    """
    def __init__(self, viewConfig, piMenu):
        super().__init__(piMenu)
        self.images = {}
        self.piMenu = piMenu
        self.initialize(viewConfig)


    def initialize(self, viewConfig):        
        # calculate tile distribution
        itemsNumber = len(viewConfig["buttons"])
        rows = floor(sqrt(itemsNumber))
        cols = ceil(itemsNumber / rows)

        # make cells autoscale
        for x in range(int(cols)):
            self.columnconfigure(x, weight=1)
        
        for y in range(int(rows)):
            self.rowconfigure(y, weight=1)

        #initialize each buttons in the frame
        btnCount = 0
        for button in viewConfig["buttons"]:
            # Initialize
            print(button["icon"])
            b = FlatButton(
                imagePath=button["icon"],
                parent=self,
                text=button["label"],
                color=button["color"],
                command=lambda view=button["goToView"] : self.btnPressed(view)
            )

            # add buton to the grid
            b.grid(
                row=int(floor(btnCount / cols)),
                column=int(btnCount % cols),
                padx=1,
                pady=1,
                sticky=TkC.W + TkC.E + TkC.N + TkC.S
            )

            btnCount += 1

    # When a button is pressed, this function is called
    def btnPressed(self, action):
        if(action == "Back"):
            self.piMenu.go_back()
        elif(action == "Exit"):
            exit(1)
        else:
            self.piMenu.pushNewView(action)
