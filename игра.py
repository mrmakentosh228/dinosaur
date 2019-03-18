import pygame
import os
import random


pygame.init()
size1 = 800, 800
COLOR = (255, 255, 255)
screen = pygame.display.set_mode(size1)
screen.fill(COLOR)


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def jump_coords(y_position, speed):
    y_position -= speed
    global current_speed
    global jump_flag
    global h
    if y_position > 800 - size:
        y_position = 800 - size
        jump_flag = False
        current_speed = 200 / fps
        h = False
    return y_position


def draw_count():
    font = pygame.font.Font(None, 100)
    text = font.render(str(count), 1, (0, 0, 0))
    text_x = 0
    text_y = 0
    screen.blit(text, (text_x, text_y))




class Dino(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows):
        super().__init__(all_sprites)
        self.im = pygame.transform.scale(load_image('dino.png', -1), (50, 50))
        self.im_reverse = False
        self.add(dino_sprite)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.im
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 800 - size
        self.lvl_life = 500

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.lvl_life -= 1.5
        if self.lvl_life <= 0:
            global game
            game = False
            print(game)
            self.kill()
        # изменяем картинку
        if change_image_dino % 10 == 0 and t and (go_left or go_right):
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            if go_right:
                self.image = self.frames[self.cur_frame]
                if self.im_reverse:
                    self.im = pygame.transform.flip(self.im, True, False)
                    self.im_reverse = False
            elif go_left:
                self.image = pygame.transform.flip(self.frames[self.cur_frame], True, False)
                if not self.im_reverse:
                    self.im = pygame.transform.flip(self.im, True, False)
                    self.im_reverse = True
        elif change_image_dino % 10 == 0 and jump_flag and (go_left or go_right):
            if go_right:
                if self.im_reverse:
                    self.im = pygame.transform.flip(self.im, True, False)
                    self.im_reverse = False
                self.image = self.im
            elif go_left:
                if not self.im_reverse:
                    self.im = pygame.transform.flip(self.im, True, False)
                    self.im_reverse = True
                self.image = self.im
        elif change_image_dino % 10 == 0:
            self.image = self.im
        # проверяем столкновения
        global h
        if pygame.sprite.spritecollideany(self, horizontal_borders) and not h:
            global current_speed
            h = True
            current_speed = -current_speed
        self.rect.x = x_pos
        self.rect.y = y_pos

    def set_life(self):
        self.lvl_life += 100
        if self.lvl_life > 500:
            self.lvl_life = 500

    def get_life(self):
        return self.lvl_life


class Strawberry(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.im = pygame.transform.scale(load_image('str.png', -1), (50, 50))
        self.im_boom = pygame.transform.scale(load_image('boom.png', -1), (50, 50))
        self.im_nom = pygame.transform.scale(load_image('nom.jpg'), (50, 50))
        self.image = self.im
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(size1[0] - 50)
        self.rect.y = random.randrange(size1[1] - 50)
        while pygame.sprite.spritecollideany(self, str_sprite) is not None:
            self.rect.x = random.randrange(size1[0] - 50)
            self.rect.y = random.randrange(size1[1] - 50)
        self.add(str_sprite)
        self.life = 0
        self.fresh = True # свежесть
        self.eaten = False # съеден или нет

    def update(self):
        self.life += 1
        if pygame.sprite.spritecollideany(self, dino_sprite) and not self.eaten and self.fresh:
            global DINO
            global count
            DINO.set_life()
            count += 1
            self.life = 0
            self.eaten = True
        if self.eaten and self.life < 50:
            self.image = self.im_nom
        elif self.eaten and self.life > 50:
            self.kill()
        elif 400 < self.life < 500:
            self.rect = self.rect.move(random.randrange(3) - 1, random.randrange(3) - 1)
        elif 500 < self.life < 570:
            self.image = self.im_boom
            self.fresh = False
        elif self.life >= 570:
            self.kill()

    def getFresh(self):
        return self.fresh


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Zast(pygame.sprite.Sprite):
    im = load_image('over.jpg')
    im1 = pygame.transform.scale(im, (size1[0], size1[1]))

    def __init__(self):
        super().__init__(zast_sprite)
        self.image = Zast.im1
        self.rect = self.image.get_rect()
        self.rect.x = size1[0]
        self.rect.y = size1[1]

    def update(self):
        if self.rect.x > 0 and self.rect.y > 0:
            self.rect.x -= 4
            self.rect.y -= 4


size = 50  # размер динозаврика
fps = 60
count = 0 # счет
x_pos = 400  # координаты динозаврика
y_pos = 800 - size
x_old = x_pos  # старые координаты динозаврика
y_old = y_pos
current_speed = 200 / fps # скорость во время прыжка
clock = pygame.time.Clock()
running = True
game = True # динозаврик живет
h = False # столкнулись ли мы с потолком
jump_flag = False # прыгаем
g = False # увеличиваем прогресс прыжка
t = True # мы на земле
go_right = False # движемся вправо
go_left = False # движемся влево
change_image_dino = 0 # счетчик для анимации динозаврика

all_sprites = pygame.sprite.Group()
dino_sprite = pygame.sprite.Group()
zast_sprite = pygame.sprite.Group()
Zast()
DINO = Dino(pygame.transform.scale(load_image('2x-trex.png', -1), (100, 50)), 2, 1)
str_sprite = pygame.sprite.Group()
for _ in range(4):
    Strawberry()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
Border(0, 0, size1[0], 0)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and t:
                g = True
            if event.key == pygame.K_RIGHT:
                go_right = True
            if event.key == pygame.K_LEFT:
                go_left = True
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_SPACE]:
                g = False
                jump_flag = True
            if event.key in [pygame.K_RIGHT]:
                go_right = False
            if event.key in [pygame.K_LEFT]:
                go_left = False
    # вычисляем координаты по x
    if go_right:
        if x_pos <= size1[0] - size:
            x_pos += 3
    if go_left:
        if x_pos >= 3:
            x_pos -= 3
    # изменение скорости
    if g and current_speed <= 23:
        current_speed += 0.35
    elif current_speed > 23:
        current_speed = 200 / fps
    # вычисление координат по y
    if jump_flag:
        x_old = x_pos
        y_old = y_pos
        y_pos = jump_coords(y_pos, current_speed)
        current_speed -= 20 / fps
    # проверка нулевого положения
    if y_pos != size1[1] - size:
        t = False
    else:
        t = True

    if game:
        screen.fill(COLOR)
        change_image_dino += 1
        if change_image_dino == 100:
            for _ in range(2):
                Strawberry()
        all_sprites.update()
        all_sprites.draw(screen)
        draw_count()
        if change_image_dino >= 100:
            change_image_dino = 0
        # рисуем прогресс
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, size1[1] - 23 * 20, 20, 23 * 20), 1)
        if g and t:
            rect_prog = pygame.Rect(0, size1[1] - abs(int(current_speed) * 20), 20, abs(int(current_speed) * 20))
            pygame.draw.rect(screen, (0, 0, 0), rect_prog)
        # рисуем прогресс жизней
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(size1[0] - (DINO.get_life() // 2), 5, DINO.get_life() // 2, 20))
    else:
        screen.fill(COLOR)
        zast_sprite.update()
        zast_sprite.draw(screen)

    clock.tick(fps)
    pygame.display.flip()
