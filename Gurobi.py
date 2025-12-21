# -*- coding: utf-8 -*-
"""
Created on Sat Nov 29 14:18:55 2025

@author: Pc
"""
import math
import gurobipy as gp
from gurobipy import GRB
cus_no = 200
sat_no = 10
cte_no = 10
vehicle_capacity = 600
hub_no = sat_no + cte_no
x = []
y = []
flow = []
capacity = []
fixed_cost = []
satellite1 = [31,49,54,79,80,120,142,146,155,178]
center = [21,47,48,53,77,110,114,131,140,143]
hubs = satellite1 + center
link = []
allclient = []
allnode = []
allhub = []
allsatellite = []
allcenter = []
for i in range(0,cus_no):
    middle = []
    flow.append(middle)
for i in range(0,hub_no):
    middle = []
    middle.extend([0] * hub_no)
    middle[i] = 1
    link.append(middle)
with open(r"D:\以前的文件\MAHLRP-SCI\200.txt", "r", encoding="utf-8") as f:
    line_num = 0
    for line in f:
        if line_num == 0:
            line_num = line_num + 1
            continue
        elif line_num <= cus_no:        
            parts = line.strip().split()
            row = [float(num_str) for num_str in parts]  
            x.append(row[0])
            y.append(row[1])
            line_num = line_num + 1
        elif line_num<=2*cus_no:
            parts = line.strip().split()
            row = [float(num_str) for num_str in parts]  
            if line_num - cus_no -1 !=1148:
                for i in range(0,cus_no):
                    flow[line_num-cus_no-1].append(row[i])
            else:
                for i in range(0,cus_no):
                    flow[line_num-cus_no-1].append(row[i]-0.55)
            line_num = line_num + 1
with open(r"D:\以前的文件\MAHLRP-SCI\CapL10.txt", "r", encoding="utf-8") as f:
    for line in f:
        capacity.append(float(line))
with open(r"D:\以前的文件\MAHLRP-SCI\FixT10.txt", "r", encoding="utf-8") as f:
    for line in f:
        fixed_cost.append(float(line))
hebing = satellite1 + center
hebing_shunxu = hebing.copy()
hebing_shunxu.sort()
deduplicated_list = list(dict.fromkeys(hebing_shunxu))
hebing_shunxu.clear()
hebing_shunxu.extend(deduplicated_list)
aa = []
bb = []
with open(r"D:\以前的文件\MAHLRP-SCI\link10-200.txt", "r", encoding="utf-8") as f:
    content = f.readlines()
    for k in range(0,hub_no):
        xuhao = hebing_shunxu.index(hebing[k])
        parts = content[xuhao].strip().split()
        row = [int(num_str) for num_str in parts]
        for l in row:
            if l in satellite1:
                link[k][satellite1.index(l)] = 1
            if l in center:
                link[k][center.index(l)+sat_no] = 1


# 父类 Node：对应Java的Node类
class Node:
    def __init__(self, ident: int, zuobiao_x: float, zuobiao_y: float):
        # 定义实例属性，对应Java的成员变量
        self.id = ident
        self.x = zuobiao_x
        self.y = zuobiao_y

    # 对应Java的distanceto方法，计算到另一个Node的距离并取整
    def distanceto(self, c: 'Node') -> int:
        # 计算欧几里得距离，Math.pow替换为Python的**幂运算符
        distance = math.sqrt((self.x - c.x) ** 2 + (self.y - c.y) ** 2)
        # 转换为整数，与Java的(int)强制转换一致
        return int(distance)

# 子类 Client：继承自Node，对应Java的Client类
class Client(Node):
    def __init__(self, ident: int, zuobiao_x: float, zuobiao_y: float,
                 client_id: int, demand: list[float], total_demand: float,
                 pickup_demand: float, delivery_demand: float):
        # 调用父类的构造方法，初始化父类的属性
        super().__init__(ident, zuobiao_x, zuobiao_y)
        # 定义Client独有的实例属性
        self.client_id = client_id
        self.demand = demand  # Java的double[]替换为Python的float列表
        self.total_demand = total_demand
        self.pickup_demand = pickup_demand
        self.delivery_demand = delivery_demand

