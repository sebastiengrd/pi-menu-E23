from Playlist import Playlist
import tkinter.constants as TkC
from tkinter import Frame, PhotoImage
from pimenu import FlatButton
from math import floor, sqrt, ceil
from pygame import mixer

class MusicView(Frame):
    """
    Easily configure a tkinter Frame for the Music app
    """
    playlist = Playlist("playlist/")
    
    volume = 0.7
    isPlaying = False
    buttons = [
        {
            "label": "Back",
            "color": "#0091A0",
            "icon": "ico/arrow.left.gif",
            "goToView": "Back"
        },
        {
            "label": "Title",
            "color": "#0B2F6D",
            "icon": None,
            "goToView": "Title"
        },
        {
            "label": "Decrease Volume",
            "color": "#0B2F6D",
            "icon": "ico/minus.gif",
            "goToView": "DecreaseVolume"
        },
        # {
        #     "label": "Shuffle",
        #     "color": "#2ba887",
        #     "icon": "ico/shuffle.gif",
        #     "goToView": "Shuffle"
        # },
        # {
        #     "label": "Repeat",
        #     "color": "#2ba887",
        #     "icon": "ico/repeat.gif",
        #     "goToView": "Repeat"
        # },
        {
            "label": "Increase Volume",
            "color": "#0B2F6D",
            "icon": "ico/add.gif",
            "goToView": "IncreaseVolume"
        },
        {
            "label": "Previous",
            "color": "#0B2F6D",
            "icon": "ico/navigate.previous.gif",
            "goToView": "Previous"
        },
        {
            "label": "Play",
            "color": "#0091A0",
            "icon": "ico/control.play.gif",
            "goToView": "Play"
        },
        {
            "label": "Next",
            "color": "#0B2F6D",
            "icon": "ico/navigate.next.gif",
            "goToView": "Next"
        }
    ]

    def __init__(self, viewConfig, piMenu):
        super().__init__(piMenu)
        self.images = {}
        self.piMenu = piMenu
        self.buttonObjects = []
        self.playButtonIdx = None
        # add static list of buttons to viewConfig since this is an app view
        viewConfig["buttons"] = self.buttons

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
            # import the image 
            image = None
            if button["icon"] != None:
                # keep reference of PhotoImage to prevent destruction of the object
                self.images[button["icon"]] = PhotoImage(file=button["icon"])
                image = self.images[button["icon"]]

            # Initialize
            b = FlatButton(
                self,
                text=button["label"],
                image=image,
                command=lambda view=button["goToView"] : self.btnPressed(view))
            
            self.buttonObjects.append(b)
            if button["goToView"] == "Play":
                self.playButtonIdx = btnCount
            if button["goToView"] == "Title":
                self.titleButtonIdx = btnCount

            # Initialize the color of the button
            b.set_color(button["color"])

            # add buton to the grid
            b.grid(
                row=int(floor(btnCount / cols)),
                column=int(btnCount % cols) + (1 if button["goToView"] == "Next" else 0),
                padx=1,
                pady=1,
                columnspan=2 if button["goToView"] == "Play" else 1 ,
                sticky=TkC.W + TkC.E + TkC.N + TkC.S
            )
            

            btnCount += 1

        # if music is already playing then modify button
        self.updatePlayButton()

    # When a button is pressed, this function is called
    def btnPressed(self, action):
        if action == "Back":
            self.piMenu.go_back()

        elif action == "Title":
            pass

        elif action == "DecreaseVolume":
            self.volume -= 0.1
            mixer.music.set_volume(self.volume)

        elif action == "Shuffle":
            pass

        elif action == "Repeat":
            pass

        elif action == "IncreaseVolume":
            self.volume += 0.1
            mixer.music.set_volume(self.volume)

        elif action == "Previous":
            mixer.music.set_volume(self.volume)
            mixer.music.load(self.playlist.previous())
            mixer.music.play()
            self.piMenu.isPlaying = True
            self.updatePlayButton()

        elif action == "Play":
            mixer.music.set_volume(self.volume)
            mixer.music.load(self.playlist.getCurrent())
            # if we want to play
            if not self.piMenu.isPlaying:
                mixer.music.play()
            else:
                mixer.music.stop()

            self.piMenu.isPlaying = not self.piMenu.isPlaying
            self.updatePlayButton()            
            
        elif action == "Next":
            mixer.music.set_volume(self.volume)
            mixer.music.load(self.playlist.next())
            mixer.music.play()
            self.piMenu.isPlaying = True
            self.updatePlayButton()


    def updatePlayButton(self):
        if not self.piMenu.isPlaying:
            self.buttonObjects[self.playButtonIdx].config(text="Play")
        else:
            self.buttonObjects[self.playButtonIdx].config(text="Stop")

        self.buttonObjects[self.titleButtonIdx].config(text = self.playlist.getCurrent()[9:-4])