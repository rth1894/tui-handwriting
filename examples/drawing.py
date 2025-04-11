from textual import on
from textual_canvas import Canvas
from textual.color import Color
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button, Footer, Static


class Header(Static):
    """App header with a title."""
    DEFAULT_CSS = """
    Header {
        height: 3;
        dock: top;
        content-align: center middle;
    }
    """

    def __init__(self, text: str):
        super().__init__(text)


class DrawingCanvas(Canvas):
    """A custom canvas widget that supports mouse drawing."""

    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.clear_canvas()

    def on_mount(self):
        """Initialize the canvas."""
        self.refresh()

    def on_mouse_move(self, event):
        """Allows drawing on the canvas with the left mouse button."""
        if event.button == 0:
            x, y = event.x, event.y+5
            if 0 <= x < self.width and 0 <= y < self.height:
                self.set_pixel(x, y, Color(255, 255, 255))
                self.refresh()

    def clear_canvas(self):
        """Clears the canvas by setting all pixels to black."""
        for y in range(self.height):
            for x in range(self.width):
                self.set_pixel(x, y, Color(0, 0, 0))  # Set all to black
        self.refresh()


class Main(Screen):
    """Main screen with a drawing canvas and buttons."""

    def compose(self) -> ComposeResult:
        yield Header("🎨 Drawing to Text 🖌️")
        
        with Container():
            self.canvas = DrawingCanvas(50, 20)  # Custom canvas
            yield self.canvas
            yield Button("Clear", id="clear")
            yield Button("Exit", id="exit")

        yield Footer()

    @on(Button.Pressed, "#clear")
    def on_clear_pressed(self):
        """Clears the canvas when 'Clear' is pressed."""
        self.canvas.clear_canvas()

    @on(Button.Pressed, "#exit")
    def on_exit_pressed(self):
        """Exits the application."""
        self.app.exit()


class MainApp(App):
    """Main application class."""

    CSS = "Screen { align: center middle; }"

    def on_ready(self):
        """Runs when the app is ready."""
        self.push_screen(Main())


if __name__ == "__main__":
    app = MainApp()
    app.run()
