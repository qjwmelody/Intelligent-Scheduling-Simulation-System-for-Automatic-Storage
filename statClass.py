from scheduleClass import *

# 小车类定义
class AGV:
    shelves = []
    tasks = 0
    # 方向：1-东，2-南，3-西，4-北
    direction = 1
    # 运行状态：1-直行，2-停车，3-正转，4-逆转
    runningCondition = 2
    speed = 0
    energy = 100
    # 报警信息：0-无报警，1-障碍物，2-路径有偏移，3-位置信息缺失，4-KIVA心跳数据缺失，5-电量不足，6-任务过多，7-抛锚
    alarmCondition = 0

    def getXpos(self):
        return self.x_pos
    
    def getYpos(self):
        return self.y_pos

    def __init__(self, AGVId, x_pos, y_pos):
        self.AGVId = AGVId
        self.x_pos = x_pos
        self.y_pos = y_pos

    def getTasks(self, tasks):
        self.tasks = tasks
        
    def doTask(self, task):
        print(task)

    def alarm(self, alarmType):
        print(alarmType, "Alarm!")

    def show(self):
        print(self.AGVId, self.x_pos, self.y_pos)
        print(self.direction, self.runningCondition)
        print(self.speed, self.energy, self.alarmCondition)

    def modifyCondition(self, runningCondition):
        self.runningCondition = runningCondition

    def modifySpeed(self, speed):
        self.speed = speed

    def loadShelf(self, shelf):
        self.shelves.append(shelf)

    def unloadShelf(self, shelf):
        print(self.shelves)
    
    # def unloadShelf(self):

# 缓存区定义
class Buffer:
    # 0-A,1-B,2-C
    top = 0
    ifShelf = [0 for _ in range(40)]
    shelves = [0 for _ in range(40)]
    position = []
    
    def __init__(self, bufferType):
        self.bufferType = bufferType
        # A buffer
        if(self.bufferType == 0):
            for j in range(8, 19):
                self.position.append((8,j))
            for j in range(22,33):
                self.position.append((8,j))
            for j in range(8, 19):
                self.position.append((13, j))
            for j in range(22, 33):
                self.position.append((13, j))
        # B buffer
        elif(self.bufferType == 1):
            for j in range(8, 19):
                self.position.append((18,j))
            for j in range(22,33):
                self.position.append((18,j))
            for j in range(8, 19):
                self.position.append((23, j))
            for j in range(22, 33):
                self.position.append((23, j))

        # C buffer
        else:
            for j in range(8, 19):
                self.position.append((28,j))
            for j in range(22,33):
                self.position.append((28,j))
            for j in range(8, 19):
                self.position.append((33, j))
            for j in range(22, 33):
                self.position.append((33, j))

    def getx(self):
        return self.shelves[self.top].get_x_pos

    def gety(self):
        return self.shelves[self.top].get_y_pos

    

    def getNextBufferPostion(self):
        return self.position[self.top + 1][0], self.position[self.top + 1][1]

    def modifyBufferIfShelf(self, index, x):
        # x是0/1
        self.ifShelf[index] = x
        
    def loadShelf(self, index, shelfObject):
        self.modifyBufferIfShelf(index, 1)
        self.shelves[index] = shelfObject
    
    # 拿走shelf
    def unloadShelf(self, index):
        self.modifyBufferIfShelf(index, 0)
        self.shelves[index] = 0
        
    def loadMaterial(self, index, quantity):
        shelf = self.shelves[index]
        if(shelf.materials == []):
            material = Material(self.bufferType, quantity)
            shelf.materials.append(material)
        else:
            shelf.materials[0].quantity = shelf.materials[0].quantity + quantity
        if(shelf.materials[0].quantity == shelf.materials[0].maxLoad):
            self.top = 1 + self.top
    
    def unloadMaterial(self, index, quantity):
        shelf = self.shelves[index]
        if(shelf.materials == []):
            material = Material(self.bufferType, quantity)
            shelf.materials.append(material)
        else:
            shelf.materials[0].quantity = shelf.materials[0].quantity - quantity
        if(shelf.materials[0].quantity == shelf.materials[0].maxLoad):
            self.top = self.top - 1
            self.shelves[index] = 0

    def getShelvesForGetMaterial(self, Quantity):
        result = []
        materialQuantity = Quantity
        for shelf in self.shelves:
            if shelf != 0:
                material = shelf.getMaterials()[0]
                quantity = material.getQuantity()
                if quantity >= materialQuantity:
                    result.append((shelf, materialQuantity))
                    return result
                else:
                    result.append((shelf, quantity))
                    materialQuantity = materialQuantity - quantity
        
    

# 需求单定义
class Requirement:
	# 0-备料出料，1-送料，2-空货架调度，3-空货架回收，4-充电
    def __init__(self, requirementType = 0, start = 0, terminal = -1, shelfObject = -1, 
    materialType = -1, materialQuantity = -1, agv = -1):
        self.requirementType = requirementType
        self.start = start
        self.terminal = terminal
        self.shelfObject = shelfObject
        self.materialType = materialType
        self.materialQuantity = materialQuantity
        self.agv = agv

    def getStart(self):
        return self.start

    def getAgv(self):
        return self.agv

    def getMaterialType(self):
        return self.materialType

    def getMaterialQuantity(self):
        return self.materialQuantity

    def getShelfObject(self):
        return self.shelfObject


