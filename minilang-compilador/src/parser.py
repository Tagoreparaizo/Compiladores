from src.lexer import Lexer, LexerError, Token
from src.ast_nodes import (
    Assignment,
    Binary,
    Block,
    For,
    If,
    Literal,
    Print,
    Program,
    Unary,
    Variable,
    While,
)


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, source: str):
        try:
            self.tokens: list[Token] = Lexer(source).tokenize()
        except LexerError as error:
            raise error
        self.position = 0

    @property
    def current(self) -> Token:
        return self.tokens[self.position]

    def is_at_end(self) -> bool:
        return self.current.kind == "EOF"

    def advance(self) -> Token:
        token = self.current
        if not self.is_at_end():
            self.position += 1
        return token

    def match(self, *kinds: str) -> Token | None:
        if self.current.kind in kinds:
            return self.advance()
        return None

    def error(self, expected: str, token: Token | None = None) -> ParserError:
        token = token or self.current
        if token.kind == "EOF":
            found = "fim da entrada"
        else:
            found = f"'{token.value}'"
        return ParserError(
            f"Erro sintático esperado {expected}, encontrado {found} "
            f"na linha {token.line}, coluna {token.column}"
        )

    def expect(self, kind: str, description: str | None = None) -> Token:
        if self.current.kind != kind:
            raise self.error(description or kind)
        return self.advance()

    def parse(self) -> Program:
        statements = []
        while not self.is_at_end():
            statements.append(self.parse_command())
        return Program(statements)

    def parse_command(self):
        if self.match("LBRACE"):
            return self.parse_block_from_opening()

        if self.match("PRINT"):
            self.expect("LPAREN", "'('")
            expression = self.parse_expression()
            self.expect("RPAREN", "')'")
            self.expect("SEMI", "';'")
            return Print(expression)

        if self.match("IF"):
            self.expect("LPAREN", "'('")
            condition = self.parse_expression()
            self.expect("RPAREN", "')'")
            then_branch = self.parse_body()
            else_branch = None
            if self.match("ELSE"):
                else_branch = self.parse_body()
            return If(condition, then_branch, else_branch)

        if self.match("WHILE"):
            self.expect("LPAREN", "'('")
            condition = self.parse_expression()
            self.expect("RPAREN", "')'")
            body = self.parse_body()
            return While(condition, body)

        if self.match("FOR"):
            self.expect("LPAREN", "'('")
            initialization = self.parse_assignment()
            self.expect("SEMI", "'; entre inicialização e condição do for'")
            condition = self.parse_expression()
            self.expect("SEMI", "'; entre condição e atualização do for'")
            update = self.parse_assignment()
            self.expect("RPAREN", "')' após as três cláusulas do for")
            body = self.parse_body()
            return For(initialization, condition, update, body)

        if self.current.kind == "IDENT":
            return self.parse_assignment_command()

        raise self.error("comando válido")

    def parse_assignment_command(self) -> Assignment:
        assignment = self.parse_assignment()
        self.expect("SEMI", "'; após atribuição")
        return assignment

    def parse_assignment(self) -> Assignment:
        name = self.expect("IDENT", "IDENT na atribuição").value
        self.expect("ASSIGN", "'=' na atribuição")
        expression = self.parse_expression()
        return Assignment(name, expression)

    def parse_body(self):
        if self.current.kind == "LBRACE":
            self.advance()
            return self.parse_block_from_opening()
        return self.parse_command()

    def parse_block_from_opening(self) -> Block:
        statements = []
        while self.current.kind != "RBRACE":
            if self.is_at_end():
                raise self.error("'}'")
            statements.append(self.parse_command())
        self.advance()
        return Block(statements)

    def parse_expression(self):
        return self.parse_comparison()

    def parse_comparison(self):
        left = self.parse_additive()
        comparison_kinds = {"LT", "GT", "LE", "GE", "EQ", "NE"}
        while self.current.kind in comparison_kinds:
            operator = self.advance().value
            right = self.parse_additive()
            left = Binary(left, operator, right)
        return left

    def parse_additive(self):
        left = self.parse_multiplicative()
        while self.current.kind in ("PLUS", "MINUS"):
            operator = self.advance().value
            right = self.parse_multiplicative()
            left = Binary(left, operator, right)
        return left

    def parse_multiplicative(self):
        left = self.parse_unary()
        while self.current.kind in ("STAR", "SLASH"):
            operator = self.advance().value
            right = self.parse_unary()
            left = Binary(left, operator, right)
        return left

    def parse_unary(self):
        if self.current.kind in ("PLUS", "MINUS"):
            operator = self.advance().value
            return Unary(operator, self.parse_unary())
        return self.parse_primary()

    def parse_primary(self):
        token = self.current

        if self.match("INT"):
            return Literal(int(token.value))

        if self.match("TRUE"):
            return Literal(True)

        if self.match("FALSE"):
            return Literal(False)

        if self.match("IDENT"):
            return Variable(token.value)

        if self.match("LPAREN"):
            expression = self.parse_expression()
            self.expect("RPAREN", "')' em expressão entre parênteses")
            return expression

        raise self.error("INT, true, false, IDENT ou '(' expressão ')'")
