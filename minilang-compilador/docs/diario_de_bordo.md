# Diário de bordo

## Letra (a) — Definição formal da linguagem

- **Responsável pelo desenvolvimento:** Tágore Campos Paraizo.
- **Atividades realizadas:** definição do alfabeto, dos tokens, da gramática EBNF, da precedência e da associatividade. Criação dos cinco programas de exemplo e dos arquivos de programas válidos e inválidos.
- **Uso de IA:** o GitHub Copilot auxiliou na organização inicial da documentação e na revisão da estrutura formal dos exemplos.
- **Revisão humana:** Tágore Campos Paraizo verificou as produções da gramática, a separação entre erros léxicos, sintáticos e semânticos e as justificativas dos exemplos.
- **Decisões:** foram adotadas letras e dígitos ASCII, palavras reservadas fixas e operadores compostos com leitura maximal.
- **Evidência:** `docs/gramatica.md`, `exemplos/programa_valido.ml` e `exemplos/programa_invalido.ml`.

## Letra (b) — Análise léxica

- **Responsável pelo desenvolvimento:** Tágore Campos Paraizo.
- **Atividades realizadas:** implementação do lexer em `src/lexer.py`, incluindo palavras reservadas, identificadores, inteiros, operadores e comentários de linha.
- **Uso de IA:** o GitHub Copilot sugeriu a estrutura inicial do lexer, a tabela de tokens e exemplos de testes válidos e inválidos.
- **Revisão humana:** Tágore Campos Paraizo corrigiu o reconhecimento de números mal formados como `1x`, operadores compostos e caracteres fora do alfabeto. Os casos foram comparados com as expressões regulares e com a tabela de transições.
- **Testes realizados:** testes válidos e inválidos em `tests/validos/test_lexer_valido.py` e `tests/invalidos/test_lexer_invalido.py`.
- **Decisão de qualidade:** erros léxicos devem ser identificados antes da análise sintática e informar linha e coluna.
- **Evidência:** implementação do lexer, testes léxicos e justificativa formal na seção de análise léxica do relatório.

## Letra (c) — Análise sintática

- **Responsável pelo desenvolvimento:** Tágore Campos Paraizo.
- **Atividades realizadas:** implementação do parser descendente recursivo em `src/parser.py` e dos nós estruturais utilizados pelo parser em `src/ast_nodes.py`.
- **Uso de IA:** o GitHub Copilot sugeriu a separação das funções por níveis de precedência, estruturas iniciais da AST e casos de testes.
- **Revisão humana:** Tágore Campos Paraizo revisou associatividade, precedência, parênteses, fechamento de blocos e exigência das três cláusulas do `for`. A implementação foi comparada com as produções da EBNF.
- **Testes realizados:** testes válidos e inválidos em `tests/validos/test_parser_valido.py` e `tests/invalidos/test_parser_invalido.py`, incluindo precedência, associatividade, `while`, `for` e laços mal formados.
- **Decisão de qualidade:** a análise sintática informa erro com linha e coluna e rejeita entradas antes da execução.
- **Evidência:** parser, nós da AST, testes do parser e documentação da técnica descendente recursiva no relatório.

## Registro geral de validação

- As letras (a), (b) e (c) foram desenvolvidas por Tágore Campos Paraizo.
- Os artefatos dessas etapas foram revisados e testados por Tágore Campos Paraizo antes de serem considerados concluídos.
- O GitHub Copilot foi usado como ferramenta de apoio à formatação, organização, verificação e correção de código e documentação.
- O uso da IA não substituiu a autoria intelectual do responsável nem a participação técnica dos demais integrantes nas etapas futuras.
- As letras (d) a (h) ainda não foram concluídas e deverão ser registradas em novas atualizações do diário.
