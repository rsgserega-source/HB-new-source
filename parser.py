class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.pos]

    def advance(self):
        tok = self.peek()
        self.pos += 1
        return tok

    def expect(self, type_):
        tok = self.peek()
        if tok.type != type_:
            raise RuntimeError(f"Expected {type_}, got {tok.type}")
        return self.advance()

    def parse(self):
        statements = []
        while self.peek().type != "EOF":
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        tok = self.peek()

        if tok.type == "PRINT":
            return self.parse_print()

        if tok.type == "IDENT":
            return self.parse_assignment()

        if tok.type == "IF":
            return self.parse_if()

        raise RuntimeError(f"Unexpected token {tok.type}")

    def parse_print(self):
        self.expect("PRINT")
        expr = self.parse_expression()
        return ("print", expr)

    def parse_assignment(self):
        name = self.expect("IDENT").value
        self.expect("EQUAL")
        expr = self.parse_expression()
        return ("assign", name, expr)

    def parse_if(self):
        self.expect("IF")
        left = self.parse_expression()
        op = self.advance()
        right = self.parse_expression()

        self.expect("LBRACE")

        body = []
        while self.peek().type != "RBRACE":
            body.append(self.parse_statement())

        self.expect("RBRACE")

        return ("if", left, op.type, right, body)

    def parse_expression(self):
        left = self.parse_term()

        while self.peek().type in ("PLUS", "MINUS"):
            op = self.advance()
            right = self.parse_term()
            left = ("binop", op.type, left, right)

        return left

    def parse_term(self):
        left = self.parse_factor()

        while self.peek().type in ("MUL", "DIV"):
            op = self.advance()
            right = self.parse_factor()
            left = ("binop", op.type, left, right)

        return left

    def parse_factor(self):
        tok = self.peek()

        if tok.type == "NUMBER":
            return ("num", int(self.advance().value))

        if tok.type == "STRING":
            return ("str", self.advance().value)

        if tok.type == "IDENT":
            return ("var", self.advance().value)

        raise RuntimeError(f"Unexpected token {tok.type}")
