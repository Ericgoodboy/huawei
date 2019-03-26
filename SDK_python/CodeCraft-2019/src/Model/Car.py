class Car(object):
    def __init__(self,id,fromCrossId,toCrossId,speed,planTime):
        self.id=id
        self.fromCrossId=fromCrossId
        self.toCrossId=toCrossId
        self.speed=speed
        self.plantTime=planTime
        self.answer=[]
        self.startTime=0
        self.bestStartTime=0
        self.isReadyToGo=False
        self.isEnded=False
        self.direction = [0, 0, 0, 0]

    def addDirection(self, direction):
        a = direction[0] - direction[2]
        b = direction[1] - direction[3]
        if a == 0 or b == 0:
            self.direction = 0
        elif a > 0 and b > 0:
            self.direction = 1
        elif a > 0 and b < 0:
            self.direction = 2
        elif a < 0 and b < 0:
            self.direction = 3
        else:
            self.direction = 4
    def nextToGo(self):
        pass
    def addAnswer(self,path):
        self.path=[i for i in path[self.fromCrossId][self.toCrossId]]
        pass
    def getRoadline(self,crossPool,num):
        import math
        govic=[]
        nowpos=[0, 0]
        x1, y1=self.fromCross.pos
        x2, y2=self.toCross.pos
        dic1=(int(((x2-x1)/50)) , int((y2-y1)/50))
        for i in range(num):

            govic.append((nowpos[0], nowpos[1]))
        for i in range(dic1[1]):
            nowpos[1] += 1
            govic.append((nowpos[0], nowpos[1]))
        for i in range(dic1[0]-num):
            nowpos[0] += 1
            govic.append((nowpos[0], nowpos[1]))
        return govic
    def _rightroundit(self):

        pass
    def _leftroundit(self):
        pass

    def __str__(self):
        return str(self.id)+":"+str(self.plantTime)