# Tiny Basic

This is a Tiny Basic interpreter written in Python.

To find out more about Tiny Basic, check https://en.wikipedia.org/wiki/Tiny_BASIC

There was a challenge, posted by Jeff Atwood (coding-horror), to bring 100 ancient basic games back to life by porting them to mordern languages. 
The idea is to teach how you would do it nowadays.
I looked at it and walked in the wrong direction and built a basic interpreter, just for fun. It's an implementation of Tiny Basic, a very limited Basic.
It has no loops, no functions, very limited variables. It feels a bit like an
assembler of sorts.

https://github.com/coding-horror/basic-computer-games

This version of Tiny Basic differs from its initial specification:
* it supports floats
* it supports TAB() to ease print formatting
* it has built in functions like ABS, INT, SQR and RND

The interpreter has no real purpose except amusement. 

## Running

You run it like so:
`tb.py <filename>`
or without parameter to run it in repl mode.

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

Another option is to use stdin in repl mode.
```
tb.py < input_file
```
If you are using this option, don't forget to include a `RUN` statement at the end. Otherwise it would just load the program into memory and then exit.

## Twitter bot

There is  a twitter bot, that reads tweets, addressed to it, and then replies with the output of the statement or program.


## Statements

Special formatting for the PRINT statement is possible.
* Separating expressions by `,` prints without any space
* Separating expressions by `;` prints with a single space
* TAB(x) sets the cursor to position x
* a trailing `,` omits the CR at the end and makes it possible to have the 
input `?` on the same line



## Grammar
```
line ::= 
	number statement | statement
 
statement ::= 
	'PRINT' expr-list |
	'IF' expression relop expression 'THEN' statement |
	'GOTO' expression |
	'INPUT' var-list |
	'LET' var '=' expression |
	'GOSUB' expression |
	'RETURN' |
	'END' |
	'LIST' |
	'RUN' |
	'CLEAR' 

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
	" ( |!|#|$ ... -|.|/|digit|: ... |A| ... |Z)* "
```




