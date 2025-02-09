import pygame
from random import randint as rand

pygame.init()

RESOLUTION = (0, 0)

screen = pygame.display.set_mode(RESOLUTION)
w, h = screen.get_size()

mapa1 = pygame.Surface(screen.get_size())
mapa2 = pygame.Surface(screen.get_size())

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    # update
    mapa2.fill(BLACK)
    mapa2.set_at((rand(0, w), rand(0, h)), WHITE)
    mapa2.set_at((rand(0, w), rand(0, h)), WHITE)
    mapa2.set_at((rand(0, w), rand(0, h)), WHITE)
    mapa2.set_at((rand(0, w), rand(0, h)), WHITE)
    mapa2.set_at((rand(0, w), rand(0, h)), WHITE)
    mapa2.set_at((rand(0, w), rand(0, h)), WHITE)
    mapa2.set_at((rand(0, w), rand(0, h)), WHITE)
    mapa2.set_at((rand(0, w), rand(0, h)), WHITE)
    mapa2.set_at((rand(0, w), rand(0, h)), WHITE)
    mapa2.set_at((rand(0, w), rand(0, h)), WHITE)

    for x in range(1, w-1):
        for y in range(1, h-1):
            if mapa1.get_at((x, y)) == WHITE:
                continue
            n = sum(
                [
                    1 if mapa1.get_at(pos) == WHITE else 0
                    for pos in [
                        (x  , y-1),
                        (x-1, y  ),
                        (x+1, y  ),
                        (x  , y+1),
                    ]
                ]
            )
            if 0 < n < 4:
                mapa2.set_at((x, y), WHITE)
    
    for x in range(1, w-1):
        for y in range(1, h-1):
            if mapa2.get_at((x, y)) == BLACK:
                continue
            n = sum(
                [
                    1 if mapa2.get_at(pos) == WHITE else 0
                    for pos in [
                        (x-1, y-1),
                        (x, y-1),
                        (x+1, y-1),
                        (x-1, y),
                        (x+1, y),
                        (x-1, y+1),
                        (x, y+1),
                        (x+1, y+1)
                    ]
                ]
            )
            if not n > 2:
                mapa1.set_at((x, y), WHITE)

    # draw
    screen.blit(mapa1)
    pygame.display.flip()

pygame.quit()