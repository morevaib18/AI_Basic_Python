"""Tkinter GUI calculator with validation, history, and keyboard support."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, DivisionByZero, InvalidOperation
import ast
import re
import tkinter as tk
from tkinter import ttk
from typing import Optional


ALLOWED_EXPR_RE = re.compile(r"^[0-9+\-*/().\s]+$")


@dataclass
class CalculationHistory:
    last_expression: Optional[str] = None
    last_result: Optional[str] = None

    def update(self, expression: str, result: str) -> None:
        self.last_expression = expression
        self.last_result = result

    def format(self) -> str:
        if self.last_expression is None:
            return "History: None"
        return f"History: {self.last_expression} = {self.last_result}"


class CalculatorEngine:
    def evaluate(self, expression: str) -> str:
        cleaned = expression.strip()
        if not cleaned:
            raise ValueError("Expression is empty.")
        if not ALLOWED_EXPR_RE.match(cleaned):
            raise ValueError("Expression contains invalid characters.")

        try:
            tree = ast.parse(cleaned, mode="eval")
        except SyntaxError as exc:
            raise ValueError("Malformed expression.") from exc

        result = self._eval_node(tree.body)
        return self._format_decimal(result)

    def _eval_node(self, node: ast.AST) -> Decimal:
        if isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            return self._apply_binop(node.op, left, right)
        if isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            if isinstance(node.op, ast.UAdd):
                return operand
            if isinstance(node.op, ast.USub):
                return -operand
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return Decimal(str(node.value))
        if isinstance(node, ast.Num):
            return Decimal(str(node.n))
        raise ValueError("Unsupported expression element detected.")

    def _apply_binop(self, operator: ast.operator, left: Decimal, right: Decimal) -> Decimal:
        if isinstance(operator, ast.Add):
            return left + right
        if isinstance(operator, ast.Sub):
            return left - right
        if isinstance(operator, ast.Mult):
            return left * right
        if isinstance(operator, ast.Div):
            if right == 0:
                raise DivisionByZero("Division by zero.")
            return left / right
        raise ValueError("Unsupported operator detected.")

    def _format_decimal(self, value: Decimal) -> str:
        normalized = value.normalize()
        text = format(normalized, "f")
        if "." in text:
            text = text.rstrip("0").rstrip(".")
        return text or "0"


class CalculatorGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("360x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e1e")

        self.engine = CalculatorEngine()
        self.history = CalculationHistory()
        self.expression = tk.StringVar(value="")
        self.result = tk.StringVar(value="0")
        self.history_text = tk.StringVar(value=self.history.format())

        self._build_ui()
        self._bind_keyboard()

    def _build_ui(self) -> None:
        display_frame = ttk.Frame(self.root, padding=12)
        display_frame.pack(fill=tk.X)

        history_label = ttk.Label(display_frame, textvariable=self.history_text)
        history_label.pack(anchor="e")

        expr_label = ttk.Label(
            display_frame,
            textvariable=self.expression,
            font=("Segoe UI", 14),
            anchor="e",
        )
        expr_label.pack(fill=tk.X, pady=(4, 0))

        result_label = ttk.Label(
            display_frame,
            textvariable=self.result,
            font=("Segoe UI", 28, "bold"),
            anchor="e",
        )
        result_label.pack(fill=tk.X, pady=(6, 12))

        buttons_frame = ttk.Frame(self.root, padding=12)
        buttons_frame.pack(fill=tk.BOTH, expand=True)

        buttons = [
            ("C", 0, 0, self.clear),
            ("⌫", 0, 1, self.backspace),
            ("(", 0, 2, lambda: self.append("(")),
            (")", 0, 3, lambda: self.append(")")),
            ("7", 1, 0, lambda: self.append("7")),
            ("8", 1, 1, lambda: self.append("8")),
            ("9", 1, 2, lambda: self.append("9")),
            ("÷", 1, 3, lambda: self.append("/")),
            ("4", 2, 0, lambda: self.append("4")),
            ("5", 2, 1, lambda: self.append("5")),
            ("6", 2, 2, lambda: self.append("6")),
            ("×", 2, 3, lambda: self.append("*")),
            ("1", 3, 0, lambda: self.append("1")),
            ("2", 3, 1, lambda: self.append("2")),
            ("3", 3, 2, lambda: self.append("3")),
            ("−", 3, 3, lambda: self.append("-")),
            ("0", 4, 0, lambda: self.append("0")),
            (".", 4, 1, lambda: self.append(".")),
            ("+", 4, 2, lambda: self.append("+")),
            ("=", 4, 3, self.evaluate),
        ]

        for text, row, col, command in buttons:
            btn = ttk.Button(buttons_frame, text=text, command=command)
            btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")

        for i in range(5):
            buttons_frame.rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.columnconfigure(i, weight=1)

        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TFrame", background="#1e1e1e")
        style.configure(
            "TLabel",
            background="#1e1e1e",
            foreground="#f2f2f2",
        )
        style.configure(
            "TButton",
            font=("Segoe UI", 14),
            padding=8,
        )

    def _bind_keyboard(self) -> None:
        self.root.bind("<Key>", self._on_key)
        self.root.bind("<Return>", lambda _event: self.evaluate())
        self.root.bind("<BackSpace>", lambda _event: self.backspace())
        self.root.bind("<Escape>", lambda _event: self.clear())

    def _on_key(self, event: tk.Event) -> None:
        char = event.char
        if char in "0123456789+-*/().":
            self.append(char)

    def append(self, value: str) -> None:
        current = self.expression.get()
        self.expression.set(current + value)

    def clear(self) -> None:
        self.expression.set("")
        self.result.set("0")

    def backspace(self) -> None:
        current = self.expression.get()
        self.expression.set(current[:-1])

    def evaluate(self) -> None:
        expression = self.expression.get()
        try:
            result = self.engine.evaluate(expression)
        except DivisionByZero:
            self.result.set("Error: Division by zero")
            return
        except (InvalidOperation, ValueError) as exc:
            self.result.set(f"Error: {exc}")
            return

        self.result.set(result)
        self.history.update(expression, result)
        self.history_text.set(self.history.format())


def main() -> None:
    root = tk.Tk()
    CalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()