# 子类 Hub：继承自Node，对应Java的Hub类
class Hub(Node):
    def __init__(self, ident: int, zuobiao_x: float, zuobiao_y: float,
                 satellite_id: int, hub_id: int, fixed_cost: float,
                 capacity: float, link: list[int], link_fixed: list[int]):
        # 调用父类的构造方法
        super().__init__(ident, zuobiao_x, zuobiao_y)
        # 定义Hub独有的实例属性
        self.satellite_id = satellite_id
        self.hub_id = hub_id
        self.fixed_cost = fixed_cost
        self.capacity = capacity
        self.link = link  # Java的int[]替换为Python的int列表
        self.link_fixed = link_fixed  # Java的int[]替换为Python的int列表
        self.sat_or_ctr = None  # 1=satellite 0=center，初始化为None，后续赋值

for i in range(0, cus_no):
    cus_x = x[i]
    cus_y = y[i]
    total = 0;
    pickup = 0;
    delivery = 0;
    demand = [];
    for j in range(0, cus_no):
        if j!=i:
            demand.append(flow[i][j])
            pickup = pickup + flow[i][j]
            delivery = delivery + flow[j][i]
            total = total + demand[j] + flow[j][i];    
        else:
            demand.append(0)
    client = Client(i,cus_x,cus_y,i,demand,total,pickup,delivery);
    print(i, pickup, delivery)
    allclient.append(client)
    allnode.append(client)

for k in range(0, sat_no):
    hx = x[satellite1[k]-1]
    hy = y[satellite1[k]-1]
    link_fixed = []
    link_fixed.extend([10000] * hub_no)
    satellite = Hub(k + cus_no,hx,hy,k,k,fixed_cost[k],capacity[k],link[k],link_fixed)
    allsatellite.append(satellite)
    allhub.append(satellite)
    allnode.append(satellite)

for k in range(0, cte_no):
    hx = x[center[k]-1]
    hy = y[center[k]-1]
    link_fixed = []
    link_fixed.extend([10000] * hub_no)
    currentcenter = Hub(k + cus_no + sat_no,hx,hy,k,k + sat_no,fixed_cost[k],capacity[k],link[k+cte_no],link_fixed);
    allcenter.append(currentcenter)
    allhub.append(currentcenter)
    allnode.append(currentcenter)

satelite2 = {4,5,6,9};
center2 = {6,9};
ttcost = 0;
for i in satelite2:
	ttcost += allsatellite[i-1].fixed_cost;
for i in center2:
	ttcost += allcenter[i-1].fixed_cost;
print(ttcost)

model = gp.Model("MultiDepotColdChainOptimization")
x = model.addVars(cus_no+sat_no,cus_no+sat_no,vtype=GRB.BINARY, name="x")
z = model.addVars(cus_no,sat_no,vtype=GRB.BINARY, name="z")
g = model.addVars(sat_no,cte_no,vtype=GRB.BINARY, name="g")
b = model.addVars(sat_no+cte_no,vtype=GRB.BINARY, name="b")
f = model.addVars(cus_no,sat_no+cte_no,sat_no+cte_no,lb=0, name="f")
h = model.addVars(cus_no,sat_no+cte_no,sat_no+cte_no,lb=0, name="h")
y = model.addVars(sat_no+cte_no,sat_no+cte_no,vtype=GRB.BINARY, name="b")
u = model.addVars(cus_no+sat_no,lb=0, name="u")
v = model.addVars(cus_no+sat_no,lb=0, name="v")
a = model.addVars(cus_no,sat_no,cte_no,vtype=GRB.BINARY, name="a")
model.addConstrs(
    (gp.quicksum(a[i,k,l] for l in range(0,cte_no)) == z[i,k] for i in range(0, cus_no) for k in range(0, sat_no))
)
model.addConstrs(
    (a[i,k,l] <= g[k,l] for i in range(0, cus_no) for k in range(0, sat_no) for l in range(0,cte_no))
)

