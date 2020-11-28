import os
import tkinter as tk
from Playlist import Playlist
from tkinter import Frame
from math import floor, sqrt, ceil
from FlatButton import *
import vlc


class VideoView(Frame):
    vlc_instance = vlc.Instance()
    vlc_media_player_instance = vlc_instance.media_player_new()
    playlist = Playlist("videos/")
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
            "label": "Decrease Volume",
            "color": "#0B2F6D",
            "icon": "ico/minus.gif",
            "goToView": "DecreaseVolume"
        },
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
        self.view = self
        self.piMenu = piMenu
        self.showControlPanel = True
        self.buttonObjects = []
        self.playButtonIdx = None
        # add static list of buttons to viewConfig since this is an app view
        viewConfig["buttons"] = self.buttons
        self.viewConfig = viewConfig
        self.initialize(viewConfig)

    
    def videoPanelPressed(self, event):

        if self.showControlPanel:
            self.control_panel.destroy()
        else:
            self.create_control_panel(self.viewConfig)
        
        self.showControlPanel = 1 - self.showControlPanel



    def initialize(self, viewConfig):
        self.piMenu.update()
        
        # vlc video frame
        self.videopanel = tk.Frame(self)

        self.canvas = tk.Canvas(self.videopanel, background="black")
        self.canvas.bind("<Button-1>", self.videoPanelPressed)
        self.videopanel.bind("<Button-1>", self.videoPanelPressed)
        self.canvas.focus_set()
        self.canvas.pack(fill=tk.BOTH,expand=1)
        self.videopanel.pack(fill=tk.BOTH, expand=True)
        self.playFilm()

        self.create_control_panel(viewConfig)
        self.piMenu.isVideoPlaying = True
        

    # When a button is pressed, this function is called

    def btnPressed(self, action):
        if action == "Back":
            self.vlc_media_player_instance.pause()
            self.piMenu.go_back()

        elif action == "DecreaseVolume":
            self.volume -= 0.1
            self.vlc_media_player_instance.audio_set_volume(int(self.volume*100))

        elif action == "IncreaseVolume":
            self.volume += 0.1
            self.vlc_media_player_instance.audio_set_volume(int(self.volume*100))

        elif action == "Previous":
            self.playlist.previous()
            self.playFilm()

        elif action == "Play":
            # if we want to play
            if not self.piMenu.isVideoPlaying:
                self.playFilm()
                print("play")
            else:
                print("stop")
                self.vlc_media_player_instance.stop()

            self.piMenu.isVideoPlaying = not self.piMenu.isVideoPlaying
            self.updatePlayButton()       
            # self.updatePlayButton()

        elif action == "Next":
            self.playlist.next()
            self.playFilm()

    def playFilm(self):
        directory_name = os.path.dirname(self.playlist.getCurrent())
        file_name = os.path.basename(self.playlist.getCurrent())
        self.Media = self.vlc_instance.media_new(
            str(os.path.join(directory_name, file_name))
        )
        self.vlc_media_player_instance.set_media(self.Media)
        self.vlc_media_player_instance.set_xwindow(self.get_handle())
        
        self.piMenu.update()
        self.vlc_media_player_instance.play()


    def get_handle(self):
        return self.videopanel.winfo_id()


    def create_control_panel(self, viewConfig):
        """Add control panel."""
        self.control_panel = tk.Frame(self)

        # calculate tile distribution
        itemsNumber = len(viewConfig["buttons"])
        rows = floor(sqrt(itemsNumber))
        cols = ceil(itemsNumber / rows)

        #initialize each buttons in the frame
        btnCount = 0
        for button in viewConfig["buttons"]:
            # Initialize
            b = FlatButton(
                imagePath=button["icon"],
                parent=self.control_panel,
                text=button["label"],
                color=button["color"],
                command=lambda view=button["goToView"] : self.btnPressed(view))
            
            self.buttonObjects.append(b)
            if button["goToView"] == "Play":
                self.playButtonIdx = btnCount
                b["text"] = "Stop"
            
            # add buton to the grid
            b.grid(
                row=int(floor(btnCount / cols)),
                column=int(btnCount % cols),
                padx=1,
                pady=1,
                columnspan=1 ,
                sticky=TkC.W + TkC.E + TkC.N + TkC.S
            )

            btnCount += 1

        # make cells autoscale
        for x in range(int(cols)):
            self.control_panel.columnconfigure(x, weight=1)
        
        for y in range(int(rows)):
            self.control_panel.rowconfigure(y, weight=1)

        self.control_panel.pack(fill=tk.BOTH, expand=True)

    def updatePlayButton(self):
        if not self.piMenu.isVideoPlaying:
            self.buttonObjects[self.playButtonIdx].config(text="Play")
        else:
            self.buttonObjects[self.playButtonIdx].config(text="Stop")

  