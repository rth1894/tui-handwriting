import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from prediction import predict
import pygame
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import Screen
from textual.widgets import Button, Footer, Label, Placeholder, Static
import threading


def run_pygame():
    os.environ["SDL_VIDEO_WINDOW_POS"] = "150,300"
    pygame.init()
    screen = pygame.display.set_mode((560, 560))
    font = pygame.font.Font(None, 36)

    running = True
    drawing = False



    while running:
        """
        # reset button
        screen.fill((37, 40, 58), (420, 520, 140, 40))
        pygame.draw.rect(screen, (27, 27, 39), (420, 520, 140, 40), 2)
        text_surface = font.render("Reset", True, (168, 176, 213))
        screen.blit(text_surface, (450, 530))
        """

        # drawing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (420 <= x <= 560) and (520 <= y <= 560):
                    screen.fill((0, 0, 0))
                else:
                    drawing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False
            elif event.type == pygame.MOUSEMOTION and drawing:
                pygame.draw.circle(screen, (255, 255, 255), event.pos, 8)

        pygame.display.flip()

    pygame.quit()


class Header(Placeholder):
    DEFAULT_CSS = """
    Header {
        height: 5;
        dock: top;
        text-style: bold;
        content-align: center middle;
    }
    """


class Main(Screen):
    def compose(self) -> ComposeResult:
        yield Header("[bold white] Handwriting AI")

        with Container(id="exit_container"):
            yield Button("Exit", id="exit")

        with Container(id="thought"):
            yield Button("Process", id="process")
            yield Label("Prediction: ", id="prediction")

        yield Footer()

    @on(Button.Pressed, "#exit")
    def on_exit_pressed(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))  # close pygame
        self.app.exit()



    @on(Button.Pressed, "#process")
    def on_process_pressed(self):
        pygame.image.save(pygame.display.get_surface(), "image.png")
        predictions = predict("image.png")

        prediction = self.query_one("#prediction", Label)

        if predictions:
            result_text = "Predictions:\n"
            for char, confidence in predictions:
                result_text += f"{char}: {confidence * 100:.2f}%\n"
            prediction.update(result_text.strip())
        else:
            prediction.update("Prediction: [Error]")


class MainApp(App):
    CSS = """
    Screen {
        align: center middle;
    }

    .title {
        text-align: right;
        margin-bottom: 1;
    }

    #exit_container {
        width: 100%;
        height: 3;
        margin-top: 2;
        content-align: center middle;
        dock: bottom;
        margin-bottom: 3;
    }

    Button {
        width: auto;
        text-align: center;
    }

    Horizontal {
        width: 100%;
        content-align: center middle;
    }

    #thought {
        margin-top: 10;
        margin-right: 8;
        dock: right;
        width: 50%;
        height: 80%;
        border: solid white;
        padding: 1;
        content-align: center middle;
    }
    """

    def on_mount(self):
        self.theme = "tokyo-night"
        threading.Thread(target=run_pygame, daemon=True).start()

    def on_ready(self):
        self.push_screen(Main())


if __name__ == "__main__":
    app = MainApp()
    app.run()
