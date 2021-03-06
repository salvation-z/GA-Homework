import math

def get_x(a):
    return a[1]
def get_y(a):
    return a[2]

def distance(a,b):
    dis=math.sqrt((a[1]-b[1])*(a[1]-b[1])+(a[2]-b[2])*(a[2]-b[2]))
    return dis

def KD_find_near(kd,point,layer):
    if(len(kd)==0):
        return 2147483647,(0,0,0,0)
    current_point=kd[0]
    if((layer%2)==0):
        if(point[1]<current_point[1]):
            num,near_point=KD_find_near(kd[1],point,layer+1)
        else:
            num,near_point=KD_find_near(kd[2],point,layer+1)
    else:
        if(point[2]<current_point[2]):
            num,near_point=KD_find_near(kd[1],point,layer+1)
        else:
            num,near_point=KD_find_near(kd[2],point,layer+1)      
    
    if((current_point[0]!=point[0])and(distance(current_point,point)<num)):
        num=min(distance(current_point,point),num)
        near_point=current_point
    return num,near_point

#file format
#1st line :turning_rate sample_rate minus_distance
#2-n line :x1 y1 t1 x2 y2 t2 ...
#each line is a path generated by dubins_sample

file_point=open('point_list.dat','r')
file_content=file_point.readlines()
lines=0
point_list=[]
for i in file_content:
    lines+=1
    if(lines==1):
        line=i.split()
        turning_rate=float(line[0])
        sample_rate=float(line[1])
        min_distance=float(line[2])
        continue
    line=i.split()
    num=0
    while(num<len(line)):
        point=(lines-1,float(line[num]),float(line[num+1]),float(line[num+2]))
        num+=3
        point_list.append(point)

#for i in point_list:
#    print(i)
file_point.close()

#KD
kd_tree=[]
def KD(layer,points,father):
    current=[]
    n=len(points)
    if(n==0):
        father.append(current)
        return
    if(n==1):
        current.append(points[0])
        current.append([])
        current.append([])
        father.append(current)
        return
    if((layer%2)==0):
        points.sort(key=get_x)
    else:
        points.sort(key=get_y)
    current_point=points[int(n/2)]
    current.append(current_point)
    left_points=points[:int(n/2)]
    right_points=points[1+int(n/2):]
    KD(layer+1,left_points,current)
    KD(layer+1,right_points,current)
    father.append(current)
    
KD(0,point_list,kd_tree)
file_out=open('collision.dat','w')
for i in point_list:
    dis,point=KD_find_near(kd_tree[0],i,0)
    if((dis<min_distance)and(abs(point[3]-i[3])<sample_rate)):
        #print(i,point,dis)
        file_out.write(str(i))
        file_out.write(' ')
        file_out.write(str(i))
        file_out.write(' ')
        file_out.write(str(dis))
        file_out.write('\n')

file_out.close()
#print('done!')