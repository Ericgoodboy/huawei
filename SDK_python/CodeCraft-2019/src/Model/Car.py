import numpy as np
np.random.seed(123)
class Car(object):
    CARINPORT=0
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
        self.nowChannel="start"
    def scan(self,crossPool,roadPool,carPool):
        if self.nowChannel=="start":
            road = roadPool[self.path[0]]
            direction = road.directions[0] if road.fromCrossId==self.id else road.directions[1]
            v=min(self.speed,road.speed)
            channel,index=self.handlePlace(direction,v)
            return channel,index
        else:
            pass
    def handleChannel(self,v):
        length=v
        index = len(self.nowChannel) - self.lest
        for i in range(v):
                if self.nowChannel[index]!=0:
                    return index-1,self.nowChannel[index]
                index+=1
        return index-1,0

    def goOnRoad(self,crossPool,roadPool,carPool):
        road=self.nowRoad
        if self.canGoOnRoad:
            index,carId=self.handleChannel(min(road.speed, self.speed))
            if carId!=0:
                car = carPool[carId]
                if car.isReadyToGo==False:#当前面的车进入终止状态，本车也进入终止状态
                    self.isReadyToGo=False
            else:
                self.carMove(self.nowChannel,index,road,crossPool,roadPool)
        else:
            index, carId = self.handleChannel(min(road.speed, self.speed,self.lest))
            # if self.id == 61122:
            #     # print("()()()()()()()()()()()()()()(")
            #     # print(index,carId)
            #     # print(self.nowChannel)
            #     # print(self.isReadyToGo)
            #     # print(self.nowRoad.id)

            if carId!=0:
                car = carPool[carId]
                # if self.id == 61122:
                #     # print("<<<<<<<<<<<<<<<<<<<<<")
                #     # print(index, carId)
                #     # print(self.nowChannel)
                #     # print(self.isReadyToGo)
                #     # print(self.nowRoad.id)
                #     # print(car.isReadyToGo)
                #     # print(">>>>>>>>>>>>>>>>>>>>")
                if car.isReadyToGo==False:#当前面的车进入终止状态，本车也进入终止状态
                    self.isReadyToGo=False
    def carMove(self,toChannel,toIndex,road,crossPool,roadPool):#road 是对象
        # print("car:",self.id,"wo zai zou ",self.nowRoad,">",road,">",toIndex)
        if self.nowChannel is not "start":
            templist=list(self.nowChannel)
            fromIndex=templist.index(self.id)
            self.nowChannel[fromIndex]=0
        if toChannel[toIndex]!=0:
            print("----------------------------------------")
            print("***** WARNING IMPORTANT WARING *********")
            print("road Channel:",self.nowChannel)
            print("about Car :",self.id)
            print("----------------------------------------")
            return
        else:
            self.nowChannel=toChannel
            toChannel[toIndex]=self.id
            self.isReadyToGo=False
            self.lest=len(toChannel)-toIndex-1
            self.canGoOnRoad=self.lest>= min(road.speed,self.speed)
            self.nowRoad=road
            if self.canGoOnRoad==False:

                if self.nowRoad.id== self.path[-1]:
                    self.togoNext=0
                else:
                    nextRoad = roadPool[self.path[self.path.index(self.nowRoad.id) + 1]]
                    crossID = self.nowRoad.toCrossId if self.nowRoad.toCrossId in [nextRoad.toCrossId,
                                                                                   nextRoad.fromCrossId] else self.nowRoad.fromCrossId
                    cross = crossPool[crossID]
                    fromIndex=cross.allRoad.index(self.nowRoad.id)
                    toIndex = cross.allRoad.index(nextRoad.id)
                    self.togoNext=(fromIndex-toIndex)%4

    def handelPlace(self,direction,length,carPool):
        for channel in direction:
            if channel[0]!=0:
                if carPool[channel[0]].isReadyToGo== True:
                    return None ,-1
                continue
            cloum=0
            for place in channel:
                if place != 0:
                    return channel,cloum-1
                if cloum>=(length -1):
                    return channel,cloum
                cloum+=1
            return channel, cloum-1
        return None,-1

    def moveToNextRoad(self,carOnRoad,cross,crossPool,roadPool):#待定
        if self.togoNext==0:
            # print("有车入库了:",self.id)
            Car.CARINPORT+=1
            #print(" Car.CARINPORT", Car.CARINPORT)
            self.endState=True
            carOnRoad.pop(self.id)
            templist=list(self.nowChannel)
            tempIndex=templist.index(self.id)
            self.nowChannel[tempIndex]=0
            return True,True
        else:
            nowIndex=self.path.index(self.nowRoad.id)
            nextRoad=roadPool[self.path[nowIndex+1]]
            direction=nextRoad.directions[0] if nextRoad.fromCrossId==cross else nextRoad.directions[1]
            length=min(nextRoad.speed,self.speed)-self.lest#待验证
            if length<=0:
                self.carMove(self.nowChannel, len(self.nowChannel) - 1, self.nowRoad, crossPool, roadPool)
                return True, False
            channel,index = self.handelPlace(direction,length,carOnRoad)
            if length==0:
                print(channel,index)
            if channel is not None:
                if index < length -1:#---------------
                    car = carOnRoad[channel[index + 1]]  # nowchanged
                    if car.isReadyToGo == True:
                        return False,False
                self.carMove(channel,index,nextRoad,crossPool,roadPool)
                return True,False
            elif self.lest==0:
                self.isReadyToGo=False
                for c in direction:
                    if carOnRoad[c[0]].isReadyToGo==True:
                        self.isReadyToGo=True
                        return False,False
                return True,False
            else:#toChannel,toIndex,road,crossPool,roadPool
                for c in direction:
                    if carOnRoad[c[0]].isReadyToGo==True:
                        self.isReadyToGo=True
                        return False,False
                self.carMove(self.nowChannel,len(self.nowChannel)-1,self.nowRoad,crossPool,roadPool)
                return True,False

    def runToRoad(self,carPool,roadPool,crossPool):
        road=roadPool[self.path[0]]
        direction=road.directions[0] if road.fromCrossId==self.fromCrossId else road.directions[1]
        channel,index= self.handelPlace(direction,min(self.speed,road.speed),carPool)
        if channel is None:
            return False
        else:#toChannel,toIndex,road,crossPool,roadPool
            length=min(self.speed,road.speed)
            if index<length-1:
                car=carPool[channel[index+1]]#nowchanged
                if car.isReadyToGo==True:
                    return False
            self.carMove(channel,index,road,crossPool,roadPool)
            return True





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
        midX1 = maxpos[0]*1 / 3
        midX2 = maxpos[0] * 2 / 3
        midY1 = maxpos[1] * 1/ 3
        midY2 = maxpos[1] * 2 / 3
        a=self.__calPlace(mid1=midX1,mid2=midX2,item=crossPos[0])
        b=self.__calPlace(mid1=midY1,mid2=midY2,item=crossPos[1])
        self.place=a * 3 + b
    def __calPlace(self,mid1,mid2,item):
        if item<mid1:
            return 0
        elif item<mid2:
            return 1
        else:return 2
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
    def _rightroundit(self):
        pass
    def _leftroundit(self):
        pass

    def __str__(self):
        return str(self.id)+":"+str(self.bestStartTime)