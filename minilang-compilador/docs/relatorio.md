# Relatório final da Questão 01

## Pergunta orientadora

A IA foi mais útil na geração inicial de esqueletos, tabelas e casos repetitivos. Introduziu ou sugeriu erros em detalhes de precedência, classificação de tipos, validação de cláusulas do for e limites de execução. A correção humana foi essencial para fundamentar e testar cada decisão.

## Letra (a) — Definição formal da linguagem

### Alfabeto, gramática e exemplos

A linguagem MiniLang foi definida por meio de um alfabeto léxico, uma tabela de tokens, uma gramática EBNF, uma tabela de precedência e associatividade e cinco programas de exemplo. A gramática define atribuições, impressão, condicionais, blocos, `while` e `for`, além das regras para expressões aritméticas e relacionais.

A precedência foi organizada do menor para o maior nível: comparação, adição/subtração, multiplicação/divisão e operadores unários. Os parênteses da produção primária permitem alterar explicitamente essa ordem. A associatividade esquerda é obtida pelas repetições da EBNF, enquanto o operador unário é associativo à direita por sua chamada recursiva.

Os exemplos documentam pelo menos um programa válido e uma entrada inválida em cada categoria exigida: léxico, sintático e semântico. O laço mal formado também foi incluído para demonstrar que `for` requer obrigatoriamente inicialização, condição e atualização.

## Letra (b) — Análise léxica

### Justificativa formal

A análise léxica foi definida pelas expressões regulares dos tokens da MiniLang: `[0-9]+` para inteiros, `[A-Za-z_][A-Za-z0-9_]*` para identificadores e `//[^\n]*` para comentários de linha. Palavras reservadas são reconhecidas por correspondência exata entre uma cadeia já formada e o conjunto `{true, false, print, if, else, while, for}`. Operadores compostos são tratados antes dos operadores simples para que sequências como `<=`, `>=`, `==` e `!=` não sejam divididas em dois tokens incorretos.

Essas expressões regulares podem ser implementadas por um autômato finito determinístico com estados inicial, inteiro, identificador, comentário e operador. Os estados de inteiro e identificador são estados de aceitação; a leitura é maximal, isto é, o autômato permanece no estado enquanto o próximo caractere pertence à classe do token. Ao encontrar um caractere que não pertence à classe, o token é emitido sem perder esse caractere no processamento seguinte.

Se o token inteiro contém apenas dígitos, é emitido `INT`. Se o identificador é uma palavra reservada, é emitido o token correspondente; caso contrário, é emitido `IDENT`. A implementação em `src/lexer.py` representa essa construção de maneira procedural: o estado inicial examina o caractere atual, os laços consomem dígitos ou caracteres válidos de identificadores, os espaços são descartados e `//` inicia o estado de comentário até o fim da linha.

Essa justificativa usa a equivalência entre expressões regulares e autômatos finitos. Todo padrão utilizado possui uma representação regular, e a execução do analisador corresponde à aceitação desses padrões. Assim, o lexer não necessita de contexto sintático para classificar os tokens. Erros léxicos são detectados antes da análise sintática e incluem linha e coluna para diagnóstico. Foram testadas entradas válidas e inválidas, como `@`, `1x` e comentário não fechado ou não permitido.

