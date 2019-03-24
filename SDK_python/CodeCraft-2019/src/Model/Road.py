import numpy
class Road():
    NOCAR="none"
    TYPE="Road"
    def __init__(self,id,length,speed,channel,fromCrossId,toCrossId,isDuplex,pool):
        self.id=id
        self.length=length
        self.speed=speed
        self.fromCrossId=fromCrossId
        self.channel=channel
        self.toCrossID=toCrossId
        self.isDuplex=isDuplex
        self.places=numpy.zeros((channel,length),dtype="int32")
        self.__link(pool)
    def __link(self,pool):
        start=pool[0].id
        neg=self.fromCrossId-start
        self.fromCross=pool[neg]
        pool[neg].link(self)
        neg = self.toCrossID - start
        self.toCross = pool[neg]
        pool[neg].link(self)
        pass

    def __inComeCar(self):
        pass
    def __testClear(self,start,end):#参数是起末位置
        temp=start
        if end >= self.__length:
            return False
        while(temp<=end):
            if(self.__places[temp] is not NOCAR):
                return False
        return True
    def comeInCar(self,car):
        pass
    def __str__(self):
        return str(self.fromCrossId)+">"+str(self.toCrossID)