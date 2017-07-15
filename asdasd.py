import pygame
import time
import random
import sys
import os

pygame.init()

screen=pygame.display.set_mode((700,400), 0, 32)
pygame.display.set_caption('Start Menu')
font1=pygame.font.Font("freesansbold.ttf", 40)

WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,128,0)

count=0
timer=0
blank=15

shuffling=True
done=False

clock=pygame.time.Clock()
curtime=0
psttime=0

screen.fill(WHITE)

nlist=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
loc=[]

for i in range(4):
    for j in range(4):
        loc.append((j*100+50, i*100+50))

def Smove():
    d=random.choice(('u','d','l','r'))
    
    if d == 'u' and not blank in range(4):
        Sm(-4)
    elif d == 'd' and not blank in range(12, 16):
        Sm(4)
    elif d == 'l' and not (blank+1) % 4 == 1:
        Sm(-1)
    elif d == 'r' and not (blank+1) % 4 == 0:
        Sm(1)
    else:
        Smove()

def Sm(num):
    global blank
    
    nlist[blank]=nlist[blank+num]
    nlist[blank+num]=0
    blank+=num

def shuffle(s):
    global count
    for i in range(s):
        Smove()
        
#컴퓨터 플레이 알고리즘 소스

shuffle(100)

puzzle = nlist
answer = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
movecount = 0

def move(puzzle, index):
    newpuzzle = puzzle[:]
    newpuzzle[newpuzzle.index(0)] = newpuzzle[index]
    newpuzzle[index] = 0
    global movecount
    movecount += 1
    return newpuzzle
    
def manhattan(puzzle):
    md = 0
    for i in range(16):
        row1 = i // 4
        col1 = i % 4
        if puzzle[i] != 0:
            row2 = (puzzle[i]-1) // 4
            col2 = (puzzle[i]-1) % 4
        else:
            row2 = 3
            col2 = 3
        md += (abs(row1-row2) + abs(col1-col2))
    return md

class node:
    def __init__(self,puzzle,parent,depth):
        self.puzzle = puzzle
        self.parent = parent
        self.depth = depth
        self.md = manhattan(puzzle)
        self.f = self.depth + self.md
    
start = node(puzzle, None, 0)

