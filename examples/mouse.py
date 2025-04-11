from textual import events
from textual.app import App, ComposeResult
from textual.widgets import RichLog, Static


class Ball(Static):
    pass


class MouseApp(App):
    DEFAULT_CSS = """
    Screen {
    layers: log ball;
}

RichLog {
    layer: log;
}

Ball {
    layer: ball;
    width: auto;
    height: 1;
    background: $secondary;
    border: tall $secondary;
    color: $background;
    box-sizing: content-box;
    text-style: bold;
    padding: 0 4;
}
    """

    def compose(self) -> ComposeResult:
        yield RichLog()
        yield Ball("Textual")

    def on_mouse_move(self, event: events.MouseMove) -> None:
        self.screen.query_one(RichLog).write(event)
        self.query_one(Ball).offset = event.screen_offset - (8, 2)


if __name__ == "__main__":
    app = MouseApp()
    app.run()
