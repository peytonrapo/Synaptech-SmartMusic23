from music21 import *
from midiutil import MIDIFile
import numpy as np
import csv



# midi = converter.parse("midiSamples\Cymatics - Posty MIDI Loop 6 - 150 BPM C# Min.mid")
# midi = converter.parse("midiSamples\lullaby-4.mid")
# midi = converter.parse("midiSamples\Cymatics - Lofi MIDI 1 - C# Maj.mid")
# midi = converter.parse("midiSamples\millenium1.mid") 
# midi = converter.parse("midiSamples\Porter Robinson - Goodbye To A World.mid")




#read song into lists&dicts of ints and strings with music21
def readMidi():
    song = []
    
    for partElement in midi.recurse():
      if type(partElement)==stream.Part: 
        measureNumber = 0
        partArr = []

        for measureElement in partElement:
          if type(measureElement)==stream.Measure:
            thisMeasureList = []
            for elementInMeasure in measureElement.recurse():
              if type(elementInMeasure) == note.Note:
                thisNoteDict = {}
                thisNoteDict["name"] = elementInMeasure.name + ""+ str(elementInMeasure.octave)
                thisNoteDict["number"] = elementInMeasure.pitch.midi
                thisNoteDict["length"] = elementInMeasure.quarterLength
                thisNoteDict["offset"] = elementInMeasure.offset
                thisMeasureList.append(thisNoteDict)
              if type(elementInMeasure) == chord.Chord:
                length = elementInMeasure.quarterLength
                offset = elementInMeasure.offset
                for thisPitch in elementInMeasure.pitches:
                  thisNoteDict = {}
                  thisNoteDict["name"] = thisPitch.name +""+ str(thisPitch.octave)
                  thisNoteDict["number"] = thisPitch.midi
                  thisNoteDict["length"] = length
                  thisNoteDict["offset"] = offset
                  thisMeasureList.append(thisNoteDict)

            
            partArr.append(thisMeasureList)
            measureNumber+=1
        

        song.append(partArr)


    return song
# song = readMidi()
# print(song[0])

#WRITE midi with midiutil
def writeMidi(song):
    degrees  = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
    track    = 0
    channel  = 0
    time     = 0    # In beats
    duration = 1    # In beats
    tempo    = 130   # In BPM
    volume   = 100  # 0-127, as per the MIDI standard
    MyMIDI = MIDIFile(1)  # One track
    MyMIDI.addTempo(track, time, tempo)

    currentMeasure=0
    for i in range (0, len(song)):
      for note in song[i]:
        MyMIDI.addNote(track, channel, note["number"], (currentMeasure * 4 + note["offset"]), note["length"], volume)
    # print(pitchesDict[note["name"]])
      currentMeasure+= 1

# for i, pitch in enumerate(degrees):
#     MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)
    with open("writeMidiOut.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)
# writeMidi(song[0])


def makeMatrixNP(song):
  
  # songMatrix = []
  # for i in range (0, 127):
  #   songMatrix.append([])
  #   for j in range (0, len(song)*16):
  #     songMatrix[i].append(0)

  songMatrix= np.zeros((127,len(song)*16), dtype=int)
  for i in range (0, len(song)):
    myMeasure = song[i]
    for myNote in myMeasure:
      songMatrix[myNote["number"]][int(
        (i*4+myNote["offset"])*4        
        )]= myNote["length"]
        


  np.save("file", songMatrix, allow_pickle=True, fix_imports=True)
  # with open('sample.csv', 'w') as f:
  #   mywriter = csv.writer(f, delimiter=',')
  #   mywriter.writerows(songMatrix)   
  return songMatrix

# songMatrix = makeMatrix(song[0])
# print(songMatrix[0])


def makeMatrix(song):
  songMatrix = []
  for i in range (0, 127):
    songMatrix.append([])
    for j in range (0, len(song)*16):
      songMatrix[i].append(0)
  for i in range (0, len(song)):
    myMeasure = song[i]
    for myNote in myMeasure:
      songMatrix[myNote["number"]][int(
        (i*4+myNote["offset"])*4        
        )]= myNote["length"]
  np.save("file", songMatrix, allow_pickle=True, fix_imports=True)
  # with open('sample.csv', 'w') as f:
  #   mywriter = csv.writer(f, delimiter=',')
  #   mywriter.writerows(songMatrix)   
  return songMatrix







# converts pitchxtime matrix into midi file
# parameter- matrix
def writeMidiFromMatrix(songMatrix, fileName):
    degrees  = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
    track    = 0
    channel  = 0
    time     = 0    # In beats
    duration = 1    # In beats
    tempo    = 130   # In BPM
    volume   = 100  # 0-127, as per the MIDI standard
    MyMIDI = MIDIFile(1)  # One track
    MyMIDI.addTempo(track, time, tempo)
    # print(songMatrix.shape)
    for i in range (songMatrix.shape[0]):
      for j in range (songMatrix.shape[1]):
        lengthOfNote = songMatrix[i][j]
        if (lengthOfNote !=0):
          # print(lengthOfNote)
          MyMIDI.addNote(track, channel, i , j/4, lengthOfNote, volume)



    #     MyMIDI.addNote(track, channel, note["number"], (currentMeasure * 4 + note["offset"]), note["length"], volume)


    with open(fileName, "wb") as output_file:
        MyMIDI.writeFile(output_file)
# writeMidiFromMatrix(songMatrix, "writeMidiFromMatrixOut1.mid")

# arr = np.random.randint(5, size=(127, 128))
# print(arr)
# writeMidiFromMatrix(arr,"out1.mid")









## Trying to writi midi with music 21 (REALLY STUPID)
# #sort by offset
# def returnKey(e):
#   return e['offset']

# for measure in song:
#   measure.sort(key=returnKey)

#   chords = []
#   currentOffset = -1;
#   currentChord = []
#   for i in range(0,len(measure)):
#     note = measure[i]
#     noteOffset = note[offset]

#     if noteOffset != currentOffset:
#       currentOffset = note[offset]
      
#       if note[offset] == measure[i+1][offset]:
#         currentChord.append(note)

#     else:
      
#       if note[length]
#       currentChord.append(note)
#       if note[offset] == measure[i+1][offset]:
#         chords.append(currentChord)
      




def componentsmaker():
  components = []

  for element in midi.recurse():
    components.append(element)
    
  print(components)

  print(components[20].offset)
  print(components[20].name)
  print(components[20].activeSite)


def writeCaillou():
  stream1 = stream.Stream()

  thisNote = note.Note("B-4")
  stream1.append(thisNote)

  thisNote = note.Note("G")
  thisNote.quarterLength = .75
  stream1.append(thisNote)

  thisNote = note.Note("F")
  thisNote.quarterLength = .25
  stream1.append(thisNote)

  thisNote = note.Note("E-4")
  thisNote.quarterLength = .75
  stream1.append(thisNote)

  thisNote = note.Note("F")
  thisNote.quarterLength = .25
  stream1.append(thisNote)

  thisNote = note.Note("G")
  stream1.append(thisNote)

  thisNote = note.Note("c5")
  stream1.append(thisNote)

  thisNote = note.Note("G")
  thisNote.quarterLength = .75
  stream1.append(thisNote)

  thisNote = note.Note("F")
  thisNote.quarterLength = .25
  stream1.append(thisNote)

  thisNote = note.Note("E-4")
  thisNote.quarterLength = .75
  stream1.append(thisNote)

  thisNote = note.Note("F")
  thisNote.quarterLength = .25
  stream1.append(thisNote)

  thisNote = note.Note("G")
  stream1.append(thisNote)

  stream1.show()