import sys, os
from PyQt5.QtWidgets import (QWidget, QGridLayout,
                             QPushButton, QApplication,QScrollArea,QVBoxLayout,QHBoxLayout,QLabel,QMainWindow,QScroller)
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtGui import QIcon,QPixmap

class AlbumItem(QWidget):
    def __init__(self,uri):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        albumArt = QPushButton("")
        albumArt.setStyleSheet("")
        albumArt.setIcon(QIcon(QPixmap("/home/jonas/mopidyFrontend/album.jpeg")))
        albumArt.setIconSize(QSize(300,300))
        
        title = uri
        titleButton = QPushButton(title)
        titleButton.setStyleSheet("color:#ffffff;")

        artist = "Artist"
        artistButton = QPushButton(artist)
        artistButton.setStyleSheet("color:#a3a3a3")

        layout.addWidget(albumArt)
        layout.addWidget(titleButton)
        layout.addWidget(artistButton)



    


class mainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.setStyleSheet("background-color: #121212;color:white;font-size:12pt;font-family: 'Circular', sans-serif;text-align:left;font-weight:bold;border:none;")
        self.scroll = QScrollArea()   
        self.widget = QWidget()   
        self.vbox = QVBoxLayout() 
        

        for i in range(1,50):
            object = AlbumItem("The First Album ever")
            object2 = AlbumItem("Best albym ever")
            hbox = QHBoxLayout()
            hbox.addWidget(object)
            hbox.addWidget(object2)
            self.vbox.addLayout(hbox)

        self.widget.setLayout(self.vbox)
        self.vbox.setContentsMargins(25, 0, 0, 0)
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


def main():
    app = QApplication(sys.argv)
    win = mainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

