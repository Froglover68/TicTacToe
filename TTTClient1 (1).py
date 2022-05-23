# put everything in function
import socket
import sys
import pygame
import threading

#קלאסים
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostname()
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id = self.client.connect(self.addr)

        print(self.id)

boardreg = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0]]
counter = 1
affirm = ['False', 'False']


#פונקציות

 # clear the whole display === redraw the board again
def BoardWipe(display, exes, circles):
    global boardreg
    global counter
    global affirm
    c = pygame.Color(0, 0, 0)
    display.fill(c)
    circles.clear()
    exes.clear()
    affirm = ['False', 'False']
    for i in range(3):
        for j in range(3):
            boardreg[i][j] = 0
    
    
    
    

    counter = 1

    DRAW(display, exes, circles)

def WhatPos(pos):
    x = pos[0]
    y = pos[1]
    arrpos = [0, 0]
    arrpos[0] = int(x / 100)
    arrpos[1] = int(y / 100)
    try:
        return arrpos
    except:
        print('You cant click there!')

def DRAW(display, exes, circles):
    radius = 30
    width = 300
    height = 300
    black = pygame.Color(0, 0, 0)
    display.fill(black)


    # redraw all circles again (because it was clear line above)
    c = pygame.Color(154, 101, 187)
    for i in circles:
        pygame.draw.circle(display, c, i, radius)
        pygame.draw.circle(display, black, i, radius - 7)
        
        
    for i in exes:
        c = pygame.Color(255,105,180)  # pink
        pygame.draw.line(display, c, (i[0] - 30, i[1] - 30), (i[0] + 30, i[1] + 30), 6)
        pygame.draw.line(display, c, (i[0] - 30, i[1] + 30), (i[0] + 30, i[1] - 30), 6)

    c = pygame.Color(0,0,200)  # pink
    y = 100
    x = 100
    for i in range(0, 2):
        start = (x, 0)
        end = (x, height)
        line_width = 4
        pygame.draw.line(display, c, start, end, line_width)
        x = x + 100
    for i in range(0, 2):
        start = (0, y)
        end = (width, y)
        line_width = 4
        pygame.draw.line(display, c, start, end, line_width)
        y = y + 100
    
    rect = (0, 300, 300, 100)
    pygame.draw.rect(display, c, rect)
    
    pygame.display.update()




def IsGame():
    global counter
    global boardreg
    if counter >= 4:
        if boardreg[0][0] == boardreg[0][1] == boardreg[0][2] != 0:
            return True
        elif boardreg[1][0] == boardreg[1][1] == boardreg[1][2] != 0:
            return True
        elif boardreg[2][0] == boardreg[2][1] == boardreg[2][2] != 0:
            return True
        elif boardreg[0][0] == boardreg[1][0] == boardreg[2][0] != 0:
            return True
        elif boardreg[0][1] == boardreg[1][1] == boardreg[2][1] != 0:
            return True
        elif boardreg[0][2] == boardreg[1][2] == boardreg[2][2] != 0:
            return True
        elif boardreg[0][0] == boardreg [1][1] == boardreg[2][2] != 0:
            return True
        elif boardreg[2][0] == boardreg[1][1] == boardreg[0][2] != 0:
            return True
    return False

