#!/usr/bin/python3

import string

vars = {}
stack = []

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
STRING = 'STRING'
NUMBER = 'NUMBER'
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

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({}, {})'.format(self.type, repr(self.value))

    def __repr__(self):
        return self.__str__()


RESERVED_KEYWORDS = {
    'REM':      Token('REM', 'REM'),
    'PRINT':    Token('PRINT', 'PRINT'),
    'IF':       Token('IF', 'IF'),
    'THEN':     Token('THEN', 'THEN'),
    'GOTO':     Token('GOTO', 'GOTO'),
    'INPUT':    Token('INPUT', 'INPUT'),
    'LET':      Token('LET', 'LET'),
    'GOSUB':    Token('GOSUB', 'GOSUB'),
    'RETURN':   Token('RETURN', 'RETURN'),
    'TAB':      Token('TAB', 'TAB'),
    'END':      Token('END', 'END')
}


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
        # print("  char: {}, pos: {}".format(self.current_char, self.pos))

    def skip_whitespace(self):
        while self.current_char != None and self.current_char.isspace():
            self.advance()

    def skip_line_comment(self):
        # result = ''
        while self.current_char is not None:
            # result += self.current_char
            self.advance()
        # token = Token(STRING, result)
        # return token

    def number(self):
        result = ''
        while (self.current_char is not None
                   and (self.current_char.isdigit() or self.current_char == '.')):
            result += self.current_char
            self.advance()
        return Token(NUMBER, int(result))

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
                # token = Token(INTEGER, self.integer(), self.line_number)
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
            
        return Token(EOL, None)

#--- lexer ------------------

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
        # result = self.expr.visit()
        # print("-------- result: {}".format(result))
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
                s = expr.visit()
                pos += len(s)
                print(s, end = "")
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
        return

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
        stack.push(self.line_number)

    def __str__(self):
        return "GOSUB {}".format(self.expr)


class ReturnStatement(AST):
    def __init__(self, line_number):
        self.line_number = line_number

    def visit(self):
        return stack.pop(0)

    def __str__(self):
        return "RETURN"


class EndStatement(AST):
    def __init__(self):
        pass

    def visit(self):
        return -1

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
        return vars[self.name]

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


class UnOp(AST):
    def __init__(self, op, factor):
        self.op = op
        self.factor = factor

    def visit(self):
        if self.op.type == PLUS:
            return self.factor.visit()
        elif self.op.type == MINUS:
            return -self.factor.visit()


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
        # print("  eating {}".format(type))
        if type == self.current_token.type or type == None:
            if len(self.line) > 0:
                self.current_token = self.line.pop(0)
            else:
                self.current_token == None
        else:
            raise Exception("expected {} but got {}".format(type, self.current_token.type))
        # print("current: {}".format(self.current_token))        

    def parse_var(self):
        name = self.current_token.value
        self.eat(ID)
        if len(name) > 1:
            raise Exception("vars length must be 1: {}".format(name))
        elif name not in string.ascii_uppercase:
            raise Exception("var name {} not allowed".format(name))
        return Var(name)

    def parse_factor(self):
        # print("  parse factor")
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            return UnOp(token, self.factor())
        elif token.type == MINUS:
            self.eat(MINUS)
            return UnOp(token, self.factor()) 
        elif token.type == NUMBER:
            self.eat(NUMBER)            
            return Num(token)
        elif token.type == ID:
            self.eat(ID)
            return Var(token.value)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.parse_expr()
            self.eat(RPAREN)
            return node
        raise Exception("parsing factor failed: {}".format(token))

    # term ::=
    #   factor ((* | /) factor)*
    def parse_term(self):        
        # print("  parse term")
        node = self.parse_factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            self.eat(None)
            node = BinOp(left=node, op=token, right=self.parse_factor())
        # logging.debug("return term node: " + str(node))
        return node    

    # expr ::=
    #   term ((+ | -) term)*
    def parse_expr(self):
        # print("  parse expr")
        node = self.parse_term()
        # print("  current: {}".format(self.current_token))
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            self.eat(None)
            node = BinOp(left=node, op=token, right=self.parse_term())
        return node


    def parse_TAB(self):
        print("TAB")
        self.eat(TAB)
        self.eat(LPAREN)
        expr = self.parse_expr()
        self.eat(RPAREN)
        return Tab(expr)


    def parse_expr_or_string(self):  
        print("c: {}".format(self.current_token))
        if self.current_token.type == TAB:
            node = self.parse_TAB()      
        elif self.current_token.type == STRING:
            node = String(self.current_token)
            self.eat(STRING)
        else:
            node = self.parse_expr()
        print("parse exp str: {}".format(node))
        return node

    def parse_expr_list(self):
        expr_list = []
        print("current: {}".format(self.current_token))
        expr_list.append(self.parse_expr_or_string())
        while self.current_token.type in (COMMA, SEMICOLON):
            expr_list.append(self.current_token)
            self.eat(None)
            expr_list.append(self.parse_expr_or_string())
        print("expr list: {}".format(expr_list))
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
            self.eat(None)
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
        return ReturnStatement(self.line_number)

    def parse_END(self):
        self.eat(END)
        return EndStatement()

    def parse_REM(self):
        self.eat(REM)
        return RemStatement()

    def parse_statement(self):
        # print("parse_statement: {}".format(self.line))
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

