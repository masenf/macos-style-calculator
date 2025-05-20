import reflex as rx
import math


class CalculatorState(rx.State):
    display: str = "0"
    expression: str = ""
    operand1: float | None = None
    operator: str | None = None
    waiting_for_operand2: bool = False

    def _get_display_operator(
        self, op_char: str | None
    ) -> str:
        if op_char is None:
            return ""
        op_map = {"/": "÷", "*": "×", "-": "−", "+": "+"}
        return op_map.get(op_char, "")

    def _format_number_for_display(
        self, num: float | str
    ) -> str:
        if isinstance(num, str):
            return num
        if abs(num) > 999999999.9999999 or (
            abs(num) < 1e-08 and num != 0
        ):
            return "Error"
        formatted_num_str = f"{num:.15g}"
        if "e" in formatted_num_str:
            try:
                val = float(formatted_num_str)
                if abs(val) > 999999999 or (
                    abs(val) < 1e-07 and val != 0
                ):
                    return "Error"
                if (
                    "." in formatted_num_str
                    or "e-" in formatted_num_str
                ):
                    formatted_num_str = f"{val:.8f}"
                else:
                    formatted_num_str = f"{val:.0f}"
            except ValueError:
                return "Error"
        if "." in formatted_num_str:
            formatted_num_str = formatted_num_str.rstrip(
                "0"
            ).rstrip(".")
        if (
            len(formatted_num_str) > 10
            and "." not in formatted_num_str
        ):
            return "Error"
        if len(formatted_num_str) > 15:
            return "Error"
        return formatted_num_str

    def _perform_calculation(self) -> float | str:
        if self.operand1 is None or self.operator is None:
            return (
                float(self.display)
                if self.display != "Error"
                else "Error"
            )
        val2 = float(self.display)
        op = self.operator
        val1 = self.operand1
        result: float | str
        if op == "+":
            result = val1 + val2
        elif op == "-":
            result = val1 - val2
        elif op == "*":
            result = val1 * val2
        elif op == "/":
            if val2 == 0:
                return "Error"
            result = val1 / val2
        else:
            return "Error"
        if math.isnan(result) or math.isinf(result):
            return "Error"
        return result

    def input_digit(self, digit: str):
        if self.display == "Error":
            self.display = digit
            self.waiting_for_operand2 = False
            return
        if self.waiting_for_operand2:
            self.display = digit
            self.waiting_for_operand2 = False
        elif self.display == "0":
            self.display = digit
        elif len(self.display) < 10:
            self.display += digit

    def input_operator(self, op_char: str):
        if self.display == "Error":
            return
        current_val_float: float
        try:
            current_val_float = float(self.display)
        except ValueError:
            self.display = "Error"
            return
        if self.operator is not None and (
            not self.waiting_for_operand2
        ):
            calc_result = self._perform_calculation()
            if calc_result == "Error":
                self.display = "Error"
                self.expression = "Error"
                self.operand1 = None
                self.operator = None
                self.waiting_for_operand2 = True
                return
            self.display = self._format_number_for_display(
                calc_result
            )
            self.operand1 = (
                calc_result
                if isinstance(calc_result, float)
                else None
            )
        else:
            self.operand1 = current_val_float
        if (
            self.operand1 is not None
            and self.operand1 != "Error"
        ):
            self.operator = op_char
            self.expression = f"{self._format_number_for_display(self.operand1)} {self._get_display_operator(op_char)}"
            self.waiting_for_operand2 = True
        else:
            self.display = "Error"
            self.expression = "Error"
            self.operand1 = None
            self.operator = None
            self.waiting_for_operand2 = True

    def calculate_equals(self):
        if (
            self.display == "Error"
            or self.operand1 is None
            or self.operator is None
        ):
            if (
                self.operator is None
                and self.operand1 is not None
            ):
                self.expression = f"{self._format_number_for_display(self.operand1)} ="
                self.display = (
                    self._format_number_for_display(
                        self.operand1
                    )
                )
            return
        val2_str = self.display
        calc_result = self._perform_calculation()
        if calc_result == "Error":
            self.display = "Error"
            self.expression = "Error"
        else:
            self.display = self._format_number_for_display(
                calc_result
            )
            val1_disp = self._format_number_for_display(
                self.operand1
            )
            val2_disp = self._format_number_for_display(
                float(val2_str)
            )
            self.expression = f"{val1_disp} {self._get_display_operator(self.operator)} {val2_disp} ="
        self.operand1 = None
        self.waiting_for_operand2 = True

    def clear_all(self):
        self.display = "0"
        self.expression = ""
        self.operand1 = None
        self.operator = None
        self.waiting_for_operand2 = False

    def toggle_sign(self):
        if self.display == "Error" or self.display == "0":
            return
        val = float(self.display) * -1
        self.display = self._format_number_for_display(val)

    def input_percentage(self):
        if self.display == "Error":
            return
        val = float(self.display) / 100
        self.display = self._format_number_for_display(val)
        self.waiting_for_operand2 = True
        self.operand1 = None
        self.operator = None
        self.expression = self.display

    def input_decimal(self):
        if self.display == "Error":
            return
        if self.waiting_for_operand2:
            self.display = "0."
            self.waiting_for_operand2 = False
        elif "." not in self.display:
            if len(self.display) < 10:
                self.display += "."