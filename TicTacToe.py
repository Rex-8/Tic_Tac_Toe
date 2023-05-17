import pygame
import itertools

#Dimensions
WW = 320 + 20
WH = 320 + 20

#Colours
WHITE = (255,255,255)
GREY  = (128,128,128)
BLACK = (0,0,0)

pygame.init()
win = pygame.display.set_mode((WW,WH))
win.fill(WHITE)
font = pygame.font.SysFont('Calibri bold',165)

bd = ['','','','','','','','','']

def print_bd(bd):
    x_img = font.render('X',True,WHITE)
    o_img = font.render('O',True,WHITE)
    e_img = font.render(' ',True,WHITE)
    d = {'X':x_img,'O':o_img,'':e_img}
    for n in range(len(bd)):
        x = 10 + ((n%3)*110)
        y = 10 + ((n//3)*110)
        pygame.draw.rect(win,GREY,pygame.Rect(x,y,100,100))
        l = d[bd[n]].get_rect()
        l[0] = x+10
        l[1] = y
        win.blit(d[bd[n]],l)

    if check_win(bd) == 'X':
        pygame.draw.rect(win,GREY,pygame.Rect(10,10,320,320))
        l = font.render('X Wins',True,WHITE)
        d = l.get_rect()
        d[0] = 20
        d[1] = 100
        win.blit(l,d)
    elif check_win(bd) == 'O':
        pygame.draw.rect(win,GREY,pygame.Rect(10,10,320,320))
        l = font.render('O Wins',True,WHITE)
        d = l.get_rect()
        d[0] = 20
        d[1] = 100
        win.blit(l,d)
    elif (check_win(bd) == 'None') and (bd.count('')==0):
        pygame.draw.rect(win,GREY,pygame.Rect(10,10,320,320))
        l = font.render('Draw',True,WHITE)
        d = l.get_rect()
        d[0] = 20
        d[1] = 100
        win.blit(l,d)
       
def check_win(bd):
    if (bd[0] == bd[1] == bd[2] == 'X') or (bd[3] == bd[4] == bd[5] == 'X') or (bd[6] == bd[7] == bd[8] == 'X'):return 'X'
    elif (bd[0] == bd[1] == bd[2] == 'O') or (bd[3] == bd[4] == bd[5] == 'O') or (bd[6] == bd[7] == bd[8] == 'O'):return 'O'
    elif (bd[0] == bd[3] == bd[6] == 'X') or (bd[1] == bd[4] == bd[7] == 'X') or (bd[2] == bd[5] == bd[8] == 'X'):return 'X'
    elif (bd[0] == bd[3] == bd[6] == 'O') or (bd[1] == bd[4] == bd[7] == 'O') or (bd[2] == bd[5] == bd[8] == 'O'):return 'O'
    elif (bd[0] == bd[4] == bd[8] == 'X') or (bd[2] == bd[4] == bd[6] == 'X'):return 'X'
    elif (bd[0] == bd[4] == bd[8] == 'O') or (bd[2] == bd[4] == bd[6] == 'O'):return 'O'
    else:return "None"
        

def findsubsets(s, n):
    return list(itertools.combinations(s, n))

#player is always X
def check_per_position(pos,possible_positions):
    l = possible_positions.index(pos)
    possible_positions.remove(pos)
    winrate = [0,0,0]   #X,O,draw
    o_no = (len(possible_positions))//2
    board_pos = findsubsets(possible_positions,o_no)
    for n in board_pos:
        bd1 = bd.copy()
        for t in n:
            bd1[t] = 'O'
        for t in range(9):
            if bd1[t] == '':bd1[t] = 'X'
        d = check_win(bd1)
        if d == 'X':winrate[0]+=1
        elif d == 'O':winrate[1]+=1
        elif d == 'None':winrate[2]+=1
    possible_positions.insert(l,pos)
    return winrate

def next_move():
    global bd
    winrate = {}
    possible_positions = [n for n in range(9) if bd[n]=='']
    for n in possible_positions:
        bd1 = bd.copy()
        bd1[n] = 'X'
        if check_win(bd1) == 'X':
            return n
    
    for n in possible_positions:
        bd1 = bd.copy()
        bd1[n] = 'O'
        if check_win(bd1) == 'O':
            return n
            
    for n in possible_positions:
        winrate[n] = check_per_position(n,possible_positions)
    
    x = 0
    t = possible_positions[0]
    for n in winrate:
        try:
            if x <= (winrate[n][0])/(winrate[n][1]+winrate[n][0]):
                x = (winrate[n][0])/(winrate[n][1]+winrate[n][0])
                t = n
        except:pass
    return t

player = 'X'
l = {(10,110):0,(120,220):1,(230,330):2}
run = True
while run == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if (event.type == pygame.MOUSEBUTTONDOWN) and (player == 'O') and (check_win(bd) == 'None'):
            pos = pygame.mouse.get_pos()
            for n in l:
                if n[0]<pos[0]<n[1]:x = l[n]
                if n[0]<pos[1]<n[1]:y = l[n]
            if bd[int((y*3)+x)] == '':
                bd[int((y*3)+x)] = 'O'
                player = 'X'
        
    if player == 'X' and (check_win(bd)=="None"):
        bd[next_move()] = 'X'
        player = 'O'
    print_bd(bd)
    pygame.display.update()
pygame.quit()