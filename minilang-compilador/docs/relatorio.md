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

## Letra (c) — Análise sintática

### Técnica adotada: descendente recursivo

O parser foi implementado em `src/parser.py` com a técnica descendente recursiva. Cada produção não terminal da gramática EBNF corresponde a um método: `parse_expression`, `parse_comparison`, `parse_additive`, `parse_multiplicative`, `parse_unary` e `parse_primary`. Os métodos correspondentes aos comandos verificam os tokens `PRINT`, `IF`, `WHILE`, `FOR`, `IDENT` e `LBRACE`, enquanto blocos são reconhecidos por `parse_body` e `parse_block_from_opening`.

Essa técnica é compatível com a gramática construída no item (a), pois ela não possui recursão à esquerda. Em particular, as produções repetitivas das operações são implementadas por laços `while`, enquanto os operadores unários usam recursão à direita em `parse_unary`. O token atual é analisado por inspeção direta e, após o reconhecimento de um símbolo terminal, o método `advance` avança a posição da entrada.

### Árvore sintática de `1 + 2 * 3`

A expressão é analisada com a árvore abaixo:

```text
+
├── 1
└── *
    ├── 2
    └── 3
```

### Árvore sintática de `(1 + 2) * 3`

Os parênteses fazem a adição tornar-se o operando esquerdo da multiplicação:

```text
*
├── +
│   ├── 1
│   └── 2
└── 3
```

As duas árvores são diferentes porque o primeiro caso aplica a precedência natural, na qual `*` liga os operandos `2` e `3` antes da soma com `1`. No segundo caso, `parse_primary` reconhece `(expressão)` e força a soma a ser calculada antes da multiplicação. Portanto, a posição dos parênteses altera diretamente a forma da árvore.

### Precedência e associatividade

A precedência é implementada pela separação das chamadas: `parse_comparison` chama `parse_additive`, que chama `parse_multiplicative`, que chama `parse_unary`, e esta chama `parse_primary`. Assim, multiplicação e divisão são processadas antes da adição e subtração, e estas são processadas antes da comparação.

Os operadores binários aditivos, multiplicativos e comparativos são associativos à esquerda. Por exemplo, `1 - 2 - 3` forma `(- (- 1 2) 3)`, pois cada repetição constrói um novo nó binário tendo o resultado anterior como operando esquerdo. Os operadores unários `+` e `-` são associativos à direita, pois `parse_unary` chama novamente `parse_unary` após consumir o operador.

### Reconhecimento de `while` e `for`

O comando `while` reconhece exatamente `WHILE`, `LPAREN`, uma expressão inteira, `RPAREN` e um corpo. O corpo pode ser um bloco ou um único comando. Seu nó da AST contém a condição e o corpo.

O comando `for` exige todas as cláusulas: `for (`, atribuição de inicialização, `;`, expressão de condição, `;`, atribuição de atualização e `)`. A árvore representa separadamente:

```text
For
├── inicialização: i = 0
├── condição: i < 5
├── atualização: i = i + 1
└── corpo
    └── Print(i)
```

As três partes são obrigatórias. Assim, uma entrada como `for (i = 0; i < 10) { ... }` é rejeitada ao faltar o segundo separador `;` e a cláusula de atualização. Laços com atualização vazia, condição vazia ou inicialização vazia também são rejeitados pela implementação atual.

### Rejeição das entradas inválidas

O parser lança `ParserError` com linha e coluna quando encontra uma construção incompatível com a gramática. Exemplos cobertos pelos testes são expressão incompleta como `x = (1 + ;`, parênteses não fechados, atribuição sem `;`, `for` sem cláusula de atualização, `for` sem `)` e bloco não fechado. A entrada `x = (1 + ;` é rejeitada em `parse_primary`, pois após o operador `+` o token encontrado é `SEMI`, que não inicia uma expressão primária.

### Comparação com uma técnica alternativa

Uma técnica alternativa seria o analisador LR, que constrói tabelas de análise a partir de gramáticas com mais expressividade e pode lidar com uma família maior de gramáticas. Sua vantagem é detectar diferentes conflitos e processar gramáticas maiores de forma eficiente. Porém, exige uma infraestrutura de estados e tabelas, muitas vezes gerada por ferramentas, o que torna a implementação menos transparente para um projeto didático inicial.

Os métodos descendentes recursivos foram escolhidos porque a gramática da MiniLang é pequena, estruturada e não possui recursão à esquerda. Essa decisão permite relacionar diretamente cada produção da EBNF a uma função e facilita a compreensão, demonstração e depuração dos resultados.

