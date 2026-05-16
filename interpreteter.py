
class Interpreter:
    def __init__(self):
        self.vars = {}

    def run(self, program):
        if program.mode is None:
            program.mode = "higher"
        for stmt in program.main_body:
            self.exec_stmt(stmt)

    def exec_stmt(self, stmt):
        if isinstance(stmt, Assign):
            self.vars[stmt.name] = self.eval_expr(stmt.value)
            return

        if isinstance(stmt, PrintStmt):
            print(self.eval_expr(stmt.value))
            return

        if isinstance(stmt, IfStmt):
            cond = self.eval_expr(stmt.condition)
            if cond:
                for s in stmt.if_body:
                    self.exec_stmt(s)
            elif stmt.else_body:
                for s in stmt.else_body:
                    self.exec_stmt(s)
            return

        raise RuntimeError("Unknown AST node")

    def eval_expr(self, expr):
        if isinstance(expr, int):
            return expr
        if isinstance(expr, str):
            return expr
        if isinstance(expr, tuple):
            op = expr[0]
            if op == "var":
                name = expr[1]
                if name not in self.vars:
                    raise RuntimeError(f"Variable '{name}' not defined")
                return self.vars[name]

            left = self.eval_expr(expr[1])
            right = self.eval_expr(expr[2])

            if op == "PLUS":
                return str(left) + str(right) if isinstance(left, str) or isinstance(right, str) else left + right
            if op == "MINUS":
                return left - right
            if op == "MUL":
                return left * right
            if op == "DIV":
                return left // right
            if op == "GT":
                return left > right
            if op == "LT":
                return left < right
            if op == "EQEQ":
                return left == right
            if op == "NOTEQ":
                return left != right
        return expr
