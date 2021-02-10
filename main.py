import pygame
import time
import random

screen_width = 800
screen_height = 600

player_width = 70
player_height = 140
wh = (screen_width, screen_height)

PAUSE_STATUS = False
GAME_SCORE = 0

game_screen = pygame.display.set_mode(wh)

clock = pygame.time.Clock()


def game_init():
    pygame.init()

    pygame.display.set_caption("Camry 3.5 Simulator")


def screen(count, x, y, message_format="Обгонов: %d"):
    font = pygame.font.SysFont("calibri", 25)
    text = font.render(message_format % count, True, (0, 0, 0))
    game_screen.blit(text, (x, y))


def objects(object_x, object_y, object_w, object_h, color):
    pygame.draw.rect(game_screen, color, [object_x, object_y, object_w, object_h])


def border(border_x, border_y, border_w, border_h, color):
    pygame.draw.rect(game_screen, color, [border_x, border_y, border_w, border_h])


def load_sprite(x, y, image_name):
    img = pygame.image.load(image_name)
    game_screen.blit(img, (x, y))


def label(text, font):
    text_surface = font.render(text, True, (0, 0, 0))
    return text_surface, text_surface.get_rect()


def message_display(text):
    main_text = pygame.font.SysFont("calibri", 115)
    text_surface, text_box = label(text, main_text)
    text_box.center = ((screen_width / 2), (screen_height / 2))
    game_screen.blit(text_surface, text_box)

    pygame.display.update()

    time.sleep(2)

    loop()


def crash(x, y):
    car_crash = pygame.image.load("images/bang.png")
    game_screen.blit(car_crash, ((x - 45), (y - 30)))
    crash_sound = pygame.mixer.Sound("music/crash.wav")
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()
    main_text = pygame.font.SysFont("calibri", 100)
    text_surface, text_box = label("Че за суета!", main_text)
    text_box.center = ((screen_width / 2), (screen_height / 4))
    game_screen.blit(text_surface, text_box)

    while True:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                quit()

        click_button("Заново", 150, 250, 100, 50, (0, 255, 0), (0, 255, 0), loop)
        click_button("Выйти", 550, 250, 100, 50, (255, 0, 0), (255, 0, 0), quitgame)

        pygame.display.update()
        clock.tick(15)


def click_button(img, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    press = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(game_screen, ac, (x, y, w, h))
        if press[0] == 1 and action is not None:
            action()

    else:
        pygame.draw.rect(game_screen, ic, (x, y, w, h))

    text = pygame.font.SysFont("calibri", 20)
    text_surface, text_box = label(img, text)
    text_box.center = ((x + (w / 2)), (y + (h / 2)))
    game_screen.blit(text_surface, text_box)


def quitgame():
    pygame.quit()
    quit()


def game_unpause():
    global PAUSE_STATUS
    pygame.mixer.music.unpause()
    PAUSE_STATUS = False


def game_break():
    global PAUSE_STATUS
    pygame.mixer.music.pause()
    while PAUSE_STATUS:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        main_text = pygame.font.SysFont("calibri", 90)
        text_surface, text_box = label("Пауза", main_text)
        text_box.center = ((screen_width / 2), (screen_height / 4))
        game_screen.blit(text_surface, text_box)

        click_button("Продолжить", 150, 250, 100, 50, (0, 255, 0), (0, 255, 0), game_unpause)
        click_button("Выйти", 550, 250, 100, 50, (255, 0, 0), (255, 0, 0), quitgame)

        pygame.display.update()
        clock.tick(15)


def game_menu():
    pygame.mixer.music.load("music/menu.wav")
    pygame.mixer.music.play(-1)

    menu_status = True

    while menu_status:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        game_screen.fill((255, 255, 255))

        main_text = pygame.font.SysFont("calibri", 90)
        text_surface, text_box = label("Camry 3.5 Simulator", main_text)

        load_sprite(0, 0, "images/kamri.jpg")

        text_box.center = ((screen_width / 2), (screen_height / 2))
        game_screen.blit(text_surface, text_box)

        click_button("Старт", 150, 450, 100, 50, (0, 255, 0), (0, 255, 0), loop)
        click_button("Выход", 550, 450, 100, 50, (255, 0, 0), (255, 0, 0), quitgame)

        pygame.display.update()
        clock.tick(15)


def loop():
    global PAUSE_STATUS
    global GAME_SCORE

    pygame.mixer.music.load("music/game.wav")
    pygame.mixer.music.play(-1)

    x = (screen_width * 0.45)
    y = (screen_height * 0.75)

    x_plus = 0

    object_w = 70
    object_h = 140

    object_x_start = random.randrange(100, screen_width - 200)
    object_y_start = -600
    object_speed = 4

    border_y = 0
    border_h = 450
    border_speed = 10

    mash_y_r = 600
    mash_y_l = 300
    tree_h = 600
    bacground_speed = 10

    overtaking = 0

    exit_status = False

    while not exit_status:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    x_plus = -5
                if event.key == pygame.K_RIGHT:
                    x_plus = 5

                if event.key == pygame.K_ESCAPE:
                    PAUSE_STATUS = True
                    game_break()

            if event.type == pygame.KEYUP:
                x_plus = 0
        x += x_plus

        game_screen.fill((255, 255, 255))

        border(150, 0, 20, screen_height, (255, 255, 0))
        border(screen_width - 150, 0, 20, screen_height, (255, 255, 0))

        load_sprite(object_x_start, object_y_start, "images/car.png")
        load_sprite(80, mash_y_l, "images/background.png")
        load_sprite(700, mash_y_r, "images/background.png")
        load_sprite(x, y, "images/npc.png")

        object_y_start += object_speed
        border_y += border_speed
        mash_y_l += bacground_speed
        mash_y_r += bacground_speed

        screen(overtaking, 5, 25)
        screen(object_speed * 60, 5, 50, "Скорость: %d")
        screen(GAME_SCORE, 5, 5, "Всего: %d")

        if x > screen_width - player_width - 150 or x < 150:
            crash(x, y)

        if object_y_start > screen_height:
            object_y_start = 0 - object_h
            object_x_start = random.randrange(170, screen_width - object_w - 150)
            overtaking += 1
            GAME_SCORE += 1
            object_speed += 1 / 20

        if border_y > screen_height:
            border_y = 0 - border_h
            object_speed += 1 / 15

        if mash_y_l > screen_height:
            mash_y_l = 0 - tree_h
            object_speed += 1 / 15

        if mash_y_r > screen_height:
            mash_y_r = 0 - tree_h
            object_speed += 1 / 15

        if y < (object_y_start + object_h) and y + player_height >= object_y_start + object_h:
            if x > object_x_start and x < (object_x_start + object_w) \
                    or x + player_width > object_x_start \
                    and x + player_width < object_x_start + object_w:
                crash(x, y)

        pygame.display.update()
        clock.tick(60)


def main():
    game_init()
    game_menu()
    loop()
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
