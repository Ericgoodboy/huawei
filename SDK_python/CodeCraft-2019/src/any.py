import re
r=re.compile("\D+")
with open("run.log","r") as f:
    all1=[]
    temp=[]
    all1.append(temp)
    for i in f.readlines():
        arr=[int(stt) for stt in r.split(i) if stt != '']
        if len(arr)>5:
            temp.append(arr)
        else:
            temp=[]
            all1.append(temp)
with open("Output.txt","r") as f:
    all2=[]
    temp=[]
    all2.append(temp)
    for i in f.readlines():
        arr=[int(stt) for stt in r.split(i) if stt != '']
        if len(arr)>5:
            temp.append(arr)
        else:
            temp=[]
            all2.append(temp)
#all1.remove(all1[0])
temp1=[]
temp2=[]
for i in range(1,30):
    if len(all1[i])!=len(all2[i]):
        print("i:",i)
    all1[i].sort(key=lambda a:a[0])
    all2[i].sort(key=lambda a:a[0])
    Cross1=[a[2] for a in all1[i]]
    Cross2=[a[2] for a in all2[i]]
    temp1.append({p[0]:p for p in all1[i]})
    temp2.append({p[0]:p for p in all2[i]})
    if tuple(Cross1) != tuple(Cross2):
        print("cross_different:",i)
        print(tuple(Cross1))
        print(tuple(Cross2))
        break
    Cross1 = [a[5] for a in all1[i]]
    Cross2 = [a[5] for a in all2[i]]
    if tuple(Cross1) != tuple(Cross2):
        print("pos_different:", i)
        print(tuple(Cross1))
        print(tuple(Cross2))
        for j in range(len(Cross2)):
            if Cross2[j]!=Cross1[j]:
                print("all1_n:",all1[i][j])
                print("all1_l:",temp1[i-2][all1[i][j][0]])
                print("all2_n:",all2[i][j])
                print("all2_l:",temp2[i-2][all2[i][j][0]])
                break

        break