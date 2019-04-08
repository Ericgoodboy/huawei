#判题器相关算法

finishedCar =0
def judge(carPool,roadPool,crossPool):
    tempCrossList=[crossPool[i] for i in crossPool]
    tempCrossList.sort(key=lambda c:c.id)
    crossPool={cross.id:cross for cross in tempCrossList}
    del tempCrossList
    tempRoadList = [roadPool[i] for i in roadPool]
    tempRoadList.sort(key=lambda r:r.id)
    roadPool={road.id:road for road in tempRoadList}
    del tempRoadList
    countCar=len(carPool)
    stamptime=0
    toGoCarPool={}
    carOnRoad={}
    #
    createInitCarList(carPool, roadPool)
    with open("run.log", "w+") as f:
        while True:
            stamptime+=1
            for car in carOnRoad:
                carOnRoad[car].isReadyToGo=True
            driveJustCurrentRoad(carPool,roadPool,crossPool)#道路内车辆标定与驱动
            carOnRoad.update(driveCarInitList(carPool, roadPool, crossPool,stamptime,True))#优先车辆上路
            if driveCarInWaitState(carOnRoad,carPool,roadPool,stamptime,crossPool)!=True:
                return False
            carOnRoad.update(driveCarInitList(carPool,roadPool, crossPool,stamptime,False))  # 所有车辆车辆上路
            print(len(carOnRoad))

            print(stamptime)
            print("len(carOnRoad):", len(carOnRoad))
            if (isFinish(countCar)):
                break

            if stamptime<=50:

                    f.writelines("---------------------time{0} start---------------------------\n".format(stamptime))
                    for c in carOnRoad:
                        f.writelines("car.id:"+str(carOnRoad[c].id)+"\n")
                        f.writelines("carOnRoad[c].nowRoad.id:"+str(carOnRoad[c].nowRoad.id)+"\n")
                        f.writelines(str(carOnRoad[c].nowChannel)+"\n")
                        f.writelines("-------------------------------\n")


def isFinish(countCar):
    print(countCar,finishedCar)
    if finishedCar== countCar:
        return True
    return False
def createInitCarList(carPool,roadPool):
    for carId in carPool:
        car=carPool[carId]
        startRoad= roadPool[car.path[0]]
        if startRoad.fromCrossId == car.fromCrossId:
            startRoad.InitCar[0].append(car)
        else:
            startRoad.InitCar[1].append(car)
    for roadId in roadPool:
        road=roadPool[roadId]
        road.InitCar[0].sort(key=lambda car:(-car.priority,car.bestStartTime,car.id))
        road.InitCar[1].sort(key=lambda car: (-car.priority, car.bestStartTime, car.id))

def driveJustCurrentRoad(carPool,roadPool,crossPool):
    for road in roadPool:
        for dir in roadPool[road].directions:
            for channel in dir:
                length = len(channel)
                index=length-1
                for i in range(length):
                    if channel[index]!=0:
                        car=carPool[channel[index]]
                        #print("--------car:",car.id)
                        car.goOnRoad(crossPool,roadPool,carPool)#待写
                    index-=1
def driveJustCurrentOneRoad(road,carPool,roadPool,crossPool):#整理单车道！！！！！
    for dir in road.directions:
        for channel in dir:
            length = len(channel)
            index=length-1
            for i in range(length):
                if channel[index]!=0:
                    car=carPool[channel[index]]#,crossPool,roadPool,carPool
                    car.goOnRoad(crossPool,roadPool,carPool)#待写
                index -= 1


def driveCarInitList(carPool,roadPool,crossPool,stamptime,priority):
    goneCar={}
    for road in roadPool:
        goneCar.update(roadPool[road].runCarInitList(carPool,roadPool,crossPool,stamptime,priority))
    return goneCar
def driveCarOneInitList(road,carPool,roadPool,crossPool,stamptime,priority,crossId):
    goneCar={}
    goneCar.update(road.runCarInitList(carPool,roadPool,crossPool,stamptime,priority,crossId))
    return goneCar


# def createCarSequence(carPool,roadPool,crossPool):
#     for road in roadPool:
#         roadPool[road].createSequence(carPool,roadPool,crossPool)#待写


