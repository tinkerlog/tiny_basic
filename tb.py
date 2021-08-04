#!/usr/bin/python3

import string
import math
import random

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
RND = 'RND'
ABS = 'ABS'
LIST = 'LIST'
RUN = 'RUN'
CLEAR = 'CLEAR'
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
        # return 'Token({}, {})'.format(self.type, repr(self.value))
        return self.value if self.value else self.type

    def __repr__(self):
        return self.__str__()


LANGUAGE_KEYWORDS = {
    REM:    Token(REM),
    PRINT:  Token(PRINT),
    IF:     Token(IF),
    THEN:   Token(THEN),
    GOTO:   Token(GOTO),
    INPUT:  Token(INPUT),
    LET:    Token(LET),
    GOSUB:  Token(GOSUB),
    RETURN: Token(RETURN),
    TAB:    Token(TAB),
    SQR:    Token(SQR),
    INT:    Token(INT),
    RND:    Token(RND),
    ABS:    Token(ABS),
    END:    Token(END)
#    LIST:   Token(LIST),
#    RUN:    Token(RUN),
#    CLEAR:  Token(CLEAR)
}

IMMEDIATE_KEYWORDS = {
    LIST,
    RUN,
    CLEAR
}


EOLT = Token(EOL)

class Lexer(object):

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[self.pos]
        self.current_token = None        
        self.peek_token = None

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

    def get_line_comment(self):
        result = ""
        while self.current_char is not None:
            result += self.current_char
            self.advance()
        return result

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
        token = LANGUAGE_KEYWORDS.get(result.upper(), Token(ID, result))        
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
                    comment = self.get_line_comment()
                    token = Token(REM, comment)
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
                raise Exception(f"Invalid character: {self.current_char}")

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
    def __init__(self, var, expr, vars):
        self.var = var
        self.expr = expr
        self.vars = vars

    def visit(self):
        self.vars[self.var.name] = self.expr.visit()        

    def __str__(self):
        return f"LET {self.var} = {self.expr}"


class PrintStatement(AST):
    def __init__(self, output, expr_list):
        self.output = output
        self.expr_list = expr_list

    def visit(self):
        pos = 0
        for expr in self.expr_list:      
            if isinstance(expr, Token):
                if expr.type == SEMICOLON:
                    self.output.write(" ")
                    pos += 1
                elif expr.type == COMMA:
                    pass
            elif isinstance(expr, Tab):
                next_pos = int(expr.visit())
                if next_pos > pos:
                    self.output.write(" " * (next_pos - pos))
                    pos = next_pos
            else:
                res = expr.visit()
                if isinstance(res, float):
                    s = "{:.2f}".format(res)
                else:
                    s = res
                pos += len(str(s))
                self.output.write(str(s))
        if not(isinstance(expr, Token) and expr.type == COMMA):
            self.output.write("\n")            
        self.output.flush()

    def __str__(self):
        s = ''
        for e in self.expr_list:
            s += str(e)
        return "PRINT {}".format(s)


class InputStatement(AST):
    def __init__(self, input, output, var_list, vars):
        self.input = input
        self.output = output
        self.var_list = var_list
        self.vars = vars

    def visit(self):
        for var in self.var_list:
            self.output.write("?")
            self.output.flush()
            value = self.input.readline()
            if value == '':
                raise EOFError("no input")
            try:                
                self.vars[var.name] = int(value.strip())
            except:
                raise Exception(f"not an int: {value}")

    def __str__(self):
        s = ''
        for v in self.var_list:
            s += v.name + ','
        return f"INPUT {s[:-1]}"


class IfStatement(AST):
    def __init__(self, bool_expr, then_statement):
        self.bool_expr = bool_expr
        self.then_statement = then_statement

    def visit(self):
        cond = self.bool_expr.visit()
        if cond == True:
            return self.then_statement.visit()

    def __str__(self):
        return f"IF {self.bool_expr} THEN {self.then_statement}"


class GotoStatement(AST):
    def __init__(self, expr):
        self.expr = expr

    def visit(self):
        return self.expr.visit()

    def __str__(self):
        return f"GOTO {self.expr}"


class GosubStatement(AST):
    def __init__(self, expr, line_number, stack):
        self.expr = expr
        self.line_number = line_number
        self.stack = stack

    def visit(self):
        self.stack.append(self.line_number)
        return self.expr.visit()

    def __str__(self):
        return f"GOSUB {self.expr}"


