from huaweiUtil import loadData
from Model import Car,Cross,Road

def loadMap(crossPath,roadPath):
    crossPool=loadCrossPool(crossPath)
    roadPool=loadRoadPool(roadPath,crossPool)
    return (crossPool,roadPool)

def loadCrossPool(crossPath):
    datas=loadData.loadData(crossPath)
    crossPool=[]

    for data in datas:
        cross=Cross.Cross(data[0],data[1],data[2],data[3],data[4])
        crossPool.append(cross)
        #(self,id,nRoadId,eRoadId,sRoadId,wRoadId)
    return crossPool

def loadRoadPool(roadPath,crossPool):
    datas=loadData.loadData(roadPath)
    roadPool=[]
    print(datas)
    for d in datas:
        road=Road.Road(d[0],d[1],d[2],d[3],d[4],d[5],d[6],crossPool)
        roadPool.append(road)
    return roadPool

def loadCar(carPath):

    pass

crossPool,roadPool = loadMap("../1-map-training-1/cross.txt","../1-map-training-1/road.txt")
print(crossPool[0].nRoad)
for i in range(32):
    print("\n:crossPool[{0}]".format(i)+str(crossPool[i]))
    print(roadPool[i])


import turtle
def draw(cross):

    if cross.flag==1:
        return
    turtle.pencolor("black")
    turtle.write(str(cross.id)+"")
    if cross.eRoadId != -1:
        if cross.eRoad.isDuplex:
            turtle.pencolor("green")
        else: turtle.pencolor("red")
        turtle.right(90)
        turtle.fd(20)
        turtle.right(90)
        turtle.penup()
        turtle.fd(7)
        turtle.left(90)
        turtle.pendown()
        if cross.eRoad.isDuplex:
            turtle.write("><")
        else:
            if cross.eRoad.fromCrossId== cross.id:
                turtle.write(">")
            else:turtle.write("<")
        turtle.penup()
        turtle.left(90)
        turtle.fd(7)
        turtle.right(90)
        turtle.pendown()
        turtle.fd(30)
        turtle.left(90)
        if cross.eRoad.fromCrossId==cross.id:
            turtle.dot()
            draw(cross.eRoad.toCross)
        else:
            turtle.dot()
            draw(cross.eRoad.fromCross)
        turtle.penup()
        turtle.left(90)
        turtle.fd(50)
        turtle.right(90)
        turtle.pendown()
    if cross.nRoadId != -1:
        if cross.nRoad.isDuplex:
            turtle.pencolor("green")
        else: turtle.pencolor("red")
        turtle.fd(25)
        turtle.write(str(cross.nRoad))
        turtle.fd(25)
        if cross.nRoad.fromCrossId==cross.id:
            turtle.dot()
            draw(cross.nRoad.toCross)
        else:
            turtle.dot()
            draw(cross.nRoad.fromCross)
        turtle.penup()
        turtle.backward(50)
        turtle.pendown()
    cross.flag=1
turtle.penup()
turtle.goto(-200,-200)
turtle.pendown()
turtle.left(90)
turtle.speed(0)

draw(crossPool[0])
import time
time.sleep(1000)




