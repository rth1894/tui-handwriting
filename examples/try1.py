from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Static, Footer
from textual.color import Color
from textual.events import Key


class DrawingCanvas(Static):
    """A simple text-based drawing canvas."""

    def __init__(self, width: int, height: int, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.height = height
        self.canvas = [[" " for _ in range(width)] for _ in range(height)]  # Blank space
        self.cursor_x = width // 2  # Start cursor at center
        self.cursor_y = height // 2
        self.update_canvas()

    def draw_at_cursor(self):
        """Draw `@` at the cursor position."""
        self.canvas[self.cursor_y][self.cursor_x] = "@"
        self.update_canvas()

    def move_cursor(self, dx: int, dy: int):
        """Move the cursor while staying within bounds."""
        self.cursor_x = max(0, min(self.width - 1, self.cursor_x + dx))
        self.cursor_y = max(0, min(self.height - 1, self.cursor_y + dy))
        self.update_canvas()

    def clear_canvas(self):
        """Clear the entire canvas (except the cursor)."""
        self.canvas = [[" " for _ in range(self.width)] for _ in range(self.height)]
        self.update_canvas()

    def render_canvas(self) -> str:
        """Render the canvas as a text-based drawing area."""
        canvas_str = ""
        for y in range(self.height):
            for x in range(self.width):
                if x == self.cursor_x and y == self.cursor_y:
                    canvas_str += "█"  # Cursor symbol
                else:
                    canvas_str += self.canvas[y][x]
            canvas_str += "\n"
        return canvas_str

    def update_canvas(self):
        """Update the widget display with the latest canvas."""
        self.update(f"[bold magenta]Drawing Mode:[/]\n```\n{self.render_canvas()}\n```")


class Main(Screen):
    """Main screen containing the interactive drawing interface."""

    def compose(self) -> ComposeResult:
        yield Static("[bold cyan]Use ARROW KEYS to move, SPACE to draw, C to clear, Q to quit.[/]")
        with Container():
            self.canvas = DrawingCanvas(30, 15)
            yield self.canvas
        yield Footer()

    def on_key(self, event: Key):
        """Handle keyboard input for drawing."""
        if event.key == "up":
            self.canvas.move_cursor(0, -1)
        elif event.key == "down":
            self.canvas.move_cursor(0, 1)
        elif event.key == "left":
            self.canvas.move_cursor(-1, 0)
        elif event.key == "right":
            self.canvas.move_cursor(1, 0)
        elif event.key == "space":
            self.canvas.draw_at_cursor()
        elif event.key.lower() == "c":
            self.canvas.clear_canvas()
        elif event.key.lower() == "q":
            self.app.exit()


class DrawingApp(App):
    """Main drawing application."""

    def on_ready(self):
        self.push_screen(Main())


if __name__ == "__main__":
    app = DrawingApp()
    app.run()
