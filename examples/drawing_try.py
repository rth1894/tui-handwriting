from textual import on
from textual_canvas import Canvas
from textual.color import Color
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Placeholder, Button, Footer, DataTable, Static, Input

class Header(Placeholder):
    DEFAULT_CSS = """
    Header {
        height: 3;
        dock: top;
    }

    Container {
    align: center middle;
    border: wide gray;
    }

    """

class Main(Screen):
    def compose(self) -> ComposeResult:
        yield Header("Drawing to Text")
        # yield Button("", id="")
        with Container():
            yield Canvas(50, 50)
            yield Button("Exit", id="exit")
        yield Footer()

    def on_mount(self):
        canvas = self.query_one(Canvas)
        canvas.set_pixel(20,20, Color(255,0,0))

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


"""
back:
on_presed(slef):
    self.app.pop_screen()
"""
