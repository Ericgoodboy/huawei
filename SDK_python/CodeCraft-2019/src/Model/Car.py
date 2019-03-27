import numpy as np
np.random.seed(123)
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
            self.direct = 0
        elif a > 0 and b > 0:
            self.direct = 1
        elif a > 0 and b < 0:
            self.direct = 2
        elif a < 0 and b < 0:
            self.direct = 3
        else:
            self.direct = 4
    def reRoad(self,roadPool,crossPool):
        a=np.random.randint(2)
        count=0
        for i in self.direction:
            if i>0:
                count+=1
        if count<3:
            tempPath1=[]
            cango1=True
            tempPath2=[]
            cango2=True
            now_cross=self.fromCrossId
            index=0
            for i in self.direction:
                for j in range(i):
                    if crossPool[now_cross].allRoad[index] !=-1:
                        cross=roadPool[crossPool[now_cross].allRoad[index]]
                        tempPath1.append(crossPool[now_cross].allRoad[index])
                        if True!= cross.isDuplex and cross.fromCrossId!=now_cross:
                            cango1=False
                        now_cross=cross.fromCrossId if now_cross==cross.toCrossId else cross.toCrossId
                    else:
                        cango1=False
                index+=1
            index=3
            now_cross = self.fromCrossId
            self.direction.reverse()
            for i in self.direction:
                for j in range(i):
                    if crossPool[now_cross].allRoad[index] !=-1:
                        cross=roadPool[crossPool[now_cross].allRoad[index]]
                        tempPath2.append(crossPool[now_cross].allRoad[index])
                        if True!= cross.isDuplex and cross.fromCrossId!=now_cross:
                            cango2=False
                        now_cross=cross.fromCrossId if now_cross==cross.toCrossId else cross.toCrossId
                    else:
                        cango2=False
                index-=1
            self.direction.reverse()
            if cango1 and cango2:
                self.path=tempPath1 if np.random.randint(2)==0 else tempPath2
                return 1
            elif cango1:
                self.path=tempPath1
                return 1
            elif cango2:
                self.path=tempPath2
                return 1
        return 0
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