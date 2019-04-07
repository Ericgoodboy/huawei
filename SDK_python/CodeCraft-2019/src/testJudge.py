import time
start_time=time.time()

import logging
import sys

from huaweiUtil import loadData,alg
from Model import Car,Cross,Road
import numpy as np

#np.caonima
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
def loadCar(carPath,answer_path,preset_answer_path):
    datas = loadData.loadData(carPath)
    #answer=[]
    #answer.extend()
    answer = loadData.loadData(preset_answer_path)
    answer.extend(loadData.loadData(answer_path))
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
        if id in carDic:
            carDic[id].bestStartTime=best_time
            carDic[id].path=path
            # print("loadCar,path:",path)
            presetCarPool.update({id:carDic[id]})
            carDic.pop(id)
    return presetCarPool,carDic


car_path="../2-map-training-1/car.txt"
cross_path="../2-map-training-1/cross.txt"
road_path="../2-map-training-1/road.txt"
answer_path="../2-map-training-1/answer.txt"
presetAnswer_path="../2-map-training-1/presetAnswer.txt"
# car_path="../2-training-training-1-answer/car.txt"
# cross_path="../2-training-training-1-answer/cross.txt"
# road_path="../2-training-training-1-answer/road.txt"
# answer_path="../2-training-training-1-answer/answer.txt"
# presetAnswer_path="../2-training-training-1-answer/presetAnswer.txt"
crossPool, roadPool = loadMap(cross_path, road_path)
presetCarPool, carPool = loadCar(car_path, answer_path,presetAnswer_path)
assert len(carPool)==0
from huaweiUtil import JudgeApp
JudgeApp.judge(presetCarPool,roadPool,crossPool)