route_cost_component = gp.quicksum(x[i,j] * allnode[i].distanceto(allnode[j]) for i in range(0,cus_no+sat_no) for j in range(0,cus_no+sat_no))
backbone_cost_component = (
    gp.quicksum(f[i,k,l] * 0.002 * allhub[k].distanceto(allhub[l]) for k in range(0,sat_no+cte_no) for l in range(0,sat_no+cte_no) for i in range(0, cus_no)) +
    gp.quicksum(h[i,k,l] * 0.002 * allhub[k].distanceto(allhub[l]) for k in range(0,sat_no+cte_no) for l in range(0,sat_no+cte_no) for i in range(0, cus_no)) 
)
fixed_hub_cost_component = gp.quicksum(b[k] * allhub[k].fixed_cost for k in range(0,sat_no+cte_no))
fixed_vehicle_cost_component = gp.quicksum(x[cus_no+k,j] * 3000 for k in range(0,sat_no) for j in range(0,cus_no+sat_no))
fixed_link_cost_component = gp.quicksum(y[k,l] * 10000 for k in range(0,sat_no+cte_no) for l in range(0,sat_no+cte_no))
model.setObjective(route_cost_component + backbone_cost_component + fixed_hub_cost_component + fixed_vehicle_cost_component + fixed_link_cost_component, GRB.MINIMIZE)

#Constraint 1 Single allocation between clients and satellite hubs
model.addConstrs(
    (gp.quicksum(z[i,k] for k in range(0,sat_no)) == 1 for i in range(0, cus_no))
)

#Constraint 2 Single allocation between satellite hubs and center hubs
model.addConstrs(
    (gp.quicksum(g[k,l] for l in range(0,cte_no)) == b[k] for k in range(0, sat_no))
)

for k in range(0, sat_no):
    print(allsatellite[k].capacity)
#Constraint 3 Capacity constraints for satellite hubs
model.addConstrs(
    (gp.quicksum(z[i,k]*allclient[i].total_demand for i in range(0,cus_no)) <= allsatellite[k].capacity*b[k] for k in range(0, sat_no))
)

#Constraint 4 Capacity constraints for center hubs
model.addConstrs(
    (gp.quicksum(a[i,k,l]*allclient[i].pickup_demand for i in range(0,cus_no) for k in range(0,sat_no)) <= allcenter[l].capacity*b[l+sat_no] for l in range(0, cte_no))
)

#Constraint 5 Flow conservation at satellite hubs
model.addConstrs(
    (gp.quicksum(f[i,m,k]-f[i,k,m] for m in range(0,sat_no+cte_no) if m!=k) == -z[i,k]*allclient[i].pickup_demand for i in range(0, cus_no) for k in range(0, sat_no))
)
model.addConstrs(
    (gp.quicksum(h[i,m,k]-h[i,k,m] for m in range(0,sat_no+cte_no)) == gp.quicksum(z[j,k]*allclient[i].demand[j] for j in range(0, cus_no)) for i in range(0, cus_no) for k in range(0, sat_no))
)

#Constraint 6 Flow conservation at center hubs
model.addConstrs(
    (gp.quicksum(f[i,m,l+sat_no]-f[i,l+sat_no,m] for m in range(0,sat_no+cte_no) if m!=l+sat_no) == gp.quicksum(a[i,k,l]*allclient[i].pickup_demand for k in range(0, sat_no)) for i in range(0, cus_no) for l in range(0, cte_no))
)
model.addConstrs(
    (gp.quicksum(h[i,m,l+sat_no]-h[i,l+sat_no,m] for m in range(0,sat_no+cte_no)) == -gp.quicksum(a[i,k,l]*allclient[i].pickup_demand for k in range(0, sat_no)) for i in range(0, cus_no) for l in range(0, cte_no))
)

