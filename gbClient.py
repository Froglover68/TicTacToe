# put everything in function
import socket
import sys
import pygame
import threading


# קלאסים
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostname()
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


def what_pos(pos):
    x = pos[0]
    y = pos[1]
    arrpos = [0, 0]
    arrpos[0] = int(x / 100)
    arrpos[1] = int(y / 100)
    return arrpos


def drop_piece(pos):
    global boardreg

    x = int(pos[0] / 100)
    for i in range(5, -1, -1):
        if boardreg[x][i] == 0:
            arrpos = [x, i]
            return arrpos

    return False


def drop_piece_graph(pos):
    x = drop_piece(pos)[0]
    y = drop_piece(pos)[1]
    arrpos = [0, 0]
    arrpos[0] = (x * 100) + 50
    arrpos[1] = (y * 100) + 50
    return arrpos


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


def c4_row():
    global boardreg
    for x in range(6):
        for i in range(3):
            if boardreg[i][x] == boardreg[i + 1][x] == boardreg[i + 2][x] == boardreg[i + 3][x] != 0:
                return True
    return False


def c4_column():
    global boardreg
    for x in range(7):
        for i in range(3):
            if boardreg[x][i] == boardreg[x][i + 1] == boardreg[x][i + 2] == boardreg[x][i + 3] != 0:
                return True


def c4_diagonal():
    global boardreg
    for i in range(4):
        for x in range(3):
            if boardreg[i][x] == boardreg[i + 1][x + 1] == boardreg[i + 2][x + 2] == boardreg[i + 3][x + 3] != 0:
                return True
    for i in range(6,2, -1):
        for x in range(3):
            print(i, x)
            if boardreg[i][x] == boardreg[i - 1][x + 1] == boardreg[i - 2][x + 2] == boardreg[i - 3][x + 3] != 0:
                return True
    return False


def is_game_c4():
    global boardreg
    if c4_column() or c4_row() or c4_diagonal():
        return True
    return False


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
    pygame.display.update()


