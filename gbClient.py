
import socket
import sys
import pygame
import threading


# קלאסים
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostname() # THIS IS ONLY THE CASE FOR PLAYING LOCALLY ON THE SAME COMPUTER, IF NOT, YOU NEED TO SWITCH OUT "socket.gethostname()" WITH YOUR DESIRED SERVER'S IPv4 ADRESS
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id = self.client.connect(self.addr)

        print(self.id)


# גלובלים
boardreg = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
counter = 1
affirm = ['False', 'False']
game = 0
game_sel = ['Menu', 'Menu']


# פונקציות

# clear the whole display === redraw the board again
def board_wipe(display, exes, circles):
    global boardreg
    global counter
    global affirm
    global game
    c = pygame.Color(0, 0, 0)
    display.fill(c)
    circles.clear()
    exes.clear()
    affirm = ['False', 'False']
    for i in range(7):
        for j in range(6):
            boardreg[i][j] = 0

    counter = 1
    if game == 1:
        draw_ttt(display, exes, circles)
    elif game == 2:
        draw_c4(display)
    else:
        menu_ui(display)

#What position of the board does the piece go (Tic Tac Toe)
def what_pos(pos):
    x = pos[0]
    y = pos[1]
    arrpos = [0, 0]
    arrpos[0] = int(x / 100)
    arrpos[1] = int(y / 100)
    return arrpos

#What position of the board does the piece go (Connect Four)
def drop_piece(pos):
    global boardreg

    x = int(pos[0] / 100)
    for i in range(5, -1, -1):
        if boardreg[x][i] == 0:
            arrpos = [x, i]
            return arrpos

    return False


#Draw the board (Tic Tac Toe)
def draw_ttt(display, exes, circles):
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
        c = pygame.Color(255, 105, 180)  # pink
        pygame.draw.line(display, c, (i[0] - 30, i[1] - 30), (i[0] + 30, i[1] + 30), 6)
        pygame.draw.line(display, c, (i[0] - 30, i[1] + 30), (i[0] + 30, i[1] - 30), 6)

    c = pygame.Color(0, 0, 200)  # pink
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

#Draw the board (Connect Four)
def draw_c4(display):
    radius = 30
    width = 700
    height = 600
    black = pygame.Color(0, 0, 0)
    display.fill(black)

    for x in range(7):
        for y in range(6):
            if boardreg[x][y] == 1:
                pygame.draw.circle(display, pygame.Color(0, 0, 255), (x * 100 + 50, y * 100 + 50), radius)
            elif boardreg[x][y] == 2:
                pygame.draw.circle(display, pygame.Color(255, 0, 0), (x * 100 + 50, y * 100 + 50), radius)

    c = pygame.Color(250, 250, 255)  # white

    y = 100
    x = 100
    for i in range(0, 6):
        start = (x, 0)
        end = (x, height)
        line_width = 4
        pygame.draw.line(display, c, start, end, line_width)
        x = x + 100
    for i in range(0, 5):
        start = (0, y)
        end = (width, y)
        line_width = 4
        pygame.draw.line(display, c, start, end, line_width)
        y = y + 100

    rect = (0, display.get_height() - 100, display.get_width() - 100, 100)
    pygame.draw.rect(display, c, rect)

    pygame.display.update()

#Decide if the game is over (Tic Tac Toe)
def is_game_ttt():
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
        elif boardreg[0][0] == boardreg[1][1] == boardreg[2][2] != 0:
            return True
        elif boardreg[2][0] == boardreg[1][1] == boardreg[0][2] != 0:
            return True
    return False

#Check all rows for a 4
def c4_row():
    global boardreg
    for x in range(6):
        for i in range(4):
            if boardreg[i][x] == boardreg[i + 1][x] == boardreg[i + 2][x] == boardreg[i + 3][x] != 0:
                return True
    return False

#Check all columns for a 4
def c4_column():
    global boardreg
    for x in range(7):
        for i in range(3):
            if boardreg[x][i] == boardreg[x][i + 1] == boardreg[x][i + 2] == boardreg[x][i + 3] != 0:
                return True

