import ast

class SyntaxChecker:
    def check(self, code: str) -> dict:
        try:
            ast.parse(code)
            return {
                "syntax_valid": True,
                "syntax_error": None
            }
        except SyntaxError as e:
            return {
                "syntax_valid": False,
                "syntax_error": f"Line {e.lineno}: {e.msg}"
            }