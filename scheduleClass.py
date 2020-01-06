from statClass import *


class Scheduling:
    tasks = []
    def __init__(self, requirement, buffers, FactoryMap, productLine):
        self.requirement = requirement
        self.transfer(self.tasks ,self.requirement ,buffers)
        self.FactoryMap = FactoryMap

    def transfer(self,tasks,requirement,buffers):
        #备料出料
        if requirement.type == 0:
            shelfObject = requirement.getShelf()
            count = 0
            putposition = []
            for material in shelfObject.materials:
                if buffers[material.getMaterialType()].getLastModifiedLeftSize() < material.getQuantity(): #剩余容量大于
                    putposition.append(material.getNextBufferPostion())
                    count+=1

            if count == 0:       #不需要拿空货架
                agv = self.getNearestFreeAgv(18, 2)
                startPosx = 18
                startPosy = 2
                for material in shelfObject.materials:
                    terminalPosx = buffers[material.getMaterialType()].getx()   #需要得到
                    terminalPosy = buffers[material.getMaterialType()].gety()
                    path = self.getClosestPath(startPosx,startPosy,terminalPosx,terminalPosy)
                    tasks.append(Task(overAllTaskid, 0, startPosx, startPosy, terminalPosx, terminalPosy, path, 0,0,material[0],material[1],0,0))
                    startPosx = terminalPosx
                    startPosy = terminalPosy
                terminalPosx, terminalPosy = self.FindClosetestFreeShelfBuffer(startPosx,startPosy)
                path = self.getClosestPath(startPosx, startPosy, terminalPosx, terminalPosy)
                tasks.append(Task(overAllTaskid, 3, startPosx, startPosy, terminalPosx, terminalPosy, path, 0, unloadShelfId, 0, 0, 0, 0))
                agv.getTasks(tasks)
            else: #需要拿count-1个空货架
                if self.hasFreeCar():
                    agv = self.getFreeCar()
                    i = 0
                    shelves = []
                    while i < count - 1:
                        shelf = self.getFreeShelf()
                        shelves.append(shelf)
                        tasks.append(Task(overAllTaskid, 0, startPosx, startPosy, startPosx, startPosy, 0, shelf, 0,
                                        0, 0, 0, 0))
                    startPosx = agv.getXpos()
                    startPosy = agv.getYpos()
                    while putposition:
                        terminalPosx, terminalPosy = putposition[-1]
                        path = self.getClosestPath(startPosx, startPosy, terminalPosx, terminalPosy)
                        tasks.append(Task(overAllTaskid, 0, startPosx, startPosy, terminalPosx, terminalPosy, path, 0, 0,
                                       0, 0, 0, 0))
                        tasks.append(Task(overAllTaskid, 0, startPosx, startPosy, terminalPosx, terminalPosy, 0, 0, 0,
                                       0, shelves[-1], 0, 0))
                    startPosx = 18
                    startPosy = 2
                    for material in shelfObject.materials:
                        terminalPosx = buffers[material.getMaterialType()].getx()  # 需要得到
                        terminalPosy = buffers[material.getMaterialType()].gety()
                        path = self.getClosestPath(startPosx, startPosy, terminalPosx, terminalPosy)
                        tasks.append(Task(overAllTaskid, 0, startPosx, startPosy, terminalPosx, terminalPosy, path, 0, 0,
                                        material[0], material[1], 0, 0))
                        startPosx = terminalPosx
                        startPosy = terminalPosy
                    terminalPosx, terminalPosy = self.FindClosetestFreeShelfBuffer(startPosx, startPosy)
                    path = self.getClosestPath(startPosx, startPosy, terminalPosx, terminalPosy)
                    tasks.append(Task(overAllTaskid, 3, startPosx, startPosy, terminalPosx, terminalPosy, path, 0, unloadShelfId,
                             0, 0, 0, 0))
                else:
                    i = 0
                    while i < count - 1:
                        shelf = self.getFreeShelf()
                        shelves.append(shelf)
                        tasks.append(Task(overAllTaskid, 0, startPosx, startPosy, startPosx, startPosy, 0, shelf, 0,
                                        0, 0, 0, 0))
                    agv = self.getNearestFreeAgv(shelf)
                    startPosx = agv.getXpos()
                    startPosy = agv.getYpos()
                    while putposition:
                        terminalPosx, terminalPosy = putposition[-1]
                        path = self.getClosestPath(startPosx, startPosy, terminalPosx, terminalPosy)
                        tasks.append(Task(overAllTaskid, 0, startPosx, startPosy, terminalPosx, terminalPosy, path, 0, 0,
                                        0, 0, 0, 0))
                        tasks.append(Task(overAllTaskid, 0, startPosx, startPosy, terminalPosx, terminalPosy, 0, 0, 0,
                                        0, shelves[-1], 0, 0))
                    startPosx = 18
                    startPosy = 2
                    for material in shelfObject.materials:
                        terminalPosx = buffers[material.getMaterialType()].getx()  # 需要得到
                        terminalPosy = buffers[material.getMaterialType()].gety()
                        path = self.getClosestPath(startPosx, startPosy, terminalPosx, terminalPosy)
                        tasks.append(Task(overAllTaskid, 0, startPosx, startPosy, terminalPosx, terminalPosy, path, 0, 0,
                                        material[0], material[1], 0, 0))
                        startPosx = terminalPosx
                        startPosy = terminalPosy
                    terminalPosx, terminalPosy = self.FindClosetestFreeShelfBuffer(startPosx, startPosy)
                    path = self.getClosestPath(startPosx, startPosy, terminalPosx, terminalPosy)
                    tasks.append(
                        Task(overAllTaskid, 3, startPosx, startPosy, terminalPosx, terminalPosy, path, 0, unloadShelfId,
                             0, 0, 0, 0))

            #送料
        elif requirement.type == 1:
            materialType = requirement.getMaterialType()
            materialQuantity = requirement.getMaterialQuantity()
            buffer = buffers[materialType]
            bufferList = buffer.getShelvesForGetMaterial(materialQuantity)
            firstX = bufferList[0].get_x_pos()
            firstY = bufferList[0].get_y_pos()

            acg = getNearestFreeAgv(firstX, firstY)
            startPosx = acg.getXpos()
            startPosy = acg.getYpos()
            terminalPosx, terminalPosy = self.getFreeShelf()
            path1 = self.getClosestPath(startPosx,startPosy,terminalPosx,terminalPosy)

            # go to free shelf position
            task1 = Task(overAllTaskid, 0, startPosx, startPosy, terminalPosx, terminalPosy, 
            path1, self.getFreeShelf(), 0, 0, 0, 0, 0, 0)
            overAllTaskid = overAllTaskid + 1

            startPosx = terminalPosx
            startPosy = terminalPosy

            # get Free Shelf
            task2 = Task(overAllTaskid, 0, startPosx, startPosy, startPosx, startPosy, 
            null, self.getFreeShelf(), 0, 0, 0, 0, 0, 0)
            overAllTaskid = overAllTaskid + 1

            tasks = []
            tasks.append(task1)
            tasks.append(task2)

            # get materials
            for shelf, materialQuantity in bufferList:
                # go to shelf
                path = self.getClosestPath(startPosx,startPosy,shelf.get_x_pos(),shelf.get_y_pos())

                task = Task(overAllTaskid, 0, startPosx, startPosy, terminalPosx, terminalPosy, 
                path, self.getFreeShelf(), 0, 0, 0, 0, 0, 0)
                tasks.append(task)
                startPosx = shelf.get_x_pos()
                startPosy = shelf.get_y_pos()
                overAllTaskid = overAllTaskid + 1

                # load material
                task = Task(overAllTaskid, 4, startPosx, startPosy, terminalPosx, terminalPosy, 
                0, self.getFreeShelf(), 0, 0, 0, 0, 0, materialQuantity)
                tasks.append(task)
                overAllTaskid = overAllTaskid + 1
            
            # go to productLine

            productIndex = requirement.getStart()
            endx, endy = productLine.getPosition(startIndex)
            path3 = self.getClosestPath(startPosx, startPosy, endx, endy)
            task3 = Task(overAllTaskid, 2, startPosx, startPosy, terminalPosx, terminalPosy, 
                path3, self.getFreeShelf(), 0, 0, 0, 0, 0, materialQuantity)
            tasks.append(task3)
            overAllTaskid = overAllTaskid + 1


            #空货架调度
        elif requirement.type == 2:
            shelf = requirement.getShelf()
            terminalPosx = shelf.get_x_pos()
            terminalPosy = shelf.get_y_pos()
            shelfId = shelf.getId()
            startPosx, startPosy= self.FindClosetestFreeShelfBuffer(terminalPosx, terminalPosy)
            # 小车到空货架缓存区
            agv = getNearestFreeAgv(startPosx, startPosy)
            path1 = self.getClosestPath(agv.getXpos(), agv.getYpos(), startPosx, startPosy)
            tasks.push(Task(overAllTaskid, 0, agv.getXpos(), agv.getYpos(), startPosx, startPosy, path1, 0, 0, 0, 0))
            overAllTaskid = overAllTaskid + 1
            # 装上空货架
            tasks.push(Task(overAllTaskid, 1, 0, 0, 0, 0, 0, shelfId, 0, 0, 0))
            overAllTaskid = overAllTaskid + 1
            # 空货架缓存区到buffer
            path2 = self.getClosestPath(startPosx, startPosy, terminalPosx, terminalPosy)
            tasks.push(Task(overAllTaskid, 0, startPosx, startPosy, terminalPosx, terminalPosy, path2, 0, 0, 0, 0))
            overAllTaskid = overAllTaskid + 1
            # 卸下空货架
            tasks.push(Task(overAllTaskid, 2, 0, 0, 0, 0, 0, 0, shelfId, 0, 0))
            overAllTaskid = overAllTaskid + 1

        # 空货架回收
        elif requirement.type == 3:
            shelf = requirement.getShelf()
            startPosx = 18
            startPosy = 38
            shelfId = shelf.getId()
            # 小车到生产线
            agv = getNearestFreeAgv(startPosx, startPosy)
            path1 = self.getClosestPath(agv.getXpos(), agv.getYpos(), startPosx, startPosy)
            tasks.push(Task(overAllTaskid, 0, agv.getXpos(), agv.getYpos(), startPosx, startPosy, path1, 0, 0, 0, 0))
            overAllTaskid = overAllTaskid + 1
            # 装上空货架
            tasks.push(Task(overAllTaskid, 1, 0, 0, 0, 0, 0, shelfId, 0, 0, 0))
            overAllTaskid = overAllTaskid + 1
            # 生产线到空货架缓存区
            terminalPosx, terminalPosy = self.FindClosetestFreeShelfBuffer(startPosx, startPosy)
            path = self.getClosestPath(startPosx, startPosy, terminalPosx, terminalPosy)
            tasks.push(Task(overAllTaskid, 0, startPosx, startPosy, terminalPosx, terminalPosy, path, 0, 0, 0, 0))
            overAllTaskid = overAllTaskid + 1
            # 卸下空货架
            tasks.push(Task(overAllTaskid, 2, 0, 0, 0, 0, 0, 0, shelfId, 0, 0))
            overAllTaskid = overAllTaskid + 1

        # 充电
        elif requirement.type == 4:
            agv = requirement.getAgv()
            startPosx = agv.getXpos()
            startPosy = agv.getYpos()
            terminalPosx = 0
            terminalPosy = 0
            path = self.getClosestPath(startPosx, startPosy, terminalPosx, terminalPosy)
            tasks.push(Task(overAllTaskid, 0, startPosx, startPosy, terminalPosx, terminalPosy, path, 0, 0, 0, 0))
            overAllTaskid = overAllTaskid + 1
            print("充上电啦！")


    def getClosestPath(self, startPosx,startPosy,terminalPosx,terminalPosy):
        #BFS搜索
        path = [[(startPosx,startPosy)]]
        while path:
            p = path[0]
            path.remove(0)
            s = p[-1]
            if FactoryMap[s[0]-1][s[1]] == 1:
                p.append((s[0]-1,s[1]))
                if (s[0]-1,s[1]) == (terminalPosx,terminalPosy):
                    return p
                    break
            if FactoryMap[s[0]][s[1]-1] == 1:
                p.append((s[0] , s[1]-1))
                if (s[0] , s[1]-1) == (terminalPosx,terminalPosy):
                    return p
                    break
            if FactoryMap[s[0] + 1][s[1]] == 1:
                p.append((s[0] + 1, s[1]))
                if (s[0] + 1, s[1]) == (terminalPosx,terminalPosy):
                    return p
                    break
            if FactoryMap[s[0]][s[1]+1] == 1:
                p.append((s[0] , s[1]+1))
                if (s[0] , s[1]+1) == (terminalPosx,terminalPosy):
                    return p
                    break


    def hasFreeCar(self):
        for j in range(12,29,4):
            if FactoryMap[36][j] != 1:
                return True
        return False

    def getFreeShelf(self):
        shelfId += 1
        return shelf(shelfId, [], 10, 0, 36, 20)