class ReturnStatement(AST):
    def __init__(self, stack):
        self.stack = stack

    def visit(self):
        return -self.stack.pop()

    def __str__(self):
        return "RETURN"


class EndStatement(AST):
    def visit(self):
        return 0

    def __str__(self):
        return "END"


class RemStatement(AST):
    def __init__(self, comment):
        self.comment = comment
    def __str__(self):
        return "REM " + self.comment


class Var(AST):
    def __init__(self, name, vars):
        self.name = name
        self.vars = vars

    def visit(self):
        return self.vars.get(self.name, 0)

    def __str__(self):
        return self.name


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
        return f'"{self.value}"'


class Tab(AST):
    def __init__(self, expr):
        self.expr = expr

    def visit(self):
        return self.expr.visit()

    def __str__(self):
        return f"TAB({str(self.expr)})"


class Function(AST):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def visit(self):
        value = self.expr.visit()
        if   self.name == SQR: return math.sqrt(value)
        elif self.name == INT: return int(value)
        elif self.name == RND: return random.random()
        elif self.name == ABS: return abs(value)
        else: raise Exception(f"unknow function {self.name}")

    def __str__(self):
        return f"{self.name}({str(self.expr)})"


class UnOp(AST):
    def __init__(self, op, factor):
        self.op = op
        self.factor = factor

    def visit(self):
        if   self.op.type == PLUS: return self.factor.visit()
        elif self.op.type == MINUS: return -self.factor.visit()
    
    def __str__(self):
        # return "UnOp {} {}".format(self.op, self.factor)
        return f"{self.op.type}{self.factor}"


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
        
    def visit(self):
        if self.op.type == PLUS:
            return self.left.visit() + self.right.visit()
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
        # return "(BinOp " + str(self.left) + " " +  self.op.value + " " + str(self.right) + ")";
        return f"{str(self.left)} {self.op.value} {str(self.right)}"


class Parser(object):

    def __init__(self, input, output, line_number, line, vars, stack):
        self.input = input
        self.output = output
        self.line_number = line_number
        self.line = line
        self.vars = vars
        self.stack = stack
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
            raise Exception(f"expected {type} but got {self.current_token.type}")

    def parse_var(self):
        name = self.current_token.value
        self.eat(ID)
        if len(name) > 1:
            raise Exception(f"length of variable names must be 1: {name}")
        elif name not in string.ascii_uppercase:
            raise Exception(f"variable name {name} not allowed")
        return Var(name, self.vars)

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
        elif token.type == NUMBER:
            self.eat(NUMBER)            
            return Num(token)
        elif token.type == ID:
            return self.parse_var()            
        elif token.type in (SQR, INT, RND, ABS):
            return self.parse_function()
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.parse_expr()
            self.eat(RPAREN)
            return node
        raise Exception(f"parsing factor failed: {token}")

    def parse_term(self):        
        node = self.parse_factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            self.eat(ANY)
            node = BinOp(left=node, op=token, right=self.parse_factor())
        return node    

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
        if self.current_token.type == TAB:
            node = self.parse_TAB()      
        elif self.current_token.type == STRING:
            node = String(self.current_token)
            self.eat(STRING)
        else:
            node = self.parse_expr()
        return node

    def parse_expr_list(self):
        expr_list = []
        expr_list.append(self.parse_expr_or_string())
        while self.current_token.type in (COMMA, SEMICOLON):
            expr_list.append(self.current_token)
            self.eat(ANY)
            if self.current_token == EOLT:
                break
            expr_list.append(self.parse_expr_or_string())
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
        return LetStatement(var, expr, self.vars)

    def parse_PRINT(self):
        self.eat(PRINT)
        return PrintStatement(self.output, self.parse_expr_list())

    def parse_INPUT(self):
        self.eat(INPUT)
        return InputStatement(self.input, self.output, self.parse_var_list(), self.vars)

    def parse_IF(self):
        self.eat(IF)
        left = self.parse_expr()
        token = self.current_token
        if token.type in (LT, GT, LTE, GTE, EQUALS, NEQUALS):
            self.eat(ANY)
        else:
            self.error(f"relational operator expected: {token.value}")
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
        return GosubStatement(self.parse_expr(), self.line_number, self.stack)

    def parse_RETURN(self):
        self.eat(RETURN)
        return ReturnStatement(self.stack)

    def parse_END(self):
        self.eat(END)
        return EndStatement()

    def parse_REM(self):
        comment = self.current_token.value
        self.eat(REM)
        return RemStatement(comment)

    def parse_statement(self):
        type = self.current_token.type.upper()
        if   type == LET:    return self.parse_LET()
        elif type == PRINT:  return self.parse_PRINT()
        elif type == INPUT:  return self.parse_INPUT()
        elif type == IF:     return self.parse_IF()
        elif type == GOTO:   return self.parse_GOTO()
        elif type == GOSUB:  return self.parse_GOSUB()
        elif type == RETURN: return self.parse_RETURN()
        elif type == END:    return self.parse_END()   
        elif type == REM:    return self.parse_REM()         
        else: raise Exception(f"parsing: {self.current_token}")
        

