from langchain_core.tools import tool
import ast
import operator

# Safe operators for evaluation
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

def _safe_eval(node):
    if isinstance(node, ast.Num):  # <number>
        return node.n
    elif isinstance(node, ast.BinOp):  # <left> <op> <right>
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        op = SAFE_OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError("Unsupported operation")
        return op(left, right)
    elif isinstance(node, ast.UnaryOp):  # - <operand>
        operand = _safe_eval(node.operand)
        op = SAFE_OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError("Unsupported unary operation")
        return op(operand)
    else:
        raise ValueError("Unsupported expression")

@tool
def calculator_tool(expression: str) -> str:
    """
    Safely evaluates a basic mathematical expression.
    Supports: +, -, *, /, **, parentheses, negative numbers.
    Example inputs: '2 + 3 * 4', '(10 - 5) / 2', '2 ** 3'
    """
    try:
        tree = ast.parse(expression, mode='eval')
        result = _safe_eval(tree.body)
        return f"The result of '{expression}' is {result}"
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"
