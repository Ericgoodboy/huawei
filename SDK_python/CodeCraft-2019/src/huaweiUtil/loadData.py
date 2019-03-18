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
            #Qprint([int(w) for w in case] )
            case=f.readline()
    return data
def hello():
    print("hello I'm loader")