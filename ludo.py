import turtle
from time import sleep
import random
import math
from tkinter import PhotoImage
from sys import setrecursionlimit
from datetime import datetime
from os import makedirs , path

setrecursionlimit(20000)

#if not (path.exists('.\\Save')):
    #makedirs('.\\Save')

load = False
player = []
for i in range(4):
    while True:
        ans = input('Enter Player:'+str(i+1)+' [C : Computer , P : Player] :').lower()
        if ans in ['p','c']:
            player += [ans]
            break
        else:
            print('Type \"P\" Or \"C\"')

pieces = [ [ [],[],[],[] ],[ [],[],[],[] ],[ [],[],[],[] ],[ [],[],[],[] ] ]

coords = [[ [-173,155.5],[-113,155.5],[-173,95.5],[-113,95.5] ],[ [106,155.5],[166,155.5],[106,95.5],[166,95.5] ],[ [106,-119.5],[166,-119.5],[106,-179.5],[166,-179.5] ],[ [-173,-119.5],[-113,-119.5],[-173,-179.5],[-113,-179.5] ]]

start_coords = [ [-187.33488091290286 , 19.2822763746225],[29.0000000000001,172.5],[183.61772362537752 , -42.017723625377556],[-32.85857864376271 , -195.09402589451776] ]
dice_coords = [ [-102,-142,283.5,243.5 , -122,263.5] , [137,97,283.5,243.5 , 117,263.5] ,[137,97,-268.5,-308.5 , 117,-288.5] , [-102,-142,-268.5,-308.5  , -122,-288.5]]

safe = [1,9,14,22,27,35,40,48]
last = [52,53,54,55,56]
end = []
write_coords = [ [-144,108.5],[135,108.5],[135,-166.5],[-144,-166.5] ]

move_difference = [ ['r','ur','u','r','d','dr','r','d','l','dl','d','l','u','ul','l','u','r'] , ['d','dr','r','d','l','dl','d','l','u','ul','l','u','r','ur','u','r','d'] , ['l','dl','d','l','u','ul','l','u','r','ur','u','r','d','dr','r','d','l'] , ['u','ul','l','u','r','ur','u','r','d','dr','r','d','l','dl','d','l','u']  ]

diff_point = [1,5,6,11,13,18,19,24,26,31,32,37,39,44,45,50,51]

behind_check = [[29,172] , [29,141], [29,111] ,[29,80] , [29,49] , [59,19] , [90,19] , [121,19] , [152,19] , [183,19] , [214,19] , [214,-11] , [214,-42] , [183,-42] , [152,-42] , [121,-42] , [90,-42] , [59,-42] , [29,-72] , [29,-103] , [29,-133] , [29,-164] , [29,-195] , [29,-225] , [-1,-225] , [-32,-225] , [-32,-195] , [-32,-164] , [-32,-133] , [-32,-103] , [-32,-72] , [-63,-42] , [-94,-42] , [-125,-42] , [-156,-42] , [-187,-42] , [-218,-42] , [-218,-11] , [-218,19] , [-187,19] , [-156,19] , [-125,19] , [-94,19] , [-63,19] , [-32,49] , [-32,80]
, [-32,111] , [-32,141] , [-32,172] , [-32,203] , [-1,203] , [29,203] ]

behind_check_move = ['-u','-u','-u','-u','-u',  '-ul'  ,'-l','-l','-l','-l','-l',  '-u','-u'  ,'-r','-r','-r','-r','-r',  '-ur'  ,'-u','-u','-u','-u','-u',  '-r','-r'  ,'-d','-d','-d','-d','-d', '-dr'  ,'-r','-r','-r','-r','-r',  '-d','-d'  ,'-l','-l','-l','-l','-l',  '-dl'  ,'-d','-d','-d','-d','-d',  '-l','-l'  ]

a = 31
b = 30.65
c = 43.3
d = 43.1
dice = 0
turn = random.randint(-1,2)

def safe_image(x,y):
    global pieces , icon
    small_obj = []
    for s in range(4):
        for i in range(4):
            if int(pieces[s][i][0].xcor()) == x and int(pieces[s][i][0].ycor()) == y and pieces[s][i][2] in ['b','t','s','e']:
                small_obj += [s*10 + i]

    place = 0
    length = len(small_obj)
    for k in small_obj:
        s = k//10
        i = k%10

        pieces[s][i][0].hideturtle()
        pieces[s][i][5] += 1

        add = 30/length
        place += add

        smaller = PhotoImage(file=icon[s]).subsample(length, length)
        screen.addshape("pieces[{}][{}]".format(s,i), turtle.Shape("image", smaller))
        pieces[s][i][4].shape("pieces[{}][{}]".format(s,i))
        if pieces[s][4] != 'c' :
            pieces[s][i][4].onclick(object_click)

        pieces[s][i][4].goto(pieces[s][i][0].xcor(),pieces[s][i][0].ycor())
        pieces[s][i][4].setheading(pieces[s][i][0].heading())

        pieces[s][i][4].left(90)

        pieces[s][i][4].forward(15+(15/length))
        pieces[s][i][4].backward(place)
        pieces[s][i][4].showturtle()
        pieces[s][i][4].pensize(add)
    small_obj.clear()

