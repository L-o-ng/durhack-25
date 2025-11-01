### LIB ###
import pygame
import pygame.camera

### FUNCTION ###
from cam import img

### INIT ###
pygame.init()
pygame.camera.init()
display = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
cam = pygame.camera.Camera(pygame.camera.list_cameras()[0], (640, 480))
cam.start()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    ### Logic Updates ###
    

    ### Graphics Render ###
    pygame.display.flip()
    clock.tick(60)
