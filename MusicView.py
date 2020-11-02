import tkinter.constants as TkC
from tkinter import Frame, PhotoImage
from pimenu import FlatButton
from math import floor, sqrt, ceil
from pygame import mixer

class MusicView(Frame):
    """
    Easily configure a tkinter Frame for the Music app
    """
    def __init__(self, piMenu):
        super().__init__(piMenu)
        self.images = {}
        self.piMenu = piMenu
        self.initialize()


    def initialize(self):        
        # calculate tile distribution
        itemsNumber = 3
        rows = floor(sqrt(itemsNumber))
        cols = ceil(itemsNumber / rows)

        # make cells autoscale
        for x in range(int(cols)):
            self.columnconfigure(x, weight=1)
        
        for y in range(int(rows)):
            self.rowconfigure(y, weight=1)

        #initialize each buttons in the frame

        playBtn = FlatButton(
            self,
            text="Play",
            # image=self.images[button["icon"]],
            command=lambda : self.btnPressed("startMusic")
        )

        # Initialize the color of the button
        playBtn.set_color("#2ba887")

        # add buton to the grid
        playBtn.grid(
            row=int(floor(0 / cols)),
            column=int(0 % cols),
            padx=1,
            pady=1,
            sticky=TkC.W + TkC.E + TkC.N + TkC.S
        )

        stopBtn = FlatButton(
            self,
            text="Stop",
            # image=self.images[button["icon"]],
            command=lambda : self.btnPressed("stopMusic")
        )

        # Initialize the color of the button
        stopBtn.set_color("#2ba887")

        # add buton to the grid
        stopBtn.grid(
            row=int(floor(1 / cols)),
            column=int(1 % cols),
            padx=1,
            pady=1,
            sticky=TkC.W + TkC.E + TkC.N + TkC.S
        )

        backBtn = FlatButton(
            self,
            text="Back",
            # image=self.images[button["icon"]],
            command=lambda : self.btnPressed("Back")
        )

        # Initialize the color of the button
        backBtn.set_color("#2ba887")

        # add buton to the grid
        backBtn.grid(
            row=int(floor(2 / cols)),
            column=int(2 % cols),
            padx=1,
            pady=1,
            sticky=TkC.W + TkC.E + TkC.N + TkC.S
        )

      

    # When a button is pressed, this function is called
    def btnPressed(self, action):
        if(action == "startMusic"):
            print("start")
            mixer.music.play()
        elif(action == "stopMusic"):
            print("stop")
            mixer.music.stop() 

        elif(action == "Back"):
            self.piMenu.go_back()
        # else:
        #     self.piMenu.pushNewView(action)
