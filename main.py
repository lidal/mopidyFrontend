from mopidyapi import MopidyAPI
from operator import itemgetter
import time

m = MopidyAPI()


#library = m.library.browse('local:directory?type=album')
library = m.library.browse('spotify:your:albums')

albumNR = 0


libraryoverview= []

for album in library:
    libraryoverview.append([album[1].lower(),album[0]])
libraryoverview = sorted(libraryoverview, key=itemgetter(0))

albumURI = libraryoverview[albumNR][1]

print('title: ' ,libraryoverview[albumNR][0])
print('uri: ', libraryoverview[albumNR][1])
print('image', m.library.get_images([libraryoverview[albumNR][1]]))

tracklist = m.library.lookup([albumURI])[albumURI]
m.tracklist.clear()
m.tracklist.add(tracklist)
m.playback.play()
time.sleep(10)
m.playback.pause()