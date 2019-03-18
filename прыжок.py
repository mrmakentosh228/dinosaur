import pygame

pygame.init()
screen = pygame.display.set_mode((800, 800))


fps = 60
x_pos = 400
y_pos = 400
x_old = x_pos
y_old = y_pos
current_speed = 200/fps
clock = pygame.time.Clock()

def jump_coords(y_position, speed):
    y_position -= speed
    if y_position > 400:
        y_position = 400
        global jump_flag
        jump_flag = False
        global current_speed
        current_speed = 200/fps
    return y_position

running = True
jump_flag = False
g = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                g = True
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_SPACE]:
                g = False
                jump_flag = True
                print(current_speed)
    if g and current_speed <= 16:
        current_speed += 0.2
    elif current_speed > 16:
        current_speed = 200 / fps

    if jump_flag:
        x_old = x_pos
        y_old = y_pos
        y_pos = jump_coords(y_pos, current_speed)
        current_speed -= 20/fps

    screen.fill((0, 0, 0))
    rect_one = pygame.Rect(x_pos, y_pos, 10, 10)
    pygame.draw.rect(screen, (255, 0, 0), rect_one)
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(100, 400 - 16 * 20, 20, 16 * 20), 1)
    if g:
        rect_prog = pygame.Rect(100, 400 - abs(int(current_speed) * 20), 20, abs(int(current_speed) * 20))
        pygame.draw.rect(screen, (255, 255, 255), rect_prog)
    clock.tick(fps)
    pygame.display.flip()
