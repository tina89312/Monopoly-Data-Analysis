import pygame
import random
import sys
import pymysql
import math

def main():
    for adjust in range(11):

        if adjust == 0:
            table_name = 'normal'
        else:
            table_name = 'normal-%s' %str(adjust)

        #連結mysql
        connect_db = pymysql.connect(host='localhost', port=3306, user='root', passwd='password', charset='utf8', db='monopoly')

        with connect_db.cursor() as cursor:
            creat_table = """
            CREATE TABLE IF NOT EXISTS `%s`(
                `Player1_Money` INT(7),
                `Player2_Money` INT(7),
                `Player3_Money` INT(7),
                `Player4_Money` INT(7),
                `Gate_Owner` VARCHAR(255) NULL,
                `Fountain_Owner` VARCHAR(255) NULL,
                `Path_Owner` VARCHAR(255) NULL,
                `Library_Owner` VARCHAR(255) NULL,
                `Classroom10_Owner` VARCHAR(255) NULL,
                `Classroom9_Owner` VARCHAR(255) NULL,
                `Restaurant3_Owner` VARCHAR(255) NULL,
                `Restaurant2_Owner` VARCHAR(255) NULL,
                `Restaurant1_Owner` VARCHAR(255) NULL,
                `Round` INT(6)
            );
            """ %table_name

            connect_db.ping(reconnect=True)

            # 執行 SQL 指令
            cursor.execute(creat_table)
            
            # 提交至 SQL
            connect_db.commit()

            cursor.close()
            
        # 關閉 SQL 連線
        connect_db.close()
    
        times = 1000
        for i in range(times):
            pygame.init()   # 初始化pygame库
            clock = pygame.time.Clock() # 創建一個clock對象來幫助跟蹤時間

            # 初始化屏幕
            size = (1270,768)
            screen = pygame.display.set_mode(size)
            pygame.display.set_caption("大富翁")

            # 定義玩家
            class Player():
                def __init__(self, image ,name ):
                    self.name = name    # 玩家名稱
                    self.money = 10000  # 玩家資產
                    self.image = image  # 棋子圖片位置
                    self.position = 0   # 玩家位置(數字)  
                    self.temp_position = False #(暫時不用)
                    self.dice_value = 0 #投擲骰子點數
                    self.locatedBuilding = 0    #玩家位置(名稱)
                    self.showText = []  #顯示的文字
                    self.ownedBuildings = []    #已被購買的建築陣列(可不用先暫留)
                    self.caishen = 0    #財神
                    self.shuaishen = 0  #衰神
                    self.tudishen = 0   #土地神
                    self.pohuaishen = 0 #破壞神

                def judgePosition(self,buildings): # 位置判断 返回值是所在位置的建筑名稱
                    for each in buildings:
                        for every in each.location:
                            if self.position == every:
                                return each
                        
                def buyaBuilding(self,isPressYes):    # 购买方法
                    #如果擁有者不是自己(應改為擁有者==no)且按下是
                    if isPressYes and self.locatedBuilding.owner != self.name:
                        self.locatedBuilding.owner = self.name  #變更建築物擁有者
                        self.locatedBuilding.wasBought = True   #變更是否被購買的狀態
                        self.ownedBuildings.append(self.locatedBuilding)    #將建築加入已被購買的建築陣列
                        self.money -= self.locatedBuilding.price    #將玩家資產扣除購買建築物的價錢
                        self.showText.append('購買了' + self.locatedBuilding.name + '!')
                        return True #表示購買成功
                    else:
                        return False    #表示購買失敗或無購買
                        
                def addaHouse(self,isPressYes): # 在建筑物上添加一个房子
                    try:
                        #如果擁有者是自己且按下是
                        if isPressYes and self.locatedBuilding.owner == self.name:
                            self.locatedBuilding.builtRoom += 1 #建築上建造的房子加一
                            self.money -= self.locatedBuilding.payment  #玩家資產減建造費(建造費=過路費)
                            self.showText.append('在' + self.locatedBuilding.name + '上!','蓋了一座房子！',\
                                            '有%d' % self.locatedBuilding.builtRoom + '個房子了！',\
                                            "它的過路費是%d" % (self.locatedBuilding.payment * \
                                                            (self.locatedBuilding.builtRoom + 1)))
                            return True #表示建造成功
                        else:
                            return False    #表示建造失敗或無建造
                    except:
                        pass
                
                def move(self,buildings,allplayers):   # 移動方法 返回值是所在的建筑位置
                    self.dice_value =  random.randint(1,6)  #random骰子點數
                    self.position += self.dice_value    #玩家位置+骰到點數
                    if self.position >= 16: #如果位置超過16就-16
                        self.position -= 16
                    self.locatedBuilding = self.judgePosition(buildings)    #將位置名稱更新
                    self.showText.append(self.name + "投擲了" + str(self.dice_value) + "點")
                    return self.eventInPosition(allplayers) #回傳eventInPosition的結果
                
                
                def eventInPosition(self,allplayers):        # 判断在建筑位置应该发生的事件        
                    building = self.locatedBuilding #玩家位置(名稱)
                    #如果玩家不在空地上
                    if building.name != '空地':
                        self.showText.append('来到了' + building.name)
                        if self.locatedBuilding.wasBought == False: # 如果建築物尚未被購買
                            self.addaHouse(not self.buyaBuilding(True))#如果建築尚未被購買則購買建築，若已被購買則蓋房子
                        elif building.owner == self.name: # 路过自己建筑物
                            # 如果之前經過空地抽到破壞神
                            if self.pohuaishen == 1:
                                self.showText.append(self.name + '破壞神附體！')
                                self.showText.append('摧毀了自己的房子！')
                                building.owner = 'no'
                                building.wasBought = False
                                self.pohuaishen = 0
                            else:
                                self.addaHouse(True)
                        #如果建築已被別人購買
                        else:
                            for each in allplayers: # 被收费！
                                #如果建築擁有者非當前玩家
                                if self.locatedBuilding.owner == each.name and each.name != self.name:
                                    #如果當前玩家之前經過空地抽到財神
                                    if self.caishen == 1:
                                        self.showText.append(self.name + '財神附體！')
                                        self.showText.append('免除過路費%d！' % (building.payment * (building.builtRoom + 1)))
                                        self.caishen = 0
                                    else:
                                        #如果當前玩家之前經過空地抽到土地神
                                        if self.tudishen == 1:
                                            self.showText.append(self.name + '土地神附體')
                                            self.showText.append('強佔土地！')
                                            self.showText.append(building.name + '屬於'+ self.name)
                                            self.locatedBuilding.owner = self.name
                                            each.ownedBuildings.remove(building)
                                            self.ownedBuildings.append(building)
                                            self.tudishen = 0
                                        else:
                                            #如果當前玩家之前經過空地抽到破壞神
                                            if self.pohuaishen == 1:
                                                self.showText.append(self.name + '破壞神附體')
                                                self.showText.append('摧毀對手房子')
                                                building.owner = 'no'
                                                building.wasBought = False
                                                each.ownedBuildings.remove(building)
                                                self.pohuaishen = 0   
                                            else:
                                                self.showText.append(self.name+ '來到了'+ each.name)
                                                self.showText.append('的' + building.name)
                                                #如果當前玩家之前經過空地抽到衰神
                                                if self.shuaishen == 1:
                                                    self.showText.append('過路費：%d*2!' % (building.payment * (building.builtRoom + 1)*2))
                                                    self.shuaishen = 0
                                                else:
                                                    self.showText.append('過路收費：%d' % (building.payment * (building.builtRoom + 1)))
                                                # 收费！
                                                self.money -= building.payment * (building.builtRoom + 1)
                                                each.money += building.payment * (building.builtRoom + 1)
                    #如果玩家在空地上                
                    else:
                        self.showText.append('来到了运气地点')
                        whichone = random.randint(0,3)
                        if whichone == 0:
                            self.caishen = 1
                            self.showText.append('遇到了财神！')
                            self.showText.append('免一次过路费！')
                        if whichone == 1:
                            self.shuaishen = 1
                            self.showText.append('遇到了衰神！')
                            self.showText.append('过路费加倍一次')
                        if whichone == 2:
                            self.tudishen = 1
                            self.showText.append('遇到了土地神！')
                            self.showText.append('强占一次房子！')
                        if whichone == 3:
                            self.pohuaishen = 1
                            self.showText.append('摧毁路过的房子！')
                            self.showText.append('遇到了破坏神！')

            # 建築物的class
            class Building():                           
                def __init__(self,name,price,payment,location):
                    self.name = name    # 建築物名稱
                    self.price = price  # 建築物價值
                    self.payment = payment  # 建築物過路費也是加蓋房子的價錢
                    self.location = location    # 建築物位置
                    self.wasBought = False               # 是否被購買
                    self.builtRoom = 0                   # 小房子建造的数目
                    self.owner = 'no'   # 建築物擁有者

            # 带透明度的繪圖方法
            def blit_alpha(target,source,location,opacity):
                x = location[0]     #位置的x座標
                y = location[1]     #位置的y座標
                #創建與source大小一致的圖像區域(convert()用於轉換格式，加快blit()速度)
                temp = pygame.Surface((source.get_width(),source.get_height())).convert()
                temp.blit(target , (-x , -y))   #把target圖片放進temp(由於按鈕的邊角會黑掉，所以先放一張與背景一樣的圖片)
                temp.blit(source,(0,0))     #把source圖片放進temp
                temp.set_alpha(opacity)     #設定圖像透明度
                target.blit(temp,location)  #把temp(設定好的source)放到target上



            # 讀取字體及有關數據
            textColorInMessageBox = (141,146,152)   #訊息文字顏色
            white = (255,255,255)
            black = (0,0,0)
            red = (255,0,0)
            font = pygame.font.Font('resource\\font\\myfont.ttf',30)

            # 讀取資源
            backgroud = pygame.image.load("resource\\picture\\GameMap.png")
            chess_1 = pygame.image.load("resource\\picture\\chess_1.png")
            chess_2 = pygame.image.load("resource\\picture\\chess_2.png")
            chess_3 = pygame.image.load("resource\\picture\\chess_3.png")
            chess_4 = pygame.image.load("resource\\picture\\chess_4.png")
            dice_1 = pygame.image.load("resource\\picture\\dice_1.png")
            dice_2 = pygame.image.load("resource\\picture\\dice_2.png")
            dice_3 = pygame.image.load("resource\\picture\\dice_3.png")
            dice_4 = pygame.image.load("resource\\picture\\dice_4.png")
            dice_5 = pygame.image.load("resource\\picture\\dice_5.png")
            dice_6 = pygame.image.load("resource\\picture\\dice_6.png")
            dices = [dice_1,dice_2,dice_3,dice_4,dice_5,dice_6]
            GameStart = pygame.image.load("resource\\picture\\GameStart.png")
            StartGameButton = pygame.image.load("resource\\picture\\StartGameButton.png").convert_alpha()
            
            shuaishen = pygame.image.load("resource\\picture\\shuaishen.png").convert_alpha()
            tudishen = pygame.image.load("resource\\picture\\tudishen.png").convert_alpha()
            caishen = pygame.image.load("resource\\picture\\caishen.png").convert_alpha()
            pohuaishen = pygame.image.load("resource\\picture\\pohuaishen.png").convert_alpha()
            
            # 將圖片放到該放的位置
            StartGameButton_rect = StartGameButton.get_rect()
            StartGameButton_rect.left , StartGameButton_rect.top = 1003,30

            # 實體化對象
            allplayers = []
            player_1 = Player(chess_1 , '玩家1' )
            player_2 = Player(chess_2 , '玩家2' )
            player_3 = Player(chess_3 , '玩家3' )
            player_4 = Player(chess_4 , '玩家4' )
            allplayers.append(player_1)
            allplayers.append(player_2)
            allplayers.append(player_3)
            allplayers.append(player_4)

            presentPlayer = player_1 # 當前是哪個玩家的回合
            previousPlayer = player_4   #上一個回合是哪個玩家
            presentPlayer_index = 0

            # 初始化建築物數據
            gate = Building('大門',1000-(100*adjust),200-(20*adjust),[1,2])
            fountain = Building('噴泉',2000-(200*adjust),400-(40*adjust),[3,4])
            path = Building('小道',800,160,[5])
            library = Building('圖書館',2000-(200*adjust),400-(40*adjust),[6,7])
            space1 = Building('空地',0,0,[8])
            classroom10 = Building('教室十',1200-(120*adjust),240-(24*adjust),[9,10])
            classroom9 = Building('教室九',1200-(120*adjust),240-(24*adjust),[11,12])
            restaurant3 = Building('三餐厅',800,160,[13])
            restaurant2 = Building('二餐厅',800,160,[14])
            restaurant1 = Building('一餐厅',800,160,[15])
            space2 = Building('空地',0,0,[0])

            # 建築陣列
            buildings = [gate,fountain,path,library,classroom10,\
                        classroom9,restaurant3,restaurant2,restaurant1,space1,space2]

            # 建築的坐標數據
            MapXYvalue = [(435.5,231.5),(509.5,231.5),(588.5,231.5),(675.5,231.5),(758.5,231.5),\
                        (758.5,317.0),(758.5,405.5),(758.5,484.5),(758.5,558.5),(679.5,558.5),\
                        (601.5,558.5),(518.5,556.5),(435.5,556.5),(435.5,479.5),(435.5,399.0),\
                        (435.5,315.5)]
            
            MapChessPosition_Player = []    #放置玩家棋子位置
            MapChessPosition_Payment = []   #過路費放置位置陣列

            #各物件位置
            MapMessageBoxPosition = (474.1 , 276.9) #訊息格位置
            StartGameButtonPosition = (1003,30)     #開始遊戲按鈕位置

            # 调整位置
            for i in range(0,16):
                MapChessPosition_Player.append((MapXYvalue[i][0]-70,MapXYvalue[i][1]-60))
                MapChessPosition_Payment.append((MapXYvalue[i][0]-20,MapXYvalue[i][1]-15))

            # 循环时所用的一些变量    
            running = True  # 判斷遊戲是否結束
            StartGameButton_alpha = 120  # 開始遊戲按鈕的透明度
            half_alpha = 30
            gameStarted = False # 判斷遊戲是否開始(是否已經進入遊戲非在首頁)
            

        ###################################################################################################

            play_round = 0

            # 循环开始！ 
            while running:
                # 如果還在遊戲首頁
                if not gameStarted:
                    for event in pygame.event.get():
                        # 如果按下窗口的關閉按鈕就退出遊戲
                        if event.type == pygame.QUIT:
                            sys.exit()
                    
                    #   將首頁的圖像放上去
                    screen.blit(GameStart , (0,0))
                    pygame.display.update()
                    #   繪製開始遊戲的按鈕
                    blit_alpha(screen, StartGameButton, StartGameButtonPosition, StartGameButton_alpha)
                    pygame.display.update(StartGameButton_rect)
                    # pygame.time.delay(500) #延遲0.5秒
                    StartGameButton_alpha = 255
                    blit_alpha(screen, StartGameButton, StartGameButtonPosition, StartGameButton_alpha)
                    pygame.display.update(StartGameButton_rect)
                    # pygame.time.delay(500) #延遲0.5秒
                    gameStarted = True

                #如果已進入遊戲(非首頁)
                if gameStarted:
                    for event in pygame.event.get():
                        # 如果按下窗口的關閉按鈕就退出遊戲
                        if event.type == pygame.QUIT:
                            sys.exit()
                    
                    #   將地圖的圖像放上去            
                    screen.blit( backgroud , (0,0) )
                    
                    play_round = play_round + 1

                    presentPlayer.move(buildings,allplayers)    #移動玩家(回傳值為是否出現是否按紐)
                    presentPlayer_index = (presentPlayer_index + 1) % 4   #當前玩家index加1
                    previousPlayer = presentPlayer
                    presentPlayer = allplayers[presentPlayer_index]    #當前玩家改為下一位玩家

                    # 訊息放置位置
                    textPosition = [MapMessageBoxPosition[0],MapMessageBoxPosition[1]]
                    
                    # 打印信息
                    for each in previousPlayer.showText:
                        text = font.render(each, True, white, textColorInMessageBox)    #(文字,抗鋸齒,顏色,背景)
                        screen.blit(text,textPosition)  #把文字放上螢幕
                        textPosition[1] += 30   #將下一段文字往下移
                    previousPlayer.showText = []

                    # 在位置上显示过路费
                    for i in range(1,8):
                        for each in buildings:
                            for every in each.location:
                                if i == every:
                                    if each.owner == previousPlayer.name:
                                        text = font.render('%d' % (each.payment * (each.builtRoom + 1))\
                                                        , True, red)
                                    elif each.owner == 'no':
                                        text = font.render('%d' % (each.payment * (each.builtRoom + 1))\
                                                        , True, white)
                                    elif each.owner != previousPlayer.name and each.owner != 'no':
                                        text = font.render('%d' % (each.payment * (each.builtRoom + 1))\
                                                        , True, black)
                                    screen.blit(text,MapChessPosition_Payment[i])
                    
                    for i in range(9,16):
                        for each in buildings:
                            for every in each.location:
                                if i == every:
                                    if each.owner == previousPlayer.name:
                                        text = font.render('%d' % (each.payment * (each.builtRoom + 1))\
                                                        , True, red)
                                    elif each.owner == 'no':
                                        text = font.render('%d' % (each.payment * (each.builtRoom + 1))\
                                                        , True, white)
                                    elif each.owner != previousPlayer.name and each.owner != 'no':
                                        text = font.render('%d' % (each.payment * (each.builtRoom + 1))\
                                                        , True, black)
                                    screen.blit(text,MapChessPosition_Payment[i])    

                    # 打印金钱数和幸运状态
                    money_1 = font.render(player_1.name +'金钱：%d' % player_1.money, True, black, white)
                    screen.blit(money_1,(5,0))
                    
                    if player_1.pohuaishen == True:
                        screen.blit(pohuaishen,(0,30))
                    else:
                        blit_alpha(screen, pohuaishen, (0, 30), half_alpha)
                        
                    if player_1.caishen == True:
                        screen.blit(caishen,(55,30))
                    else:
                        blit_alpha(screen, caishen, (55, 30), half_alpha)
                    
                    if player_1.shuaishen == True:
                        screen.blit(shuaishen,(110,30))
                    else:
                        blit_alpha(screen, shuaishen, (110, 30), half_alpha)
                    
                    if player_1.tudishen == True:
                        screen.blit(tudishen,(165,30))
                    else:
                        blit_alpha(screen, tudishen, (165, 30), half_alpha)
                    
                
                    money_2 = font.render(player_2.name +'金钱：%d' % player_2.money, True, black, white)
                    screen.blit(money_2,(1003,0))      

                    if player_2.pohuaishen == True:
                        screen.blit(pohuaishen,(1000,30))
                    else:
                        blit_alpha(screen, pohuaishen, (1000, 30), half_alpha)
                
                    if player_2.caishen == True:
                        screen.blit(caishen,(1055,30))
                    else:
                        blit_alpha(screen, caishen, (1055, 30), half_alpha)
                    
                    if player_2.shuaishen == True:
                        screen.blit(shuaishen,(1110,30))
                    else:
                        blit_alpha(screen, shuaishen, (1110, 30), half_alpha)
                        
                    if player_2.tudishen == True:
                        screen.blit(tudishen,(1165,30))
                    else:
                        blit_alpha(screen, tudishen, (1165, 30), half_alpha)

                    
                    money_3 = font.render(player_3.name +'金钱：%d' % player_3.money, True, black, white)
                    screen.blit(money_3,(5,101))
                    
                    if player_3.pohuaishen == True:
                        screen.blit(pohuaishen,(0,130))
                    else:
                        blit_alpha(screen, pohuaishen, (0, 130), half_alpha)
                        
                    if player_3.caishen == True:
                        screen.blit(caishen,(55,130))
                    else:
                        blit_alpha(screen, caishen, (55, 130), half_alpha)
                    
                    if player_3.shuaishen == True:
                        screen.blit(shuaishen,(110,130))
                    else:
                        blit_alpha(screen, shuaishen, (110, 130), half_alpha)
                    
                    if player_3.tudishen == True:
                        screen.blit(tudishen,(165,130))
                    else:
                        blit_alpha(screen, tudishen, (165, 130), half_alpha)

                    money_4 = font.render(player_4.name +'金钱：%d' % player_4.money, True, black, white)
                    screen.blit(money_4,(1003,101))      

                    if player_4.pohuaishen == True:
                        screen.blit(pohuaishen,(1000,130))
                    else:
                        blit_alpha(screen, pohuaishen, (1000, 130), half_alpha)
                
                    if player_4.caishen == True:
                        screen.blit(caishen,(1055,130))
                    else:
                        blit_alpha(screen, caishen, (1055, 130), half_alpha)
                    
                    if player_4.shuaishen == True:
                        screen.blit(shuaishen,(1110,130))
                    else:
                        blit_alpha(screen, shuaishen, (1110, 130), half_alpha)
                        
                    if player_4.tudishen == True:
                        screen.blit(tudishen,(1165,130))
                    else:
                        blit_alpha(screen, tudishen, (1165, 130), half_alpha)

                    # 放置扔出来的骰子
                    if previousPlayer.dice_value != 0:
                        screen.blit(dices[previousPlayer.dice_value - 1],(70,590)) 

                    # 放置玩家與電腦的位置
                    for each in allplayers:
                        screen.blit(each.image,MapChessPosition_Player[each.position])

                    # 输赢判断
                    for each in allplayers:
                        if each.money <= 0:
                            
                            #連結mysql
                            connect_db = pymysql.connect(host='localhost', port=3306, user='root', passwd='password', charset='utf8', db='monopoly')

                            with connect_db.cursor() as cursor:

                                transfer_data = "INSERT INTO `%s`(`Player1_Money`, `Player2_Money`, `Player3_Money`, `Player4_Money`, `Gate_Owner`, `Fountain_Owner`, `Path_Owner`, `Library_Owner`, `Classroom10_Owner`, `Classroom9_Owner`, `Restaurant3_Owner`, `Restaurant2_Owner`, `Restaurant1_Owner`, `Round`) VALUES (%d,%d,%d,%d,'%s','%s','%s','%s','%s','%s','%s','%s','%s',%d)" %(table_name, player_1.money, player_2.money, player_3.money, player_4.money, gate.owner, fountain.owner, path.owner, library.owner, classroom10.owner, classroom9.owner, restaurant3.owner, restaurant2.owner, restaurant1.owner, math.ceil(play_round / 4))

                                # 執行 SQL 指令
                                cursor.execute(transfer_data)
                                
                                # 提交至 SQL
                                connect_db.commit()

                                cursor.close()

                            # 關閉 SQL 連線
                            connect_db.close()
                            

                            font = pygame.font.Font('resource\\font\\myfont.ttf',200)
                            loseText = font.render(each.name +'输了！', True, red)
                            screen.fill(black)
                            screen.blit(loseText,(100,100))
                            font = pygame.font.Font('resource\\font\\myfont.ttf',30)
                            pygame.display.flip()            
                            # pygame.time.delay(500)
                            running = False
                    
                    # pygame.time.delay(100) #延遲0.1秒

                # 画面运行
                pygame.display.flip()
                clock.tick(1000)              # 刷新率
    
            

# 双击打开运行            
if __name__ == "__main__":
    main()             