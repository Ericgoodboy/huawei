

class Cross(object):
    TYPE="Cross"
    def __init__(self,id,nRoadId,eRoadId,sRoadId,wRoadId):
        self.id=id
        self.nRoadId=nRoadId
        self.eRoadId=eRoadId
        self.wRoadId=wRoadId
        self.sRoadId=sRoadId
        self.allRoad =[nRoadId,eRoadId,sRoadId,wRoadId]#n=0,e=1,s=
        self.flag=0
        self.pos=()
        self.calPlaceFlag=0
    def moveAllRoad(self,roadId,index):
        index=index%4
        indexnow=self.allRoad.index(roadId)
        neg=(index-indexnow)%4
        for i in range(neg):
            self.allRoad.insert(0,self.allRoad.pop())
        pass
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