def astar(start):
    opened_puzzle = list()
    opened_node = list()
    closed_puzzle = list()
    closed_node = list()

    nowpuzzle = start.puzzle
    
    if nowpuzzle.index(0)%4 != 3:
        opened_puzzle.append(move(start.puzzle, nowpuzzle.index(0)+1))
        nextnode = node(move(start.puzzle, nowpuzzle.index(0)+1),start,1)
        opened_node.append(nextnode)
    if nowpuzzle.index(0)%4 != 0:
        opened_puzzle.append(move(start.puzzle, nowpuzzle.index(0)-1))
        nextnode = node(move(start.puzzle, nowpuzzle.index(0)-1),start,1)
        opened_node.append(nextnode)
    if nowpuzzle.index(0)+4 <= 15:
        opened_puzzle.append(move(start.puzzle, nowpuzzle.index(0)+4))
        nextnode = node(move(start.puzzle, nowpuzzle.index(0)+4),start,1)
        opened_node.append(nextnode)
    if nowpuzzle.index(0)-4 >= 0:
        opened_puzzle.append(move(start.puzzle, nowpuzzle.index(0)-4))
        nextnode = node(move(start.puzzle, nowpuzzle.index(0)-4),start,1)
        opened_node.append(nextnode)
    
    while True:
        F_min = 10000
        minpoint = -1
        for i in range(len(opened_puzzle)):    
            if opened_node[i].f < F_min:
                F_min = opened_node[i].f
                minpoint = i
        closed_node.append(opened_node[minpoint])
        closed_puzzle.append(opened_puzzle[minpoint])
        nowpuzzle = opened_puzzle[minpoint]
        nownode = opened_node[minpoint]
        del opened_node[minpoint]
        del opened_puzzle[minpoint]

        
        if nowpuzzle.index(0)%4 != 3:
            nextnode = node(move(nownode.puzzle, nowpuzzle.index(0)+1),nownode,nownode.depth+1)
            if nextnode.puzzle not in closed_puzzle:
                if nextnode.puzzle not in opened_puzzle:
                    opened_puzzle.append(nextnode.puzzle)
                    nextnode.parent = nownode
                    opened_node.append(nextnode)
                else:
                    oripuzzleindex = opened_puzzle.index(nextnode.puzzle)
                    if opened_node[oripuzzleindex].depth > nextnode.depth:
                        opened_node[oripuzzleindex].parent = nextnode.parent
                        opened_node[oripuzzleindex].depth += 1
        if nowpuzzle.index(0)%4 != 0:
            nextnode = node(move(nownode.puzzle, nowpuzzle.index(0)-1),nownode,nownode.depth+1)
            if nextnode.puzzle not in closed_puzzle:
                if nextnode.puzzle not in opened_puzzle:
                    opened_puzzle.append(nextnode.puzzle)
                    nextnode.parent = nownode
                    opened_node.append(nextnode)
                else:
                    oripuzzleindex = opened_puzzle.index(nextnode.puzzle)
                    if opened_node[oripuzzleindex].depth > nextnode.depth:
                        opened_node[oripuzzleindex].parent = nextnode.parent
                        opened_node[oripuzzleindex].depth += 1
        if nowpuzzle.index(0)+4 <= 15:
            nextnode = node(move(nownode.puzzle, nowpuzzle.index(0)+4),nownode,nownode.depth+1)
            if nextnode.puzzle not in closed_puzzle:
                if nextnode.puzzle not in opened_puzzle:
                    opened_puzzle.append(nextnode.puzzle)
                    nextnode.parent = nownode
                    opened_node.append(nextnode)
                else:
                    oripuzzleindex = opened_puzzle.index(nextnode.puzzle)
                    if opened_node[oripuzzleindex].depth > nextnode.depth:
                        opened_node[oripuzzleindex].parent = nextnode.parent
                        opened_node[oripuzzleindex].depth += 1
        if nowpuzzle.index(0)-4 >= 0:
            nextnode = node(move(nownode.puzzle, nowpuzzle.index(0)-4),nownode,nownode.depth+1)
            if nextnode.puzzle not in closed_puzzle:
                if nextnode.puzzle not in opened_puzzle:
                    opened_puzzle.append(nextnode.puzzle)
                    nextnode.parent = nownode
                    opened_node.append(nextnode)
                else:
                    oripuzzleindex = opened_puzzle.index(nextnode.puzzle)
                    if opened_node[oripuzzleindex].depth > nextnode.depth:
                        opened_node[oripuzzleindex].parent = nextnode.parent
                        opened_node[oripuzzleindex].depth += 1

        for i in range(len(opened_puzzle)):
            if opened_puzzle[i] == answer:
                return opened_node[i]

def start1():       
    finalanswer = astar(start)
    mobum_ans = list()
    passing = list()
    while True:
        mobum_ans.append(finalanswer.puzzle)
        if finalanswer.parent == None:
            break
        finalanswer = finalanswer.parent
    for i in range(len(mobum_ans)):
        for j in range(16):
            if mobum_ans[i][j] == 0:
                passing.append(mobum_ans[i].index(0))
    passing.reverse()
    return passing
#passing이 0의 위치를 나타내는 리스트, 0~15까지의 값이 저장되어있음

#그래픽 소스

def retry(pos):
    if 450<pos[0]<750 and 250<pos[1]<350:
        return True
    return False
            
def timeShow():
    global curtime, psttime
    if not shuffling:
        curtime=time.time()
    t=curtime-psttime
    
    timerText=font1.render(str(round(t, 1)), True, BLACK, WHITE)
    timerRect=timerText.get_rect()
    timerRect.center=(600,50)

    screen.blit(timerText, timerRect)

