import ast
import operator as op

# supported operators
operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv, ast.FloorDiv: op.floordiv,
             ast.Pow: op.pow, ast.Mod: op.mod}


def eval_arithmetic_expression(expression: str):
    """
    >>> eval_arithmetic_expression('15+2')
    17
    >>> eval_arithmetic_expression('15-2')
    13
    >>> eval_arithmetic_expression('15*2')
    30
    >>> eval_arithmetic_expression('15/2')
    7.5
    >>> eval_arithmetic_expression('15//2')
    7
    >>> eval_arithmetic_expression('15**2')
    225
    >>> eval_arithmetic_expression('15%2')
    1
    """
    return __eval(ast.parse(expression, mode='eval').body)


def __eval(node):
    if isinstance(node, ast.Num):  # <number>
        return node.n
    elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
        return operators[type(node.op)](__eval(node.left), __eval(node.right))
    else:
        raise TypeError(node)
