# Tiny Basic

This is a Tiny Basic interpreter written in Python.

To find out more about Tiny Basic, check https://en.wikipedia.org/wiki/Tiny_BASIC

This version differs from its initial specification:
* it supports floats
* it supports TAB() to ease print formatting
* it has built in functions like ABS, INT, SQR and RND
* it does not have an interactive repl mode, so no LIST or RUN

The interpreter has no real purpose except amusement. 

You run it like so:
`tb.py sine.bas`

A simple program to compute sine:
```basic
10 PRINT "COMPUTING SIN(X)"
20 PRINT "ANGLE",
30 INPUT X
40 REM sin x = x − x^3/3! + x^5/5! − x^7/7!
50 LET X = X/180*3.141592
60 LET A = X*X*X
70 LET B = A*X*X
80 LET C = B*X*X
90 LET S = X - A/6 + B/120 - C/5040
100 PRINT "SIN=",S
110 END
```

## Grammar
```
line ::= 
	number statement | statement
 
statement ::= 
	'PRINT' expr-list
	'IF' expression relop expression 'THEN' statement
	'GOTO' expression
	'INPUT' var-list
	'LET' var '=' expression
	'GOSUB' expression
	'RETURN'
	'END'

expr-list ::= 
	(tab | string | expression) (',' (tab | string | expression))*

tab ::=
	'TAB(' expr ')'
 
var-list ::= 
	var (',' var)*
 
expression ::=
	term (('+' | '-') term)*
 
term ::= 
	factor (('*' | '/') factor)*
 	
factor ::= 
	'+' factor |
	'-' factor |
	var |
	number |
	function |
	'(' expression ')'
 
function ::=
	'INT(' expression ')' |
	'SQR(' expression ')' |
	'RND(' expression ')' |
	'ABS(' expression ')'

var ::= 
	'A' | 'B' | ... | 'Z'
 
number ::= 
	integer | float

integer ::=
	digit_seq

float ::=
	(digit_seq '.' digit_seq) 

digit_seq ::=
	digit digit*

digit ::= 
	'0' | '1' | ... | '9'
 
relop ::= 
	'<' | '=' | '>' | '<=' | '>=' | '<>'

string ::= 
	" ( |!|#|$ ... -|.|/|digit|: ... @|A|B|C ... |X|Y|Z)* "
```




