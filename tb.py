#!/usr/bin/python3

import string
import math

debug = False

vars = {}
stack = []

ANY = 'any'
REM = 'REM'
PRINT = 'PRINT'
IF = 'IF'
THEN = 'THEN'
GOTO = 'GOTO'
INPUT = 'INPUT'
LET = 'LET'
GOSUB = 'GOSUB'
RETURN = 'RETURN'
END = 'END'
PLUS = '+'
MINUS = '-'
MUL = '*'
DIV = '/'
ID = 'ID'
TAB = 'TAB'
SQR = 'SQR'
INT = 'INT'
STRING = 'STRING'
NUMBER = 'NUMBER'
FLOAT = 'FLOAT'
INTEGER = 'INTEGER'
COMMA = ','
SEMICOLON = ';'
LT = '<'
GT = '>'
LTE = '<='
GTE = '=>'
EQUALS = '='
NEQUALS = '<>'
LPAREN = '('
RPAREN = ')'
EOL = 'EOL'


class Token(object):

    def __init__(self, type, value = None):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({}, {})'.format(self.type, repr(self.value))

    def __repr__(self):
        return self.__str__()


RESERVED_KEYWORDS = {
    REM:      Token(REM),
    PRINT:    Token(PRINT),
    IF:       Token(IF),
    THEN:     Token(THEN),
    GOTO:     Token(GOTO),
    INPUT:    Token(INPUT),
    LET:      Token(LET),
    GOSUB:    Token(GOSUB),
    RETURN:   Token(RETURN),
    TAB:      Token(TAB),
    SQR:      Token(SQR),
    INT:      Token(INT),
    END:      Token(END)
}

EOLT = Token(EOL)

