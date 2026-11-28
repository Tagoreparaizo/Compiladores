# Testes léxicos reservados para o item (b).

import pytest

from src.lexer import Lexer, LexerError


def test_caractere_nao_pertencente_ao_alfabeto():
    with pytest.raises(LexerError, match="Caractere inesperado '@'"):
        Lexer("x = @42;").tokenize()


def test_numero_mal_formado_com_letras():
    with pytest.raises(LexerError, match="Número mal formado '1x'"):
        Lexer("x = 1x;").tokenize()


def test_comentario_nao_permitido_nao_fechado():
    with pytest.raises(LexerError, match="Comentário de bloco não fechado ou não permitido"):
        Lexer("/* comentário sem fechamento").tokenize()


def test_comentario_de_bloco_fechado_tambem_nao_e_aceito():
    with pytest.raises(LexerError, match="Comentário de bloco"):
        Lexer("/* comentário */ x = 1;").tokenize()


def test_letra_nao_ascii_e_rejeitada():
    with pytest.raises(LexerError, match="Caractere inesperado 'ç'"):
        Lexer("ç = 1;").tokenize()