class Material:
    def __init__(self, materialType, quantity):
        # 0-A/1-B/2-C
        self.materialType = materialType
        self.quantity = quantity

    def getQuantity(self):
        return self.quantity

    def getMaterialType(self):
        return self.materialType

    def modifyMinusQuantity(self, quantity):
        self.quantity = self.quantity - quantity
    
    def showMaterialType(self):
        print(self.materialType)
        
    def showQuantity(self):
        print(self.quantity)

class Shelf:
    def __init__(self, shelfId, materials, maxLoad, load, x_pos, y_pos):
        
        self.shelfId = shelfId
        self.materials = []
        self.maxLoad = 10
        self.load = 0
        self.x_pos = x_pos
        self.y_pos = y_pos

    def getShelfId(self):
        return self.shelfId

    def getMaterials(self):
        return self.materials

    def get_x_pos(self):
        return self.x_pos

    def get_y_pos(self):
        return self.y_pos
        
    def showInfomation(self):
        print(self.shelfId)
        print(self.materials)
        print(self.maxLoad)
        print(self.load)
        print(self.x_pos)
        print(self.y_pos)

    def loadMaterials(self, materials):

        self.materials = self.materials + materials

    def unloadMaterials(self, materialType, quantity):
        for i in self.materials:
            if materialType == i.getMaterialType():
                i.modifyMinusQuantity(quantity)
                break
            
    def changePosition(self, x, y):
        self.x_pos = x
        self.y_pos = y

class Task:
    def __init__(self, taskId, taskType, start_x_pos = 0, start_y_pos=0, terminal_x_pos=0, 
    terminal_y_pos=0, path=[], loadShelfId=-1, unloadShelfId=-1, unloadMaterialType=-1, unloadMaterialQuantity=-1,
    loadMaterialQuantity=-1):
        # 0-path 1-loadShelf 2-unloadShelf 3-unloadMaterial 4-loadMaterial
        self.taskId = taskId
        self.taskType = taskType
        self.start_x_pos = start_x_pos
        self.start_y_pos = start_y_pos
        self.terminal_x_pos = terminal_x_pos
        self.terminal_y_pos = terminal_y_pos
        self.path = path
        self.loadShelfId = loadShelfId
        self.unloadShelfId = unloadShelfId
        self.unloadMaterialType = unloadMaterialType
        self.unloadMaterialQuantity = unloadMaterialQuantity
        self.loadMaterialQuantity = loadMaterialQuantity
        
    def showInfomation(self):
        print(self.taskId)
        print(self.taskType)
        print(self.start_x_pos)
        print(self.start_y_pos)
        print(self.terminal_x_pos)
        print(self.terminal_y_pos)
        print(self.path)




# 充电桩定义
class ChargingPoint:
    def __init__(self, pointId, x_pos, y_pos):
        self.ChargingPointId = pointId
        self.x_pos = x_pos
        self.y_pos = y_pos

# 充电区定义
class ChargingArea:
    ifCharging = [0 for _ in range(5)]
    #ChargingPoint = [0 for _ in range(5)]
    top=0

    def __init__(self):
        self.position = []
        self.chargingPoint = []
        for j in range(12,29,4):
            self.position.append((2, j))
            point = ChargingPoint(j, 2, j)
            self.chargingPoint.append(point)

    def getNextChargingPosition(self):
        return self.position[self.top + 1][0]

    def modifyChargingAreaIfCar(self, index, x):
        # x是0/1
        self.ifCharging[index] = x

    def ChargingAgv(self, index, agv):
        self.modifyChargingAreaIfCar(index, 1)
        self.chargingPoint[index] = agv



# 空货架缓存区定义
class FreeArea:
    ifShelf = [0 for _ in range(5)]
    shelves = [0 for _ in range(5)]
    top = 0

    def __init__(self):
        self.position = []
        for j in range(12,29,4):
            self.position.append((36, j))

    def modifyFreeAreaIfShelf(self, index, x):
        # x是0/1
        self.ifShelf[index] = x

    def loadShelf(self, index, shelfObject):
        self.modifyFreeAreaIfShelf(index, 1)
        self.shelves[index] = shelfObject

    def getNextFreePosition(self):
        return self.position[self.top + 1][0]


class ProductionLine:

    def __init__(self):
        self.requirement = Requirement()

    def SetRequiremtn(self, requirement):
        self.requirement = requirement

    def SendMessage(self):
        scheduleSystem.getMessage(self.requirement)


class SupplyArea:
    def __init__(self):
        self.requirement = Requirement()

    def SetRequiremtn(self, requirement):
        self.requirement = requirement

    def SendMessage(self):
        scheduleSystem.getMessage(self.requirement)


        


scheduleSystem = Scheduling()


    
