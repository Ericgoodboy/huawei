import numpy
class Road():
    NOCAR="none"
    TYPE="Road"
    def __init__(self,id,length,speed,channel,fromCrossId,toCrossId,isDuplex):
        self.id=id
        self.length=length
        self.speed=speed
        self.fromCrossId=fromCrossId
        self.channel=channel
        self.toCrossId=toCrossId
        self.isDuplex=isDuplex
        self.arg=0
        self.InitCar=[[],[]]#初始化车辆集合 对象这有一个问题
        if isDuplex:#places[0]表示正向，places[1]表示反向
            self.directions=numpy.zeros((2,channel,length),dtype="int32")#from - to
        else:
            self.directions=numpy.zeros((1,channel,length),dtype="int32")#from - tos
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
            if len(self.InitCar[i])==0:
                continue
            if priority:
                car = self.InitCar[i][0]
                while car.priority==1 and car.bestStartTime<=nowTime:
                    isGo=car.runToRoad(carPool,roadPool,crossPool)
                    if isGo:
                        goneCar.update({car.id:car})
                        self.InitCar[i].remove(car)
                    else:
                        break
                    if len(self.InitCar[i])==0:
                        break
                    car=self.InitCar[i][0]
            else:
                car = self.InitCar[i][0]
                while car.bestStartTime<=nowTime:
                    isGo=car.runToRoad(carPool,roadPool,crossPool)
                    if isGo:
                        goneCar.update({car.id:car})
                        self.InitCar[i].remove(car)
                    else:
                        break
                    if len(self.InitCar[i])==0:
                        break
                    car = self.InitCar[i][0]
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

