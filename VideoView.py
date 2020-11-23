import os
from tkinter import ttk
import tkinter as tk
from Playlist import Playlist
from tkinter import Frame, PhotoImage
from pimenu import FlatButton
from math import floor, sqrt, ceil
import vlc

class VideoView(Frame):
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
        self.piMenu = piMenu
        self.buttonObjects = []
        self.playButtonIdx = None
        # add static list of buttons to viewConfig since this is an app view
        viewConfig["buttons"] = self.buttons

        self.initialize(viewConfig)


    def initialize(self, viewConfig):
        # create vlc instance
        self.vlc_instance, self.vlc_media_player_instance = self.create_vlc_instance()

        # vlc video frame
        self.video_panel = ttk.Frame(self.piMenu)
        self.canvas = tk.Canvas(self.video_panel, background='black')
        self.canvas.pack(fill=tk.BOTH, expand=1)
        self.video_panel.pack(fill=tk.BOTH, expand=1)
        self.playFilm()

        # controls 
        
        # # calculate tile distribution
        # itemsNumber = len(viewConfig["buttons"])
        # rows = floor(sqrt(itemsNumber))
        # cols = ceil(itemsNumber / rows)

        # # make cells autoscale
        # for x in range(int(cols)):
        #     self.columnconfigure(x, weight=1)
        
        # for y in range(int(rows)):
        #     self.rowconfigure(y, weight=1)

        # #initialize each buttons in the frame
        # btnCount = 0
        # for button in viewConfig["buttons"]:
        #     # import the image 
        #     image = None
        #     if button["icon"] != None:
        #         # keep reference of PhotoImage to prevent destruction of the object
        #         self.images[button["icon"]] = PhotoImage(file=button["icon"])
        #         image = self.images[button["icon"]]

        #     # Initialize
        #     b = FlatButton(
        #         self,
        #         text=button["label"],
        #         image=image,
        #         command=lambda view=button["goToView"] : self.btnPressed(view))
            
        #     self.buttonObjects.append(b)
        #     if button["goToView"] == "Play":
        #         self.playButtonIdx = btnCount
        #     if button["goToView"] == "Title":
        #         self.titleButtonIdx = btnCount

        #     # Initialize the color of the button
        #     b.set_color(button["color"])

        #     # add buton to the grid
        #     b.grid(
        #         row=int(floor(btnCount / cols)),
        #         column=int(btnCount % cols) + (1 if button["goToView"] == "Next" else 0),
        #         padx=1,
        #         pady=1,
        #         columnspan=2 if button["goToView"] == "Play" else 1 ,
        #         sticky=TkC.W + TkC.E + TkC.N + TkC.S
        #     )
            

        #     btnCount += 1

    # When a button is pressed, this function is called
    def btnPressed(self, action):
        if action == "Back":
            self.piMenu.go_back()

        elif action == "DecreaseVolume":
            self.volume -= 0.1
            self.vlc_media_player_instance.set_volume(self.volume)

        elif action == "IncreaseVolume":
            self.volume += 0.1
            self.vlc_media_player_instance.set_volume(self.volume)

        elif action == "Previous":
            self.playlist.previous()
            self.playFilm()

        elif action == "Play":
            self.playFilm()
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
        self.vlc_media_player_instance.play()

    def create_vlc_instance(self):
        vlc_instance = vlc.Instance()
        vlc_media_player_instance = vlc_instance.media_player_new()
        self.piMenu.update()
        return vlc_instance, vlc_media_player_instance

    def get_handle(self):
        return self.video_panel.winfo_id()

    def create_control_panel(self):
    """Add control panel."""
    control_panel = ttk.Frame(self.container_instance)
    pause = ttk.Button(control_panel, text="Pause", command=self.pause)
    play = ttk.Button(control_panel, text="Play", command=self.play)
    stop = ttk.Button(control_panel, text="Stop", command=self.stop)
    volume = ttk.Button(control_panel, text="Volume", command=None)
    pause.pack(side=tk.LEFT)
    play.pack(side=tk.LEFT)
    stop.pack(side=tk.LEFT)
    volume.pack(side=tk.LEFT)
    control_panel.pack(side=tk.BOTTOM)