def waiting_for_opponent(display):
    font = pygame.font.SysFont("comicsansms", 16)
    text1 = font.render("waiting for opponent...", True, (255, 255, 255))
    display.blit(text1, (display.get_width() / 2 - text1.get_width() // 2, 160 - text1.get_height() // 2))
    pygame.display.update()


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


def waiting_for_opponent_menu(display):
    font = pygame.font.SysFont("comicsansms", 32)
    text1 = font.render("Waiting!", True, (255, 255, 255))
    display.blit(text1, (
        display.get_width() / 2 - text1.get_width() // 2, display.get_height() - 50 - text1.get_height() // 2))
    pygame.display.update()


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
        font = pygame.font.SysFont("comicsansms", 16)
        text1 = font.render("press w to play again", True, (255, 255, 255))
        display.blit(text1, (
            display.get_width() / 2 - text1.get_width() // 2, display.get_height() / 3 + 50 - text1.get_height() // 2))
        print('Circles win!')
    else:
        display.blit(text2, (
            display.get_width() / 2 - text2.get_width() // 2, display.get_height() / 3 - text2.get_height() // 2))
        font = pygame.font.SysFont("comicsansms", 16)
        text2 = font.render("press w to play again", True, (255, 255, 255))
        display.blit(text2, (
            display.get_width() / 2 - text2.get_width() // 2, display.get_height() / 3 + 50 - text2.get_height() // 2))
        print('Xs win!')
    pygame.display.update()


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


def RecieveThread(client, display, exes, circles):
    global counter
    global boardreg
    global affirm
    global p2
    global game
    global game_sel
    while True:
        p2pos1 = client.recv(2048).decode('utf-8')
        p2pos = p2pos1.split(",")
        print(p2pos)

        if (p2pos == ['p2', 'p2']):
            p2 = True
            print(p2)

        if (p2pos == ['True', 'True']):
            board_wipe(display, exes, circles)
        elif (p2pos == ['False', 'True']):
            affirm[1] = 'True'
            opponent_waiting(display)
        elif (p2pos == ['False', 'False']):
            affirm = ['False', 'False']
            if (game == 1):
                draw_ttt(display, exes, circles)
            elif (game == 2):
                draw_c4(display)
            else:
                menu_ui(display)

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
            game = 0

        if (game == 1):
            try:
                pos = (int(p2pos[0]), int(p2pos[1]))

                if boardreg[what_pos(pos)[0]][what_pos(pos)[1]] == 0:

                    boardreg[what_pos(pos)[0]][what_pos(pos)[1]] = counter % 2 + 1
                    print(counter % 2)
                    if counter % 2 != 0:
                        circles.append(pos)
                        counter = counter + 1

                    else:
                        exes.append(pos)
                        counter = counter + 1
                    print(is_game_ttt())
                    draw_ttt(display, exes, circles)
                    if (is_game_ttt() == True):  ###############################################################
                        end_game(display)


            except:
                pass
        if (game == 2):
            try:
                pos = (int(p2pos[0]), int(p2pos[1]))

                if boardreg[drop_piece(pos)[0]][drop_piece(pos)[1]] == 0:

                    boardreg[drop_piece(pos)[0]][drop_piece(pos)[1]] = counter % 2 + 1

                    if counter % 2 != 0:
                        circles.append(drop_piece_graph(pos))
                        counter = counter + 1

                    else:
                        exes.append(drop_piece_graph(pos))
                        counter = counter + 1

                    draw_c4(display)
                    if (is_game_c4() == True):  ###############################################################
                        end_game(display)

            except:
                pass


def Send(client, mousex, mousey):
    msg = str(mousex) + "," + str(mousey)
    client.send(msg.encode('utf-8'))


def main():
    width = 300
    height = 400
    pygame.init()

    display = pygame.display.set_mode((width, height))
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

    recieve_thread = threading.Thread(target=RecieveThread, args=(n.client, display, exes, circles,))
    recieve_thread.start()

    while True:
        if (game == 1):
            draw_ttt(display, exes, circles)
            counter = 1
            while (game == 1):
                turn_flag(display)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print("bye")
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:
                            affirm[0] = 'True'
                            Send(n.client, affirm[1], affirm[0])  #####

                            waiting_for_opponent(display)
                            if affirm == ['True', 'True']:
                                board_wipe(display, exes, circles)

                        elif event.key == pygame.K_n:
                            affirm = ['False', 'False']
                            Send(n.client, affirm[1], affirm[0])
                            game_sel = ['TTT', 'TTT']
                            Send(n.client, affirm[1], affirm[0])
                            draw_ttt(display, exes, circles)

                        elif event.key == pygame.K_m:
                            game_sel[0] = 'Menu'
                            Send(n.client, game_sel[0], 0)
                            if (game_sel == ['Menu', 'Menu']):
                                game = 0
                            draw_ttt(display, exes, circles)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        mousex = event.pos[0]
                        mousey = event.pos[1]
                        print(p2)
                        print(pos, mousex, mousey)
                        pos = (mousex, mousey)
                        try:
                            if boardreg[what_pos(pos)[0]][what_pos(pos)[1]] == 0:
                                if (p2 == False and counter % 2 != 0):
                                    boardreg[what_pos(pos)[0]][what_pos(pos)[1]] = counter % 2 + 1
                                    print(counter % 2)
                                    circles.append(pos)
                                    Send(n.client, mousex, mousey)
                                    counter = counter + 1
                                    print("o appended")

                                if (p2 != False and counter % 2 == 0):
                                    boardreg[what_pos(pos)[0]][what_pos(pos)[1]] = counter % 2 + 1
                                    print(counter % 2)
                                    exes.append(pos)
                                    Send(n.client, mousex, mousey)
                                    counter = counter + 1
                                    print("x appended")
                        except:
                            print('You cant click there!')
                        draw_ttt(display, exes, circles)
                        if (is_game_ttt() == True):  ###############################################################
                            end_game(display)
                    if (counter == 10 and is_game_ttt() == False):
                        tie(display)

        elif (game == 2):
            display = pygame.display.set_mode((700, 700))
            draw_c4(display)
            while (game == 2):
                turn_flag(display)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print("bye")
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:
                            affirm[0] = 'True'
                            Send(n.client, affirm[1], affirm[0])  #####
                            waiting_for_opponent(display)
                            if affirm == ['True', 'True']:
                                board_wipe(display, exes, circles)

                        elif event.key == pygame.K_n:
                            affirm = ['False', 'False']
                            Send(n.client, affirm[1], affirm[0])
                            game_sel = ['TTT', 'TTT']
                            Send(n.client, affirm[1], affirm[0])
                            draw_c4(display)

                        elif event.key == pygame.K_m:
                            game_sel[0] = 'Menu'
                            Send(n.client, game_sel[0], 0)
                            if (game_sel == ['Menu', 'Menu']):
                                game = 0
                            draw_c4(display)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        mousex = event.pos[0]
                        mousey = event.pos[1]
                        pos = (mousex, mousey)
                        try:
                            if boardreg[what_pos(pos)[0]][what_pos(pos)[1]] == 0:
                                if (p2 == False and counter % 2 != 0):
                                    boardreg[drop_piece(pos)[0]][drop_piece(pos)[1]] = counter % 2 + 1
                                    circles.append(drop_piece_graph(pos))
                                    Send(n.client, mousex, mousey)
                                    counter = counter + 1

                                if (p2 != False and counter % 2 == 0):
                                    boardreg[drop_piece(pos)[0]][drop_piece(pos)[1]] = counter % 2 + 1
                                    exes.append(drop_piece_graph(pos))
                                    Send(n.client, mousex, mousey)
                                    counter = counter + 1

                        except:
                            pass
                        draw_c4(display)
                        if is_game_c4():
                            end_game(display)
                        if (counter == 43 and is_game_ttt() == False):
                            tie(display)

        elif (game == 0):
            display = pygame.display.set_mode((300, 400))
            menu_ui(display)
            while game == 0:
                if (game_sel == ['C4', 'C4']):
                    game = 2
                if (game_sel == ['TTT', 'TTT']):
                    game = 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print("bye")
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:
                            affirm[0] = 'True'
                            Send(n.client, affirm[1], affirm[0])  #####

                            waiting_for_opponent(display)
                            if affirm == ['True', 'True']:
                                board_wipe(display, exes, circles)

                        elif event.key == pygame.K_n:
                            affirm = ['False', 'False']
                            Send(n.client, affirm[1], affirm[0])
                            menu_ui(display)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        mousex = event.pos[0]
                        mousey = event.pos[1]
                        pos = (mousex, mousey)
                        if ((mousex >= 20 and mousex <= 260) and (mousey >= 100 and mousey <= 200)):
                            game_sel[0] = 'TTT'
                            Send(n.client, game_sel[0], 0)
                            waiting_for_opponent_menu(display)


                        elif ((mousex >= 20 and mousex <= 260) and (mousey >= 210 and mousey <= 310)):
                            game_sel[0] = 'C4'
                            print(game_sel)
                            Send(n.client, game_sel[0], 0)
                            waiting_for_opponent_menu(display)


main()
