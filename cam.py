import pygame
import pygame.camera

def img(x, y, cam, display):
    img = cam.get_image()
    display.blit(img, (x,y))