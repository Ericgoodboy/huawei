class Car(object):
    def __init__(self,id,fromCrossId,toCrossId,speed,planTime,crossPool):
        self.id=id
        self.fromCrossId=fromCrossId
        self.toCrossId=toCrossId
        self.speed=speed
        self.plantTime=planTime
        self.answer=[]
        tag=crossPool[0].id
        neg=fromCrossId-tag
        self.fromCross=crossPool[neg]
        neg=toCrossId-tag
        self.toCross=crossPool[neg]
        self.pos=self.fromCross.pos
    def nextToGo(self):
        pass

    def __str__(self):
        return str(self.id)+":"+str(self.plantTime)