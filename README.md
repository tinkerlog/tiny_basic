# tiny_basic

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
	'CLEAR'
	'LIST'
	'RUN'
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
	'RND(' expression ')'

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