def show_arrow():
    global dice_coords , turn , arrow , no_arrow

    check = ['r','l','l','r']
    if check[turn] == 'r':
        add = 70
    elif check[turn] == 'l':
        add = -70
    arrow.setpos(dice_coords[turn][4] + add,dice_coords[turn][5])
    arrow.setheading(arrow.towards(dice_coords[turn][4],dice_coords[turn][5]))
    arrow.showturtle()

def draw_dice(option,x,y):
    global drawdice
    drawdice.setpos(x,y)
    drawdice.shape('dice'+str(option)+'.gif')
    drawdice.showturtle()

def turn_plus():
    global turn , drawdice , dice_coords , end , dice ,  pieces
    turn += 1
    if turn == 4:
        turn = 0
    while True:
        if turn in end:
            turn += 1
            if turn == 4:
                turn = 0
        else:
            break

    sleep(0)
    drawdice.hideturtle()
    draw_dice(dice,dice_coords[turn][4],dice_coords[turn][5])
    show_arrow()
    if pieces[turn][4] == 'c':
        dice_check(dice_coords[turn][4],dice_coords[turn][5])

def overlap_check():
    global pieces , turn , dice
    tlist = []
    blist = []
    bcheck = []
    tcheck = []
    for s in range(4):
        for i in range(4):
            if pieces[s][i][2] == 't':
                tlist.append([s,i,int(pieces[s][i][0].xcor()),int(pieces[s][i][0].ycor())])
            elif pieces[s][i][2] == 'b':
                blist.append([s,i,int(pieces[s][i][0].xcor()),int(pieces[s][i][0].ycor())])

    if len(tlist) > 0:
        for t in tlist:
            for b in blist:
                if (t[2] == b[2]) and (t[3] == b[3]) and (t[0] != b[0]):
                    bcheck += [b]
                    tcheck += [t]

            if len(bcheck) == 1:
                pieces[bcheck[0][0]][bcheck[0][1]][4].hideturtle()
                pieces[tcheck[0][0]][tcheck[0][1]][4].hideturtle()
                pieces[tcheck[0][0]][tcheck[0][1]][0].showturtle()
                pieces[tcheck[0][0]][tcheck[0][1]][5] += 1

                for m in range(4*(pieces[bcheck[0][0]][bcheck[0][1]][1] - 1) + 1 + pieces[bcheck[0][0]][bcheck[0][1]][5]):
                    pieces[bcheck[0][0]][bcheck[0][1]][0].undo()

                pieces[bcheck[0][0]][bcheck[0][1]][2] = 'h'
                pieces[bcheck[0][0]][bcheck[0][1]][1] = 0
                pieces[bcheck[0][0]][bcheck[0][1]][3] = ''
                pieces[bcheck[0][0]][bcheck[0][1]][5] = 0

                pieces[tcheck[0][0]][tcheck[0][1]][2] = 'n'
                if dice != 6:
                    turn -= 1
            bcheck.clear()
            tcheck.clear()
    tlist.clear()
    blist.clear()

