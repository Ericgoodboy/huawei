import numpy
import math
class Road():
    NOCAR="none"
    TYPE="Road"
    def __init__(self,id,length,speed,channel,fromCrossId,toCrossId,isDuplex):
        self.id=id
        self.maxCar=length*channel
        self.length=length
        self.speed=speed
        self.fromCrossId=fromCrossId
        self.channel=channel
        self.toCrossId=toCrossId
        self.isDuplex=isDuplex
        self.arg=0
        self.roadOut = [0, 0]
        self.roadIn = [0, 0]
        self.deployeeArg=0.1
        self.maxCarOnroad=2000
        self.waitList = [[], []]
        self.InitCar=[[],[]]#初始化车辆集合 对象这有一个问题
        if isDuplex:#places[0]表示正向，places[1]表示反向
            self.directions=numpy.zeros((2,channel,length),dtype="int32")#from - to
        else:
            self.directions=numpy.zeros((1,channel,length),dtype="int32")#from - tos
    # def depoloyeeCar(self,timestamp,carOnRoad):
    #     self.InitCar[0].extend(self.waitList[0])
    #     self.InitCar[0].sort(key=lambda car:(-car.priority,car.bestStartTime,car.id))
    #     if self.isDuplex==1:
    #         self.InitCar[1].extend(self.waitList[1])
    #         self.InitCar[1].sort(key=lambda car:(-car.priority,car.bestStartTime,car.id))
    def deployee(self,timestamp)->int:
        added = 0
        i = 0
        kIn=1
        kOut=0.4
        maxpresure=5000
        if timestamp<800:
            kIn = 1
            kOut = 0.4
        for direction in self.directions:
            if len(direction)<2:
                if timestamp<800:
                    return 0
            countnowCar=len(direction.nonzero()[0])
            # if countnowCar>self.maxCar*0.5:
            #     print(direction)

            toOutCar = self.roadOut[i]
            toInCar = self.roadIn[i]
            waitCar =len([car for car in self.InitCar[i] if car.bestStartTime <= timestamp])
            if timestamp<30:
                return 0
            toOnRoad = self.maxCar*self.deployeeArg-countnowCar + toOutCar*kOut -toInCar*kIn-waitCar
            if toOnRoad>0:
                ina=int(toOnRoad)
                if len(self.waitList[i])>=ina:
                    temp=self.waitList[i][0:ina]
                    for c in temp:
                        c.bestStartTime = max(timestamp,c.plantTime)
                    self.InitCar[i].extend(temp)
                    self.waitList[i] = self.waitList[i][ina:]
                    added+=ina
                else:
                    added += len(self.waitList[i])
                    temp = self.waitList[i]
                    for c in temp:
                        c.bestStartTime = max(timestamp,c.plantTime)
                    self.InitCar[i].extend(temp)
                    self.waitList[i]=[]
                self.InitCar[i].sort(key=lambda car:(-car.priority,car.bestStartTime,car.id))
            i+=1
        return added



    def addInitCar(self,car):
        # if car.fromCrossId == self.fromCrossId:
        #     self.InitCar[0].append(car)
        # else:
        #     self.InitCar[1].append(car)
        if car.preset==1:
            if car.fromCrossId==self.fromCrossId:
                self.InitCar[0].append(car)
            else:
                self.InitCar[1].append(car)
        else:
            if car.fromCrossId==self.fromCrossId:
                self.waitList[0].append(car)
            else:
                self.waitList[1].append(car)


    def runCarInitList(self,carPool,roadPool,crossPool,nowTime,priority,crossId=-1):
        k=2 if self.isDuplex==1 else 1
        # print(len(self.InitCar[1]))
        # if len(self.InitCar[1])>0:
        #     print(self.isDuplex)
        #     print("----------------------")
        goneCar = {}
        for i in range(k):
            if i == 0 and crossId == self.toCrossId:
                continue
            if i == 1 and crossId == self.fromCrossId:
                continue
            if len(self.InitCar[i]) == 0:
                continue
            toGoCars=[]
            if priority:
                toGoCars = [car for car in self.InitCar[i] if car.priority == 1 and car.bestStartTime <= nowTime]
            else:
                toGoCars = [car for car in self.InitCar[i] if car.bestStartTime <= nowTime]

            #修改了

            for car in toGoCars:
                isGo=car.runToRoad(carPool,roadPool,crossPool)
                if isGo:
                    goneCar.update({car.id:car})
                    self.InitCar[i].remove(car)
        return goneCar

    def getFirstToGoCar(self,cross,carPool):
        if self.isDuplex == 0 and cross.id == self.fromCrossId:
            return False
        elif cross.id == self.toCrossId:
            direction = self.directions[0]
        else:
            #print(cross, self.fromCrossId, self.toCrossId)
            direction = self.directions[1]
        row = self.length
        rowIndex=row-1
        colum = self.channel
        tempCar=False
        headList=[True for i in range(colum)]
        for i in range(row):
            for j in range(colum):
                if headList[j] != True:
                    continue
                if direction[j][rowIndex]!=0:
                    headList[j]=False
                    car = carPool[direction[j][rowIndex]]
                    if car.isReadyToGo ==True and car.canGoOnRoad == False:#shi不是要转弯？
                        if car.priority==1:
                            return car
                        else:
                            if tempCar==False:
                                tempCar=car
            rowIndex-=1
        return tempCar


    def __str__(self):
        return str(self.fromCrossId)+">"+str(self.toCrossId) + "---id:"+ str(self.id)+ '\n' +  'isD' + str(self.isDuplex)

