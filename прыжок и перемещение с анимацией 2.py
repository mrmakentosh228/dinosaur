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

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
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


class Strawberry(pygame.sprite.Sprite):
    pass


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



size = 50  # размер динозаврика
fps = 60
x_pos = 400  # координаты динозаврика
y_pos = 800 - size
x_old = x_pos  # старые координаты динозаврика
y_old = y_pos
current_speed = 200 / fps # скорость во время прыжка
clock = pygame.time.Clock()
running = True
h = False # столкнулись ли мы с потолком
jump_flag = False # прыгаем
g = False # увеличиваем прогресс прыжка
t = True # мы на земле
go_right = False # движемся вправо
go_left = False # движемся влево
change_image_dino = 0 # счетчик для анимации динозаврика

all_sprites = pygame.sprite.Group()

dino_sprite = pygame.sprite.Group()
dino = Dino(pygame.transform.scale(load_image('2x-trex.png', -1), (100, 50)), 2, 1)
str_sprite = pygame.sprite.Group()
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

    screen.fill(COLOR)
    change_image_dino += 1
    all_sprites.update()
    all_sprites.draw(screen)
    if change_image_dino == 10:
        change_image_dino = 0
    # рисуем прогресс
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, size1[1] - 23 * 20, 20, 23 * 20), 1)
    if g and t:
        rect_prog = pygame.Rect(0, size1[1] - abs(int(current_speed) * 20), 20, abs(int(current_speed) * 20))
        pygame.draw.rect(screen, (0, 0, 0), rect_prog)
    clock.tick(fps)
    pygame.display.flip()
