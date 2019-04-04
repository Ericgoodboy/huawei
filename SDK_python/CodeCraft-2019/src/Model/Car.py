import numpy as np
np.random.seed(123)
class Car(object):
    def __init__(self,id,fromCrossId,toCrossId,speed,planTime,priority,preset):
        self.id=id
        self.fromCrossId=fromCrossId
        self.toCrossId=toCrossId
        self.speed=speed
        self.plantTime=planTime
        self.answer=[]
        self.startTime=0
        self.bestStartTime=0
        self.direction = [0, 0, 0, 0]
        self.nowRoad=-1
        self.canGoOnRoad = True
        self.isReadyToGo = False
        self.togoNext = -1
        self.lest=0
        self.path=[]
        self.endState=False
        self.priority=priority
        self.preset=preset
    def outCarPort(self,processingCarPool,timecarPool,roadPool,crossPool):
        road=roadPool[self.path[0]]
        place=road.placesA if road.fromCrossId==self.fromCrossId else road.placesB
        x,y = self.handlePlace(place)
        v=min(road.speed,self.speed)
        if x == -2:
            self.isReadyToGo = False
            for i in place:
                car=processingCarPool[i[0]]
                print(-2)
                if car.isReadyToGo==True:
                    self.isReadyToGo = True
                    return False
            timecarPool.remove(self)
            return True
        elif x==-1:
            print(-1)
            self.handleCarGo(place,(0,v-1),self,v,roadPool,crossPool,self.path[0])
            timecarPool.remove(self)
            return True
        else:
            print(self.id,x,y)
            self.handleCarGo(place,(x,min(v-1,y)),self,v,roadPool,crossPool,self.path[0])
            timecarPool.remove(self)
            return True
    def handleCarGo(self, toRoad, toIndex, car, v, roadPool, crossPool, roadId):
        tx, ty = toIndex
        toRoad[tx][ty] = car.id
        self.isReadyToGo=False
        if ty + v - 1 < len(toRoad[0]):
            car.canGoOnRoad = True
        else:
            car.canGoOnRoad = False
            car.lest = len(toRoad[0]) - ty

            indexRoad = car.path.index(roadId)
            if indexRoad == len(car.path) - 1:
                car.togoNext = 0
            else:
                # 待检查
                nextRoad = car.path[indexRoad + 1]
                temp = [roadPool[roadId].fromCrossId, roadPool[roadId].toCrossId]
                cross = roadPool[nextRoad].fromCrossId if roadPool[nextRoad].fromCrossId in temp else roadPool[
                    nextRoad].toCrossId
                f = crossPool[cross].allRoad.index(roadPool[roadId].id)
                t = crossPool[cross].allRoad.index(nextRoad)
                print("car"+"carId:", car.id, "f:", f, "t", t)
                direction = (f - t) % 4
                car.togoNext = direction
    def handlePlace(self,place):
        for i in range(len(place)):
            if place[i][0]!=0:
                continue
            index=0
            for j in place[i]:
                if j !=0:
                    return (i,index-1)
                index+=1
        if place[len(place)-1][0] !=0:
            return (-2,0)
        return (-1,-1)
    def addDirection(self, direction):
        a = direction[0] - direction[2]
        b = direction[1] - direction[3]
        if a == 0 or b == 0:
            self.direct= 0
        elif a > 0 and b > 0:
            self.direct = 1
        elif a > 0 and b < 0:
            self.direct= 2
        elif a < 0 and b < 0:
            self.direct= 3
        else:
            self.direct = 4
    def addMaxRoadId(self,path,count):
        maxCount = 0
        for i in path:
            self.maxRoadId = i if count[i] > maxCount else 0
    # 划分区域
    # 0为初始值，1为左下，2为左上，3为右下，4为右上下同
    def zoning(self, maxpos, crossPool):
        crossPos = crossPool[self.fromCrossId].pos
        midX = maxpos[0] / 2
        midY = maxpos[1] / 2
        if crossPos[0] < midX and crossPos[1] < midY:
            self.fromPos = 1
        elif crossPos[0] < midX and crossPos[1] > midY:
            self.fromPos = 2
        elif crossPos[0] > midX and crossPos[1] < midY:
            self.fromPos = 3
        else:
            self.fromPos = 4
    # 把路线捋直
    def reRoad(self, roadPool, crossPool):
        a = np.random.randint(2)
        count = 0
        for i in self.direction:
            if i > 0:
                count += 1
        if count < 3:
            tempPath1 = []
            cango1 = True
            tempPath2 = []
            cango2 = True
            now_cross = self.fromCrossId
            index = 0
            for i in self.direction:
                for j in range(i):
                    if crossPool[now_cross].allRoad[index] != -1:
                        if now_cross == self.toCrossId:
                            continue
                        cross = roadPool[crossPool[now_cross].allRoad[index]]
                        tempPath1.append(crossPool[now_cross].allRoad[index])
                        if True != cross.isDuplex and cross.fromCrossId != now_cross:
                            cango1 = False
                        now_cross = cross.fromCrossId if now_cross == cross.toCrossId else cross.toCrossId
                    else:
                        cango1 = False
                index += 1
            cango1 = cango1 and now_cross == self.toCrossId
            index = 3
            now_cross = self.fromCrossId
            self.direction.reverse()
            for i in self.direction:
                for j in range(i):
                    if crossPool[now_cross].allRoad[index] != -1:
                        if now_cross == self.toCrossId:
                            continue
                        cross = roadPool[crossPool[now_cross].allRoad[index]]
                        tempPath2.append(crossPool[now_cross].allRoad[index])
                        if True != cross.isDuplex and cross.fromCrossId != now_cross:
                            cango2 = False
                        now_cross = cross.fromCrossId if now_cross == cross.toCrossId else cross.toCrossId
                    else:
                        cango2 = False
                index -= 1
            cango1 = cango1 and now_cross == self.toCrossId
            self.direction.reverse()
            if cango1 and cango2:
                self.path = tempPath1 if np.random.randint(2) == 0 else tempPath2
                return 1
            elif cango1:
                self.path = tempPath1
                return 1
            elif cango2:
                self.path = tempPath2
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
        return str(self.id)+":"+str(self.bestStartTime)