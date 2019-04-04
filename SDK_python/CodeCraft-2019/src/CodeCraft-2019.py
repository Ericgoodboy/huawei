import time
start_time=time.time()

import logging
import sys

from huaweiUtil import loadData,alg
from Model import Car,Cross,Road
import numpy as np

logging.basicConfig(level=logging.DEBUG,
                    filename='../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')

#载入四联
def loadMap(crossPath,roadPath):
    crossPool=loadCrossPool(crossPath)
    roadPool=loadRoadPool(roadPath)
    return (crossPool,roadPool)
def loadCrossPool(crossPath):
    datas=loadData.loadData(crossPath)
    crossPool=[]
    for data in datas:
        cross=Cross.Cross(data[0],data[1],data[2],data[3],data[4])
        crossPool.append(cross)
    crossdict={cross.id:cross for cross in crossPool}
    return crossdict
def loadRoadPool(roadPath):
    datas=loadData.loadData(roadPath)
    roadPool=[]
    for d in datas:
        road=Road.Road(d[0],d[1],d[2],d[3],d[4],d[5],d[6])
        roadPool.append(road)
    roadDic={road.id:road for road in roadPool}
    return roadDic
def loadCar(carPath,preset_answer_path):
    datas = loadData.loadData(carPath)
    answer = loadData.loadData(preset_answer_path)
    carPool = []
    for d in datas:
        car = Car.Car(d[0], d[1], d[2], d[3], d[4], d[5], d[6])
        carPool.append(car)
    #carPool.sort(key=lambda car: (car.fromCrossId, car.plantTime))
    carDic={car.id : car for car in carPool}
    presetCarPool={}
    for a in answer:
        id = a[0]
        best_time=a[1]
        path=a[2:]
        carDic[id].bestStartTime=best_time
        carDic[id].path=path
        print("loadCar,path:",path)
        presetCarPool.update({id:carDic[id]})
        carDic.pop(id)
    return presetCarPool,carDic


# 生成地图
def get_map(crosses, roads):
    length = len(crosses)
    graph_list=np.zeros((length,length),dtype="int32")
    graph_list[:]=9999
    map=[]
    for cross in crosses:
        map.append(cross)
    for i in range(len(crosses)):
        for j in range(len(crosses)):
            if i == j:
                graph_list[i][j] = 0
            else:
                for k in crosses[map[i]].allRoad:
                    if k is not -1:
                        road=roads[k]
                        previousCross = road.fromCrossId
                        nextCross = road.toCrossId
                        if road.isDuplex == 1:
                            if sorted([previousCross,nextCross]) == sorted([crosses[map[i]].id,crosses[map[j]].id]):
                                graph_list[i][j] = (1 / road.channel) + 1
                        elif previousCross == crosses[map[i]].id and nextCross == crosses[map[j]].id:
                             graph_list[i][j] = (1 / road.channel) + 1
                        else:
                            pass
    return graph_list

#得出答案
def dumpAnswer(path,cars):
    with open(path,"w") as f:
        for car in cars:
            tempStr=str(cars[car].id)+" ,"+str(cars[car].bestStartTime)+" ,"+" ,".join([str(i) for i in cars[car].path])
            tempStr="("+tempStr+")\r"
            f.writelines(tempStr)

def process(presetCarPool,car,roadPool,crossPool):
    mapp = get_map(crossPool, roadPool)
    map_cross = []
    for cross in crossPool:
        map_cross.append(cross)

    path = {}
    # 把图摆正
    alg.calPlace(crossPool[map_cross[0]], crossPool, roadPool, (0, 0))
    testList = [crossPool[c] for c in crossPool]
    testList.sort(key=lambda x: (x.pos[0], x.pos[1]))
    minid = testList[0].id
    for i in testList:
        i.pos = ()
    alg.calPlace(crossPool[minid], crossPool, roadPool, (0, 0))
    testList = [crossPool[c] for c in crossPool]
    testList.sort(key=lambda x: (x.pos[0], x.pos[1]))
    maxPos = testList[-1].pos

    for c in range(len(crossPool)):
        path.update({map_cross[c]: alg.dijkstra(mapp, c, crossPool, roadPool)})
    carPool=car
    # count = {road: 0 for road in roadPool}  # 记录每条道路使用数量

    for c in carPool:
        carPool[c].addAnswer(path)
        print("processing path:",carPool[c].path)


    for row in carPool:
        nowPlace=carPool[row].fromCrossId
        for i in carPool[row].path:
            # count[i] += 1  # 计数
            # 计算方位
            toCrossId=roadPool[i].fromCrossId if roadPool[i].fromCrossId!=nowPlace else roadPool[i].toCrossId
            car[row].direction[crossPool[nowPlace].allRoad.index(i)] += 1
            nowPlace=toCrossId

    for i in carPool:
        # carPool[i].zoning(maxPos,crossPool)
        # carPool[i].addMaxRoadId(carPool[i].path, count)
        carPool[i].addDirection(carPool[i].direction)
        carPool[i].reRoad(roadPool,crossPool)
    cartemp=[car[i] for i in car]
    cartemp.sort(key=lambda car:(car.fromCrossId,len(car.path),-car.speed))
    car={i.id:i for i in cartemp}

    # #方位法
    # flagPool = [1,1,1,1]
    # nowTimePool = [0,0,0,0]
    # betweenTime = [30,30,30,30]
    # sendCar = [10,10,10,10]
    #
    # for c in car:
    #     num = car[c].fromPos - 1
    #     car[c].bestStartTime = max(int(nowTimePool[num]), car[c].plantTime)
    #     nowTimePool[num] += 1 if flagPool[num] % sendCar[num] == 0 else 0
    #     flagPool[num] += 1
    flag = 1

    nowTime = 800
    for c in car:
        car[c].bestStartTime = nowTime
        nowTime += 1 if flag % 10 == 0 else 0
        flag += 1



def main():
    if len(sys.argv) != 6:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    preset_answer_path = sys.argv[4]
    answer_path = sys.argv[5]

    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("preset_answer_path is %s" % (preset_answer_path))
    logging.info("answer_path is %s" % (answer_path))

    crossPool, roadPool = loadMap(cross_path, road_path)
    presetCarPool, carPool= loadCar(car_path,preset_answer_path)

    process(presetCarPool, carPool, roadPool, crossPool)
    carPool.update(presetCarPool)
    dumpAnswer(answer_path, carPool)
# to read input carPool
# process
# to write output file


if __name__ == "__main__":
    main()
    end_time = time.time()
    print(end_time - start_time)