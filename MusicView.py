from Playlist import Playlist
import tkinter.constants as TkC
from tkinter import Frame, PhotoImage
from pimenu import FlatButton
from math import floor, sqrt, ceil
import vlc

class MusicView(Frame):
    """
    Easily configure a tkinter Frame for the Music app
    """
    playlist = Playlist("playlist/")
    
    volume = 0.2
    isPlaying = False
    # creating vlc media player object 
    mediaPlayer = vlc.MediaPlayer() 
    buttons = [
        {
            "label": "Back",
            "color": "#0091A0",
            "icon": "ico/arrow.left.gif",
            "goToView": "Back"
        },
        {
            "label": "Title",
            "color": "#0091A0",
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
            "color": "#0B2F6D",
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
        

        self.bind("<Key>", lambda i : self.pressedKey(i))
        self.focus_set()

        
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
            b = FlatButton(
                imagePath=button["icon"],
                parent=self,
                text=button["label"],
                color=button["color"],
                command=lambda view=button["goToView"] : self.btnPressed(view))
            
            self.buttonObjects.append(b)
            if button["goToView"] == "Play":
                self.playButtonIdx = btnCount
            if button["goToView"] == "Title":
                self.titleButtonIdx = btnCount

            # add button to the grid
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
    def pressedKey(self, k):
        if(k.keysym == "p") :
            self.btnPressed("Play")
        elif(k.keysym == "b") :
            self.btnPressed("Back")
        elif(k.keysym == "Left") :
            self.btnPressed("Previous")
        elif(k.keysym == "Right") :
            self.btnPressed("Next")
        elif(k.keysym == "KP_Add" or k.keysym == "equal" or k.keysym == "Up"):
            self.btnPressed("IncreaseVolume")
        elif(k.keysym == "KP_Subtract" or k.keysym == "minus" or k.keysym == "Down"):
            self.btnPressed("DecreaseVolume")
        print(k)


    # When a button is pressed, this function is called
    def btnPressed(self, action):
        if action == "Back":
            self.piMenu.go_back()

        elif action == "Title":
            pass

        elif action == "DecreaseVolume":
            self.volume -= 0.1
            self.mediaPlayer.audio_set_volume(int(self.volume*100))

        elif action == "Shuffle":
            pass

        elif action == "Repeat":
            pass

        elif action == "IncreaseVolume":
            self.volume += 0.1
            self.mediaPlayer.audio_set_volume(int(self.volume*100))


        elif action == "Previous":
            self.media = vlc.Media(self.playlist.previous())
            self.mediaPlayer.set_media(self.media)
            self.mediaPlayer.audio_set_volume(int(self.volume*100)) 
            self.mediaPlayer.play()
            self.piMenu.isPlaying = True
            self.updatePlayButton()

        elif action == "Play":
            self.media = vlc.Media(self.playlist.getCurrent())
            self.mediaPlayer.set_media(self.media)
            self.mediaPlayer.audio_set_volume(int(self.volume*100)) 
            # if we want to play
            if not self.piMenu.isPlaying:
                self.mediaPlayer.play()
            else:
                self.mediaPlayer.stop()

            self.piMenu.isPlaying = not self.piMenu.isPlaying
            self.updatePlayButton()            
            
        elif action == "Next":
            self.media = vlc.Media(self.playlist.next())
            self.mediaPlayer.set_media(self.media)
            self.mediaPlayer.audio_set_volume(int(self.volume*100))
            self.mediaPlayer.play()
            self.piMenu.isPlaying = True
            self.updatePlayButton()


    def updatePlayButton(self):
        if not self.piMenu.isPlaying:
            self.buttonObjects[self.playButtonIdx].config(text="Play")
        else:
            self.buttonObjects[self.playButtonIdx].config(text="Stop")

        self.buttonObjects[self.titleButtonIdx].config(text = self.playlist.getCurrent()[9:-4])
