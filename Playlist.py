class Playlist:

    def __init__(self, itemsPaths):
        self.current = -1
        self.items = itemsPaths
        self.length = len(itemsPaths)

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