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
        if isDuplex:
            self.placesA=numpy.zeros((channel,length),dtype="int32")#from - to
            self.placesB=numpy.zeros((channel,length),dtype="int32")#to - from
        else:
            self.placesA=numpy.zeros((channel,length),dtype="int32")#from - tos
    def maxToGo(self,v,start):#获取最大的可走的距离
        temp=None
        if start=="from":
            temp=self.placesA
        else:
            temp=self.placesB

        for i in range(self.channel):
            if self.placesA[i][0] !=0:
                continue
            else:

                pass
    def __str__(self):
        return str(self.fromCrossId)+">"+str(self.toCrossId)