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

def comsult(carPool,roadPool):
    temp={0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}
    for i in carPool:
        temp[carPool[i].fromPos].append(carPool[i])
    return temp


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
    graph_list=np.zeros((length,length),dtype="float64")
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
                                graph_list[i][j] = (1/road.channel)*road.arg
                        elif previousCross == crosses[map[i]].id and nextCross == crosses[map[j]].id:
                             graph_list[i][j] = (1/road.channel)*road.arg
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
def mySortCar(carPool,crossPool):
    temp={cross:[] for cross in crossPool}
    for car in carPool:
        temp[carPool[car].fromCrossId].append(carPool[car])
    for crossCar in temp:
        temp[crossCar].sort(key=lambda car:(car.direct,len(car.path),-car.speed))
    max=0
    for i in temp:
        #print(len(temp[i]))
        if len(temp[i])>max:
            max=len(temp[i])
    res = []
    for i in range(max):
        for j in temp:
            if len(temp[j]) > 0:
                res.append(temp[j].pop())

    res ={r.id:r for r in res}
    return res

# def splitCar(carArray):
#     temp=[[],[],[],[]]
#     for car in carArray:
#         temp[car.positionFrom-1].append(car)
#     temp2=[]
#     for t in temp:
#         temp2.extend(t)
#     return temp2
def countRoad(carPool,roadPool):
    count={id:0for id in roadPool}
    for car in carPool:
        for roadId in carPool[car].path:
            count[roadId]+=1
    count=[count[i] for i in count]
    return max(count),count.count(0),count
def process(car,roadPool,crossPool):
    from huaweiUtil import alg
    mapp = get_map(crossPool, roadPool)
    map_cross = []
    for cross in crossPool:
        map_cross.append(cross)


    #把图摆正
    alg.calPlace(crossPool[map_cross[0]], crossPool, roadPool, (0, 0))
    testList = [crossPool[c] for c in crossPool]
    testList.sort(key=lambda x: (x.pos[0], x.pos[1]))
    k = 0
    tempStr = ""
    minid=testList[0].id
    for i in testList:
        i.pos=()
    alg.calPlace(crossPool[minid], crossPool, roadPool, (0, 0))
    testList = [crossPool[c] for c in crossPool]
    testList.sort(key=lambda x: (x.pos[0], x.pos[1]))
    # for c in testList:
    #     if c.pos[0] != k:
    #         k = c.pos[0]
    #         tempStr += "\n"
    #     tempStr += str(c.pos)
    # print(tempStr)
    path = {}
    maxPos=testList[-1].pos



    #计算最短路
    for c in range(len(crossPool)):
        path.update({map_cross[c]: alg.dijkstra(mapp, c, crossPool, roadPool)})
    carPool=car
    count = {road: 0 for road in roadPool}  # 记录每条道路使用数量
    global position

    moveTime = {car: 0 for car in carPool}  # 记录每条路径所用时间
    lose = 0
    #添加最短路
    for c in car:
        car[c].addAnswer(path)

    k=0
    #预估方向
    for row in carPool:
        nowPlace = carPool[row].fromCrossId
        for i in carPool[row].path:
            count[i] += 1  # 计数
            # 计算方位
            toCrossId = roadPool[i].fromCrossId if roadPool[i].fromCrossId != nowPlace else roadPool[i].toCrossId
            car[row].direction[crossPool[nowPlace].allRoad.index(i)] += 1
            nowPlace = toCrossId
    for i in carPool:
        carPool[i].addDirection(carPool[i].direction)
        k+=carPool[i].reRoad(roadPool,crossPool)
    print(k)
    del k
    for c in carPool:
        carPool[c].zoning(maxPos, crossPool)
    #分析位置
    carPool=comsult(car, roadPool)
    m=1250
    #mp1 1450
    #
    #1750:4000
    if len(crossPool)<150:
        m=1450
    else:
        m=1750
    for i in carPool:
        print("car:",len(carPool[i]))
    now_time={r:[0.0,m/(1+len(carPool[r])),1] for r in carPool}

    for r in carPool:
        carPool[r].sort(key=lambda x:(-x.speed,len(x.path)))
        for car in carPool[r]:
            car.bestStartTime = max(int(now_time[r][0]), car.plantTime)
            now_time[r][0]+=now_time[r][1]
            # if now_time[r][0]<50:
            #     now_time[r][0]-=now_time[r][1]/2
            # if now_time[r][0]>50 and now_time[r][0]<100:
            #     now_time[r][0] += now_time[r][1]/2
            # now_time[r][2]+=1



def main():
    # if len(sys.argv) != 5:
    #     print("11111111111111")
    #     logging.info('please input args: car_path, road_path, cross_path, answerPath')
    #     exit(1)
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
    car = loadCar(car_path)
    process(car,roadPool,crossPool)
    dumpAnswer(answer_path, car)
# to read input file
# process
# to write output file


if __name__ == "__main__":
    main()
    print(time.time()-start_time)
