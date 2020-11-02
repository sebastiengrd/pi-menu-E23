#!/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter.constants as TkC
import os
import subprocess
import sys
from tkinter import Tk, Frame, Label, PhotoImage
from math import sqrt, floor, ceil
from subprocess import Popen
import time
import json
from View import *
from FlatButton import *

class PiMenu(Frame):
    framestack = []
    icons = {}
    path = ''
    lastinit = 0

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.pack(fill=TkC.BOTH, expand=1)

        self.path = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.parseConfigFile("config.json")
        self.initialize()

    def parseConfigFile(self, file_name):
        # open config file and put it into a dictionnary
        with open(file_name) as f:
            data = json.load(f)

        self.defaultViewName = data["defaultView"]
        self.views = data["views"]
    
    def initialize(self):
        """
        (re)load the the items from the yaml configuration and (re)init
        the whole menu system

        :return: None
        """
        subprocess.call(self.path + "/BruyerewifiagreeCurl.sh")
        # with open(self.path + '/pimenu.yaml', 'r') as f:
        #     doc = yaml.load(f)
        # self.lastinit = os.path.getmtime(self.path + '/pimenu.yaml')

        if len(self.framestack):
            self.destroy_all()
            self.destroy_top()

        # self.show_items(doc)

        # create initial view
        self.pushNewView(self.defaultViewName)


    def pushNewView(self, name):
        if len(self.framestack):
            self.hide_top()
        
        viewConfig = self.views[name]

        self.framestack.append(View(viewConfig, self))
        self.show_top()


    def has_config_changed(self):
        """
        Checks if the configuration has been changed since last loading

        :return: Boolean
        """
        return self.lastinit != os.path.getmtime(self.path + '/pimenu.yaml')


    def hide_top(self):
        """
        hide the top page
        :return:
        """
        self.framestack[len(self.framestack) - 1].getFrame().pack_forget()

    def show_top(self):
        """
        show the top page
        :return:
        """
        self.framestack[len(self.framestack) - 1].getFrame().pack(fill=TkC.BOTH, expand=1)

    def destroy_top(self):
        """
        destroy the top page
        :return:
        """
        self.framestack[len(self.framestack) - 1].getFrame().destroy()
        self.framestack.pop()

    def destroy_all(self):
        """
        destroy all pages except the first aka. go back to start
        :return:
        """
        while len(self.framestack) > 1:
            self.destroy_top()

    def go_back(self):
        """
        destroy the current frame and reshow the one below, except when the config has changed
        then reinitialize everything
        :return:
        """
        # if self.has_config_changed():
        #     self.initialize()
        # else:
        self.destroy_top()
        self.show_top()


def main():
    root = Tk()
    root.geometry("1280x500+0+0")
    root.wm_title('PiMenu')
    if len(sys.argv) > 1 and sys.argv[1] == 'fs':
        root.wm_attributes('-fullscreen', True)
    PiMenu(root)
    root.mainloop()


if __name__ == '__main__':
    main()
