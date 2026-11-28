import pytest

from src.parser import Parser, ParserError


def test_expressao_incompleta():
    with pytest.raises(ParserError, match="Erro sintático"):
        Parser("x = (1 + ;").parse()


def test_parenteses_nao_fechado():
    with pytest.raises(ParserError, match="'\\)' em expressão"):
        Parser("x = (1 + 2;").parse()


def test_atribuicao_sem_ponto_e_virgula():
    with pytest.raises(ParserError, match="Erro sintático"):
        Parser("x = 10").parse()


def test_for_sem_clausula_de_atualizacao():
    with pytest.raises(ParserError, match="'; entre condição"):
        Parser("for (i = 0; i < 10) { print(i); }").parse()


def test_for_sem_parenteses_apos_clausulas():
    with pytest.raises(ParserError, match="após as três cláusulas do for"):
        Parser("for (i = 0; i < 10; i = i + 1 { print(i); }").parse()


def test_for_sem_todas_as_clausulas():
    with pytest.raises(ParserError, match="Erro sintático"):
        Parser("for (i = 0; i < 10;) { print(i); }").parse()


def test_bloco_nao_fechado():
    with pytest.raises(ParserError, match="'}'"):
        Parser("while (true) { print(1); ").parse()


def test_print_sem_parenteses():
    with pytest.raises(ParserError, match="'\\('"):
        Parser("print 1;").parse()