def move(s,i):
    global pieces , dice , move_difference , diff_point , a , b , c , d , end , icon , safe , last , turn , endwriter , write_coords
    if pieces[s][i][2] == 's' or pieces[s][i][2] == 't' or pieces[s][i][2] == 'b':
        pieces[s][i][0].showturtle()
        pieces[s][i][4].hideturtle()
        pieces[s][i][5] += 1

    for m in range(dice):
        if pieces[s][i][1] in diff_point:
            pieces[s][i][3]= move_difference[s][diff_point.index(pieces[s][i][1])]

        if pieces[s][i][3] == 'u':
            pieces[s][i][0].speed(0)
            pieces[s][i][0].setheading(90)
            pieces[s][i][0].speed(1)
            pieces[s][i][0].forward(b)

        elif pieces[s][i][3] == 'd':
            pieces[s][i][0].speed(0)
            pieces[s][i][0].setheading(270)
            pieces[s][i][0].speed(1)
            pieces[s][i][0].forward(b)

        elif pieces[s][i][3] == 'r':
            pieces[s][i][0].speed(0)
            pieces[s][i][0].setheading(0)
            pieces[s][i][0].speed(1)
            pieces[s][i][0].forward(a)

        elif pieces[s][i][3] == 'l':
            pieces[s][i][0].speed(0)
            pieces[s][i][0].setheading(180)
            pieces[s][i][0].speed(1)
            pieces[s][i][0].forward(a)

        elif pieces[s][i][3] == 'dr':
            pieces[s][i][0].speed(0)
            pieces[s][i][0].setheading(315)
            pieces[s][i][0].speed(1)
            pieces[s][i][0].forward(c)
            pieces[s][i][0].setheading(0)
            pieces[s][i][5] += 1

        elif pieces[s][i][3] == 'dl':
            pieces[s][i][0].speed(0)
            pieces[s][i][0].setheading(225)
            pieces[s][i][0].speed(1)
            pieces[s][i][0].forward(d)
            pieces[s][i][0].setheading(270)
            pieces[s][i][5] += 1

        elif pieces[s][i][3] == 'ur':
            pieces[s][i][0].speed(0)
            pieces[s][i][0].setheading(45)
            pieces[s][i][0].speed(1)
            pieces[s][i][0].forward(c)
            pieces[s][i][0].setheading(90)
            pieces[s][i][5] += 1

        elif pieces[s][i][3] == 'ul':
            pieces[s][i][0].speed(0)
            pieces[s][i][0].setheading(135)
            pieces[s][i][0].speed(1)
            pieces[s][i][0].forward(d)
            pieces[s][i][0].setheading(180)
            pieces[s][i][5] += 1

        pieces[s][i][1] += 1

    if pieces[s][i][1] in safe:
        pieces[s][i][2] = 's'
    elif pieces[s][i][1] in last:
        pieces[s][i][2] = 'l'
    elif pieces[s][i][1] != 57:
        pieces[s][i][2] = 'n'

    elif pieces[s][i][1] == 57:
        pieces[s][i][2] = 'e'
        turn -= 1
        e = 0
        for m in range(4):
            if pieces[s][m][1] == 57:
                e += 1
        if e == 4:
            turn += 1
            end.append(s)
            print(icon[s][:-4].upper()+' Player\'s Position : '+str(len(end)))
            endwriter.goto(write_coords[s][0],write_coords[s][1])
            endwriter.pendown()
            endwriter.write(icon[s][:-4].upper()+' Player\'s Position : '+str(len(end)),False,'center')
            endwriter.penup()
            if len(end) == 3:
                print('Since 3 Player Reached End')
                print('Game Ends Here')
                endwriter.goto(0,0)
                endwriter.pendown()
                endwriter.pensize(15)
                endwriter.write('Thanks For Playing',False,'center')
                sleep(2)
                exit()
    for bs in range(4):
        for bi in range(4):
            if pieces[s][i][2] != 's' and (bs != s or bi != i):
                if ( int(pieces[bs][bi][0].xcor()) == int(pieces[s][i][0].xcor()) ) and ( int(pieces[bs][bi][0].ycor()) == int(pieces[s][i][0].ycor()) ):
                    pieces[bs][bi][2] = 'b'
                    pieces[s][i][2] = 't'

