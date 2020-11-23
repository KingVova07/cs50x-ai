import pygame
import os



class Player(pygame.sprite.Sprite):

    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.kill()


class map(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = map_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (300,350)

class wins(pygame.sprite.Sprite):

    def __init__(self,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (300,25)

    def update(self):
        self.kill()

class Playagain(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Playagain_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (300,685)

def DRAW(arr):
    for i in range(1,4):
        for j in range(1,4):
            if arr[i][j] == 1:
                sprites.add(Player(i*200-100, j*200-50,playerX_img))
            elif arr[i][j] == -1:
                sprites.add(Player(i*200-100, j*200-50,playerO_img))

def Check():
    for i in range(1,4):
        if arr[i][4] == 3:
            sprites.add(wins(Xwins_img))
            return
        if arr[i][4] == -3:
            sprites.add(wins(Owins_img))
            return
        if arr[4][i] == 3:
            sprites.add(wins(Xwins_img))
            return
        if arr[4][i] == -3:
            sprites.add(wins(Owins_img))
            return
    if arr[4][4] == 3:
        sprites.add(wins(Xwins_img))
        return
    if arr[4][4] == -3:
        sprites.add(wins(Owins_img))
        return
    if arr[4][0] == 3:
        sprites.add(wins(Xwins_img))
        return
    if arr[4][0] == -3:
        sprites.add(wins(Owins_img))
        return
    sprites.add(wins(tie_img))
    return

def Reset():

    global arr
    global cnt
    global firstAI
    global stop
    sprites.update()
    stop = False
    firstAI = 0
    cnt = 0
    arr = [[0] * 5 for i in range(5)]
    #arr = np.arange(25).reshape(5, 5)
    #for i in range(5):
        #for j in range(5):
            #arr[i][j] = 0





def XorO(arr):
    cnt = 0
    for i in range(1, 4):
        for j in range(1, 4):
            if arr[i][j] != 0:
                cnt += 1
    if cnt % 2 == 0:
        return (1)
    return (-1)



def actions(arr):

    cnt = 0
    action = [(0,0)]*9

    for i in range(1,4):
        for j in range(1,4):
            if arr[i][j] == 0:
                action[cnt] = (i,j)
                cnt += 1

    return action[0:cnt]


def Clear(arr, action):
    i, j = action
    flag = arr[i][j]
    if arr[i][j] != 0:
        arr[i][j] = 0
        arr[i][4] -= flag
        arr[4][j] -= flag

        if i == j:
            arr[4][4] -= flag
        if i + j == 4:
            arr[4][0] -= flag
    return arr

def result(arr,action):
    i,j = action
    flag = XorO(arr)
    if arr[i][j] == 0:
        arr[i][j] = flag
        arr[i][4] += flag
        arr[4][j] += flag

        if i == j:
            arr[4][4] += flag
        if i + j == 4:
            arr[4][0] += flag

    return arr


def terminal(arr):
    for i in range(1,4):
        if arr[i][4] == 3:
            return (True)
        if arr[i][4] == -3:
            return (True)
        if arr[4][i] == 3:
            return (True)
        if arr[4][i] == -3:
            return (True)
    if arr[4][4] == 3:
        return (True)
    if arr[4][4] == -3:
        return (True)
    if arr[4][0] == 3:
        return (True)
    if arr[4][0] == -3:
        return (True)
    flag = 0
    for i in range(1,4):
        for j in range(1,4):
            if arr[i][j] == 0:
                flag = 1
                break
    if flag == 0:
        return (True)
    else:
        return (False)



def Utility(arr):

    for i in range(1, 4):
        if arr[i][4] == 3:
            return (1)
        if arr[i][4] == -3:
            return (-1)
        if arr[4][i] == 3:
            return (1)
        if arr[4][i] == -3:
            return (-1)
    if arr[4][4] == 3:
        return (1)
    if arr[4][4] == -3:
        return (-1)
    if arr[4][0] == 3:
        return (1)
    if arr[4][0] == -3:
        return (-1)
    return (0)



def maxvalue(arr):
    if terminal(arr):
        return Utility(arr)
    v = -5
    for action in actions(arr):
        local_arr = arr
        v = max(v,minvalue(result(local_arr,action)))
        Clear(local_arr, action)
    return v



def minvalue(arr):
    if terminal(arr):
        return Utility(arr)
    v = 5

    for action in actions(arr):
        local_arr = arr
        v = min(v,maxvalue(result(local_arr,action)))
        Clear(local_arr,action)

    return v



def AI(arr):
    if firstAI == 1:
        v = -5
        i,j = 0,0

        for action in actions(arr):
            local_arr = arr
            info = minvalue(result(local_arr,action))
            Clear(local_arr, action)
            if v < info:
                v = info
                i,j = action
        return result(arr,(i,j))

    v = 5
    i, j = 0, 0
    moves = actions(arr)

    for action in moves:
        local_arr = arr
        info = maxvalue(result(local_arr, action))
        Clear(local_arr, action)
        if v > info:
            v = info
            i, j = action

    return result(arr, (i, j))



game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
playerX_img = pygame.image.load(os.path.join(img_folder, 'крестик.jpg'))
playerO_img = pygame.image.load(os.path.join(img_folder, 'нолик.jpg'))
Xwins_img = pygame.image.load(os.path.join(img_folder, 'x - wins.jpg'))
Owins_img = pygame.image.load(os.path.join(img_folder, 'o - wins.jpg'))
Playagain_img = pygame.image.load(os.path.join(img_folder, 'Play again.png'))
map_img = pygame.image.load(os.path.join(img_folder, 'карта.jpg'))
tie_img = pygame.image.load(os.path.join(img_folder, 'tie.jpg'))

WIDTH = 600
HEIGHT = 750
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)





pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")
clock = pygame.time.Clock()

sprites = pygame.sprite.Group()
sprites.add(map())
sprites.add(Playagain())

firstAI = 0
cnt = 0
stop = False

arr = [[0] * 5 for i in range(5)]
running = True

while running:
    clock.tick(FPS)
    screen.fill(BLACK)
    flag = XorO(arr)
    #print (flag)

    if terminal(arr):
        stop = True
        Check()

    if firstAI:
        ai = 1
        player = -1
    else:
        ai = -1
        player = 1


    if ai == flag and not stop:
        if cnt == 0:
            arr[2][2] = 1
        else:
            arr = AI(arr)
        cnt += 1
        DRAW(arr)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and cnt == 0:
            firstAI = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                i, j = event.pos
                if i > 125 and i < 475 and j> 645 and j<725:
                    Reset()

                elif j>50 and j<645 and flag == player and not stop:
                    j -= 50
                    i = i // 200 + 1
                    j = j // 200 + 1
                    if (arr[i][j] == 0):
                        arr = result(arr,(i,j))
                        cnt+=1
                        DRAW(arr)






    sprites.draw(screen)
    pygame.display.flip()

pygame.quit()