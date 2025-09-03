import pymysql
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties as font

# 持有各地點勝率圖(長條圖)、持有各地點敗率圖(長條圖)
def land_winning_percentage_graph():
    #連結mysql
    connect_db = pymysql.connect(host='localhost', port=3306, user='root', passwd='password', charset='utf8', db='monopoly')

    with connect_db.cursor() as cursor:
        select_normal_data = "SELECT `Player1_Money`, `Player2_Money`, `Player3_Money`, `Player4_Money`, `Gate_Owner`, `Fountain_Owner`, `Path_Owner`, `Library_Owner`, `Classroom10_Owner`, `Classroom9_Owner`, `Restaurant3_Owner`, `Restaurant2_Owner`, `Restaurant1_Owner` FROM `normal-5` WHERE 1"

        # 執行 SQL 指令
        cursor.execute(select_normal_data)
        
        # 提交至 SQL
        connect_db.commit()

        #未調整前的結束輪數
        normal_data = cursor.fetchall()

    # 關閉 SQL 連線
    connect_db.close()

    land_winning_percentage = [0,0,0,0,0,0,0,0,0]
    land_failure_rate = [0,0,0,0,0,0,0,0,0]
    for i in range(1000):
        winner = []
        loser = ''
        for j in range(4):
            if normal_data[i][j] == max(normal_data[i][0:4]):
                if j == 0:
                    winner.append('玩家1')
                elif j == 1:
                    winner.append('玩家2')
                elif j == 2:
                    winner.append('玩家3')
                elif j == 3:
                    winner.append('玩家4')
            if normal_data[i][j] == min(normal_data[i][0:4]):
                if j == 0:
                    loser = '玩家1'
                elif j == 1:
                    loser = '玩家2'
                elif j == 2:
                    loser = '玩家3'
                elif j == 3:
                    loser = '玩家4'
        
        for j in range(4,13):
            for k in range(len(winner)):
                if normal_data[i][j] == winner[k]:
                    land_winning_percentage[j-4] = land_winning_percentage[j-4] + 1
            if normal_data[i][j] == loser:
                land_failure_rate[j-4] = land_failure_rate[j-4] + 1

    for i in range(9):
        land_winning_percentage[i] = land_winning_percentage[i] / 1000
        land_failure_rate[i] = land_failure_rate[i] / 1000
    
    # 持有各地點勝率圖(長條圖)
    plt.grid(axis='y', ls='--', zorder=0)
    plt.bar([0,1,2,3,4,5,6,7,8], land_winning_percentage, color='#375da1', width=0.4, zorder=10)
    plt.xticks([0,1,2,3,4,5,6,7,8], ['大門','噴泉','小道','圖書館','教室十','教室九','三餐厅','二餐厅','一餐厅'], fontproperties=font(fname="resource\\font\\myfont.ttf"))
    plt.ylim(0,1)
    plt.title('持有各地點勝率圖', fontproperties=font(fname="resource\\font\\myfont.ttf"), fontsize=15)
    for i in range(9):
        plt.text(i-0.2,land_winning_percentage[i]+0.02,land_winning_percentage[i],fontsize=7)
    plt.savefig('graph\\持有各地點勝率圖.png')
    plt.show()

    # 持有各地點敗率圖(長條圖)
    plt.grid(axis='y', ls='--', zorder=0)
    plt.bar([0,1,2,3,4,5,6,7,8], land_failure_rate, color='#375da1', width=0.4, zorder=10)
    plt.xticks([0,1,2,3,4,5,6,7,8], ['大門','噴泉','小道','圖書館','教室十','教室九','三餐厅','二餐厅','一餐厅'], fontproperties=font(fname="resource\\font\\myfont.ttf"))
    plt.ylim(0,1)
    plt.title('持有各地點敗率圖', fontproperties=font(fname="resource\\font\\myfont.ttf"), fontsize=15)
    for i in range(9):
        plt.text(i-0.2,land_failure_rate[i]+0.02,land_failure_rate[i],fontsize=7)
    plt.savefig('graph\\持有各地點敗率圖.png')
    plt.show()