def get_lines(raw_lines):
    lines = {}
    line_index = 0
    for raw_line in raw_lines:
        if len(raw_line.strip()) == 0:
            continue
        if raw_line[0].isdigit():
            tokens = raw_line.strip().split(' ', 1)
            parsed_index = parse_int(tokens[0])
            lines[parsed_index] = tokens[1]
            line_index = parsed_index
        else:
            lines[line_index] = raw_line
        line_index += 1
    return lines

def tokenize(line):
    # print("tokenizing: {}".format(line))
    tokens = []
    lexer = Lexer(line)
    while (True):
        token = lexer.get_next_token()
        if token.type == EOL:
            break
        tokens.append(token)
    return tokens

def tokenize_all(raw_lines):
    lines = get_lines(raw_lines)    
    tokenized_lines = {}
    new_index = 0
    for index, line in lines.items():
        print("{}, line: {}".format(index, line))
        tokens = tokenize(line)
        # print("tokens: {}".format(tokens))
        if len(tokens) > 0:
            tokenized_lines[index] = tokens
            new_index += 1
    return tokenized_lines

def parse_all(tokenized_lines):
    parsed_lines = {}
    for index, line in list(tokenized_lines.items()):
        print("parse: {}".format(line))
        parser = Parser(index, line)
        node = parser.parse_statement()
        print("node: {}".format(node))
        parsed_lines[index] = node
    return parsed_lines

def interpret_all(parsed_lines):
    # print("p: {}".format(parsed_lines))
    line_numbers = list(parsed_lines.keys())
    next = line_numbers[0]
    while True:        
        # print("next line: {}".format(next))
        statement = parsed_lines[next]
        if statement == None:
            print("ERROR: line not found: {}".format(next))
            break        
        # print("statement: {}".format(statement))
        try:
            result = statement.visit()
        except Exception as exception:            
            print("\nError executing: {}".format(statement))
            print(exception)
            break
        if result == None:
            # prev statement returned no new line number
            next_index = line_numbers.index(next) + 1
            if next_index >= len(line_numbers):
                print("OK.")
                break
            next = line_numbers[next_index]            
        elif result == -1:
            # prev statement was END
            print("END. OK.")
            break
        else:
            next = result    

def main():
    import sys
    if len(sys.argv) < 2:
        print("syntax: tb <filename>")
        return
    print("==================================================")
    file = open(sys.argv[1], 'r')
    lines = file.readlines()
    tokenized_lines = tokenize_all(lines)
    parsed_lines = parse_all(tokenized_lines)
    interpret_all(parsed_lines)
    
if __name__ == '__main__':
    main()