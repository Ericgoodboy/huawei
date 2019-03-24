# huawei
        flagOY
        for(/* 按时间片处理 */) {
                    while(/* all car in road run into end state */){
                        foreach(roads) {
                            /* 调整所有道路上在道路上的车辆，让道路上车辆前进，只要不出路口且可以到达终止状态的车辆
                             * 分别标记出来等待的车辆（要出路口的车辆，或者因为要出路口的车辆阻挡而不能前进的车辆）
                             * 和终止状态的车辆（在该车道内可以经过这一次调度可以行驶其最大可行驶距离的车辆）*/
                            driveAllCarJustOnRoadToEndState(allChannle);/* 对所有车道进行调整 */
        
                            /* driveAllCarJustOnRoadToEndState该处理内的算法与性能自行考虑 */
                        }
                    }
                    
                    while(/* all car in road run into end state */){
                        /* driveAllWaitCar() */
                        foreach(crosses){
                            foreach(roads){
                    while(/* wait car on the road */){
                        Direction dir = getDirection();
                        Car car = getCarFromRoad(road, dir);
                        if (conflict){
                            break;
                        }
        
                        channle = car.getChannel();
                        car.moveToNextRoad();
        
                        /* driveAllCarJustOnRoadToEndState该处理内的算法与性能自行考虑 */
                        driveAllCarJustOnRoadToEndState(channel);
                    }
                    }
                        }
                    }
        
                    /* 车库中的车辆上路行驶 */
                    driveCarInGarage();
                }
           
        

