import logging
import sys
logging.basicConfig(level=logging.DEBUG,
                    filename='../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')
def loadData(path):
    print("loading data:",path)
    data=[]
    with open(path,"r") as f:
        case=f.readline()
        case=f.readline()
        i=1
        while case:
            case=case.strip().strip(")").lstrip("(").split(",")
            data.append([int(w) for w in case])
            #print([int(w) for w in case] )
            case=f.readline()
    return data
#CodeCraft-2019.py ../config/car.txt ../config/road.txt ../config/cross.txt
#vim
def main():
    # if len(sys.argv) != 5:
    #     print("11111111111111")
    #     logging.info('please input args: car_path, road_path, cross_path, answerPath')
    #     exit(1)
    road_path = sys.argv[1]
    cross_path = sys.argv[2]
    roads=loadData(road_path)
    cross=loadData(cross_path)
    import turtle
    for c in roads:
        print(c)


# to read input file
# process
# to write output file


if __name__ == "__main__":
    main()