def Tie(display):
    global counter
    
    font = pygame.font.SysFont("comicsansms", 32)
    text1 = font.render("Tie!", True, (255, 255, 255))
    c = pygame.Color(0, 0, 0)
    display.fill(c)
    display.blit(text1, (100 - text1.get_width() // 2, 100 - text1.get_height() // 2))
    font = pygame.font.SysFont("comicsansms", 16)
    text1 = font.render("press w to play again", True, (255, 255, 255))
    display.blit(text1, (100 - text1.get_width() // 2, 140 - text1.get_height() // 2))
    pygame.display.update()    

def Waiting_For_Opponent(display):
    font = pygame.font.SysFont("comicsansms", 16)
    text1 = font.render("waiting for opponent...", True, (255, 255, 255))
    display.blit(text1, (100 - text1.get_width() // 2, 160 - text1.get_height() // 2))
    pygame.display.update()
    
def Opponent_Waiting(display):
    font = pygame.font.SysFont("comicsansms", 14)
    text1 = font.render("your opponent wants to reset the game", True, (255, 255, 255))
    display.blit(text1, (100 - text1.get_width() // 2, 160 - text1.get_height() // 2))
    text1 = font.render("press 'w' to accept", True, (255, 255, 255))
    display.blit(text1, (100 - text1.get_width() // 2, 175 - text1.get_height() // 2))
    pygame.display.update()

def TurnFlag(display):
    global p2
    global counter
    rect = (0, 300, 300, 100)
    c = pygame.Color(0,0,200)
    font = pygame.font.SysFont("comicsansms", 32)
    if(IsGame() == True or counter == 10):
        c = pygame.Color(0, 0, 0)
    else:
        c = pygame.Color(0,0,200)
    if((p2 == False and counter % 2 != 0) or(p2 != False and counter % 2 == 0)):
        pygame.draw.rect(display, c, rect)
        text1 = font.render("Your move!", True, (0, 0, 0))
        display.blit(text1, (150 - text1.get_width() // 2, 350 - text1.get_height() // 2))
    else: 
        pygame.draw.rect(display, c, rect)
        text1 = font.render("Oppenent's move!", True, (0, 0, 0))
        display.blit(text1, (150 - text1.get_width() // 2, 350 - text1.get_height() // 2))
    pygame.display.update()


def EndGame(display):
    global boardreg
    global counter
    font = pygame.font.SysFont("comicsansms", 32)
    text1 = font.render("circle win :)", True, (154, 101, 187))
    text2 = font.render("X win :)", True, (255,105,180))
    c = pygame.Color(0, 0, 0)
    display.fill(c)
    if (counter % 2 == 0):
        display.blit(text1, (100 - text1.get_width() // 2, 100 - text1.get_height() // 2))
        font = pygame.font.SysFont("comicsansms", 16)
        text1 = font.render("press w to play again", True, (255, 255, 255))
        display.blit(text1, (100 - text1.get_width() // 2, 140 - text1.get_height() // 2))
        print('Circles win!')
    else:
        display.blit(text2, (100 - text2.get_width() // 2, 100 - text2.get_height() // 2))
        font = pygame.font.SysFont("comicsansms", 16)
        text2 = font.render("press w to play again", True, (255, 255, 255))
        display.blit(text2, (100 - text2.get_width() // 2, 140 - text2.get_height() // 2))
        print('Xs win!')
    pygame.display.update()

def RecieveThread(client, display, exes, circles):
    global counter
    global boardreg  
    global affirm
    global p2
    while True:
        p2pos1 = client.recv(2048).decode('utf-8')
        p2pos = p2pos1.split(",")
        print(p2pos)
        
        
        if (p2pos == ['p2','p2']):
           p2 = True
           print(p2)
          
        
        if (p2pos == ['True', 'True']):
            BoardWipe(display, exes, circles)
        elif (p2pos == ['False', 'True']):
            affirm[1] = 'True'
            Opponent_Waiting(display)
        
        
        
        #if (p2pos == ['w', 'w']):
         #   affirm = True
         #   Opponent_Waiting(display)

            ########################################################
        
        
        try:
            pos = (int(p2pos[0]), int(p2pos[1]))
            
            if boardreg[WhatPos(pos)[0]][WhatPos(pos)[1]] == 0:
                
                boardreg[WhatPos(pos)[0]][WhatPos(pos)[1]] = counter % 2 + 1
                print(counter % 2)
                if counter % 2 != 0:
                    circles.append(pos)
                    counter = counter + 1

                else:
                    exes.append(pos)
                    counter = counter + 1
                print(IsGame())
                DRAW(display, exes, circles)
                if (IsGame() == True): ###############################################################
                    EndGame(display)

            
        except:
            pass
    
def  Send(client, mousex, mousey):
    msg = str(mousex) + "," + str(mousey)
    client.send(msg.encode('utf-8'))
    print(msg)
    
    
    

def main():
    width = 300
    height = 400
    pygame.init()
    # clock = pygame.time.Clock()
    display = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Client_TTT")
    global p2
    global affirm
    global boardreg
    global counter
    circles = []
    exes = []
    p2 = False
    n = Network()
    
    DRAW(display, exes, circles)
    recieve_thread = threading.Thread(target=RecieveThread, args=(n.client, display, exes, circles,))
    recieve_thread.start()
    
    
    while True:
        TurnFlag(display)
        if affirm == ['True', 'True']:
            BoardWipe(display, exes, circles)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("bye")
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    affirm[0] = 'True'
                    Send(n.client, affirm[1], affirm[0])#####
                    
                    Waiting_For_Opponent(display)
                    

                elif event.key == pygame.K_q:
                    print("bye")
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                mousex = event.pos[0]
                mousey = event.pos[1]
                print(p2)
                print(pos, mousex, mousey)
                c = pygame.Color(200, 0, 0)
                pos = (mousex, mousey)
                try:
                    if boardreg[WhatPos(pos)[0]][WhatPos(pos)[1]] == 0:
                        if(p2 == False and counter % 2 != 0):
                            boardreg[WhatPos(pos)[0]][WhatPos(pos)[1]] = counter % 2 + 1
                            print(counter % 2)
                            circles.append(pos)
                            Send(n.client, mousex, mousey)
                            counter = counter + 1
                            print("o appended")

                        if(p2 != False and counter % 2 == 0):
                            boardreg[WhatPos(pos)[0]][WhatPos(pos)[1]] = counter % 2 + 1
                            print(counter % 2)
                            exes.append(pos)
                            Send(n.client, mousex, mousey)
                            counter = counter + 1
                            print("x appended")
                except:
                    print('You cant click there!')
                DRAW(display, exes, circles)
                print("drawing")
                if (IsGame() == True): ###############################################################
                    EndGame(display)
            if (counter == 10 and IsGame() == False):
                Tie(display)
                   





main()