class TinyBasic(object):

    def __init__(self, input, output, vars, stack, line_number, raw_lines):
        self.input = input
        self.output = output
        self.vars = vars
        self.stack = stack
        self.line_number = line_number
        self.raw_lines = raw_lines
        self.memory = {}

    def tokenize(self, line):
        tokens = []
        lexer = Lexer(line)    
        while (True):
            token = lexer.get_next_token()
            if token.type == EOL:
                break
            tokens.append(token)
        return tokens

    def parse_line(self, raw_line):        
        tokens = raw_line.split(' ', 1)
        if len(tokens) == 1: raise Exception("empty line?")
        line_number = int(tokens[0])
        raw_sub_line = tokens[1]
        if not raw_sub_line: raise Exception("empty line")
        tokens = self.tokenize(raw_sub_line)
        parser = Parser(self.input, self.output, line_number, tokens, self.vars, self.stack)
        node = parser.parse_statement()
        self.memory[line_number] = node

    def parse_all(self):
        for raw_line in self.raw_lines:
            if not raw_line.strip(): continue
            try:
                self.parse_line(raw_line)
            except Exception as e:
                raise Exception(f"{raw_line}, {e}")

    def get_next_line_number(self, line_number, line_numbers, current_index):
        if line_number == None:                    # just use next line
            next_index = line_numbers.index(current_index) + 1
        elif line_number < 0:                      # coming from RETURN
            next_index = line_numbers.index(-line_number) + 1
        elif line_number == 0: return              # coming from END
        else: return line_number                   # coming from GOTO or GOSUB              
        if next_index >= len(line_numbers): return # last statement reached
        return line_numbers[next_index]  

    def run(self):
        if len(self.memory) == 0: raise Exception("nothing to run")
        self.line_numbers = sorted(self.memory.keys())
        self.line_number = self.line_numbers[0]
        while True:
            if self.line_number not in self.memory:
                raise Exception(f"{statement}, line number not found")
            statement = self.memory[self.line_number]
            result = statement.visit()
            self.line_number = self.get_next_line_number(result, self.line_numbers, self.line_number)
            if self.line_number == None: break

    def execute_immediate(self, command):
        if command == LIST:
            lines_numbers = sorted(self.memory.keys())
            for line_number in lines_numbers:
                statement = self.memory[line_number]                
                self.output.write(f"{line_number} {statement}\n")
        elif command == RUN: self.run()
        elif command == CLEAR: self.memory.clear()
        self.output.write("OK\n")

    def repl(self):
        for raw_line in self.input:
            try:
                raw_line = raw_line.strip()
                if not raw_line: continue
                if raw_line[0].isdigit():
                    self.parse_line(raw_line)
                else:
                    tokens = self.tokenize(raw_line)
                    if tokens[0].value.upper() in IMMEDIATE_KEYWORDS:
                        self.execute_immediate(tokens[0].value.upper())
                    else:
                        parser = Parser(self.input, self.output, 0, tokens, self.vars, self.stack)
                        node = parser.parse_statement()
                        node.visit()
                        self.output.write("OK\n")
            except Exception as e:
                print(f"ERROR: {raw_line}, {e}", file=sys.stderr)
                raise e


def run(source_filename):
    with open(source_filename, 'r') as file:
        raw_lines = file.readlines()
    tiny_basic = TinyBasic(sys.stdin, sys.stdout, {}, [], 0, raw_lines)
    try:
        tiny_basic.parse_all()
        tiny_basic.run()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)

def repl():
    tiny_basic = TinyBasic(sys.stdin, sys.stdout, {}, [], 0, None)
    tiny_basic.repl()

def main(argv):
    print("Tiny Basic v0.1")
    if len(argv) == 1:
        run(argv[0])
    else:
        repl()

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
