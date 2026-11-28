from dataclasses import dataclass


class LexerError(Exception):
    pass


@dataclass(frozen=True)
class Token:
    kind: str
    value: str
    line: int
    column: int


KEYWORDS = {
    "true": "TRUE",
    "false": "FALSE",
    "print": "PRINT",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "for": "FOR",
}


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.index = 0
        self.line = 1
        self.column = 1

    def advance(self) -> str:
        char = self.source[self.index]
        self.index += 1
        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    @staticmethod
    def is_ascii_letter(char: str) -> bool:
        return ("A" <= char <= "Z") or ("a" <= char <= "z")

    @staticmethod
    def is_ascii_digit(char: str) -> bool:
        return "0" <= char <= "9"

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []

        while self.index < len(self.source):
            char = self.source[self.index]

            if char.isspace():
                self.advance()
                continue

            if char == "/" and self.source.startswith("//", self.index):
                while self.index < len(self.source) and self.source[self.index] != "\n":
                    self.advance()
                continue

            line, column = self.line, self.column

            if char == "/" and self.source.startswith("/*", self.index):
                raise LexerError(
                    f"Comentário de bloco não fechado ou não permitido na linha {line}, coluna {column}"
                )

            if self.is_ascii_digit(char):
                value = ""
                while (
                    self.index < len(self.source)
                    and self.is_ascii_digit(self.source[self.index])
                ):
                    value += self.advance()

                if self.index < len(self.source):
                    next_char = self.source[self.index]
                    if self.is_ascii_letter(next_char) or next_char == "_":
                        bad = value
                        while (
                            self.index < len(self.source)
                            and (
                                self.is_ascii_letter(self.source[self.index])
                                or self.is_ascii_digit(self.source[self.index])
                                or self.source[self.index] == "_"
                            )
                        ):
                            bad += self.advance()
                        raise LexerError(
                            f"Número mal formado '{bad}' na linha {line}, coluna {column}"
                        )

                tokens.append(Token("INT", value, line, column))
                continue

            if self.is_ascii_letter(char) or char == "_":
                value = ""
                while (
                    self.index < len(self.source)
                    and (
                        self.is_ascii_letter(self.source[self.index])
                        or self.is_ascii_digit(self.source[self.index])
                        or self.source[self.index] == "_"
                    )
                ):
                    value += self.advance()

                tokens.append(Token(KEYWORDS.get(value, "IDENT"), value, line, column))
                continue

            two = self.source[self.index:self.index + 2]
            double_operators = {
                "<=": "LE",
                ">=": "GE",
                "==": "EQ",
                "!=": "NE",
            }
            if two in double_operators:
                self.advance()
                self.advance()
                tokens.append(Token(double_operators[two], two, line, column))
                continue

            single_operators = {
                "+": "PLUS",
                "-": "MINUS",
                "*": "STAR",
                "/": "SLASH",
                "<": "LT",
                ">": "GT",
                "=": "ASSIGN",
                "(": "LPAREN",
                ")": "RPAREN",
                "{": "LBRACE",
                "}": "RBRACE",
                ";": "SEMI",
            }
            if char in single_operators:
                kind = single_operators[char]
                self.advance()
                tokens.append(Token(kind, char, line, column))
                continue

            raise LexerError(
                f"Caractere inesperado '{char}' na linha {line}, coluna {column}"
            )

        tokens.append(Token("EOF", "", self.line, self.column))
        return tokens
