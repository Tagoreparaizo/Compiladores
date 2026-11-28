# Gramática formal da MiniLang

## Alfabeto e tokens

O alfabeto léxico da MiniLang é formado por:

- letras ASCII: `A-Z`, `a-z`;
- dígitos decimais: `0-9`;
- identificadores iniciados por letra ou `_`, seguidos por letras, dígitos ou `_`;
- caracteres de pontuação: `( ) { } ;`;
- caracteres de operador: `+ - * / < > = !`;
- espaços em branco e quebras de linha;
- comentário de linha iniciado por `//`.

Palavras reservadas são membros fixos do alfabeto léxico e não podem ser usadas como identificadores:
`true`, `false`, `print`, `if`, `else`, `while`, `for`.

| Token | Forma/padrão | Exemplos |
|---|---|---|
| INT | `[0-9]+` | `0`, `42` |
| TRUE | `true` | `true` |
| FALSE | `false` | `false` |
| IDENT | `[A-Za-z_][A-Za-z0-9_]*`, exceto palavras reservadas | `x`, `soma_1` |
| PRINT | `print` | `print` |
| IF | `if` | `if` |
| ELSE | `else` | `else` |
| WHILE | `while` | `while` |
| FOR | `for` | `for` |
| PLUS | `+` | `+` |
| MINUS | `-` | `-` |
| STAR | `*` | `*` |
| SLASH | `/` | `/` |
| LT, GT | `<`, `>` | `<`, `>` |
| LE, GE | `<=`, `>=` | `<=`, `>=` |
| EQ, NE | `==`, `!=` | `==`, `!=` |
| ASSIGN | `=` | `=` |
| LPAREN, RPAREN | `(`, `)` | `(`, `)` |
| LBRACE, RBRACE | `{`, `}` | `{`, `}` |
| SEMI | `;` | `;` |
| COMMENT | `//` até o fim da linha | `// exemplo` |

## Gramática EBNF

```ebnf
programa       ::= comando*

comando        ::= atribuicao ';'
                 | 'print' '(' expressao ')' ';'
                 | 'if' '(' expressao ')' (bloco | comando)
                   [ 'else' (bloco | comando) ]
                 | 'while' '(' expressao ')' (bloco | comando)
                 | 'for' '(' atribuicao ';' expressao ';' atribuicao ')' (bloco | comando)
                 | bloco

bloco          ::= '{' comando* '}'
atribuicao     ::= IDENT '=' expressao
expressao      ::= comparacao

comparacao     ::= aditiva { ('<' | '>' | '<=' | '>=' | '==' | '!=') aditiva }
aditiva        ::= multiplicativa { ('+' | '-') multiplicativa }
multiplicativa ::= unaria { ('*' | '/') unaria }
unaria         ::= ('+' | '-') unaria | primaria
primaria       ::= INT | 'true' | 'false' | IDENT | '(' expressao ')'
```

## Precedência e associatividade

A tabela está organizada do menor para o maior nível de precedência.

| Precedência | Operadores | Associatividade | Produção responsável |
|---|---|---|---|
| 1, menor | `<`, `>`, `<=`, `>=`, `==`, `!=` | esquerda | `comparacao` |
| 2 | `+`, `-` binários | esquerda | `aditiva` |
| 3 | `*`, `/` | esquerda | `multiplicativa` |
| 4, maior | `+`, `-` unários | direita | `unaria` |

A associatividade esquerda é obtida pelas formas repetitivas da EBNF (`{ operador operando }`), que encadeiam operações da esquerda para a direita. O operador unário usa uma chamada recursiva à própria produção `unaria`, garantindo associatividade direita.

Os parênteses de `primaria` alteram explicitamente a precedência.

## Restrições semânticas

As restrições abaixo não alteram as produções da gramática: elas são verificadas depois da análise sintática.

- Uma variável utilizada em uma expressão deve ter sido definida por uma atribuição anterior.
- Os operandos dos operadores aritméticos `+`, `-`, `*` e `/` devem ser inteiros.
- A divisão exige um divisor diferente de zero.
- Os operadores relacionais `<`, `>`, `<=`, `>=`, `==` e `!=` exigem operandos compatíveis; neste projeto, inteiros são comparados entre si e booleanos são comparados entre si.
- As condições de `if`, `while` e `for` devem produzir um valor booleano.
- A inicialização e a atualização de `for` devem ser atribuições válidas; a condição deve ser uma expressão booleana.

## Cinco programas de exemplo

### 1. Programa válido

```ml
limite = 3;
contador = 0;

while (contador < limite) {
    contador = contador + 1;
}

print(contador == limite);
```

