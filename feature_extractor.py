import ast
import re
from collections import Counter


def calculate_nesting_depth(tree):
    """
    Calculate maximum nesting depth of the Python code.
    """

    max_depth = 0

    def visit(node, depth=0):
        nonlocal max_depth

        max_depth = max(max_depth, depth)

        for child in ast.iter_child_nodes(node):
            visit(child, depth + 1)

    visit(tree)

    return max_depth


def extract_features(code):
    """
    Extract ML features from Python source code.
    """

    lines = code.splitlines()

    # -----------------------------------------
    # 1. Lines of Code
    # -----------------------------------------

    non_empty_lines = [
        line for line in lines
        if line.strip()
    ]

    total_lines = len(non_empty_lines)

    # -----------------------------------------
    # 2. Comments
    # -----------------------------------------

    comment_lines = sum(
        1
        for line in lines
        if line.strip().startswith("#")
    )

    comment_ratio = (
        comment_lines / total_lines
        if total_lines > 0
        else 0
    )

    # -----------------------------------------
    # 3. Long Lines
    # -----------------------------------------

    long_lines = sum(
        1
        for line in lines
        if len(line) > 100
    )

    # -----------------------------------------
    # 4. Duplicate Lines
    # -----------------------------------------

    normalized_lines = [
        re.sub(r"\s+", " ", line.strip())
        for line in non_empty_lines
        if not line.strip().startswith("#")
    ]

    line_counter = Counter(normalized_lines)

    duplicate_lines = sum(
        count - 1
        for count in line_counter.values()
        if count > 1
    )

    # -----------------------------------------
    # 5. Parse Python Code
    # -----------------------------------------

    try:
        tree = ast.parse(code)

    except SyntaxError as error:

        return {
            "syntax_error": True,
            "syntax_message": str(error)
        }

    # -----------------------------------------
    # 6. Number of Functions
    # -----------------------------------------

    functions = sum(
        1
        for node in ast.walk(tree)
        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef)
        )
    )

    # -----------------------------------------
    # 7. If / Conditional Statements
    # -----------------------------------------

    branches = sum(
        1
        for node in ast.walk(tree)
        if isinstance(
            node,
            (ast.If, ast.IfExp)
        )
    )

    # -----------------------------------------
    # 8. Loops
    # -----------------------------------------

    loops = sum(
        1
        for node in ast.walk(tree)
        if isinstance(
            node,
            (ast.For, ast.While, ast.AsyncFor)
        )
    )

    # -----------------------------------------
    # 9. Exception Handling
    # -----------------------------------------

    exception_handlers = sum(
        1
        for node in ast.walk(tree)
        if isinstance(node, ast.Try)
    )

    # -----------------------------------------
    # 10. Boolean Conditions
    # -----------------------------------------

    boolean_operations = sum(
        1
        for node in ast.walk(tree)
        if isinstance(node, ast.BoolOp)
    )

    # -----------------------------------------
    # 11. Risky Functions
    # -----------------------------------------

    risky_functions = {
        "eval",
        "exec",
        "compile",
        "__import__"
    }

    risky_calls = 0

    for node in ast.walk(tree):

        if isinstance(node, ast.Call):

            if isinstance(node.func, ast.Name):

                if node.func.id in risky_functions:
                    risky_calls += 1

    # -----------------------------------------
    # 12. Complexity
    # -----------------------------------------

    complexity = (
        1
        + branches
        + loops
        + boolean_operations
        + exception_handlers
    )

    # -----------------------------------------
    # 13. Nesting Depth
    # -----------------------------------------

    nesting_depth = calculate_nesting_depth(tree)

    # -----------------------------------------
    # Final Feature Dictionary
    # -----------------------------------------

    features = {

        "lines": total_lines,

        "functions": functions,

        "branches": branches,

        "loops": loops,

        "exception_handlers": exception_handlers,

        "boolean_operations": boolean_operations,

        "complexity": complexity,

        "nesting_depth": nesting_depth,

        "long_lines": long_lines,

        "duplicate_lines": duplicate_lines,

        "comments": comment_lines,

        "comment_ratio": round(
            comment_ratio,
            4
        ),

        "risky_calls": risky_calls
    }

    return features