#Check all diagonals for a 4
def c4_diagonal():
    global boardreg
    for i in range(4):#Diagonals going top left to bottom right
        for x in range(3):
            if boardreg[i][x] == boardreg[i + 1][x + 1] == boardreg[i + 2][x + 2] == boardreg[i + 3][x + 3] != 0:
                return True
    for i in range(6,2, -1):#Diagonals going top right to bottom left
        for x in range(3):
            if boardreg[i][x] == boardreg[i - 1][x + 1] == boardreg[i - 2][x + 2] == boardreg[i - 3][x + 3] != 0:
                return True
    return False


def is_game_c4():#Check if the game is over (Connect Four)
    if c4_column() or c4_row() or c4_diagonal():
        return True
    return False

#Display tie screen
def tie(display): 
    global counter

    font = pygame.font.SysFont("comicsansms", 32)
    text1 = font.render("tie!", True, (255, 255, 255))
    c = pygame.Color(0, 0, 0)
    display.fill(c)
    display.blit(text1, (display.get_width() / 2 - text1.get_width() // 2, 100 - text1.get_height() // 2))
    font = pygame.font.SysFont("comicsansms", 16)
    text1 = font.render("press w to play again", True, (255, 255, 255))
    display.blit(text1, (display.get_width() / 2 - text1.get_width() // 2, 140 - text1.get_height() // 2))
    text3 = font.render("press m to return to main menu", True, (255, 255, 255))
    display.blit(text3, (display.get_width() / 2 - 50 - text3.get_width()  // 2, display.get_height() / 3 + 100 - text3.get_height() // 2))
    pygame.display.update()

#Display a waiting for oppoenent sign
def waiting_for_opponent(display):
    font = pygame.font.SysFont("comicsansms", 16)
    text1 = font.render("waiting for opponent...", True, (255, 255, 255))
    display.blit(text1, (display.get_width() / 2 - text1.get_width() // 2, 160 - text1.get_height() // 2))
    pygame.display.update()

#Display an "Opponent waiting" sign
def opponent_waiting(display):
    font = pygame.font.SysFont("comicsansms", 14)
    text1 = font.render("your opponent wants to reset the game", True, (255, 255, 255))
    display.blit(text1,
                 (display.get_width() / 2 - text1.get_width() // 2, display.get_height() / 3 - text1.get_height() // 2))
    text1 = font.render("press 'w' to accept", True, (255, 255, 255))
    display.blit(text1, (
        display.get_width() / 2 - text1.get_width() // 2, display.get_height() / 3 + 30 - text1.get_height() // 2))
    text1 = font.render("press 'n' to decline", True, (255, 255, 255))
    display.blit(text1, (
        display.get_width() / 2 - text1.get_width() // 2, display.get_height() / 3 + 60 - text1.get_height() // 2))
    pygame.display.update()

#Display a waiting for opponent sign (menu)
def waiting_for_opponent_menu(display):
    font = pygame.font.SysFont("comicsansms", 25)
    text1 = font.render("Waiting for oppoenent...", True, (255, 255, 255))
    display.blit(text1, (
        display.get_width() / 2 - text1.get_width() // 2, display.get_height() - 50 - text1.get_height() // 2))
    pygame.display.update()

#Display the turn flag
def turn_flag(display):
    global p2
    global counter
    global game
    rect = (0, display.get_height() - 100, display.get_width(), 100)
    font = pygame.font.SysFont("comicsansms", 32)
    if ((is_game_ttt() or counter == 10) and game == 1):
        c = pygame.Color(0, 0, 0)
    else:
        c = pygame.Color(0, 0, 200)
    if ((p2 == False and counter % 2 != 0) or (p2 != False and counter % 2 == 0)):
        pygame.draw.rect(display, c, rect)
        text1 = font.render("Your move!", True, (0, 0, 0))
        display.blit(text1, (
            display.get_width() / 2 - text1.get_width() // 2, display.get_height() - 50 - text1.get_height() // 2))
    else:
        pygame.draw.rect(display, c, rect)
        text1 = font.render("Oppenent's move!", True, (0, 0, 0))
        display.blit(text1, (
            display.get_width() / 2 - text1.get_width() // 2, display.get_height() - 50 - text1.get_height() // 2))
    pygame.display.update()

#Display victory screen
def end_game(display):
    global boardreg
    global counter
    font = pygame.font.SysFont("comicsansms", 32)
    text1 = font.render("Player 1 win :)", True, (154, 101, 187))
    text2 = font.render("Player 2 win :)", True, (255, 105, 180))
    c = pygame.Color(0, 0, 0)
    display.fill(c)
    if (counter % 2 == 0):
        display.blit(text1, (
            display.get_width() / 2 - text1.get_width() // 2, display.get_height() / 3 - text1.get_height() // 2))
    else:
        display.blit(text2, (
            display.get_width() / 2 - text2.get_width() // 2, display.get_height() / 3 - text2.get_height() // 2))
    font = pygame.font.SysFont("comicsansms", 16)
    text2 = font.render("press w to play again", True, (255, 255, 255))
    display.blit(text2, (display.get_width() / 2 - text2.get_width() // 2, display.get_height() / 3 + 50 - text2.get_height() // 2))
    text3 = font.render("press m to return to main menu", True, (255, 255, 255))
    display.blit(text3, (display.get_width() / 2 - 25 - text2.get_width()  // 2, display.get_height() / 3 + 100 - text2.get_height() // 2))
    pygame.display.update()

#Display the menu 
def menu_ui(display):
    font = pygame.font.SysFont("comicsansms", 32)
    text1 = font.render("PyGame Box", True, (255, 255, 255))
    c = pygame.Color(0, 0, 0)

    text2 = font.render("Tic Tac Toe", True, c)
    text3 = font.render("Connect 4", True, c)

    display.fill(c)
    display.blit(text1, (150 - text1.get_width() // 2, 50 - text1.get_height() // 2))

    c = pygame.Color(0, 0, 255)
    pygame.draw.rect(display, c, pygame.Rect(20, 100, 260, 100))
    display.blit(text2, (150 - text2.get_width() // 2, 150 - text2.get_height() // 2))

    pygame.draw.rect(display, c, pygame.Rect(20, 210, 260, 100))
    display.blit(text3, (150 - text3.get_width() // 2, 260 - text3.get_height() // 2))

    pygame.display.update()

#The recieval thread
def RecieveThread(client, display, exes, circles):
    global counter
    global boardreg
    global affirm
    global p2
    global game
    global game_sel
    while True:
        p2pos1 = client.recv(2048).decode('utf-8') #Recieve message
        p2pos = p2pos1.split(",")
        print(p2pos)

        if (p2pos[0] == 'p2'):
            p2 = True
            print(p2)

        if (p2pos == ['True', 'True']):
            board_wipe(display, exes, circles) #Wipe board
        elif (p2pos == ['False', 'True']):
            affirm[1] = 'True'
            opponent_waiting(display) #display waiting message
        elif (p2pos == ['False', 'False']):
            affirm = ['False', 'False']
            if (game == 1):
                draw_ttt(display, exes, circles) #Switch to TTT
            elif (game == 2):
                draw_c4(display)#Switch to C4
            else:
                menu_ui(display)#Switch to menu

        if (p2pos[0] == 'TTT'):
            game_sel[1] = 'TTT'
        if (game_sel == ['TTT', 'TTT']):
            game = 1
        if (p2pos[0] == 'C4'):
            game_sel[1] = 'C4'
        if (game_sel == ['C4', 'C4']):
            game = 2
        if (p2pos[0] == 'Menu'):
            game_sel[1] = 'Menu'
        if (game_sel == ['Menu', 'Menu']):
            board_wipe(display, exes, circles)
            game = 0

        if (game == 1):
            try:
                pos = (int(p2pos[0]), int(p2pos[1]))

                if boardreg[what_pos(pos)[0]][what_pos(pos)[1]] == 0:

                    boardreg[what_pos(pos)[0]][what_pos(pos)[1]] = counter % 2 + 1
                    print(counter % 2)
                    if counter % 2 != 0:
                        circles.append(pos)#Place opponents piece
                        counter = counter + 1#pass turn

                    else:
                        exes.append(pos)
                        counter = counter + 1
                    print(is_game_ttt())
                    draw_ttt(display, exes, circles)
                    if (is_game_ttt() == True):  
                        end_game(display)


            except:
                pass
        if (game == 2):
            try:
                pos = (int(p2pos[0]), int(p2pos[1]))

                if boardreg[drop_piece(pos)[0]][drop_piece(pos)[1]] == 0:

                    boardreg[drop_piece(pos)[0]][drop_piece(pos)[1]] = counter % 2 + 1 #Place opponents piece
                    counter = counter + 1#pass turn



                    draw_c4(display)
                    if (is_game_c4() == True):  #Show victory screen
                        end_game(display)

            except:
                pass

#Send a message to the other client
def Send(client, mousex, mousey):
    msg = str(mousex) + "," + str(mousey)
    client.send(msg.encode('utf-8'))


def main():
    width = 300
    height = 400
    pygame.init()

    display = pygame.display.set_mode((width, height))#Set window size
    pygame.display.set_caption("Client_PyGamebox")
    global p2
    global affirm
    global boardreg
    global counter
    global game
    global game_sel
    circles = []
    exes = []
    p2 = False
    n = Network()

    recieve_thread = threading.Thread(target=RecieveThread, args=(n.client, display, exes, circles,))#Activate thread
    recieve_thread.start()

    while True:
        if (game == 1):
            draw_ttt(display, exes, circles)#Draw board
            counter = 1
            while (game == 1):
                turn_flag(display)#Draw turn flag
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print("bye")
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w: #Send a board wipe request to other player
                            affirm[0] = 'True'
                            Send(n.client, affirm[1], affirm[0])  #####
                            waiting_for_opponent(display)
                            if affirm == ['True', 'True']:# if accepting request, Wipe board.
                                board_wipe(display, exes, circles)

                        elif event.key == pygame.K_n:
                            affirm = ['False', 'False']# Decline requests
                            Send(n.client, affirm[1], affirm[0])
                            game_sel = ['TTT', 'TTT']
                            Send(n.client, affirm[1], affirm[0])
                            draw_ttt(display, exes, circles)

                        elif event.key == pygame.K_m: #Request to return to main menu
                            game_sel[0] = 'Menu'
                            Send(n.client, game_sel[0], 0)
                            if (game_sel == ['Menu', 'Menu']):# if accepting request, wipe board, and return to menu.
                                board_wipe(display, exes, circles)
                                game = 0
                            draw_ttt(display, exes, circles)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        mousex = event.pos[0]
                        mousey = event.pos[1]
                        print(p2)
                        print(pos, mousex, mousey)
                        pos = (mousex, mousey)# Save mouse location
                        try:
                            if boardreg[what_pos(pos)[0]][what_pos(pos)[1]] == 0  and is_game_ttt() == False: #Check if game is ongoing and if the space is open for a piece
                                if (p2 == False and counter % 2 != 0):#Check if its your turn
                                    boardreg[what_pos(pos)[0]][what_pos(pos)[1]] = counter % 2 + 1#Place your piece on the board
                                    circles.append(pos)
                                    Send(n.client, mousex, mousey)#Send placement to other client
                                    counter = counter + 1#Procced to next turn
                                    print("o appended")

                                if (p2 != False and counter % 2 == 0):#Same as above
                                    boardreg[what_pos(pos)[0]][what_pos(pos)[1]] = counter % 2 + 1
                                    print(counter % 2)
                                    exes.append(pos)
                                    Send(n.client, mousex, mousey)
                                    counter = counter + 1
                                    print("x appended")
                        except:
                            print('You cant click there!')
                        draw_ttt(display, exes, circles)#Redraw board
                        if (is_game_ttt() == True): #If the game is over, display victory screen.
                            end_game(display)
                    if (counter == 10): #If the board is full and victory wasnt reached, display tie screen
                        tie(display)

        elif (game == 2):
            display = pygame.display.set_mode((700, 700)) #Change screen size
            draw_c4(display) #Draw board
            while (game == 2):
                turn_flag(display)#Draw turn flag
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print("bye")
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:
                            affirm[0] = 'True'
                            Send(n.client, affirm[1], affirm[0])   #Send a board wipe request to other player
                            waiting_for_opponent(display)
                            if affirm == ['True', 'True']:
                                board_wipe(display, exes, circles)# if accepting request, Wipe board.

                        elif event.key == pygame.K_n: # Decline requests
                            affirm = ['False', 'False']
                            Send(n.client, affirm[1], affirm[0])
                            game_sel = ['TTT', 'TTT']
                            Send(n.client, affirm[1], affirm[0])
                            draw_c4(display)

                        elif event.key == pygame.K_m: #Request to return to main menu
                            game_sel[0] = 'Menu'
                            Send(n.client, game_sel[0], 0)
                            if (game_sel == ['Menu', 'Menu']):
                                board_wipe(display, exes, circles)# if accepting request, wipe board, and return to menu.
                                game = 0
                            draw_c4(display)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        mousex = event.pos[0]
                        mousey = event.pos[1]
                        pos = (mousex, mousey)# Save mouse location
                        try:
                            if boardreg[what_pos(pos)[0]][what_pos(pos)[1]] == 0 and is_game_c4() == False: #Check if game is ongoing and if the space is open for a piece
                                if (p2 == False and counter % 2 != 0):#Check if its your turn
                                    boardreg[drop_piece(pos)[0]][drop_piece(pos)[1]] = counter % 2 + 1 #Place your piece on the board
                                    Send(n.client, mousex, mousey)#Send placement to other client
                                    counter = counter + 1 #Procced to next turn

                                if (p2 != False and counter % 2 == 0):#Same as above
                                    boardreg[drop_piece(pos)[0]][drop_piece(pos)[1]] = counter % 2 + 1
                                    Send(n.client, mousex, mousey)
                                    counter = counter + 1

                        except:
                            pass
                        draw_c4(display)#Redraw board
                        if is_game_c4():
                            end_game(display)#If the game is over, display victory screen.
                        if (counter == 43 and is_game_ttt() == False):#If the board is full and victory wasnt reached, display tie screen
                            tie(display)

        elif (game == 0):
            display = pygame.display.set_mode((300, 400))#Change screen size
            menu_ui(display)#Draw menu
            while game == 0:
                if (game_sel == ['C4', 'C4']):
                    game = 2 #Change to Connect Four
                if (game_sel == ['TTT', 'TTT']):
                    game = 1#Change to Tic Tac Toe
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print("bye")
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:
                            affirm[0] = 'True'
                            Send(n.client, affirm[1], affirm[0])  #Send a board wipe request to other player

                            waiting_for_opponent(display)
                            if affirm == ['True', 'True']:# if accepting request, Wipe board.
                                board_wipe(display, exes, circles)

                        elif event.key == pygame.K_n:
                            affirm = ['False', 'False']# Decline requests
                            Send(n.client, affirm[1], affirm[0])
                            menu_ui(display)
                        elif event.key == pygame.K_m:#Request to return to main menu (For debugging) 
                            game_sel[0] = 'Menu'
                            Send(n.client, game_sel[0], 0)    
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        mousex = event.pos[0]
                        mousey = event.pos[1]
                        pos = (mousex, mousey)# Save mouse location
                        if ((mousex >= 20 and mousex <= 260) and (mousey >= 100 and mousey <= 200)): #If clicked top button, request a switch to Tic Tac Toe
                            game_sel[0] = 'TTT'
                            Send(n.client, game_sel[0], 0)
                            waiting_for_opponent_menu(display)


                        elif ((mousex >= 20 and mousex <= 260) and (mousey >= 210 and mousey <= 310)):#If clicked bottom button, request a switch to Connect Four
                            game_sel[0] = 'C4'
                            print(game_sel)
                            Send(n.client, game_sel[0], 0)
                            waiting_for_opponent_menu(display)


main()
