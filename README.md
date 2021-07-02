# tiny_basic

line ::= 
	number statement CR | statement CR
 
statement ::= 
	PRINT expr-list
	IF expression relop expression THEN statement
	GOTO expression
	INPUT var-list
	LET var = expression
	GOSUB expression
	RETURN
	CLEAR
	LIST
	RUN
	END

expr-list ::= 
	( tab | string | expression ) (, ( tab | string | expression ) )*

tab ::=
	TAB( expr )
 
var-list ::= 
	var (, var)*
 
expression ::=
	term ((+ | -) term)*
 
term ::= 
	factor ((* | /) factor)*
 	
factor ::= 
	+ factor |
	- factor |
	var |
	number |
	( expression )
 
var ::= 
	A | B | C ... | Y | Z
 
number ::= 
	digit digit*
 
digit ::= 
	0 | 1 | 2 | 3 | ... | 8 | 9
 
relop ::= 
	<, =, >, <=, >=, <>

string ::= 
	" ( |!|#|$ ... -|.|/|digit|: ... @|A|B|C ... |X|Y|Z)* "




