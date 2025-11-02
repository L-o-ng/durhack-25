### LIB ###
import pygame
import pygame.camera
import pygame_widgets
from pygame_widgets.button import Button
import base64
import mimetypes
import os
from google import genai
from google.genai import types

def generate_image_from_image(
    surface: pygame.Surface, 
    prompt: str, 
    image_size: str = "1K"
) -> bytes:
    """
    Generate an image using an input image + text prompt.
    
    Args:
        input_image_path: Path to the input image.
        prompt: Text prompt to influence the generated image.
        image_size: Size of the output image ("512x512", "1K", etc.)
    
    Returns:
        Bytes of the generated image.
    """
    buffer = io.BytesIO()
    pygame.image.save(surface, buffer)  # saves as PNG in-memory
    buffer.seek(0)
    image_bytes = buffer.read()
    
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    model = "gemini-2.5-flash-image"

    # Read input image as bytes
    with open(input_image_path, "rb") as f:
        image_bytes = f.read()

    content = [
        types.Content(
            role="user",
            parts=[
                # The text prompt
                types.Part.from_text(text=prompt),
                # The input image
                types.Part.from_image_bytes(data=image_bytes, mime_type="image/png")
            ]
        )
    ]

    config = types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(image_size=image_size),
    )

    # Stream API call and return first valid image
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=content,
        config=config,
    ):
        candidate = chunk.candidates[0] if chunk.candidates else None
        if candidate and candidate.content and candidate.content.parts:
            part = candidate.content.parts[0]
            if part.inline_data and part.inline_data.data:
                return part.inline_data.data  # raw image bytes

    raise RuntimeError("No image returned from Gemini API")

class Stage:
    def __init__(self, manager):
        self.manager = manager
    def handle_event(self, event): pass
    def update(self, dt): pass
    def draw(self, surface): pass

class StageManager:
    def __init__(self):
        self.stage = None
        self.user_image = None
        self.widgets = []
        self.cam = pygame.camera.Camera(pygame.camera.list_cameras()[0], (64,64))

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

        self.display = display
        self.font = pygame.font.SysFont("georgia", 60, bold=True)

        self.bg_color = (200, 215, 215)
        self.text_color = (50, 50, 50)
        self.button_color = (70, 130, 180)
        self.button_hover = (100, 149, 237)

        self.start_btn = Button(
            display,
            515, 355, 250, 90,
            text="Start",
            fontSize=35,
            margin=20,
            textColour=(255, 255, 255),
            inactiveColour=self.button_color,
            hoverColour=self.button_hover,
            pressedColour=(60, 110, 160),
            radius=12,
            onClick=self.next_stage
        )

        manager.register_widget(self.start_btn)
        
    def draw(self, display):
        display.fill(self.bg_color)
        txt = self.font.render("The Ball of Wisdom", True, self.text_color)
        rect = txt.get_rect(center=(display.get_width() // 2, 100))
        display.blit(txt, rect)
    
    def next_stage(self):
        self.manager.clear_widgets()
        self.manager.set_stage(Stage2(self.manager, self.display))

class Stage2(Stage):
    def __init__(self, manager, display):
        super().__init__(manager)
        manager.clear_widgets()
        manager.cam.start()
        self.display = display
        self.font = pygame.font.SysFont("georgia", 60, bold=True)

        self.bg_color = (200, 215, 215)
        self.text_color = (50, 50, 50)
        self.button_color = (70, 130, 180)
        self.button_hover = (100, 149, 237)

        self.capture_btn = Button(
            display,
            515, 600, 250, 90,
            text="Crystallise",
            fontSize=35,
            margin=20,
            textColour=(255, 255, 255),
            inactiveColour=self.button_color,
            hoverColour=self.button_hover,
            pressedColour=(60, 110, 160),
            radius=12,
            onClick=self.next_stage
        )
    
    def draw(self, display):
        display.fill(self.bg_color)
        orb_stand = pygame.transform.scale(pygame.image.load("orb_stand.png").convert_alpha(), (32*8, 32*8))
        orb = pygame.transform.scale(pygame.image.load("orb.png").convert_alpha(), (32*8,32*8))
        cam_img = self.manager.cam.get_image()
        cropped = cam_img.subsurface(((cam_img.get_width() - 128)//2, (cam_img.get_height() - 128)//2, 128, 128))

        display.blit(orb_stand, (300, 280))
        display.blit(orb, (300, 265))
        display.blit(cropped, (364, 313))
    
    def next_stage(self):
        cam_img = self.manager.cam.get_image()
        cropped = cam_img.subsurface(((cam_img.get_width() - 128)//2, (cam_img.get_height() - 128)//2, 128, 128))
        self.manager.user_image = cropped

