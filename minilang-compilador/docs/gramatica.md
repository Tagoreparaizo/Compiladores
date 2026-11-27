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
