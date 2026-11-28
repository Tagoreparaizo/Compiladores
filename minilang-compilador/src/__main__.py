import sys

from .lexer import LexerError
from .parser import Parser, ParserError
from .interpreter import Interpreter, SemanticError


def main():
    if len(sys.argv) != 2:
        print("Uso: python -m src arquivo.ml", file=sys.stderr)
        return 1

    try:
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            program = Parser(file.read()).parse()
        for line in Interpreter().execute(program):
            print(line)
        return 0
    except (LexerError, ParserError, SemanticError) as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 1


# Arquivo reservado para etapas posteriores da atividade.