# 各玩家勝率圖(圓餅圖)、各玩家敗率圖(圓餅圖)
def player_sequence_graph():
    #連結mysql
    connect_db = pymysql.connect(host='localhost', port=3306, user='root', passwd='password', charset='utf8', db='monopoly')

    with connect_db.cursor() as cursor:
        select_normal_player_money = "SELECT `Player1_Money`, `Player2_Money`, `Player3_Money`, `Player4_Money` FROM `normal` WHERE 1"

        # 執行 SQL 指令
        cursor.execute(select_normal_player_money)
        
        # 提交至 SQL
        connect_db.commit()

        #未調整前的結束輪數
        normal_player_money = cursor.fetchall()

    # 關閉 SQL 連線
    connect_db.close()

    win_times = [0,0,0,0]
    lose_times = [0,0,0,0]
    for i in range(1000):
        for j in range(4):
            if normal_player_money[i][j] == max(normal_player_money[i]):
                win_times[j] = win_times[j] + 1
            if normal_player_money[i][j] == min(normal_player_money[i]):
                lose_times[j] = lose_times[j] + 1
    
    #各玩家勝率圖(圓餅圖)
    plt.pie(win_times, startangle=90 , counterclock=False, labels=['player1','player2','player3','player4'], textprops={'fontproperties':font(fname="resource\\font\\myfont.ttf"), 'size':13}, autopct='%.1f%%', colors=['#335899','#3f6ab7','#778fcd','#b3bedf'])
    plt.title('各玩家勝率圖', fontproperties=font(fname="resource\\font\\myfont.ttf"), fontsize=15)
    plt.savefig('graph\\各玩家勝率圖.png')
    plt.show()

    #各玩家敗率圖(圓餅圖)
    plt.pie(lose_times, startangle=90 , counterclock=False, labels=['player1','player2','player3','player4'], textprops={'fontproperties':font(fname="resource\\font\\myfont.ttf"), 'size':13}, autopct='%.1f%%', colors=['#335899','#3f6ab7','#778fcd','#b3bedf'])
    plt.title('各玩家敗率圖', fontproperties=font(fname="resource\\font\\myfont.ttf"), fontsize=15)
    plt.savefig('graph\\各玩家敗率圖.png')
    plt.show()





