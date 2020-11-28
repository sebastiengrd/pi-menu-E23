import os
from tkinter.constants import CURRENT

class Playlist:

    def __init__(self, playlistPath):
        self.current = -1
        self.items = [(playlistPath+item) for item in os.listdir(playlistPath)]
        self.length = len(self.items)

    def next(self):
        self.current += 1
        if (self.current >= self.length):
            self.current = 0

        return self.items[self.current]
    
    def previous(self):
        self.current -= 1
        if (self.current < 0):
            self.current = self.length -1

        return self.items[self.current]
    
    def getCurrent(self):
        return self.items[self.current]