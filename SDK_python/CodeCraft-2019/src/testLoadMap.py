from huaweiUtil import loadData
from Model import Car,Cross,Road

def loadMap(crossPath,roadPath):
    crossPool=loadCrossPool(crossPath)
    roadPool=loadRoadPool(roadPath,crossPool)
    return (crossPool,roadPool)
k={}
def loadCrossPool(crossPath):
    global k
    datas=loadData.loadData(crossPath)
    crossPool=[]

    for data in datas:
        cross=Cross.Cross(data[0],data[1],data[2],data[3],data[4])
        crossPool.append(cross)
        #(self,id,nRoadId,eRoadId,sRoadId,wRoadId)
    crossdict={cross.id:cross for cross in crossPool}
    k=crossdict
    return crossPool
def loadRoadPool(roadPath,crossPool):
    datas=loadData.loadData(roadPath)
    roadPool=[]
    print(datas)
    for d in datas:
        road=Road.Road(d[0],d[1],d[2],d[3],d[4],d[5],d[6],crossPool)
        roadPool.append(road)
    return roadPool

def loadCar(carPath,crossPool):
    datas = loadData.loadData(carPath)
    carPool = []
    print(datas)
    for d in datas:
        road = Car.Car(d[0], d[1], d[2], d[3], d[4],crossPool)
        carPool.append(road)
    return carPool




now_pos=[0,0]
import turtle
def draw(cross):
    print(turtle.position())
    if cross.flag==1:
        return
    #print(turtle.getposition())
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
def draw2(cross):
    if cross.flag==1:
        return
    cross.pos=(now_pos[0],now_pos[1])
    if cross.eRoadId != -1:
        now_pos[0]+=50
        if cross.eRoad.fromCrossId==cross.id:
            draw2(cross.eRoad.toCross)
        else:draw2(cross.eRoad.fromCross)
        now_pos[0]-=50
    if cross.nRoadId != -1:
        now_pos[1]+=50
        if cross.nRoad.fromCrossId==cross.id:
            draw2(cross.nRoad.toCross)
        else:draw2(cross.nRoad.fromCross)
        now_pos[1]-=50
    cross.flag=1


def goto(position):
    pass

def crossP():
    pass
crossPool,roadPool = loadMap("../1-map-training-1/cross.txt","../1-map-training-1/road.txt")


print(crossPool[0].nRoad)
import math,random
# draw2(crossPool[0])
car =loadCar("../1-map-training-1/car.txt",crossPool)
car.sort(key=lambda c:c.plantTime,reverse=False)
for c in car:
    print(c)
# turtle.penup()
# turtle.goto(-200,-200)
# turtle.pendown()
# turtle.left(90)
# turtle.speed(0)


for c in crossPool:
    c.flag=0
# draw(crossPool[0])
# count = 0
# turtle.pencolor("red")
# car[0].fromCross = crossPool[0]
# car[0].toCross = crossPool[63]
# data = car[0].getRoadline(crossPool, 3)
# print(data)
# turtle.penup()
# turtle.goto(-200, -200)
# turtle.pendown()

# turtle.pensize(3)
# for d in data:
#     turtle.goto(d[0]*50-200, d[1]*50-200)
#
# for c in car:
#     if c.plantTime==1:
#         if c.fromCrossId==crossPool[2].id:
#             count+=1
#         turtle.penup()
#         turtle.goto(c.pos[0]-200,c.pos[1]-200)
#         turtle.pendown()
#         turtle.goto(c.toCross.pos[0]-200,c.toCross.pos[1]-200)
#         turtle.penup()
# print(count)
# turtle.mainloop()