class Lexer(object):

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[self.pos]
        self.current_token = None        
        self.peek_token = None

    def error(self):
        raise Exception("Invalid character: {}".format(self.current_char))

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char != None and self.current_char.isspace():
            self.advance()

    def skip_line_comment(self):
        while self.current_char is not None:
            self.advance()

    def number(self):
        result = ''        
        while (self.current_char is not None
                   and (self.current_char.isdigit() or self.current_char in ".E-")):
            if self.current_char == '-' and result[-1] != 'E':
                break
            result += self.current_char
            self.advance()
        try:
            return Token(NUMBER, int(result))
        except:
            return Token(NUMBER, float(result))        

    def _id(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        token = RESERVED_KEYWORDS.get(result, Token(ID, result))        
        return token

    def string(self):
        result = ''
        self.advance()
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()
        token = Token(STRING, result)
        return token

    def get_next_token(self):
        while self.current_char is not None:
            token = None
            if self.current_char.isspace():
                self.skip_whitespace()
                continue            
            elif self.current_char.isalpha():
                token = self._id()
                if token.type == REM:
                    self.skip_line_comment()
                    token = None
            elif self.current_char == '"':
                token = self.string()
            elif self.current_char.isdigit():
                token = self.number()
            elif self.current_char == '=':
                self.advance()
                token = Token(EQUALS, '=')
            elif self.current_char == '<' and self.peek() == '>':
                self.advance()
                self.advance()
                token = Token(NEQUALS, '<>')
            elif self.current_char == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                token = Token(LTE, '<=')
            elif self.current_char == '<':
                self.advance()
                token = Token(LT, '<')
            elif self.current_char == '>' and self.peek() == '=':
                self.advance()
                self.advance()
                token = Token(GTE, '>=')
            elif self.current_char == '>':
                self.advance()
                token = Token(GT, '>')   
            elif self.current_char == ',':
                self.advance()
                token = Token(COMMA, ',')
            elif self.current_char == ';':
                self.advance()
                token = Token(SEMICOLON, ';')
            elif self.current_char == '+':
                self.advance()
                token = Token(PLUS, '+')
            elif self.current_char == '-':
                self.advance()
                token = Token(MINUS, '-')
            elif self.current_char == '*':
                self.advance()
                token = Token(MUL, '*')
            elif self.current_char == '/':
                self.advance()
                token = Token(DIV, '/')
            elif self.current_char == '(':
                self.advance()
                token = Token(LPAREN, '(')
            elif self.current_char == ')':
                self.advance()
                token = Token(RPAREN, ')')
            else:
                self.error()

            if token != None:
                self.skip_whitespace()
                token.peek_char = self.current_char
                return token
            
        return EOLT

class AST(object):
    def visit(self):
        pass
    def __repr__(self):
        return self.__str__()

class LetStatement(AST):
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

    def visit(self):
        vars[self.var.name] = self.expr.visit()        

    def __str__(self):
        return "LET {} = {}".format(self.var, self.expr)


class PrintStatement(AST):
    def __init__(self, expr_list):
        self.expr_list = expr_list

    def visit(self):
        pos = 0
        for expr in self.expr_list:      
            if isinstance(expr, Token):
                if expr.type == SEMICOLON:
                    print(" ", end = "")
                    pos += 1
                elif expr.type == COMMA:
                    pass
            elif isinstance(expr, Tab):
                next_pos = expr.visit()
                if next_pos > pos:
                    print(" " * (next_pos - pos), end = "")
                    pos = next_pos
            else:
                res = expr.visit()
                if isinstance(res, float):
                    s = "{:.2f}".format(res)
                else:
                    s = res
                pos += len(str(s))
                print(s, end = "")
        if not(isinstance(expr, Token) and expr.type == COMMA):
            print("")

    def __str__(self):
        return "PRINT {}".format(self.expr_list)


class InputStatement(AST):
    def __init__(self, var_list):
        self.var_list = var_list

    def visit(self):
        for var in self.var_list:
            value = input("?")
            try:                
                vars[var.name] = int(value)
            except:
                raise Exception("not an int: {}".format(value))

    def __str__(self):
        return "INPUT {}".format(self.var_list)


class IfStatement(AST):
    def __init__(self, bool_expr, then_statement):
        self.bool_expr = bool_expr
        self.then_statement = then_statement

    def visit(self):
        cond = self.bool_expr.visit()
        if cond == True:
            return self.then_statement.visit()

    def __str__(self):
        return "IF " + str(self.bool_expr) + " THEN " + str(self.then_statement)


class GotoStatement(AST):
    def __init__(self, expr):
        self.expr = expr

    def visit(self):
        return self.expr.visit()

    def __str__(self):
        return "GOTO {}".format(self.expr)


class GosubStatement(AST):
    def __init__(self, expr, line_number):
        self.expr = expr
        self.line_number = line_number

    def visit(self):
        stack.append(self.line_number)
        return self.expr.visit()

    def __str__(self):
        return "GOSUB {}".format(self.expr)


class ReturnStatement(AST):
    def __init__(self):
        pass

    def visit(self):
        return -stack.pop()

    def __str__(self):
        return "RETURN"


class EndStatement(AST):
    def __init__(self):
        pass

    def visit(self):
        return 0

    def __str__(self):
        return "END"


class RemStatement(AST):
    def __init__(self):
        pass

    def __str__(self):
        return "REM"


class Var(AST):
    def __init__(self, name):
        self.name = name

    def visit(self):
        return vars.get(self.name, 0)

    def __str__(self):
        return "Var " + self.name


class Num(AST):
    def __init__(self, token):
        self.value = token.value

    def visit(self):
        return self.value

    def __str__(self):
        return str(self.value)


class String(AST):
    def __init__(self, token):
        self.value = token.value

    def visit(self):
        return self.value

    def __str__(self):
        return self.value


class Tab(AST):
    def __init__(self, expr):
        self.expr = expr

    def visit(self):
        return self.expr.visit()

    def __str__(self):
        return "TAB({})".format(str(self.expr))


class Function(AST):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def visit(self):
        value = self.expr.visit()
        if self.name == SQR:
            return math.sqrt(value)
        elif self.name == INT:
            return int(value)
        else: 
            raise Exception("unknow function {}".format(self.name))

    def __str__(self):
        return "FUNC {} ( {} )".format(self.name, str(self.expr))


class UnOp(AST):
    def __init__(self, op, factor):
        self.op = op
        self.factor = factor

    def visit(self):
        if self.op.type == PLUS:
            return self.factor.visit()
        elif self.op.type == MINUS:
            return -self.factor.visit()
    
    def __str__(self):
        return "UnOp {} {}".format(self.op, self.factor)


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
        
    def visit(self):
        if self.op.type == PLUS:
            left = self.left.visit()
            right = self.right.visit()
            return left + right
        elif self.op.type == MINUS:
            return self.left.visit() - self.right.visit()
        elif self.op.type == MUL:
            return self.left.visit() * self.right.visit()
        elif self.op.type == DIV:
            return self.left.visit() / self.right.visit()
        elif self.op.type == EQUALS:
            return self.left.visit() == self.right.visit()
        elif self.op.type == NEQUALS:
            return self.left.visit() != self.right.visit()
        elif self.op.type == LT:
            return self.left.visit() < self.right.visit()
        elif self.op.type == LTE:
            return self.left.visit() <= self.right.visit()
        elif self.op.type == GT:
            return self.left.visit() > self.right.visit()
        elif self.op.type == GTE:
            return self.left.visit() >= self.right.visit()

    def __str__(self):
        return "(BinOp " + str(self.left) + " " +  self.op.value + " " + str(self.right) + ")";


class Parser(object):

    def __init__(self, line_number, line):
        self.line_number = line_number
        self.line = line
        if len(line) == 0:
            self.current_token = None
        else:            
            self.current_token = line.pop(0)

    def eat(self, type):
        if type == self.current_token.type or type == ANY:
            if len(self.line) > 0:
                self.current_token = self.line.pop(0)
            else:
                self.current_token = EOLT
        else:
            raise Exception("expected {} but got {}".format(type, self.current_token.type))

    def parse_var(self):
        name = self.current_token.value
        self.eat(ID)
        if len(name) > 1:
            raise Exception("length of variable names must be 1: {}".format(name))
        elif name not in string.ascii_uppercase:
            raise Exception("variable name {} not allowed".format(name))
        return Var(name)

    def parse_function(self):
        func_name = self.current_token.type
        self.eat(ANY)
        self.eat(LPAREN)
        expr = self.parse_expr()
        self.eat(RPAREN)
        return Function(func_name, expr)

    def parse_factor(self):
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            return UnOp(token, self.parse_factor())
        elif token.type == MINUS:
            self.eat(MINUS)
            return UnOp(token, self.parse_factor()) 
        elif token.type == NUMBER: # TODO needed?
            self.eat(NUMBER)            
            return Num(token)
        elif token.type == ID:
            return self.parse_var()            
        elif token.type in (SQR, INT):
            return self.parse_function()
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.parse_expr()
            self.eat(RPAREN)
            return node
        raise Exception("parsing factor failed: {}".format(token))

    # term ::=
    #   factor ((* | /) factor)*
    def parse_term(self):        
        node = self.parse_factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            self.eat(ANY)
            node = BinOp(left=node, op=token, right=self.parse_factor())
        return node    

    # expr ::=
    #   term ((+ | -) term)*
    def parse_expr(self):
        node = self.parse_term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            self.eat(ANY)
            node = BinOp(left=node, op=token, right=self.parse_term())
        return node


    def parse_TAB(self):
        self.eat(TAB)
        self.eat(LPAREN)
        expr = self.parse_expr()
        self.eat(RPAREN)
        return Tab(expr)


    def parse_expr_or_string(self):  
        log("  parse expr or string, current: {}".format(self.current_token))
        if self.current_token.type == TAB:
            node = self.parse_TAB()      
        elif self.current_token.type == STRING:
            node = String(self.current_token)
            self.eat(STRING)
        else:
            node = self.parse_expr()
        log("  parsed expr str: {}".format(node))
        return node

    def parse_expr_list(self):
        log("  parse expr_list")
        expr_list = []
        expr_list.append(self.parse_expr_or_string())
        while self.current_token.type in (COMMA, SEMICOLON):
            expr_list.append(self.current_token)
            self.eat(ANY)
            if self.current_token == EOLT:
                break
            expr_list.append(self.parse_expr_or_string())
        log("  parsed expr list: {}".format(expr_list))
        return expr_list

    def parse_var_list(self):
        var_list = []
        var_list.append(self.parse_var())
        while self.current_token.type == COMMA:
            self.eat(COMMA)
            var_list.append(self.parse_var())
        return var_list

    def parse_LET(self):
        self.eat(LET)
        var = self.parse_var()
        self.eat(EQUALS)
        expr = self.parse_expr()
        return LetStatement(var, expr)

    def parse_PRINT(self):
        self.eat(PRINT)
        return PrintStatement(self.parse_expr_list())

    def parse_INPUT(self):
        self.eat(INPUT)
        return InputStatement(self.parse_var_list())

    def parse_IF(self):
        self.eat(IF)
        left = self.parse_expr()
        token = self.current_token
        if token.type in (LT, GT, LTE, GTE, EQUALS, NEQUALS):
            self.eat(ANY)
        else:
            raise Exception("relational operator expected: {}".format(token.value))
        right = self.parse_expr()
        self.eat(THEN)
        statement = self.parse_statement()
        condition = BinOp(left, token, right)
        return IfStatement(condition, statement)

    def parse_GOTO(self):
        self.eat(GOTO)
        return GotoStatement(self.parse_expr())

    def parse_GOSUB(self):
        self.eat(GOSUB)
        return GosubStatement(self.parse_expr(), self.line_number)

    def parse_RETURN(self):
        self.eat(RETURN)
        return ReturnStatement()

    def parse_END(self):
        self.eat(END)
        return EndStatement()

    def parse_REM(self):
        self.eat(REM)
        return RemStatement()

    def parse_statement(self):
        log("  parse_statement, current: {}".format(self.current_token))
        if self.current_token.type == LET:
            return self.parse_LET()
        elif self.current_token.type == PRINT:
            return self.parse_PRINT()
        elif self.current_token.type == INPUT:
            return self.parse_INPUT()
        elif self.current_token.type == IF:
            return self.parse_IF()
        elif self.current_token.type == GOTO:
            return self.parse_GOTO()
        elif self.current_token.type == GOSUB:
            return self.parse_GOSUB()
        elif self.current_token.type == RETURN:
            return self.parse_RETURN()
        elif self.current_token.type == END:
            return self.parse_END()   
        elif self.current_token.type == REM:
            return self.parse_REM()         
        else:
            raise Exception("can not parse: {}".format(self.current_token))


def parse_int(token):
	try:
		return int(token)
	except:
		return -1

def get_indexed_line(raw_line, index):
    line = raw_line.strip()
    if not line: return None, None
    if line[0].isdigit():
        tokens = line.split(' ', 1)
        index = parse_int(tokens[0])
        return (index, tokens[1])
    else:
        return (index, line)        

def tokenize(line):
    tokens = []
    lexer = Lexer(line)    
    while (True):
        token = lexer.get_next_token()
        if token.type == EOL:
            break
        tokens.append(token)
    return tokens

def parse_all(raw_lines):
    log("parsing ...")
    index = 0
    parsed_lines = []
    for raw_line in raw_lines:
        (new_index, sub_line) = get_indexed_line(raw_line, index)
        if not new_index: continue
        else:
            index = new_index
        try:
            tokens = tokenize(sub_line)
            log("{}, tokens: {}".format(index, tokens))
            parser = Parser(index, tokens)
            node = parser.parse_statement()
        except Exception as e:
            print("ERROR: on line: {} {}\n{}".format(index, sub_line, e))
            raise
        parsed_lines.append((index, node))
        index += 1
    return parsed_lines

def get_next_line_number(line_number, line_numbers, current_index):
    if line_number == None: # just use next line
        next_index = line_numbers.index(current_index) + 1
        if next_index >= len(line_numbers):
            return
    elif line_number < 0: # coming from RETURN
        next_index = line_numbers.index(-line_number) + 1
        if next_index >= len(line_numbers):
            return
    elif line_number == 0:  # coming from END
        print("END.")
        return
    else: # coming from GOTO or GOSUB
        return line_number  
    return line_numbers[next_index]  

def interpret_all(parsed_lines):
    log("interpreting ...")
    line_numbers = [number for number, tokens in parsed_lines]
    memory = {number: tokens for number, tokens in parsed_lines}
    line_number = line_numbers[0]
    while True:                
        if line_number not in memory:
            print("ERROR: line not found: {}".format(line_number))
            raise     
        statement = memory[line_number]
        log("  executing: {}, {}".format(line_number, statement)) 
        try:
            result = statement.visit()
        except Exception as e:            
            print("ERROR: executing {}".format(statement))     
            raise       
        line_number = get_next_line_number(result, line_numbers, line_number)
        if line_number == None:
            break
    print("OK.")

def log(msg):
    if debug:
        print(msg)

def main():
    print("Tiny Basic v0.1")
    import sys
    global debug
    if len(sys.argv) < 2:
        print("syntax: tb [-d] <filename>")
        return
    if sys.argv[1] == '-d':
        debug = True
    file = open(sys.argv[-1], 'r')
    lines = file.readlines()
    file.close()
    try:
        parsed_lines = parse_all(lines)
        interpret_all(parsed_lines)
    except:
        pass
    
if __name__ == '__main__':
    main()