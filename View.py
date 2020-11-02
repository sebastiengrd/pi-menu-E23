import tkinter.constants as TkC
from tkinter import Frame, PhotoImage
from pimenu import FlatButton
from math import floor, sqrt, ceil

class View:
    """
    Easily configure a tkinter Frame with buttons inside them
    """
    def __init__(self, viewConfig, piMenu):
        self.frame = Frame(piMenu)
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
            self.frame.columnconfigure(x, weight=1)
        
        for y in range(int(rows)):
            self.frame.rowconfigure(y, weight=1)

        #initialize each buttons in the frame
        btnCount = 0
        for button in viewConfig["buttons"]:
            # import the image 
            self.images[button["icon"]] = PhotoImage(file=button["icon"])

            # Initialize
            b = FlatButton(
                self.frame,
                text=button["label"],
                image=self.images[button["icon"]],
                command=lambda view=button["goToView"] : self.btnPressed(view)
            )

            # if we want to configure more options
            # b.configure(command=lambda act=act, item=item: self.show_items(item['items'], act)) # piMenu show view function

            # Initialize the color of the button
            b.set_color(button["color"])

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


    def getFrame(self):
        return self.frame