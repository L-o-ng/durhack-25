import pygame

pygame.init()

screen = pygame.display.set_mode((1280, 720))

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    ### Logic Updates ###

    screen.fill("white")

    ### Graphics Render ###

    pygame.display.flip()
    clock.tick(60)         