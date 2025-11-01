### LIB ###
import pygame
import pygame.camera
import pygame_widgets
from pygame_widgets.button import Button

class Stage:
    def __init__(self, manager):
        self.manager = manager
    def handle_event(self, event): pass
    def update(self, dt): pass
    def draw(self, surface): pass

class StageManager:
    def __init__(self):
        self.stage = None
        self.widgets = []

    def set_stage(self, stage):
        self.stage = stage
    
    def clear_widgets(self):
        for w in self.widgets:
            w.hide()
        self.widgets.clear()

    def register_widget(self, w):
        self.widgets.append(w)

    def draw(self, display):
        self.stage.draw(display)
        print(self.widgets)

class Stage1(Stage):
    def __init__(self, manager, display):
        super().__init__(manager)
        manager.clear_widgets()
        self.font = pygame.font.SysFont(None, 60)

        self.start_btn = Button(
            display,
            300, 20, 200, 80,
            text="Start",
            fontSize=40,
            onClick=lambda: self.manager.set_stage(Stage2)
        )
        self.manager.register_widget(self.start_btn)
        
    def draw(self, display):
        display.fill((30, 30, 30))
        txt = self.font.render("Stage 1", True, (255, 255, 255))
        display.blit(txt, (330, 15))

class Stage2(Stage):
    def __init__(self, manager):
        pass