def driveCarInWaitState(carOnRoad,carPool,roadPool,stamptime,crossPool):
    global finishedCar
    allCarInEndState = False
    lastProcess=[car for car in carOnRoad]
    while True != allCarInEndState:
        for cross in crossPool:
            roadList = [i for i in crossPool[cross].allRoad]
            roadList.sort()
            for r in roadList:#不优先的到站的车
                if r == -1:
                    continue
                road = roadPool[r]
                car = road.getFirstToGoCar(crossPool[cross],carPool)
                while car != False:
                    if conflict(cross, car , road,carOnRoad,crossPool,roadPool,carPool):
                        break
                    isGo, isGoToPort=moveToNextRoad(car,carOnRoad,cross,crossPool,roadPool)
                    if isGo:
                        if isGoToPort:
                            finishedCar += 1
                        driveJustCurrentOneRoad(road,carPool,roadPool,crossPool)   #上路问题
                        carOnRoad.update(driveCarOneInitList(road,carPool,roadPool,crossPool,stamptime,True,cross))#
                    else: break
                    car = road.getFirstToGoCar(crossPool[cross], carPool)#待重写返回对象
        len(carOnRoad)
        nowProcess = [car for car in carOnRoad if carOnRoad[car].isReadyToGo==True]
        if len(nowProcess)==0:
            allCarInEndState = True
        elif tuple(nowProcess)==tuple(lastProcess):
            roadsss = []
            print("*********************************")
            for i in nowProcess:
                print(carOnRoad[i].nowRoad)
                if carOnRoad[i].nowRoad not in roadsss:
                    roadsss.append(carOnRoad[i].nowRoad)
            print("*********************************")
            for r in roadsss:
                print("----------", r.id, "----------------")
                print(r)
                print("r.speed:", r.speed)
                print(r.directions)
                print("--------------------------")
            print("dead lock")
            exit(0)
        lastProcess=nowProcess


    return True




def moveToNextRoad(car,carOnRoad,cross,crossPool,roadPool):#done carOnRoad,cross,crossPool,roadPool
    return car.moveToNextRoad(carOnRoad,cross,crossPool,roadPool)
def conflict(cross,car,road,carOnRoad,crossPool,roadPool,carPool):#有问题-----------------
    cross = crossPool[cross]
    if car.togoNext ==0:#要比较
        nowIndex = cross.allRoad.index(road.id)
        road1Id = cross.allRoad[nowIndex - 1]
        road2Id = cross.allRoad[nowIndex - 3]
        hasRoad1 = True
        if road1Id == -1:
            hasRoad1 = False
        else:
            road1 = roadPool[road1Id]
            car1 = road1.getFirstToGoCar(cross, carPool)
        hasRoad2 = True
        if road2Id == -1:
            hasRoad2 = False
        else:
            road2 = roadPool[road2Id]
            car2 = road2.getFirstToGoCar(cross, carPool)
        if hasRoad1 and car1 != False and car1.togoNext == 1 and car1.priority > car.priority:
            return True
        if hasRoad2 and car2 != False and car2.togoNext == 3 and car2.priority > car.priority:
            return True
        return False
    if car.togoNext == 2:
        nowIndex = cross.allRoad.index(road.id)
        road1Id = cross.allRoad[nowIndex - 1]
        road2Id = cross.allRoad[nowIndex - 3]
        hasRoad1 = True
        if road1Id == -1:
            hasRoad1 = False
        else:
            road1 = roadPool[road1Id]
            car1 = road1.getFirstToGoCar(cross, carPool)
        hasRoad2 = True
        if road2Id == -1:
            hasRoad2 = False
        else:
            road2 = roadPool[road2Id]
            car2 = road2.getFirstToGoCar(cross, carPool)
        if hasRoad1 and car1 != False and car1.togoNext == 1 and car1.priority > car.priority:
            return True
        if hasRoad2 and car2 != False and car2.togoNext == 3 and car2.priority > car.priority:
            return True
        return False
    if car.togoNext==1:
        nowIndex=cross.allRoad.index(road.id)
        road1Id = cross.allRoad[nowIndex-2]
        road2Id = cross.allRoad[nowIndex-3]
        hasRoad1=True
        if road1Id==-1:
            hasRoad1=False
        else:
            road1 = roadPool[road1Id]
            car1 = road1.getFirstToGoCar(cross, carPool)
        hasRoad2 = True
        if road2Id == -1:
            hasRoad2 = False
        else:
            road2 = roadPool[road2Id]
            car2 = road2.getFirstToGoCar(cross, carPool)
        # 这个记得改
        if hasRoad1 and car1!=False and car1.togoNext==3 and car1.priority >= car.priority:
            return True

        if (hasRoad2 and car2!=False) and (car2.togoNext == 0 or car2.togoNext == 2) and car2.priority >= car.priority:
            return True
        return False
    if car.togoNext==3:
        nowIndex = cross.allRoad.index(road.id)
        road1Id = cross.allRoad[nowIndex - 2]
        road2Id = cross.allRoad[nowIndex - 1]
        hasRoad1=True
        if road1Id == -1:
            hasRoad1 = False
        else:
            road1 = roadPool[road1Id]
            car1 = road1.getFirstToGoCar(cross, carPool)
        hasRoad2 = True
        if road2Id == -1:
            hasRoad2 = False
        else:
            road2 = roadPool[road2Id]
            car2 = road2.getFirstToGoCar(cross, carPool)
        if hasRoad1 and car1 != False and car1.togoNext == 1 and car1.priority > car.priority:
            return True
        if (hasRoad2 and car2 != False) and (car2.togoNext == 0 or car2.togoNext == 2) and car2.priority >= car.priority:
            return True
        return False