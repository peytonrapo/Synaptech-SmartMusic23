from music21 import *
from midiutil import MIDIFile
import numpy as np
import csv
import os

print("---------------------------------------")
def readMidi(myMidiFile):
    song = []
    midi = converter.parse(myMidiFile)
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


def makeMatrixNP(song):
  songMatrix= np.zeros((127,len(song)*16), dtype=int)
  for i in range (0, len(song)):
    myMeasure = song[i]
    for myNote in myMeasure:
      songMatrix[myNote["number"]][int(
        (i*4+myNote["offset"])*4        
        )]= myNote["length"]  
  # with open('sample.csv', 'w') as f:
  #   mywriter = csv.writer(f, delimiter=',')
  #   mywriter.writerows(songMatrix)   
  return songMatrix



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
  # np.save("file", songMatrix, allow_pickle=True, fix_imports=True)
  # with open('sample.csv', 'w') as f:
  #   mywriter = csv.writer(f, delimiter=',')
  #   mywriter.writerows(songMatrix)   
  return songMatrix


# song = readMidi("MidiData\MidiFiles\Porter Robinson - Goodbye To A World.mid")
# # print(song)
# songMatrix = makeMatrix(song[0], "PR")
# print(songMatrix[0])



directory = 'MidiData\MidiFiles'

pathsCSVFile = open('MidiData/Paths.csv', 'w', newline="")
theWriter= csv.writer(pathsCSVFile)


for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
      print(f)
      # arr = np.empty(len(song))
      arr = []
      song = readMidi(f)
      for i, part in enumerate(song):
        arr.append(makeMatrix(part))

      arrNP = np.asarray(arr, dtype=object)


      arrayPath =  os.path.join('MidiData/ArrayFiles',os.path.splitext(os.path.basename(f))[0] )
      np.save(arrayPath, arrNP, allow_pickle=True, fix_imports=True)
      theWriter.writerow([arrayPath,'1'])
      




      
      