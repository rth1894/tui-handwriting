import pygame
import threading
from textual.app import App, ComposeResult
from textual.widgets import Button

# Pygame Drawing Canvas
def run_pygame():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Pygame Freehand Drawing")
    
    running = True
    drawing = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False
            elif event.type == pygame.MOUSEMOTION and drawing:
                pygame.draw.circle(screen, (255, 255, 255), event.pos, 3)
        
        pygame.display.flip()
    
    pygame.quit()

# Textual UI
class MyTextualApp(App):
    def compose(self) -> ComposeResult:
        threading.Thread(target=run_pygame, daemon=True).start()

# Run Textual App
if __name__ == "__main__":
    app = MyTextualApp()
    app.run()

