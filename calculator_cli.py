"""CLI calculator with validation, history, and buffer editing.

Usage:
    python calculator_cli.py

Commands:
    c / clear          Clear the current buffer
    b / back / ⌫       Backspace (remove last character)
    =                  Evaluate the current buffer
    h / history        Show last calculation
    q / quit / exit    Exit

Notes:
    - You can enter a full expression to evaluate immediately.
    - Or build an expression across multiple inputs, then press '='.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, DivisionByZero, InvalidOperation
import ast
import re
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
            return "No calculations yet."
        return f"{self.last_expression} = {self.last_result}"


class ExpressionBuffer:
    def __init__(self) -> None:
        self._buffer: list[str] = []

    def append(self, text: str) -> None:
        self._buffer.append(text)

    def backspace(self) -> None:
        if not self._buffer:
            return
        last = self._buffer.pop()
        if len(last) > 1:
            self._buffer.append(last[:-1])

    def clear(self) -> None:
        self._buffer.clear()

    def get(self) -> str:
        return "".join(self._buffer).strip()

    def is_empty(self) -> bool:
        return not self.get()


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
        if isinstance(node, ast.Num):  # For older AST nodes
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


class CalculatorCLI:
    def __init__(self) -> None:
        self.buffer = ExpressionBuffer()
        self.engine = CalculatorEngine()
        self.history = CalculationHistory()

    def run(self) -> None:
        self._print_banner()
        while True:
            try:
                prompt = self._build_prompt()
                user_input = input(prompt).strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting calculator.")
                break

            if not user_input:
                continue

            if self._handle_command(user_input):
                continue

            self._handle_expression_input(user_input)

    def _print_banner(self) -> None:
        print("=== Python CLI Calculator ===")
        print("Type an expression to evaluate, or build it in parts.")
        print("Commands: c(clear), b(backspace), =(evaluate), h(history), q(quit)")
        print("Example: 12 + 7 * 3")
        print("------------------------------")

    def _build_prompt(self) -> str:
        current = self.buffer.get()
        if current:
            return f"[{current}] > "
        return "> "

    def _handle_command(self, user_input: str) -> bool:
        normalized = user_input.lower()
        if normalized in {"q", "quit", "exit", ":q"}:
            print("Goodbye!")
            raise SystemExit
        if normalized in {"c", "clear", ":c"}:
            self.buffer.clear()
            print("Buffer cleared.")
            return True
        if normalized in {"b", "back", "backspace", ":b", "⌫"}:
            self.buffer.backspace()
            print("Backspace applied.")
            return True
        if normalized in {"h", "history", ":h"}:
            print(self.history.format())
            return True
        if normalized == "=":
            self._evaluate_buffer()
            return True
        return False

    def _handle_expression_input(self, user_input: str) -> None:
        evaluate_after = user_input.endswith("=")
        if evaluate_after:
            user_input = user_input[:-1].strip()

        if self.buffer.is_empty():
            expression = user_input
            if expression:
                self._evaluate_expression(expression)
            else:
                print("Nothing to evaluate.")
            return

        self.buffer.append(user_input)
        if evaluate_after:
            self._evaluate_buffer()

    def _evaluate_buffer(self) -> None:
        expression = self.buffer.get()
        if not expression:
            print("Nothing to evaluate.")
            return
        self._evaluate_expression(expression)
        self.buffer.clear()

    def _evaluate_expression(self, expression: str) -> None:
        try:
            result = self.engine.evaluate(expression)
        except DivisionByZero:
            print("Error: Division by zero is not allowed.")
            return
        except (InvalidOperation, ValueError) as exc:
            print(f"Error: {exc}")
            return
        print(f"{expression} = {result}")
        self.history.update(expression, result)


if __name__ == "__main__":
    CalculatorCLI().run()