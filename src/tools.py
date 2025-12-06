### Small math/code tools for ReAct agent.
import math
from typing import Callable, Dict

# Run math calculations, return result or error message.
def math_tool(expr: str) -> str:
    env = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}
    # Helpers the model uses in math questions.
    def _digit_sum(n: int) -> int:
        return sum(int(d) for d in str(int(n)))
    env.update(
        {
            "abs": abs,
            "min": min,
            "max": max,
            "round": round,
            "C": math.comb,
            "binom": math.comb,
            "s": _digit_sum,
        }
    )
    try:
        return str(eval(expr, {"__builtins__": {}}, env)) # Evaluate the expression.
    except Exception as error:
        return f"ERROR: {error}"

# Check if provided python code compiles, returns OK, or error message.
def python_tool(code: str) -> str:
    try:
        compile(code, "<python_tool>", "exec")
        return "OK"
    except SyntaxError as error:
        return f"SYNTAX ERROR: {error.msg} (line {error.lineno})"
    except Exception as error:
        return f"ERROR: {error}"

# Simple reflection tool for domains without numeric/code tools.
def reflect_tool(note: str) -> str:
    if note:
        return f"Reflect more carefully on this aspect: {note}"
    return "Reflect: double-check your reasoning, assumptions, and final answer for consistency."

# Dictionary of available tools, cool.
TOOLS: Dict[str, Callable[[str], str]] = {"math": math_tool, "python": python_tool, "reflect": reflect_tool}

# Run a tool with a given name and argument.
def run_tool(name: str, arg: str) -> str:
    tool = TOOLS.get(name.lower())
    return tool(arg) if tool else f"ERROR: unknown tool '{name}'"