#Constraint 7 Flows can be transferred only via established links
model.addConstrs(
    (gp.quicksum(f[i,m,n]+h[i,m,n] for i in range(0,cus_no)) <= 1000000*y[m,n] for m in range(0,sat_no+cte_no) for n in range(0,sat_no+cte_no))
)

#Constraint 8 Connectivity constraint
model.addConstrs(
    (y[m,n] <= allhub[m].link[n] for m in range(0,sat_no+cte_no) for n in range(0,sat_no+cte_no))
)

#Constraint 9 Each client should be visited once
model.addConstrs(
    (gp.quicksum(x[i,j] for j in range(0,cus_no+sat_no) if j!=i) == 1 for i in range(0,cus_no))
)

#Constraint 10 Vehicle conservation
model.addConstrs(
    (gp.quicksum(x[i,j]-x[j,i] for j in range(0,cus_no+sat_no)) == 0 for i in range(0,cus_no+sat_no))
)

#Constraint 11-13 Link between routing variables and allocation variables
model.addConstrs(
    (x[i,k+cus_no] <= z[i,k] for i in range(0,cus_no) for k in range(0,sat_no))
)
model.addConstrs(
    (x[k+cus_no,i] <= z[i,k] for i in range(0,cus_no) for k in range(0,sat_no))
)
model.addConstrs(
    (x[i,j] + z[i,k] + gp.quicksum(z[j,l] for l in range(0,sat_no) if l!=k) <= 2 for i in range(0,cus_no) for j in range(0,cus_no) if j!=i for k in range(0,sat_no))
)

#Constraint 14 Pickup load 
model.addConstrs(
    (u[i] + vehicle_capacity*x[i,j] - u[j] <= vehicle_capacity - allclient[j].pickup_demand for i in range(0,cus_no+sat_no) for j in range(0,cus_no) if j!=i)
)

#Constraint 15 Delivery load 
model.addConstrs(
    (v[i] - vehicle_capacity*x[i,j] - v[j] >= allclient[j].delivery_demand - vehicle_capacity for i in range(0,cus_no+sat_no) for j in range(0,cus_no) if j!=i)
)

#Constraint 16 Vehicle capacity
model.addConstrs(
    (u[i] + v[i] <= vehicle_capacity for i in range(0,cus_no+sat_no))
)

model.setParam(GRB.Param.TimeLimit, 10800)
#model.optimize()
print(model.Runtime)

for m in range(0,sat_no+cte_no):
    for n in range(0,cte_no+sat_no):
        if f[0,m,n].X>0:
            print(f[0,m,n].X,m,n,allhub[m].distanceto(allhub[n]))
        if h[0,m,n].X>0:
            print(h[0,m,n].X,m,n,allhub[m].distanceto(allhub[n]))

print('卫星枢纽')
for m in range(0,sat_no):
    if b[m].X>0.1:
        print(m)
print('中心枢纽')
for m in range(0,cte_no):
    if b[m+sat_no].X>0.1:
        print(m)
print('client分配')
for i in range(0,cus_no):
    for k in range(0,sat_no):
        if z[i,k].X>0.1:
            print(str(k) + ' ', end='')
print('\n卫星枢纽分配')
for k in range(0,sat_no):
    for l in range(0,cte_no):
        if g[k,l].X>0.1:
            print(str(l) + ' ', end='')
print('\n车辆路径')
display = []
for i in range(0,cus_no):
    display.append(0)
for k in range(0,sat_no):
    if b[k].X<0.1:
        continue
    while True:
        current = allsatellite[k]
        ks = False
        print(str(current.id), end='')
        while True:
            for i in range(0,cus_no+sat_no):
                if i<=cus_no-1 and display[i]==1:
                    continue
                if x[current.id,i].X>0.1 :
                    print(' ' + str(i), end='')
                    ks = True
                    if i<=cus_no-1:
                        display[i]=1
                    current = allnode[i]
                    break
            if current==allsatellite[k]:
                if ks==True:
                    print()
                    break
        stop = True
        for i in range(0,cus_no):
            if display[i]==0 and z[i,k].X==1:
                stop = False
        if stop==True:
            break
    



