
class Cross(object):
    TYPE="Cross"
    def __init__(self,id,nRoadId,eRoadId,sRoadId,wRoadId):
        self.id=id
        self.nRoadId=nRoadId
        self.eRoadId=eRoadId
        self.wRoadId=wRoadId
        self.sRoadId=sRoadId
        self.allRoad =[nRoadId,eRoadId,sRoadId,wRoadId]
        self.flag=0
        self.pos=()

    def link(self,road):
        if road.id == self.nRoadId:
            self.nRoad=road
        if road.id == self.eRoadId:
            self.eRoad=road
        if road.id == self.wRoadId:
            self.wRoad=road
        if road.id == self.sRoadId:
            self.sRoad=road
    def __str__(self):
        ref="\nn:"+str(self.nRoad)
        ref+="\ne:"+str(self.eRoad)
        ref+="\nw:"+str(self.wRoad)
        ref+="\ns:"+str(self.sRoad)
        return ref





