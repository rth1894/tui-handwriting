from textual import on
from textual_canvas import Canvas
from textual.color import Color
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button, Footer, Placeholder

class Header(Placeholder):
    DEFAULT_CSS = """
    Header {
        height: 3;
        dock: top;
    }

    Container {
        height: auto;
        width: auto;
        align: center middle;
    }
    """

class DrawingCanvas(Canvas):

    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.drawing = False
        self.pen_color = Color(255, 0, 0)

    def on_mouse_down(self, event) -> None:
        self.drawing = True
        self.set_pixel(event.x, event.y, self.pen_color)
        self.refresh()

    def on_mouse_up(self, event) -> None:
        self.drawing = False

    def on_mouse_move(self, event) -> None:
        if self.drawing:
            self.set_pixel(event.x-3, event.y-3, self.pen_color)
            self.refresh()

class Main(Screen):
    def compose(self) -> ComposeResult:
        yield Header("Drawing to Text")
        yield DrawingCanvas(120, 120)
        yield Button("Exit", id="exit")
        yield Footer()

    @on(Button.Pressed, "#exit")
    def on_exit_pressed(self):
        self.app.exit()

class MainApp(App):
    def on_mount(self):
        self.theme = "tokyo-night"

    def on_ready(self):
        self.push_screen(Main())

if __name__ == "__main__":
    app = MainApp()
    app.run()

