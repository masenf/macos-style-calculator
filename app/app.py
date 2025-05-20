import reflex as rx
from app.components.calculator import calculator_ui


def index() -> rx.Component:
    return rx.el.div(
        calculator_ui(),
        class_name="min-h-screen bg-neutral-900 flex items-center justify-center p-4",
    )


app = rx.App(
    theme=rx.theme(
        appearance="light", accent_color="orange"
    )
)
app.add_page(index, title="MacOS Calculator")