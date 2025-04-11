from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.reactive import Reactive

class DrawingCanvas(Static):
    """A simple text-based drawing canvas."""

    canvas_data: Reactive[str] = Reactive("")

    def __init__(self, width: int, height: int):
        super().__init__()
        self.width = width
        self.height = height
        self.canvas = [[" " for _ in range(width)] for _ in range(height)]  # Store drawing data
        self.update_canvas()

    def update_canvas(self):
        """Convert the internal canvas to a string and update the display."""
        self.canvas_data = "\n".join("".join(row) for row in self.canvas)
        self.update(self.canvas_data)

    def on_mouse_move(self, event):
        """Draw on the canvas when the left mouse button is pressed."""
        if event.button == 0:  # Left click
            x, y = event.x, event.y
            if 0 <= x < self.width and 0 <= y < self.height:
                self.canvas[y][x] = "#"  # Update the canvas data
                self.update_canvas()

class DrawingApp(App):
    BINDINGS = [("q", "quit", "Quit")]

    def on_mount(self):
        self.theme = "tokyo-night"

    def compose(self) -> ComposeResult:
        yield Header()
        yield DrawingCanvas(50, 20)  # Our custom text-based canvas
        yield Footer()

if __name__ == "__main__":
    DrawingApp().run()
