from pygame import *
from random import choice

class Game(sprite.Sprite):
    '''Главный класс с основными параметрами'''
    def __init__(self, imag, x, y, speed):
        self.image = transform.scale(image.load(imag),(39,48))
        super().__init__()
        self.rect = self.image.get_rect()
        self.rect.x = int(x)
        self.rect.y = int(y)
        self.speed = int(speed)
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(Game): # Наибольшая переработка перенос логики из игрового цикла
    '''Класс персонажа наследник Game'''
    def __init__(self, imag, x, y, speed): # Нужно было внести +3 параметра поэтому создал конструктор
        super().__init__(imag, x, y, speed)
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False # Следим касаемся ли платформ
        self.dir = 'r'
        self.imag = imag
        self.pc = 1
        self.pi = ['mario.png','mario_r.png','mario_1.png','mario_1_r.png','mario_2.png','mario_2_r.png','mario_3.png','mario_3_r.png']
        self.i = 1
        self.jump = False

    def move(self, platforms): # Добавление в логику доп обьекта
        global counter
        keys = key.get_pressed()
        # Горизонтальное движение
        self.vel_x = 0
        if keys[K_LEFT] and self.rect.x >= 0: # Пока Убрал  and self.rect.x >= 0
            self.vel_x -= self.speed # Вместо self.rect.x -> self.vel_x
            self.dir = 'l'
            # self.q =1 В новой логике не нужно
        if keys[K_RIGHT] and  self.rect.x <= 650: # делаем if И пока убираю and self.rect.x <= 650
            self.vel_x += self.speed # Анологично 30 строке
            self.dir = 'r'
            #self.q = 1 В новой логике не нужно
        '''elif keys[K_UP] and self.rect.y >= 0:
            self.rect.y -= 10'''
        '''Ниже доп код переработанный переносящий отслеживание в класс гравитацию и прыжок'''
        self.rect.x += self.vel_x # Движение
        # Проверка горизонтальных столкновений
        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                if self.vel_x > 0:
                    self.rect.right = plat.rect.left
                elif self.vel_x < 0:
                    self.rect.left = plat.rect.right
        # Прыжок
        if keys[K_UP] and self.on_ground:
            self.vel_y = -14
            jump.play()
            self.jump = True
            if self.dir == 'r':
                self.imag = 'mario_4_r.png'
            if self.dir == 'l':
                self.imag = 'mario_4.png'
            self.image = transform.scale(image.load(self.imag),(39,48))
        
        # Гравитация
        self.vel_y += 0.5
        self.rect.y += int(self.vel_y)
        # Обновляем состояние для земли
        self.on_ground = False
        # Проверка вертикальных столкновений
        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                if self.vel_y > 0:  # падаем вниз
                    self.rect.bottom = plat.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    self.jump = False
                elif self.vel_y < 0:  # летим вверх
                    self.rect.top = plat.rect.bottom
                    self.vel_y = 0
        
        if self.on_ground and self.vel_x == 0:
            if self.dir == 'r':
                self.imag = 'mario_r.png'
            if self.dir == 'l':
                self.imag = 'mario.png'
            self.image = transform.scale(image.load(self.imag),(39,48))
        '''elif counter == 29 and self.on_ground and self.vel_x != 0 or counter == 59 and self.on_ground and self.vel_x != 0:
            self.pc += 2
            if self.dir == 'l' and self.i == 1:
                self.pc -=1
                self.i = 0
            elif self.dir == 'r' and self.i == 0:
                self.pc +=1
                self.i = 1
            if self.pc == 8:
                self.pc = 0
            if self.pc == 9:
                self.pc = 1
            if self.pc == 10:
                self.pc = 2
            if self.pc == 11:
                self.pc = 3
            self.imag = self.pi[self.pc]
            self.image = transform.scale(image.load(self.imag),(39,48))'''
            
            
            