def object_click(x,y):
    global pieces , turn , dice , check_to_move , start_coords
    dis = 16
    safe_distance = 16
    bs = 5
    bi = 5
    checkstatus = ''

    if check_to_move == True:
        for i in range(4):
            if pieces[turn][i][0].isvisible() :
                if pieces[turn][i][0].distance(x,y) < dis :
                    bs = turn
                    bi = i
            else:
                if pieces[turn][i][4].distance(x,y) < safe_distance:
                    bs = turn
                    bi = i
                    safe_distance = pieces[turn][i][4].distance(x,y)

        if bs == turn and pieces[bs][bi][1] + dice <= 57:
            if pieces[bs][bi][2] == 'h' and dice == 6:
                
                pieces[bs][bi][0].goto(start_coords[bs][0],start_coords[bs][1])
                if bs == 0 :
                    pieces[bs][bi][0].setheading(0)
                    pieces[bs][bi][3] = 'r'
                elif bs == 1 :
                    pieces[bs][bi][0].setheading(270)
                    pieces[bs][bi][3] = 'd'
                elif bs == 2 :
                    pieces[bs][bi][0].setheading(180)
                    pieces[bs][bi][3] = 'l'
                elif bs == 3 :
                    pieces[bs][bi][0].setheading(90)
                    pieces[bs][bi][3] = 'u'
                pieces[bs][bi][5] += 1
                pieces[bs][bi][1] += 1
                pieces[bs][bi][2] = 's'
                check_to_move = False

                turn -= 1

            elif pieces[bs][bi][2] != 'e' and pieces[bs][bi][2] != 'h':
                checkstatus = pieces[bs][bi][2]
                if (checkstatus in ['s','t','b']):
                    xcor = int(pieces[bs][bi][0].xcor())
                    ycor = int(pieces[bs][bi][0].ycor())
                
                move(bs,bi)
                overlap_check()
                check_to_move = False

                if dice == 6:
                    turn -= 1

            if checkstatus in ['t','b',]:
                overlist = []
                for o in range(4):
                    for p in range(4):
                        if int(pieces[o][p][0].xcor()) == xcor and int(pieces[o][p][0].ycor()) == ycor :
                            overlist += [10*o + p]
                if len(overlist) == 2:
                    for m in overlist:
                        if m//10 != bs:
                            if overlist[math.fabs(overlist.index(m) - 1)]//10 != bs:
                                m = random.choice(overlist)
                            pieces[m//10][m%10][2] == 't'
                            overlap_check()
                            break
                overlist.clear()

            if (pieces[bs][bi][2] in ['s','t','e']):
                safe_image(int(pieces[bs][bi][0].xcor()),int(pieces[bs][bi][0].ycor()))
            if (checkstatus in ['s','t','b']):
                safe_image(xcor,ycor)
            turn_plus()

def dice_check(x,y):
    global turn , dice , pieces , check_to_move , dice_coords , arrow , it , dice_move
    if check_to_move == False:
        if x < dice_coords[turn][0] and x > dice_coords[turn][1] and y < dice_coords[turn][2] and y > dice_coords[turn][3]:
            h = sn = 0
            same_coords_list = []

            arrow.hideturtle()

            dice = random.randint(1,6)

            # dice_animation(dice_coords[turn][4],dice_coords[turn][5])
            draw_dice(dice,dice_coords[turn][4],dice_coords[turn][5])
            for i in range(4):
                if pieces[turn][i][2] == 'h':
                    h += 1
                elif (pieces[turn][i][2] in ['s','n','t','b','l']) and ((pieces[turn][i][1] + dice) <= 57):
                    sn += 1
                    only_piece = i
                    if [int(pieces[turn][i][0].xcor()),int(pieces[turn][i][0].ycor())] not in same_coords_list:
                        same_coords_list.append([int(pieces[turn][i][0].xcor()),int(pieces[turn][i][0].ycor())])

            if h == 4 :
                if dice == 6:
                    check_to_move = True
                
                else:
                    turn_plus()
            elif h > 0 and dice == 6:
                check_to_move = True
                # show_move(1)
            elif sn == 0:
                turn_plus()
                #Dice check here if it goes beyond the 57 and no other move Got
            elif sn == 1 or len(same_coords_list) == 1:
                check_to_move = True
                # show_move(1)
                object_click(pieces[turn][only_piece][0].xcor(),pieces[turn][only_piece][0].ycor())
            else:
                check_to_move = True
                # show_move(1)


screen = turtle.Screen()
screen.title('Ludo')
screen.setup(658,658)
screen.bgpic(".\\board.png")
screen.onscreenclick(dice_check)


icon = ['red.gif','green.gif','yellow.gif','blue.gif']
for i in range(4):
    screen.register_shape(icon[i])

#dicepic = ['dice0.gif','dice1.gif','dice2.gif','dice3.gif','dice4.gif','dice5.gif','dice6.gif']
for i in range(7):
    screen.register_shape('dice'+str(i)+'.gif')

#ALL THE TURTLE OBJECTS :--
for s in range(4):
    for i in range(4):
        pieces[s][i] += [turtle.Turtle()]
        pieces[s][i] += [0]
        pieces[s][i] += ['h']
        pieces[s][i] += ['']
        pieces[s][i] += [turtle.Turtle()]
        pieces[s][i] += [0]
        pieces[s][i][4].hideturtle()
        pieces[s][i][4].penup()
        pieces[s][i][4].speed(0)

        pieces[s][i][0].hideturtle()
        pieces[s][i][0].penup()
        pieces[s][i][0].speed(0)
        pieces[s][i][0].setpos(coords[s][i][0],coords[s][i][1])
        pieces[s][i][0].shape(icon[s])
        if player[s] != 'c':
            pieces[s][i][0].onclick(object_click)
    pieces[s] += player[s]
if load == True :
    pass
for s in range(4):
    for i in range(4):
        pieces[s][i][0].showturtle()
        pieces[s][i][0].speed(1)

#dice on screen
drawdice = turtle.Turtle()
drawdice.hideturtle()
drawdice.speed(0)
drawdice.penup()

adice = turtle.Turtle()
adice.hideturtle()
adice.penup()
adice.speed(0)

arrow = turtle.Turtle()
arrow.hideturtle()
arrow.penup()
arrow.speed(0)
arrow.shape('arrow')

endwriter = turtle.Turtle()
endwriter.hideturtle()
endwriter.penup()
endwriter.speed(0)
endwriter.pensize(5)

circle = turtle.Turtle()
circle.hideturtle()

check_to_move = False
turn_plus()
screen.mainloop()