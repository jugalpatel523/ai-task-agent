# app/tools/calculator.py
from typing import Any, Dict, List, Union

NumberLike = Union[int, float, str]

OPS = {
    "add": "+",
    "plus": "+",
    "sum": "+",
    "subtract": "-",
    "minus": "-",
    "multiply": "*",
    "times": "*",
    "divide": "/",
}

async def calculator(args: Dict[str, Any]) -> str:
    try:
        # 1) Preferred: expression
        expr = args.get("expression") or args.get("equation")
        if isinstance(expr, str) and expr.strip():
            return str(eval(expr, {"__builtins__": {}}, {}))

        # 2) Alternative: operation + operands
        op = args.get("operation")
        operands = args.get("operands")

        if not op or not isinstance(operands, list) or len(operands) < 2:
            return "Error: invalid expression."

        symbol = OPS.get(str(op).lower())
        if not symbol:
            return "Error: unsupported operation."

        # convert operands -> numbers
        nums: List[float] = [float(x["value"] if isinstance(x, dict) else x) for x in operands]

        # fold: a op b op c ...
        result = nums[0]
        for n in nums[1:]:
            if symbol == "+":
                result += n
            elif symbol == "-":
                result -= n
            elif symbol == "*":
                result *= n
            elif symbol == "/":
                result /= n

        # return as int if clean
        if result.is_integer():
            return str(int(result))
        return str(result)

    except Exception:
        return "Error: invalid expression."