class Monster(Game):
    def __init__(self, imag, x, y, speed, lx, rx, mn2 = False):
        super().__init__(imag, x, y, speed)
        self.image = transform.scale(image.load(imag),(35,35))
        self.lx = int(lx)
        self.rx = int(rx)
        self.y = 1
        self.dir = 'r'
        self.mn2 = mn2
    def move(self):
        if self.rect.x <= self.lx:
            self.y=1
            if self.mn2:
                self.image = transform.scale(image.load('m2_3.png'),(35,35))
                self.dir = 'r'
        elif self.rect.x >= self.rx:
            self.y=2
            if self.mn2:
                self.image = transform.scale(image.load('m2_1.png'),(35,35))
                self.dir = 'l'
        if self.y==1:
            self.rect.x += self.speed
            
        if self.y==2:
            self.rect.x -= self.speed

            

class Coin(sprite.Sprite):
    '''Класс монеток'''
    def __init__(self):
        super().__init__()
        self.image = transform.scale(image.load('coin.png'),(20,30))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.location = ['60-60','440-260','440-400','45-400','440-100','620-90','240-110','620-250','240-210']
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
        if self.rect.colliderect(player.rect):
            self.loct()
    def loct(self):
        global timer
        if len(self.location) != 0 and timer == True:
            global h
            elm = choice(self.location)
            h = elm
            self.location.remove(elm)
            elm = elm.split('-')
            self.rect.x = int(elm[0])
            self.rect.y = int(elm[1])
        elif len(self.location) != 0:
            elm = choice(self.location)
            h = elm
            self.location.remove(elm)
            elm = elm.split('-')
            self.rect.x = int(elm[0])
            self.rect.y = int(elm[1])
            money.play()
        else:
            global dp
            self.rect.x = -100
            self.rect.y = -100
            dp = ['60-60','440-260','440-400','45-400','440-100','620-90','240-110','620-250','240-210','45-310']
            dp.remove(h)
            door.loct()
            money.play()


class Exit(sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = transform.scale(image.load('door1.png'),(55,70))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.i = 1
    def win(self):
        if self.rect.colliderect(player.rect):
            global run
            global game
            run = False
            gamo.play()
            game = 'win'
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
    def loct(self):
        global dp
        elm = choice(dp)
        dp.remove(elm)
        elm = elm.split('-')
        self.rect.x = int(elm[0])-35/2
        self.rect.y = int(elm[1])-25


class Wall(sprite.Sprite):
    '''Класс стен'''
    def __init__(self,x,y,weidth,heidth,color = (11,244,120)):
        super().__init__()
        self.color = color
        self.width = int(weidth)
        self.heigth = int(heidth)
        self.image = Surface((self.width, self.heigth))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = int(x)
        self.rect.y = int(y)
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))


# Настройки окна
display.set_caption("Mario_2026")
window = display.set_mode((700, 500))
background = transform.scale(image.load('Sky.jpg'), (700, 500))
clock = time.Clock()

run = True
count = 0
counter = 0
dcounter = 1
mcounter = 1
font.init()
font = font.SysFont('Arial', 30)

mixer.init()
mixer.music.load('saundtrek.mp3')
mixer.music.play()
jump = mixer.Sound('jump.mp3')
money = mixer.Sound('money.mp3')
over = mixer.Sound('over.mp3')
gamo = mixer.Sound('gamo.mp3')

# Создание платформ
platforms = [] # Делаем препятствия в списке
earth = Wall(0,450,700,50)
cell = Wall(0,-1,800,1)
plat1 = Wall(580,130,100,30)
plat2 = Wall(400,300,100,30)
plat3 = Wall(20,100,100,30)
plat4 = Wall(200,150,100,30)
plats = Wall(20,350,70,30)
platforms.extend([earth, cell,plats , plat1, plat2, plat3, plat4]) # Переношу платформы в список

timer = True
coin = Coin()
coin.loct()
coin.location.append('45-310')