def show():
    screen.fill(WHITE)
    for i in range(len(nlist)):
        text=font1.render(str(nlist[i]) if str(nlist[i]) != "0" else " ", True, BLACK, WHITE)

        textRect=text.get_rect()
        textRect.center=loc[i]
        screen.blit(text, textRect)
        
    countText=font1.render(str(count), True, BLACK, WHITE)
    countRect=countText.get_rect()
    countRect.center=(600,150)

    timeShow()
    
    screen.blit(countText, countRect)
    
    buttonText=font1.render("RETRY", True, BLACK,GREEN)

    buttonRect=buttonText.get_rect()
    buttonRect.center=(600,300)
    screen.blit(buttonText, buttonRect)

    pygame.display.flip()
    
def checkLocation(point):
    xl=point[0]
    yl=point[1]

    x=int(xl/100)
    y=int(yl/100)

    loc = x+y*4
    if x>4 or y==4 :
        return 0
    return loc

def isnear(num):
    if blank+1 == num or blank-1 == num or blank+4 == num or blank-4 == num:
        return True
    return False

def isFinished():
    if nlist == answer :
        return True
    return False
    
def animation(num, blank):
    n = loc[num]
    b = loc[blank]

    nNum=nlist[num]
    bNum=nlist[blank]

    speed=60
    xd=(b[0]-n[0])/speed
    yd=(b[1]-n[1])/speed
    
    for i in range(speed):
        clock.tick(60)
        pygame.draw.rect(screen, WHITE, [n[0]-50+xd*i, n[1]-50+yd*i, 100, 100], 0)
        text=font1.render(str(nNum), True, BLACK, WHITE)
        textRect=text.get_rect()
        textRect.center=(n[0]+xd*i, n[1]+yd*i)
        
        screen.blit(text, textRect)

        pygame.display.flip()

        timeShow()

def computerPlay():
    global shuffling, count, psttime
    shuffling=False
    psttime=time.time()
    screen=pygame.display.set_mode((700,400), 0, 32)
    pygame.display.set_caption('Sliding Puzzle')

    show()
    s=start1()      

    for i in range(len(s)-1):
        count+=1
        animation(s[i+1], s[i])
        Sm(s[i+1]-s[i])
        show()
        
    shuffling=True
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retry(event.pos):
                    computerPlay()
        show()
    while 1:
        show()

def userPlay():
    screen=pygame.display.set_mode((700,400), 0, 32)
    pygame.display.set_caption('Sliding Puzzle')
    font1=pygame.font.Font("freesansbold.ttf", 50)
    nlist=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
    
    show()
    shuffle(200)
    
    global done, count, shuffling, psttime
    shuffling=False
    psttime=time.time()
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                l=checkLocation(event.pos)
                if isnear(l):
                    count+=1
                    animation(l, blank)
                    Sm(l-blank)
                if retry(event.pos):
                    userPlay()
        if isFinished():
            break
        show()
    while 1:
        show()

def whichButton(pos):
    if 50<pos[0]<150 and 150<pos[1]<250:
        userPlay()
    elif 250<pos[0]<350 and 150<pos[1]<250:
        computerPlay()
        
def startMenu():
    pygame.init()
    screen=pygame.display.set_mode((400,400), 0, 32)
    pygame.display.set_caption('start Menu')

    screen.fill(WHITE)
    
    while 1:
        pygame.draw.rect(screen, RED, [0, 0, 200, 400], 0)
        pygame.draw.rect(screen, GREEN, [200, 0, 200, 400], 0)

        button1Text=font1.render("USER", True, BLACK,RED)
        button1Rect=button1Text.get_rect()
        button1Rect.center=(100,200)
        screen.blit(button1Text, button1Rect)
        
        button2Text=font1.render("ANSWER", True, BLACK,GREEN)
        button2Rect=button2Text.get_rect()
        button2Rect.center=(300,200)
        screen.blit(button2Text, button2Rect)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done=True
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                whichButton(event.pos)
        pygame.display.flip()

startMenu()

pygame.quit()
