import time
start_time=time.time()
import logging
import sys
logging.basicConfig(level=logging.DEBUG,
                    filename='../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')
from huaweiUtil import loadData
from Model import Car,Cross,Road
import numpy as np




def loadMap(crossPath,roadPath):
    crossPool=loadCrossPool(crossPath)
    roadPool=loadRoadPool(roadPath)
    return (crossPool,roadPool)

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
    return crossdict
def loadRoadPool(roadPath):
    datas=loadData.loadData(roadPath)
    roadPool=[]
    for d in datas:
        road=Road.Road(d[0],d[1],d[2],d[3],d[4],d[5],d[6])
        roadPool.append(road)
    roadDic={road.id:road for road in roadPool}
    return roadDic

def loadCar(carPath):
    datas = loadData.loadData(carPath)
    carPool = []
    for d in datas:
        road = Car.Car(d[0], d[1], d[2], d[3], d[4])
        carPool.append(road)
    #carPool.sort(key=lambda car: (car.fromCrossId, car.plantTime))
    carDic={car.id : car for car in carPool}
    return carDic


def graph(crossPool,roadPool):
    length=len(crossPool)
    max=-1
    tgraph=np.zeros((length,length))
    map=[]
    for i in range(length):
        for j in range(length):
            if crossPool[i].nRoadId != -1:
                pass
    pass


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
                                graph_list[i][j] = (road.length/road.speed)*road.arg
                        elif previousCross == crosses[map[i]].id and nextCross == crosses[map[j]].id:
                             graph_list[i][j] = (road.length/road.speed)*road.arg
                        else:
                            pass
    return graph_list




def draw2(cross,crossPool,roadPool):
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



def dumpAnswer(path,cars):
    with open(path,"w") as f:
        for car in cars:
            tempStr=str(cars[car].id)+" ,"+str(cars[car].bestStartTime)+" ,"+" ,".join([str(i) for i in cars[car].path])
            tempStr="("+tempStr+")\r"
            f.writelines(tempStr)
def process(car,roadPool,crossPool):
    from huaweiUtil import alg
    mapp = get_map(crossPool, roadPool)
    map_cross = []
    for cross in crossPool:
        map_cross.append(cross)

    path = {}
    #
    for c in range(len(crossPool)):
        path.update({map_cross[c]: alg.dijkstra(mapp, c, crossPool, roadPool)})
    carPool=car
    count = {road: 0 for road in roadPool}  # 记录每条道路使用数量
    global position

    moveTime = {car: 0 for car in carPool}  # 记录每条路径所用时间
    lose = 0

    for c in car:
        car[c].addAnswer(path)

    for row in carPool:
        nowPlace=carPool[row].fromCrossId
        for i in carPool[row].path:
            # 判断时间
            length = roadPool[i].length
            limitSpeed = roadPool[i].speed
            carSpeed = carPool[row].speed
            actualSpeed = min(limitSpeed, carSpeed)
            # planTime到实际调用的时间差
            plantTime = carPool[row].plantTime
            realTime = carPool[row].bestStartTime
            gapTime = realTime - plantTime
            # 时间差完成
            if i != 2:
                if lose > actualSpeed:
                    lose = 0
                    moveTime[row] += 1
                else:
                    lose -= actualSpeed
                    moveTime[row] += 1
            lose = (lose + length) % actualSpeed
            moveTime[row] += (lose + length) // actualSpeed
            # moveTime[carId] += gapTime
            # 判断时间完成
            count[i] += 1  # 计数
            # 计算方位
            toCrossId=roadPool[i].fromCrossId if roadPool[i].fromCrossId!=nowPlace else roadPool[i].toCrossId
            car[row].direction[crossPool[nowPlace].allRoad.index(i)] += 1
            nowPlace=toCrossId
    k=1
    for i in carPool:
        carPool[i].addDirection(carPool[i].direction)
        k+=carPool[i].reRoad(roadPool,crossPool)
    print(k)
    del k
    cartemp=[car[i] for i in car]
    import math
    cartemp.sort(key=lambda car:(car.fromCrossId,len(car.path),-car.speed))
    now_time = 0
    flag = 1
    k=9
    car={i.id:i for i in cartemp}


    for c in car:
        # roadLength = 0
        #         # minSpeed = 1000
        # if car[c].direction==0:
        #     continue
        car[c].bestStartTime = max(int(now_time), car[c].plantTime)
        #if car[c].direction !=0:
        now_time += 1 if flag %25==0 else 0

        flag +=1
         # 计算方位完成
    #now_time+300

    # for c in car:
    #     if car[c].direction==0:
    #         car[c].bestStartTime = max(int(now_time), car[c].plantTime)
def main():
    # if len(sys.argv) != 5:
    #     print("11111111111111")
    #     logging.info('please input args: car_path, road_path, cross_path, answerPath')
    #     exit(1)
    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]
    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("answer_path is %s" % (answer_path))
    crossPool, roadPool = loadMap(cross_path, road_path)
    car = loadCar(car_path)
    process(car,roadPool,crossPool)
    dumpAnswer(answer_path, car)
# to read input file
# process
# to write output file


if __name__ == "__main__":
    main()
    print(time.time()-start_time)
