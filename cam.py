import pygame
import pygame.camera

def img(point: tuple[int,int], cam, display):
    img = cam.get_image()
    display.blit(img, (x,y))