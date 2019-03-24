import numpy as np
def dijkstra(graph, src):
    # 判断图是否为空，如果为空直接退出
    if graph is None:
        return None
    nodes = [i for i in range(len(graph))]  # 获取图中所有节点
    visited=[]  # 表示已经路由到最短路径的节点集合
    if src in nodes:
        visited.append(src)
        nodes.remove(src)
    else:
        return None
    distance = {src: 0}  # 记录源节点到各个节点的距离
    for i in nodes:
        distance[i] = graph[src][i]  # 初始化
    path = {src: []}  # 记录源节点到每个节点的路径
    k = pre = src
    while nodes:
        mid_distance = a.max()*a.shape[0]*(a.shape[1]-1)
        for v in visited:
            for d in nodes:
                new_distance = distance[v] + graph[v][d]
                if new_distance < mid_distance:
                    mid_distance = new_distance
                    k = d
                    pre = v
        distance[k] = mid_distance  # 最短路径
        path[k] = [i for i in path[pre]]
        path[k].append(k)

        visited.append(k)
        nodes.remove(k)
    return distance, path
def score(crossPool,carPool,roadPool):
    countEndedCar=0
    while countEndedCar>=len(carPool):
        pass



if __name__ == "__main__":
    import random
    a=[[random.randint(0,100) for i in range(64)] for i in range(64)]
    for i in range(64):
        a[i][i]=0
    a=np.array(a,dtype="int32")
    dis, path = dijkstra(a,0)
#sys.path.extend(['F:\\2019\\learn_python', 'F:\\2019\\learn_python\\huawei\\SDK_python\\CodeCraft-2019\\src\\huaweiUtil', 'F:/2019/learn_python'])