**Justificativa:** as atribuições terminam em `;`; as expressões e os operadores seguem a gramática; o `while` usa uma condição booleanamente avaliável entre parênteses e possui um bloco como corpo; a comparação `contador == limite` gera o valor booleano impresso por `print`.

### 2. Exemplo inválido léxico

```ml
x = @42;
```

**Justificativa:** o caractere `@` não pertence ao alfabeto léxico, não corresponde a nenhum token da tabela e não ocorre em nenhuma produção. Portanto, a entrada é rejeitada na análise léxica antes da análise sintática.

### 3. Exemplo inválido sintático

```ml
x = (1 + ;
```

**Justificativa:** após `+`, a produção `primaria` exige `INT`, `true`, `false`, `IDENT` ou uma expressão entre parênteses. O token `;` não é uma expressão primária. Também falta fechar `)`. Essa entrada viola a gramática e é rejeitada na análise sintática.

### 4. Exemplo inválido semântico

```ml
x = 10 / 0;
```

**Justificativa:** a entrada pertence à gramática e portanto é sintaticamente válida, mas viola a restrição semântica de que o divisor não pode ser zero.

### 5. Exemplo inválido: laço mal formado

```ml
for (i = 0; i < 10) {
    print(i);
}
```

**Justificativa:** a produção de `for` exige exatamente três cláusulas separadas por `;`:
`for ( atribuicao ';' expressao ';' atribuicao ')' bloco`.
A inicialização `i = 0` e a condição `i < 10` existem, mas falta a cláusula obrigatória de atualização `i = i + 1`. Assim, a entrada viola a gramática dos laços e é sintaticamente inválida.

## Implementação do lexer

### Relação entre expressões regulares, autômatos finitos e implementação

Os padrões léxicos da MiniLang são linguagens regulares. Os identificadores são descritos por `[A-Za-z_][A-Za-z0-9_]*`, os inteiros por `[0-9]+` e os comentários por `//[^\n]*`. O ponto especial é o prefixo de dois caracteres dos operadores `<=`, `>=`, `==` e `!=`.

A implementação em `src/lexer.py` usa estados realizados de forma procedural: estado inicial, identificador, inteiro, comentário, operador/pontuação e erro. Os estados de aceitação são realizados pela emissão de `Token`, acompanhada da linha e da coluna.

O autômato reconhece exatamente os padrões da linguagem:

- Em identificadores, somente letras ASCII são aceitas; dígitos e `_` podem continuar o token.
- Em inteiros, somente dígitos ASCII continuam o token. Letras ou `_` imediatamente após um número geram `Número mal formado`, pois `1x` não é válido.
- Ao reconhecer `//`, o texto é ignorado até `\n` ou EOF.
- Comentários `/* ... */` não pertencem à linguagem e são rejeitados.
- Caracteres não ASCII, como `ç`, e símbolos fora do alfabeto, como `@`, são rejeitados.

### Tabela de transições do léxico

Os estados são: `S` inicial, `I` inteiro, `A` identificador, `C` comentário, `O` operador/pontuação, `E` erro e `F` fim.

| Estado atual | Entrada | Próximo estado / ação |
|---|---|---|
| S | espaço, `\t`, `\r`, `\n` | S; consumir |
| S | `/` seguido de `/` | C; ignorar até fim da linha |
| S | `/` seguido de `*` | E; comentário de bloco não permitido |
| S | `[A-Za-z_]` | A; iniciar identificador |
| S | `[0-9]` | I; iniciar inteiro |
| S | `<=`, `>=`, `==`, `!=` | O; emitir token composto |
| S | `<`, `>`, `+`, `-`, `*`, `/`, `=`, `(`, `)`, `{`, `}`, `;` | O; emitir token simples |
| S | caractere fora do alfabeto | E; `Caractere inesperado` |
| S | EOF | F; emitir `EOF` |
| A | `[A-Za-z0-9_]` | A; continuar identificador |
| A | outro caractere/EOF | aceita IDENT ou palavra reservada; retorna a S |
| I | `[0-9]` | I; continuar inteiro |
| I | letra ASCII ou `_` | E; `Número mal formado` |
| I | outro caractere/EOF | aceita INT; retorna a S |
| C | caractere diferente de `\n` | C; consumir |
| C | `\n` | S; terminar comentário |
| C | EOF | F; comentário de linha termina normalmente |
| O | símbolo reconhecido | aceita o token correspondente; retorna a S |
| E | — | rejeita a cadeia com linha e coluna |

As transições usam leitura maximal: inteiros e identificadores continuam até encontrar outro tipo de caractere. Depois da leitura, as palavras reservadas são reconhecidas pelo valor exato da cadeia; toda outra cadeia válida vira `IDENT`.
