import pytest

from src.ast_nodes import Assignment, Binary, Block, For, If, Literal, Print, Unary, Variable, While
from src.parser import Parser


def test_programa_com_atribuicao():
    program = Parser("x = 10;").parse()
    assert len(program.statements) == 1
    assert isinstance(program.statements[0], Assignment)
    assert program.statements[0].name == "x"
    assert program.statements[0].expression == Literal(10)


def test_precedencia_de_multiplicacao():
    expression = Parser("x = 1 + 2 * 3;").parse().statements[0].expression
    assert isinstance(expression, Binary)
    assert expression.operator == "+"
    assert expression.left == Literal(1)
    assert isinstance(expression.right, Binary)
    assert expression.right.operator == "*"


def test_parenteses_alteram_precedencia():
    expression = Parser("x = (1 + 2) * 3;").parse().statements[0].expression
    assert isinstance(expression, Binary)
    assert expression.operator == "*"
    assert isinstance(expression.left, Binary)
    assert expression.left.operator == "+"
    assert expression.right == Literal(3)


def test_associatividade_esquerda_da_adicao():
    expression = Parser("x = 1 - 2 - 3;").parse().statements[0].expression
    assert isinstance(expression, Binary)
    assert expression.operator == "-"
    assert isinstance(expression.left, Binary)
    assert expression.left.operator == "-"


def test_unario_recursivo():
    expression = Parser("x = -(-5);").parse().statements[0].expression
    assert isinstance(expression, Unary)
    assert expression.operator == "-"
    assert isinstance(expression.operand, Unary)


def test_print_e_comparacao():
    program = Parser("print(x + 1 > 2);").parse()
    assert isinstance(program.statements[0], Print)
    assert isinstance(program.statements[0].expression, Binary)


def test_if_com_else():
    program = Parser("if (x > 0) { print(x); } else { print(0); }").parse()
    command = program.statements[0]
    assert isinstance(command, If)
    assert isinstance(command.then_branch, Block)
    assert isinstance(command.else_branch, Block)


def test_while():
    program = Parser("while (x > 0) { x = x - 1; }").parse()
    command = program.statements[0]
    assert isinstance(command, While)
    assert isinstance(command.condition, Binary)
    assert isinstance(command.body, Block)


def test_for_com_tres_clausulas():
    program = Parser("for (i = 0; i < 5; i = i + 1) { print(i); }").parse()
    command = program.statements[0]
    assert isinstance(command, For)
    assert command.initialization.name == "i"
    assert isinstance(command.initialization.expression, Literal)
    assert isinstance(command.condition, Binary)
    assert command.update.name == "i"
    assert isinstance(command.body, Block)


def test_comando_sem_bloco():
    program = Parser("while (true) print(1);").parse()
    command = program.statements[0]
    assert isinstance(command, While)
    assert isinstance(command.body, Print)
