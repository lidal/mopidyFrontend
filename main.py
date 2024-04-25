import sys, os
from PyQt5.QtWidgets import (QWidget, QGridLayout,
                             QPushButton, QApplication,QScrollArea,QVBoxLayout,QHBoxLayout,QLabel,QMainWindow,QScroller)
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtGui import QIcon,QPixmap,QScreen
from mopidyapi import MopidyAPI

IMAGELOCATION  = "/home/jonas/.local/share/mopidy/local/images"

class AlbumItem(QWidget):
    def __init__(self,uri,title,albumArt,artist, parent=None):
        super().__init__()
        self.parent = parent

        layout = QVBoxLayout()
        self.setLayout(layout)

        albumButton = QPushButton("")
        albumButton.setStyleSheet("")
        albumButton.setIcon(QIcon(QPixmap(albumArt)))
        albumButton.setIconSize(QSize(300,300))
        albumButton.clicked.connect(lambda: self.play(uri))
        
        title = title
        sanTitle = ((title[:27] + '...') if len(title) > 27 else title).replace('&', '&&')
        titleButton = QPushButton(sanTitle)
        titleButton.setStyleSheet("color:#ffffff;")
        titleButton.clicked.connect(lambda: self.play(uri))

        artist = artist.replace('&', '&&')
        
        artistButton = QPushButton(artist)
        artistButton.setStyleSheet("color:#a3a3a3")
        artistButton.clicked.connect(lambda: self.play(uri))

        layout.addWidget(albumButton)
        layout.addWidget(titleButton)
        layout.addWidget(artistButton)

    def play(self,uri):
        self.parent.start(uri)


    


class mainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.mopidy = MopidyAPI()
        self.setStyleSheet("background-color: #121212;color:white;font-size:12pt;font-family: 'Circular', sans-serif;text-align:left;font-weight:bold;border:none;")
        self.scroll = QScrollArea()   
        self.widget = QWidget()   
        self.vbox = QVBoxLayout() 

        library = self.mopidy.library.browse('local:directory?type=album')

        for albumNr, album in enumerate(library):
            uri = album[0]
            title = album[1]

            #takeArtist as first artist on first song
            artist =  self.mopidy.library.lookup([uri])[uri][0].artists[0].name.split(',')[0]

            #album art
            albumArt =self.mopidy.library.get_images([uri])
            ##Extract uri
            albumArt = albumArt[uri][0].uri
            ##Get to correct location
            albumArt = albumArt.replace("/local",IMAGELOCATION)

            albumItem = AlbumItem(uri,title,albumArt,artist,parent=self)
            if albumNr%2==0:
                hbox = QHBoxLayout()
            hbox.addWidget(albumItem)
            if albumNr%2==1:
                self.vbox.addLayout(hbox)
        #add the last album if there is an odd number of albums
        if(albumNr%2==0):
            self.vbox.addLayout(hbox)

        self.widget.setLayout(self.vbox)
        self.vbox.setContentsMargins(25, 25, 0, 25)
        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        QScroller.grabGesture(self.scroll.viewport(), QScroller.LeftMouseButtonGesture)


        self.setCentralWidget(self.scroll)

        self.setGeometry(300, 300, 720, 720)
        self.setWindowTitle('MopidyFrontend')
        self.show()

    def start(self,uri):
        #get tracklist
        tracklist = self.mopidy.library.lookup([uri])[uri]
        #clear tracklisst
        self.mopidy.tracklist.clear()
        #add current playlist
        self.mopidy.tracklist.add(tracklist)
        #play
        self.play()
        

    def stop(self):
        self.mopidy.playback.stop()
    def pause(self):
        self.mopidy.playback.pause()
    def play(self):
        self.mopidy.playback.play()


    def closeEvent(self, event):
        self.stop()


def main():
    app = QApplication(sys.argv)
    win = mainWindow()
    #win.showFullScreen()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()