# 遊戲結束輪數(長條圖)、遊戲結束平均輪數(折線圖)
def all_round_graph():
    end_round_average = []
    for i in range(11):
        table_name = 'normal'
        if i != 0:
            table_name = table_name + '-%s' %str(i)

        #連結mysql
        connect_db = pymysql.connect(host='localhost', port=3306, user='root', passwd='password', charset='utf8', db='monopoly')

        with connect_db.cursor() as cursor:
            select_round = "SELECT `Round` FROM `%s` WHERE 1" %table_name

            # 執行 SQL 指令
            cursor.execute(select_round)
            
            # 提交至 SQL
            connect_db.commit()

            #未調整前的結束輪數
            round = cursor.fetchall()

        # 關閉 SQL 連線
        connect_db.close()

        round_sort = sorted(round)
        end_round = []
        end_round_quantity = []
        for j in range(len(round_sort)):
            if j == 0:
                end_round.append(round_sort[j][0])
                end_round_quantity.append(1)
                end_round_average.append(round_sort[j][0])
            elif round_sort[j - 1] == round_sort[j]:
                end_round_quantity[len(end_round_quantity)-1] = end_round_quantity[len(end_round_quantity)-1] + 1
                end_round_average[len(end_round_average)-1] = end_round_average[len(end_round_average)-1] + round_sort[j][0]
            elif round_sort[j - 1] != round_sort[j]:
                end_round.append(round_sort[j][0])
                end_round_quantity.append(1)
                end_round_average[len(end_round_average)-1] = end_round_average[len(end_round_average)-1] + round_sort[j][0]
        
        end_round_average[len(end_round_average)-1] = end_round_average[len(end_round_average)-1] / len(round_sort)
        
        # 遊戲結束輪數(長條圖)
        plt.grid(axis='y', ls='--', zorder=0)
        plt.bar(end_round, end_round_quantity, color='#375da1', width=0.4, zorder=10)
        plt.ylim(0,max(end_round_quantity)+20)
        plt.title('遊戲結束輪數(%s)' %table_name, fontproperties=font(fname="resource\\font\\myfont.ttf"), fontsize=15)
        plt.savefig('graph\\遊戲結束輪數(%s).png'%table_name)
        plt.show()

    # 遊戲結束平均輪數(折線圖)
    plt.grid(axis='y', ls='--', zorder=0)
    plt.plot([0,1,2,3,4,5,6,7,8,9,10], end_round_average, color='#375da1', marker='o', zorder=10)
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10], ['0','1','2','3','4','5','6','7','8','9','10'])
    plt.ylim(0,max(end_round_average)+10)
    plt.title('遊戲結束平均輪數', fontproperties=font(fname="resource\\font\\myfont.ttf"), fontsize=15)
    for i in range(len(end_round_average)):
        plt.text(i-0.6,end_round_average[i]+3,end_round_average[i],fontsize=7)
    plt.savefig('graph\\遊戲結束平均輪數.png')
    plt.show()



