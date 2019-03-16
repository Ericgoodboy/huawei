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
            print([int(w) for w in case.split(",")] )
            case=f.readline()
#CodeCraft-2019.py ../config/car.txt ../config/road.txt ../config/cross.txt
#vim
def main():
    if len(sys.argv) != 5:
        print("11111111111111")
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)
    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    loadData(car_path)
    # logging.info("car_path is %s" % (car_path))
    # logging.info("road_path is %s" % (road_path))
    # logging.info("cross_path is %s" % (cross_path))
    # logging.info("answer_path is %s" % (answer_path))

# to read input file
# process
# to write output file


if __name__ == "__main__":
    main()
