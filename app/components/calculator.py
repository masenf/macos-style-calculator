import reflex as rx
from app.state import CalculatorState


def calculator_button(
    text: str | rx.Component,
    on_click_event,
    style_class: str,
    span_cols: int = 1,
) -> rx.Component:
    return rx.el.button(
        text,
        on_click=on_click_event,
        class_name=f"{style_class} rounded-full aspect-square text-2xl font-medium focus:outline-none transition-colors duration-150 ease-in-out flex items-center justify-center active:brightness-125 {rx.cond(span_cols > 1, 'col-span-' + str(span_cols), '')}",
        type="button",
    )


def calculator_ui() -> rx.Component:
    button_style_light_gray = (
        "bg-neutral-500 text-white hover:bg-neutral-400"
    )
    button_style_dark_gray = (
        "bg-neutral-700 text-white hover:bg-neutral-600"
    )
    button_style_orange = (
        "bg-orange-500 text-white hover:bg-orange-400"
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                class_name="w-3 h-3 bg-red-500 rounded-full"
            ),
            rx.el.div(
                class_name="w-3 h-3 bg-yellow-500 rounded-full"
            ),
            rx.el.div(
                class_name="w-3 h-3 bg-green-500 rounded-full"
            ),
            class_name="flex space-x-2 p-3",
        ),
        rx.el.div(
            rx.el.p(
                CalculatorState.expression,
                class_name="text-neutral-400 text-xl h-7 truncate text-right pr-1",
            ),
            rx.el.p(
                CalculatorState.display,
                class_name="text-white text-6xl font-light h-20 truncate text-right pr-1",
                style={"line_height": "1.2"},
            ),
            class_name="p-4 pt-0 flex flex-col justify-end items-end",
        ),
        rx.el.div(
            calculator_button(
                rx.cond(
                    (CalculatorState.display == "0")
                    & (CalculatorState.expression == ""),
                    "AC",
                    "C",
                ),
                CalculatorState.clear_all,
                button_style_light_gray,
            ),
            calculator_button(
                "+/−",
                CalculatorState.toggle_sign,
                button_style_light_gray,
            ),
            calculator_button(
                "%",
                CalculatorState.input_percentage,
                button_style_light_gray,
            ),
            calculator_button(
                "÷",
                lambda: CalculatorState.input_operator("/"),
                button_style_orange,
            ),
            calculator_button(
                "7",
                lambda: CalculatorState.input_digit("7"),
                button_style_dark_gray,
            ),
            calculator_button(
                "8",
                lambda: CalculatorState.input_digit("8"),
                button_style_dark_gray,
            ),
            calculator_button(
                "9",
                lambda: CalculatorState.input_digit("9"),
                button_style_dark_gray,
            ),
            calculator_button(
                "×",
                lambda: CalculatorState.input_operator("*"),
                button_style_orange,
            ),
            calculator_button(
                "4",
                lambda: CalculatorState.input_digit("4"),
                button_style_dark_gray,
            ),
            calculator_button(
                "5",
                lambda: CalculatorState.input_digit("5"),
                button_style_dark_gray,
            ),
            calculator_button(
                "6",
                lambda: CalculatorState.input_digit("6"),
                button_style_dark_gray,
            ),
            calculator_button(
                "−",
                lambda: CalculatorState.input_operator("-"),
                button_style_orange,
            ),
            calculator_button(
                "1",
                lambda: CalculatorState.input_digit("1"),
                button_style_dark_gray,
            ),
            calculator_button(
                "2",
                lambda: CalculatorState.input_digit("2"),
                button_style_dark_gray,
            ),
            calculator_button(
                "3",
                lambda: CalculatorState.input_digit("3"),
                button_style_dark_gray,
            ),
            calculator_button(
                "+",
                lambda: CalculatorState.input_operator("+"),
                button_style_orange,
            ),
            calculator_button(
                rx.icon(tag="calculator", size=28),
                rx.toast(
                    "Calculator Icon Clicked (No Action)"
                ),
                button_style_dark_gray,
            ),
            calculator_button(
                "0",
                lambda: CalculatorState.input_digit("0"),
                button_style_dark_gray,
            ),
            calculator_button(
                ".",
                CalculatorState.input_decimal,
                button_style_dark_gray,
            ),
            calculator_button(
                "=",
                CalculatorState.calculate_equals,
                button_style_orange,
            ),
            class_name="grid grid-cols-4 gap-2 p-3",
        ),
        class_name="bg-neutral-800 rounded-lg shadow-2xl w-80 mx-auto my-10 select-none",
    )