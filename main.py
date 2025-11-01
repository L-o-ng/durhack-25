### LIB ###
import pygame
import pygame.camera
import pygame_widgets
from pygame_widgets.button import Button

### FUNCTION ###
from cam import img
from stage import Stage, StageManager, Stage1

### INIT ###
pygame.init()
pygame.camera.init()
display = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
cam = pygame.camera.Camera(pygame.camera.list_cameras()[0], (64, 64))
cam.start()

manager = StageManager()
manager.set_stage(Stage1(manager, display))
run = True

### MAIN ###
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False

    manager.draw(display)
    pygame_widgets.update(events)
    pygame.display.flip()

pygame.quit()
raise SystemExit