player = Player('Mario_r.png',30,299,4)
door = Exit(-100,-100)
mn1 = Monster('m1_1.png', 315, 415, 2, 35, 630)
mn2 = Monster('m2_3.png', 455, 80, 2, 135, 640, True)

from time import time
start_time = time()

while run:
    window.blit(background,(0,0))
    for e in event.get():
        keys = key.get_pressed()
        if e.type == QUIT:
            run = False
        if keys[K_q]:
            coin.loct()


    now_time = time()
    timer = 60-int(-1*(start_time - now_time))
    if timer == 0:
        run = False
        game = 'lose'
        over.play()

    # Рисуем
    for plat in platforms:
        plat.reset()

    # Движение и отрисовка игрока
    door.reset()
    door.win()

    player.move(platforms)
    player.reset()
    
    coin.reset()

    mn1.move()
    mn1.reset()
    mn2.move()
    mn2.reset()

    if player.rect.colliderect(mn1.rect) or player.rect.colliderect(mn2.rect):
        over.play()
        run = False
        game = 'lose'

    timer1 = font.render(str(timer),True,(255,0,0))
    window.blit(timer1,(10,10))

    counter += 1
    if counter >= 60:
        dcounter += 1
        if dcounter == 1:
            door.image = transform.scale(image.load('door1.png'),(55,70))
        elif dcounter == 2:
            door.image = transform.scale(image.load('door2.png'),(55,70))
            dcounter = 0
        mcounter += 1
        if mcounter == 1:
            mn1.image = transform.scale(image.load('m1_1.png'),(35,35))
        elif mcounter == 2:
            mn1.image = transform.scale(image.load('m1_2.png'),(35,35))
            mcounter = 0
        if mn2.dir == 'r':
            if mcounter == 0:
                mn2.image = transform.scale(image.load('m2_3.png'),(35,35))
            if mcounter == 1:
                mn2.image = transform.scale(image.load('m2_4.png'),(35,35))
        elif mn2.dir == 'l':
            if mcounter == 0:
                mn2.image = transform.scale(image.load('m2_1.png'),(35,35))
            if mcounter == 1:
                mn2.image = transform.scale(image.load('m2_2.png'),(35,35))

        
        
        counter = 0
    if counter == 9 and player.vel_x != 0 and player.jump == False or counter == 19 and player.vel_x != 0 and player.jump == False or counter == 29 and player.vel_x != 0 and player.jump == False or counter == 39 and player.vel_x != 0 and player.jump == False or counter == 49 and player.vel_x != 0 and player.jump == False or counter == 59 and player.vel_x != 0 and player.jump == False:
        player.pc += 2
        if player.dir == 'l' and player.i == 1:
            player.pc -=1
            player.i = 0
        elif player.dir == 'r' and player.i == 0:
            player.pc +=1
            player.i = 1
        if player.pc == 8:
            player.pc = 0
        if player.pc == 9:
            player.pc = 1
        if player.pc == 10:
            player.pc = 2
        if player.pc == 11:
            player.pc = 3
        player.imag = player.pi[player.pc]
        player.image = transform.scale(image.load(player.imag),(39,48))

        


    clock.tick(60)
    display.update()

mixer.music.stop()
if game == 'lose':
    player.vel_y = -14
    player.image = transform.scale(image.load('mario_5.png'),(39,48))
counter = 0

while game == 'lose':
    window.blit(background,(0,0))

    player.vel_y += 0.5
    player.rect.y += int(player.vel_y)
    
    for plat in platforms:
        plat.reset()
    door.reset()
    player.reset()
    coin.reset()
    mn1.reset()
    mn2.reset()

    counter += 1
    if counter == 45*5:
        break

    clock.tick(45)
    display.update()

while game == 'win':
    window.blit(background,(0,0))

    
    for plat in platforms:
        plat.reset()
    door.reset()
    player.reset()
    coin.reset()
    mn1.reset()
    mn2.reset()

    counter += 1
    if counter == 45*7:
        break

    clock.tick(45)
    display.update()