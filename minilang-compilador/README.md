# MiniLang — Questão 01, letras (a), (b) e (c)

Este projeto contém:

- a definição formal da linguagem MiniLang, incluindo alfabeto, tokens, gramática EBNF, precedência e associatividade;
- cinco programas de exemplo com justificativas;
- um programa válido e um programa inválido contendo um laço mal formado;
- a implementação do lexer em `src/lexer.py`;
- testes válidos e inválidos da análise léxica;
- a implementação do parser descendente recursivo em `src/parser.py`;
- os nós iniciais da AST em `src/ast_nodes.py`;
- testes válidos e inválidos da análise sintática.

## Executar os testes

```powershell
python -m pytest
```

Para executar somente os testes do lexer:

```powershell
python -m pytest tests/validos/test_lexer_valido.py tests/invalidos/test_lexer_invalido.py -v
```

Para executar somente os testes do parser:

```powershell
python -m pytest tests/validos/test_parser_valido.py tests/invalidos/test_parser_invalido.py -v
```

Consulte `docs/gramatica.md` para a gramática, a tabela de tokens e a tabela de transições do autômata. Consulte `docs/relatorio.md` para as justificativas das letras (a), (b) e (c). Os arquivos de exemplo estão em `exemplos/`.
