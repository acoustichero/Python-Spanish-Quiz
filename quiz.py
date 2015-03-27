#!/usr/bin/python
# Written by John Black

from gi.repository import Gtk
import random


class MyWindow(Gtk.Window):

    def __init__(self):
        self.englishList = []
        self.spanishList = []
        self.number = -1
        self.indexOrder = []
        self.status = 0
        self.mode = True #Spanish to English or English to Spanish

        # Main window
        Gtk.Window.__init__(self, title="Spanish Vocab!")
        self.set_size_request(300,300)
        self.set_position(Gtk.WindowPosition.CENTER)

        # splits the window up into blocks one on top of another
        self.vbox = Gtk.VBox(spacing=10)
        self.add(self.vbox)

        # upper label
        self.spanishLabel = Gtk.Label(label="               ")
        self.spanishLabel.set_use_markup(True)
        self.vbox.pack_start(self.spanishLabel, True, True, 0)

        # lower label
        self.englishLabel = Gtk.Label(label="               ")
        self.englishLabel.set_use_markup(True)
        self.vbox.pack_start(self.englishLabel, True, True, 0)

        # button
        self.myButton = Gtk.Button(label="Start")
        self.myButton.connect("clicked", self.on_myButton_clicked)

        #check box
        self.myCheckBox = Gtk.CheckButton("mode")
        self.myCheckBox.connect("toggled", self.on_myCheckBox_toggled, "mode")

        # horizontal box layout inside lower section of vbox layout
        self.box = Gtk.HBox()
        self.vbox.pack_start(self.box, False, False, 5)
        self.box.pack_start(self.myCheckBox, True, True, 20)
        self.box.pack_start(self.myButton, True, True, 20)


        myFile = open('exam2.txt', 'r')
        x = 0
        for line in myFile:
            if line[0] != "#":
                words = line.split("|")
                if len(words) == 2:
                    self.spanishList.append(words[0])
                    self.englishList.append(words[1])
                    self.indexOrder.append(x)
                    x += 1
        myFile.close()
        random.shuffle(self.indexOrder)



    def setLabels(self, upperLabel, lowerLabel):
        self.spanishLabel.set_label(upperLabel)
        self.englishLabel.set_label(lowerLabel)
        self.show_all()

    def getNewWord(self):
        if (self.number < len(self.spanishList) -1):
            self.number += 1
        else:
            myFile = open('exam2.txt', 'r')
            for x in range (0, len(self.spanishList)):
                self.indexOrder[x] = x
            myFile.close()
            random.shuffle(self.indexOrder)

            self.status = 2
            self.number = len(self.spanishList)
            self.setLabels('<span size="18000">DONE!</span>', '<span size="18000">Press CONTINUE to restart</span>')
            self.myButton.set_label('Continue')


    def on_myCheckBox_toggled(self, widget, ischecked):
        if( self.mode == True):
            self.mode = False
        else:
            self.mode = True


    def on_myButton_clicked(self, widget): 
        if(self.status == 0):
            if( self.mode == True):
                if(self.number >= -1 and self.number < len(self.spanishList)): # spanish only
                    self.getNewWord()
                    if( self.number < len(self.spanishList)):
                        self.setLabels('<span size="18000">' + self.spanishList[self.indexOrder[self.number]] + '</span>', '  ')
                        self.myButton.set_label('Show English')
                        self.status = 1
                else:
                    self.getNewWord()
                    self.setLabels('<span size="18000">' + self.spanishList[self.indexOrder[self.number]] + '</span>', '  ')
                    self.myButton.set_label('Show English')
                    self.status = 1
            else:
                if(self.number >= -1 and self.number < len(self.spanishList)): # spanish only
                    self.getNewWord()
                    if( self.number < len(self.spanishList)):
                        self.setLabels('<span size="18000">' + self.englishList[self.indexOrder[self.number]] + '</span>', '  ')
                        self.myButton.set_label('Show Spanish')
                        self.status = 1
                else:
                    self.getNewWord()
                    self.setLabels('<span size="18000">' + self.englishList[self.indexOrder[self.number]] + '</span>', '  ')
                    self.myButton.set_label('Show Spanish')
                    self.status = 1


        elif(self.status == 1): # spanish and english
            if(self.mode == True):
                self.setLabels('<span size="18000">' + self.spanishList[self.indexOrder[self.number]] + '</span>', 
                        '<span size="18000">' + self.englishList[self.indexOrder[self.number]] + '</span>')
            else:
                self.setLabels('<span size="18000">' + self.englishList[self.indexOrder[self.number]] + '</span>', 
                        '<span size="18000">' + self.spanishList[self.indexOrder[self.number]] + '</span>')

            self.myButton.set_label('Next')
            self.status = 0
        else: # done state
            self.setLabels('   ', '  ')
            self.myButton.set_label('Start')
            self.status = 0
            self.number = -1

window = MyWindow()
MyWindow.spanishList=[]
MyWindow.englishList=[]
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
