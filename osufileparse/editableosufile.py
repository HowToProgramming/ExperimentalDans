from osuparse import osufile

class editableosufile(osufile):
    def __init__(self, data):
        super().__init__(data)
    
    def scroll(self, offset):
        t = self
        for i in range(len(t.TimingPoints)):
            t.TimingPoints[i].offset += offset
            t.TimingPoints[i].data[0] = str(t.TimingPoints[i].offset)
        for k in range(len(t.HitObjects)):
            t.HitObjects[k].offset += offset
            t.HitObjects[k].data[2] = str(t.HitObjects[k].offset)
        return t

    def __add__(self, elem):
        if isinstance(elem, float) or isinstance(elem, int):
            return self.scroll(elem)
        if isinstance(elem, osufile):
            t = self
            t.TimingPoints += elem.TimingPoints
            t.HitObjects += elem.HitObjects
            return t
        if isinstance(elem, editableosufile):
            t = self
            start = t.HitObjects[-1].offset
            elem = elem.scroll(start)
            t.TimingPoints += elem.TimingPoints
            t.HitObjects += elem.HitObjects
            return t
        else:
            raise TypeError("Invalid Operation between editableosufile and {}".format(type(elem)))