import pygame
import random
import os
import ctypes

def force_to_front():
    hwnd = pygame.display.get_wm_info()["window"]
    user32 = ctypes.windll.user32
    # Always on top (-1 = HWND_TOPMOST; 0x0003 = don't move/resize)
    user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0003)
    # Tapping Alt briefly lets SetForegroundWindow get past the focus lock
    user32.keybd_event(0x12, 0, 0, 0)
    user32.SetForegroundWindow(hwnd)
    user32.keybd_event(0x12, 0, 2, 0)

pygame.init()

os.environ["SDL_VIDEO_CENTERED"] = '1'

info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

clock = pygame.time.Clock()

bee_active = False
bee_start_time = 0

def bee_screen():
    global bee_active, bee_start_time

    screen = pygame.display.set_mode(
        (screen_width, screen_height), pygame.RESIZABLE
    )

    bees_img = pygame.image.load('bees.jpg').convert()
    pygame.mixer.Sound("buzzing.mp3").play(maxtime=1000)

    screen.blit(bees_img, (0, 0))
    pygame.display.flip()
    force_to_front()

    bee_active = True
    bee_start_time = pygame.time.get_ticks()


running = True
last_time = 0
chance = 1

while running:
    clock.tick(60)

    current_time = pygame.time.get_ticks()

    # Random event every second
    if current_time - last_time >= 1000:
        if random.randint(1, 100) <= chance and not bee_active:
            bee_screen()

        last_time = current_time

    # Close bee screen after 1 second
    if bee_active and current_time - bee_start_time >= 1000:
        pygame.display.quit()
        pygame.display.init()
        bee_active = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()