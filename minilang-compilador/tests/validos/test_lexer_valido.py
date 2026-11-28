import pytest

from src.lexer import Lexer


def test_comentario_linha():
    tokens = Lexer("x = 10; // comentário\ny = x + 1;").tokenize()
    assert [token.kind for token in tokens].count("EOF") == 1


def test_comentario_linha_e_programa_completo():
    source = """
    x = 10; // atribuição inicial
    y = 2 * (x + 5);
    while (x > 0) {
        x = x - 1;
    }
    for (i = 0; i < 5; i = i + 1) {
        print(i);
    }
    """

    tokens = Lexer(source).tokenize()

    kinds = [token.kind for token in tokens]
    assert "EOF" in kinds
    assert "WHILE" in kinds
    assert "FOR" in kinds
    assert "PRINT" in kinds
    assert kinds.count("EOF") == 1


def test_todos_os_operadores_e_booleanos():
    source = "true false + - * / < > <= >= == != = ( ) { } ;"

    kinds = [token.kind for token in Lexer(source).tokenize()]

    assert kinds == [
        "TRUE", "FALSE", "PLUS", "MINUS", "STAR", "SLASH",
        "LT", "GT", "LE", "GE", "EQ", "NE", "ASSIGN",
        "LPAREN", "RPAREN", "LBRACE", "RBRACE", "SEMI", "EOF",
    ]


def test_identificadores_numeros_e_palavras_reservadas():
    source = "x soma_1 _controle 42 0 true false print if else while for"

    tokens = Lexer(source).tokenize()

    assert tokens[0].kind == "IDENT"
    assert tokens[1].kind == "IDENT"
    assert tokens[2].kind == "IDENT"
    assert tokens[3].kind == "INT"
    assert tokens[4].kind == "INT"
    assert [token.kind for token in tokens[5:11]] == [
        "TRUE", "FALSE", "PRINT", "IF", "ELSE", "WHILE"
    ]
    assert tokens[11].kind == "FOR"


def test_trecho_do_exemplo_valido():
    tokens = Lexer("fator = 3; total = 1; print(total);").tokenize()

    assert [token.kind for token in tokens[:-1]] == [
        "IDENT", "ASSIGN", "INT", "SEMI",
        "IDENT", "ASSIGN", "INT", "SEMI",
        "PRINT", "LPAREN", "IDENT", "RPAREN", "SEMI",
    ]