# 未調整前贏家是否擁有兩倍大土地數量圖(圓餅圖)、贏家是否擁有兩倍大土地數量差距圖(長條圖)、輸家是否擁有兩倍大土地數量差距圖(長條圖)
def winer_loser_land_graph():
    #有兩倍大土地之贏家
    winner_1 = [0] * 11
    #沒有兩倍大土地之贏家
    winner_2 = [0] * 11
    #有兩倍大土地之輸家
    loser_1 = [0] * 11
    #沒有兩倍大土地之輸家
    loser_2 = [0] * 11

    for i in range(11):
        table_name = 'normal'
        if i != 0:
            table_name = table_name + '-%s' %str(i)

        #連結mysql
        connect_db = pymysql.connect(host='localhost', port=3306, user='root', passwd='password', charset='utf8', db='monopoly')

        with connect_db.cursor() as cursor:
            select_player_money = "SELECT `Player1_Money`, `Player2_Money`, `Player3_Money`, `Player4_Money` FROM `%s` WHERE 1" %table_name

            # 執行 SQL 指令
            cursor.execute(select_player_money)
            
            # 提交至 SQL
            connect_db.commit()

            #一千局中玩家的金錢
            player_money = cursor.fetchall()

            select_lend2_owner = "SELECT `Gate_Owner`, `Fountain_Owner`, `Library_Owner`, `Classroom10_Owner`, `Classroom9_Owner` FROM `normal` WHERE 1"

            # 執行 SQL 指令
            cursor.execute(select_lend2_owner)
            
            # 提交至 SQL
            connect_db.commit()

            #一千局中兩倍大土地的擁有者
            lend2_owner = cursor.fetchall()

            select_lend_owner = "SELECT `Path_Owner`, `Restaurant3_Owner`, `Restaurant2_Owner`, `Restaurant1_Owner` FROM `normal` WHERE 1"

            # 執行 SQL 指令
            cursor.execute(select_lend_owner)
            
            # 提交至 SQL
            connect_db.commit()

            #一千局中一般土地的擁有者
            lend_owner = cursor.fetchall()

        # 關閉 SQL 連線
        connect_db.close()

        for j in range(1000):
            winner_list = []
            for k in range(4):
                if player_money[j][k] == max(player_money[j]):
                    if k == 0:
                        winner_list.append('玩家1')
                    elif k == 1:
                        winner_list.append('玩家2')
                    elif k == 2:
                        winner_list.append('玩家3')
                    elif k == 3:
                        winner_list.append('玩家4')
                
            for k in range(len(winner_list)):
                for l in lend2_owner[j]:
                    if winner_list[k] == l:
                        winner_1[i] = winner_1[i] + 1
                        break
                else:
                    continue
                break
            else:
                winner_2[i] = winner_2[i] + 1
            
            loser = ''
            if min(player_money[j]) == 0:
                loser = '玩家1'
            elif min(player_money[j]) == 1:
                loser = '玩家2'
            elif min(player_money[j]) == 2:
                loser = '玩家3'
            elif min(player_money[j]) == 3:
                loser = '玩家4'
            
            for k in lend2_owner[j]:
                if loser == k:
                    loser_1[i] = loser_1[i] + 1
                    break
            else:
                loser_2[i] = loser_2[i] + 1

    #未調整前贏家是否擁有兩倍大土地數量圖(圓餅圖)
    plt.pie([winner_1[0],winner_2[0]], labels=['有2倍大土地','沒有2倍大土地'], textprops={'fontproperties':font(fname="resource\\font\\myfont.ttf"), 'size':13}, autopct='%.1f%%', colors=['#375da1','#a7b5db'])
    plt.title('贏家是否擁有兩倍大土地數量差距圖(未調整)', fontproperties=font(fname="resource\\font\\myfont.ttf"), fontsize=15)
    plt.savefig('graph\\贏家是否擁有兩倍大土地數量差距圖(未調整).png')
    plt.show()

    # 贏家是否擁有兩倍大土地數量差距圖(長條圖)
    x1 = [0.8,1.8,2.8,3.8,4.8,5.8,6.8,7.8,8.8,9.8,10.8]
    x2 = [1,2,3,4,5,6,7,8,9,10,11]
    plt.bar(x1,winner_1,color='#375da1',width=0.4, label='有2倍大土地')
    plt.bar(x2,winner_2,color='#a7b5db',width=0.4, tick_label=['0','1','2','3','4','5','6','7','8','9','10'], align='edge', label='沒有2倍大土地')
    plt.title('贏家是否擁有兩倍大土地數量差距圖', fontproperties=font(fname="resource\\font\\myfont.ttf"), fontsize=15)
    plt.legend(prop=font(fname="resource\\font\\myfont.ttf"))
    for j in x2:
        plt.text(j-0.4,winner_1[j-1]+6,winner_1[j-1],fontsize=7)
    
    plt.text(j,winner_2[j-1]+6,winner_2[j-1],fontsize=7)
    plt.savefig('graph\\贏家是否擁有兩倍大土地數量差距圖.png')
    plt.show()

    # 輸家是否擁有兩倍大土地數量差距圖(長條圖)
    plt.bar(x1,loser_1,color='#375da1',width=0.4, label='有2倍大土地')
    plt.bar(x2,loser_2,color='#a7b5db',width=0.4, tick_label=['0','1','2','3','4','5','6','7','8','9','10'], align='edge', label='沒有2倍大土地')
    plt.ylim(0,max(loser_2)+200)
    plt.title('輸家是否擁有兩倍大土地數量差距圖', fontproperties=font(fname="resource\\font\\myfont.ttf"), fontsize=15)
    plt.legend(prop=font(fname="resource\\font\\myfont.ttf"))
    for j in x2:
        plt.text(j-0.4,loser_1[j-1]+6,loser_1[j-1],fontsize=7)
    
    plt.text(j,loser_2[j-1]+6,loser_2[j-1],fontsize=7)
    plt.savefig('graph\\輸家是否擁有兩倍大土地數量差距圖.png')
    plt.show()



land_winning_percentage_graph()
player_sequence_graph()
all_round_graph()
winer_loser_land_graph()