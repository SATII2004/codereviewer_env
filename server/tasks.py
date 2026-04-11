TASK_CORPUS = {
    "style_001": {
        "difficulty": "easy",
        "category": "style",
        "files": {"app.py": "def add(a,b):\n  return a+b\nimport os, sys"},
        "bug": "E401: Multiple imports on one line.",
        "tool_outputs": {"run_ruff": "app.py:3:1: E401 Multiple imports on one line"}
    },
    "bug_101": {
        "difficulty": "medium",
        "category": "logic",
        "files": {"utils.py": "def get_div(a, b):\n    return a / b"},
        "bug": "ZeroDivisionError regression.",
        "tool_outputs": {"run_pytest": "FAILED utils.py::test_div_zero - ZeroDivisionError"}
    },
    "sec_201": {
        "difficulty": "hard",
        "category": "security",
        "files": {"db.py": "query = f'SELECT * FROM users WHERE name = {name}'"},
        "bug": "SQL Injection vulnerability.",
        "tool_outputs": {"run_bandit": "Issue: [B608] Possible SQL injection detected."}
    }
}