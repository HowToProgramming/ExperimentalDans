import os
import numpy as np

class HitObject:
    def __init__(self, code):
        self.data = code.split(",")
        self.lane = int(self.data[0])
        self.samplesound = int(self.data[1])
        self.offset = int(self.data[2])
        self.type = int(self.data[3])
        self.hitsound = int(self.data[4])
        self.release = -1
        if self.type == 128:
            self.release = int(self.data[-1].split(":")[0])

class TimingPoint:
    def __init__(self, code):
        self.data = code.split(",")
        self.offset = float(self.data[0])
        self.isBPM = int(self.data[-2])
        if self.isBPM == 1:
            self.velocity = 60000 / float(self.data[1])
        else:
            self.velocity = -100 / float(self.data[1])
        self.timeSignature = int(self.data[3])
        self.hitsoundvolume = int(self.data[5])
        self.isKiai = int(self.data[-1][0])

class osufile:
    def __init__(self, data: str):
        self.data = data.split("\n")
        self.General = None
        self.editor = None
        self.metadata = None
        self.difficulty = None
        self.TimingPoints = list()
        self.HitObjects = list()
        self.initialize_data()
    
    def initialize_data(self):
        self.parseGeneral()
        self.parseEditor()
        self.parseMetadata()
        self.parseDifficulty()
        self.parseTimingPoints()
        self.parseHitObjects()
    
    def parseGroup(self, keyword):
        start = self.data.index("[{}]".format(keyword)) + 1
        end = self.data[start:].index("") + start
        group = dict()
        for data in self.data[start:end]:
            d = data.split(":")
            try:
                d[1] = float(d[1])
            except:
                pass
            group[d[0]] = d[1]
        return group

    def parseGeneral(self):
        self.General = self.parseGroup("General")
    
    def parseEditor(self):
        self.editor = self.parseGroup("Editor")
        if "Bookmarks" in self.editor.keys():
            self.editor["Bookmarks"] = [int(k) for k in self.editor["Bookmarks"].split(",")]
    
    def parseMetadata(self):
        self.metadata = self.parseGroup("Metadata")
        self.metadata["Tags"] = self.metadata["Tags"].split(" ")
    
    def parseDifficulty(self):
        self.difficulty = self.parseGroup("Difficulty")
    
    def parseTimingPoints(self):
        start = self.data.index("[TimingPoints]") + 1
        end = self.data[start:].index("") + start
        for data in self.data[start:end]:
            self.TimingPoints.append(TimingPoint(data))
    
    def parseHitObjects(self):
        start = self.data.index("[HitObjects]") + 1
        end = self.data[start:].index("") + start
        for data in self.data[start:end]:
            self.HitObjects.append(HitObject(data))

def parse_beatmap(file):
    with open(file, "r") as f:
        data = f.read()
        return osufile(data)

if __name__ == "__main__":
    beatmap = parse_beatmap("GALNERYUS - RAISE MY SWORD (-[DaNieL_TH]-) [Synchronized Sword].osu")
    for k in beatmap.TimingPoints:
        print(k.__dict__)