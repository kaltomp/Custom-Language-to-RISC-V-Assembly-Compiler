#Tompoulidis Kallinikos AM 5368
#Spyros Samoilis  AM 5344 

import sys
import os

sym_filename = 'out.symb'
int_filename = 'out.int'
asm_filename = 'out.asm'

quad_list = []
temp_counter = 0

def nextquad():
    return len(quad_list) + 1

def genquad(op, x, y, z):
    global quad_list
    quad = (nextquad(), op, x, y, z)
    quad_list.append(quad)
    return quad

def newtemp():
    global temp_counter
    temp_counter += 1
    name = f"T_{temp_counter}"
    tv = TempVariable(name, 0)
    sym_add_entity(tv)
    return name

def emptylist():
    return []

def makelist(x):
    return [x]

def merge(list1, list2):
    return list1 + list2

def backpatch(l, z):
    global quad_list
    for idx in l:
        index = idx - 1
        if index < len(quad_list):
            q = quad_list[index]
            quad_list[index] = (q[0], q[1], q[2], q[3], z)

# --- SYMBOL TABLE ---
class Entity:
    def __init__(self, name):
        self.name = name

class Variable(Entity):
    def __init__(self, name, offset):
        super().__init__(name)
        self.type = 'Variable'
        self.offset = offset

class Parameter(Entity):
    def __init__(self, name, mode, offset):
        super().__init__(name)
        self.type = 'Parameter'
        self.mode = mode
        self.offset = offset

class TempVariable(Entity):
    def __init__(self, name, offset):
        super().__init__(name)
        self.type = 'TempVariable'
        self.offset = offset

class Function(Entity):
    def __init__(self, name):
        super().__init__(name)
        self.type = 'Function'
        self.startQuad = -1
        self.frameLength = 0
        self.argumentList = []

class Argument:
    def __init__(self, name, type_mode):
        self.name = name
        self.type = type_mode 

class Scope:
    def __init__(self, level):
        self.level = level
        self.entityList = []
        self.offset = 12

scopes = []
all_completed_scopes_for_printing = []

def sym_add_scope():
    level = len(scopes)
    scopes.append(Scope(level))

def sym_remove_scope(name_hint=""):
    if scopes:
        s = scopes.pop()
        s.name_hint = name_hint
        all_completed_scopes_for_printing.append(s)
        return s
    return None

def sym_add_entity(entity):
    if len(scopes) == 0:
        return
    scope = scopes[-1]
    if isinstance(entity, (Variable, Parameter, TempVariable)):
        entity.offset = scope.offset
        scope.offset += 4
    scope.entityList.append(entity)
    
def sym_search_entity(name):
    for scope in reversed(scopes):
        for e in scope.entityList:
            if e.name == name:
                return e, scope.level
    return None, -1


class LexicalAnalyzer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.pos = 0
        self.line = 1
        self.keywords = {
            'program', 'declare', 'if', 'else', 'while', 
            'not', 'and', 'or', 'return', 'in', 'inout', 
            'function', 'input', 'print',  'switchcase', 'forcase', 'incase', 'untilcase', 'until', 'whilecase', 'when', 'default'
        }

    def error(self: "LexicalAnalyzer", message: str):
        print(f"Lexical Error at line {self.line}: {message}")
        sys.exit(1)

    def next_token(self: "LexicalAnalyzer"):
        while self.pos < len(self.source):
            char = self.source[self.pos]

        
            if char.isspace():
                if char == '\n':
                    self.line += 1
                self.pos += 1
                continue

           
            if char == '/' and self.pos + 1 < len(self.source):
                if self.source[self.pos + 1] == '/': 
                    self.pos += 2
                    while self.pos < len(self.source) and self.source[self.pos] != '\n':
                        self.pos += 1
                    continue
                elif self.source[self.pos + 1] == '*':
                    while self.pos + 1 < len(self.source) and not (self.source[self.pos] == '*' and self.source[self.pos+1] == '/'):
                        if self.source[self.pos] == '\n': self.line += 1
                        self.pos += 1
                    if self.pos + 1 >= len(self.source):
                        self.error("Unclosed comment")
                    self.pos += 2
                    continue

  
            if char.isalpha():
                start_pos = self.pos
                while self.pos < len(self.source) and self.source[self.pos].isalnum():
                    self.pos += 1
                word = ""
                for i in range(start_pos, self.pos):
                    word += self.source[i]
                word = word[:30] 
                if word in self.keywords:
                    return ('KEYWORD', word)
                return ('ID', word)

          
            if char.isdigit():
                start_pos = self.pos
                while self.pos < len(self.source) and self.source[self.pos].isdigit():
                    self.pos += 1
                num_str = ""
                for i in range(start_pos, self.pos):
                    num_str += self.source[i]
                num = int(num_str)
                if num > 32767 or num < -32767:   
                    self.error("Integer out of range -32767 to 32767")
                return ('NUMBER', num)

            if char == ':':
                if self.pos + 1 < len(self.source) and self.source[self.pos+1] == '=':
                    self.pos += 2
                    return ('ASSIGN', ':=')
                else:
                    self.pos += 1
                    return ('COLON', ':')
            
            
            if char == '<':
                self.pos += 1
                if self.pos < len(self.source) and self.source[self.pos] == '=':
                    self.pos += 1
                    return ('REL_OP', '<=')
                if self.pos < len(self.source) and self.source[self.pos] == '>':
                    self.pos += 1
                    return ('REL_OP', '<>')
                return ('REL_OP', '<')

            if char == '>':
                self.pos += 1
                if self.pos < len(self.source) and self.source[self.pos] == '=':
                    self.pos += 1
                    return ('REL_OP', '>=')
                return ('REL_OP', '>')

            simple_symbols = {'+': 'PLUS', '-': 'MINUS', '*': 'MULT', '/': 'DIV', 
                              '=': 'EQUAL', ',': 'COMMA', ';': 'SEMICOLON', 
                              '(': 'LPAREN', ')': 'RPAREN', '{': 'LBRACE', '}': 'RBRACE', '[': 'LBRACKET', ']': 'RBRACKET'}
            if char in simple_symbols:
                self.pos += 1
                return (simple_symbols[char], char)

            self.error(f"Unknown character '{char}'")
        
        return ('EOF', None)

class SyntaxAnalyzer:
    lexer: LexicalAnalyzer
    current_token: tuple

    def __init__(self, lexer: LexicalAnalyzer):
        self.lexer = lexer
        self.current_token = self.lexer.next_token()

    def error(self, message):
        print(f"Syntax error at line {self.lexer.line}: {message}")
        print(f"Found token: {self.current_token}")
        sys.exit(1)

    def match(self, expected_type, expected_value=None):
        if self.current_token[0] == expected_type:
            if expected_value is None or self.current_token[1] == expected_value:                self.current_token = self.lexer.next_token()
            else:
                self.error(f"Error, expected '{expected_value}'")
        else:
            self.error(f"Expected {expected_type}")

    def write_scope_log(self, scope, prefix=""):
        if not scope: return
        global sym_filename
        with open(sym_filename, 'a', encoding='utf-8') as f:
            f.write(f"{prefix}Scope Level: {scope.level}, Offset: {scope.offset}\n")
            f.write(f"Entities:\n")
            for e in scope.entityList:
                if isinstance(e, Variable):
                    f.write(f"  Variable: {e.name}, Offset: {e.offset}\n")
                elif isinstance(e, Parameter):
                    f.write(f"  Parameter: {e.name}, Mode: {e.mode}, Offset: {e.offset}\n")
                elif isinstance(e, TempVariable):
                    f.write(f"  TempVar: {e.name}, Offset: {e.offset}\n")
                elif isinstance(e, Function):
                    f.write(f"  Function: {e.name}, StartQuad: {e.startQuad}, FrameLength: {e.frameLength}\n")
                    if e.argumentList:
                        args_str = ", ".join([f"{a.name}({a.type})" for a in e.argumentList])
                        f.write(f"    Arguments: {args_str}\n")
            f.write("\n")


    def start_program(self):
        sym_add_scope()
        self.match('KEYWORD', 'program')
        prog_name = self.current_token[1]
        self.match('ID') 
        self.match('LBRACE') 
        self.block_body(prog_name, is_main=True)
        self.match('RBRACE') 
        completed_scope = sym_remove_scope(prog_name)
        self.write_scope_log(completed_scope, "=== Main Program ===\n")
        print("Syntaktikos elegxos petyxe")

    def block_body(self, block_name, is_main=False, func_entity=None):
        self.declarations()
        self.functions()

        start_q = nextquad()
        if func_entity:
            func_entity.startQuad = start_q
        genquad('begin_block', block_name, '_', '_')

        self.statements_sequence()

        if is_main:
            genquad('halt', '_', '_', '_')
            
        genquad('end_block', block_name, '_', '_')
        
        if func_entity:
            if len(scopes) > 0:
                func_entity.frameLength = scopes[-1].offset

    def functions(self):
        while self.current_token[1] == 'function':
            self.match('KEYWORD', 'function')
            func_name = self.current_token[1]
            self.match('ID')

            func_entity = Function(func_name)
            sym_add_entity(func_entity)
            
            sym_add_scope()

            self.match('LPAREN')
            self.formal_pars(func_entity)
            self.match('RPAREN')
            
           
            sym_add_entity(Parameter("_ret_", "RET", 0))
            
            self.match('LBRACE')
            self.block_body(func_name, is_main=False, func_entity=func_entity)
            self.match('RBRACE')
            completed_scope = sym_remove_scope(func_name)
            self.write_scope_log(completed_scope, f"=== Function: {func_name} ===\n")

    def formal_pars(self, func_entity):
        if self.current_token[1] in ['in', 'inout']:
            self.formal_par_item(func_entity)
            while self.current_token[0] == 'COMMA':
                self.match('COMMA')
                self.formal_par_item(func_entity)

    def formal_par_item(self, func_entity):
        mode = 'in'
        if self.current_token[1] == 'in':
            self.match('KEYWORD', 'in')
        else:
            mode = 'inout'
            self.match('KEYWORD', 'inout')
        
        param_name = self.current_token[1]
        self.match('ID')

        sym_add_entity(Parameter(param_name, mode, 0))
        func_entity.argumentList.append(Argument(param_name, mode))

    def declarations(self):
        while self.current_token[1] == 'declare':
            self.match('KEYWORD', 'declare')
            self.varlist()
            self.match('SEMICOLON')

    def varlist(self):
        if self.current_token[0] == 'ID':
            var_name = self.current_token[1]
            sym_add_entity(Variable(var_name, 0))
            self.match('ID')
            while self.current_token[0] == 'COMMA':
                self.match('COMMA')
                v_name = self.current_token[1]
                sym_add_entity(Variable(v_name, 0))
                self.match('ID')

    def statements(self):
        if self.current_token[0] == 'LBRACE':
            self.match('LBRACE')
            self.statements_sequence()
            self.match('RBRACE')
        else:
            self.one_statement() 

    def statements_sequence(self):
        if self.current_token[0] not in ['RBRACE', 'EOF']:
            self.one_statement()
            while self.current_token[0] == 'SEMICOLON':
                self.match('SEMICOLON')
                self.one_statement()

    def one_statement(self):
        if self.current_token[0] == 'ID':
            name = self.current_token[1]
            self.match('ID')
            self.match('ASSIGN') 
            place = self.expression()
            genquad(':=', place, '_', name)
            
        elif self.current_token[1] == 'if':
            self.if_statement()

        elif self.current_token[1] == 'while':
            self.while_statement()

        elif self.current_token[1] == 'switchcase':
            self.switchcase_statement()

        elif self.current_token[1] == 'forcase':
            self.forcase_statement()

        elif self.current_token[1] == 'whilecase':
            self.whilecase_statement()

        elif self.current_token[1] == 'incase':
            self.incase_statement()

        elif self.current_token[1] == 'untilcase':
            self.untilcase_statement()

        elif self.current_token[1] == 'return':
            self.match('KEYWORD', 'return')
            place = self.expression()
            genquad('ret', place, '_', '_')
            
        elif self.current_token[1] == 'print':
            self.match('KEYWORD', 'print')
            place = self.expression()
            genquad('out', place, '_', '_')
            
        elif self.current_token[1] == 'input':
            self.match('KEYWORD', 'input')
            name = self.current_token[1]
            self.match('ID')
            genquad('in', name, '_', '_')
            
        else:
            self.error("Invalid prompt")
    
     

    def condition(self):
        """ condition : boolterm ( 'or' boolterm )* """
        b_true, b_false = self.boolterm()
        while self.current_token[1] == 'or':
            backpatch(b_false, nextquad())
            self.match('KEYWORD', 'or')
            t2, f2 = self.boolterm()
            b_true = merge(b_true, t2)
            b_false = f2
        return b_true, b_false

    def boolterm(self):
        """ boolterm : boolfactor ( 'and' boolfactor )* """
        b_true, b_false = self.boolfactor()
        while self.current_token[1] == 'and':
            backpatch(b_true, nextquad())
            self.match('KEYWORD', 'and')
            t2, f2 = self.boolfactor()
            b_false = merge(b_false, f2)
            b_true = t2
        return b_true, b_false

    def boolfactor(self):
        if self.current_token[1] == 'not':
            self.match('KEYWORD', 'not')
            self.match('LBRACKET') 
            b_true, b_false = self.condition()
            self.match('RBRACKET')
            return b_false, b_true
            
        elif self.current_token[0] == 'LBRACKET':
            self.match('LBRACKET')
            b_true, b_false = self.condition()
            self.match('RBRACKET')
            return b_true, b_false
            
        else:
            e1 = self.expression()
            if self.current_token[0] in ['EQUAL', 'REL_OP']:
                op = self.current_token[1]
                self.match(self.current_token[0]) 
                e2 = self.expression()
                b_true = makelist(nextquad())
                genquad(op, e1, e2, '_')
                b_false = makelist(nextquad())
                genquad('jump', '_', '_', '_')
                return b_true, b_false
            else:
                self.error("Περίμενα σχεσιακό τελεστή (=, <, >, <=, >=, <>)")


    def expression(self):
        sign = '+'
        if self.current_token[0] in ['PLUS', 'MINUS']:
            sign = self.current_token[1]
            self.match(self.current_token[0])
            
        place = self.term()
        if sign == '-':
            w = newtemp()
            genquad('-', 0, place, w)
            place = w
        
        while self.current_token[0] in ['PLUS', 'MINUS']:
            op = self.current_token[1]
            self.match(self.current_token[0])
            t_place = self.term()
            w = newtemp()
            genquad(op, place, t_place, w)
            place = w
        return place

    def term(self):
        place = self.factor()
        
        while self.current_token[0] in ['MULT', 'DIV']:
            op = self.current_token[1]
            self.match(self.current_token[0])
            f_place = self.factor()
            w = newtemp()
            genquad(op, place, f_place, w)
            place = w
        return place

    def factor(self):
        if self.current_token[0] == 'NUMBER':
            place = self.current_token[1]
            self.match('NUMBER')
            return place
            
        elif self.current_token[0] == 'LPAREN':
            self.match('LPAREN')
            place = self.expression()
            self.match('RPAREN')
            return place
            
        elif self.current_token[0] == 'ID':
            name = self.current_token[1]
            self.match('ID')
            place = self.idtail(name) 
            return place
            
        else:
            self.error("Expected number, ID or RPAREN '('")

    def idtail(self, name):
        if self.current_token[0] == 'LPAREN':
            self.actualpars()
            w = newtemp()
            genquad('par', w, 'RET', '_')
            genquad('call', name, '_', '_')
            return w
        return name

    def actualpars(self):
        self.match('LPAREN')
        self.actualparlist()
        self.match('RPAREN')

    def actualparlist(self):
        if self.current_token[1] in ['in', 'inout']:
            self.actualparitem()
            while self.current_token[0] == 'COMMA':
                self.match('COMMA')
                self.actualparitem()

    def actualparitem(self):
        if self.current_token[1] == 'in':
            self.match('KEYWORD', 'in')
            place = self.expression()
            genquad('par', place, 'CV', '_')
        elif self.current_token[1] == 'inout':
            self.match('KEYWORD', 'inout')
            name = self.current_token[1]
            self.match('ID')
            genquad('par', name, 'REF', '_')
        else:
            self.error("Expected 'in' or 'inout'")
    

    def if_statement(self):
        self.match('KEYWORD', 'if')
        b_true, b_false = self.condition()
        backpatch(b_true, nextquad())
        self.statements()
        if self.current_token[1] == 'else':
            if_list = makelist(nextquad())
            genquad('jump', '_', '_', '_')
            backpatch(b_false, nextquad())
            self.match('KEYWORD', 'else')
            self.statements()
            backpatch(if_list, nextquad())
        else:
            backpatch(b_false, nextquad())

    def while_statement(self):
        self.match('KEYWORD', 'while')
        cond_quad = nextquad()
        b_true, b_false = self.condition()
        backpatch(b_true, nextquad())
        self.statements()
        genquad('jump', '_', '_', cond_quad)
        backpatch(b_false, nextquad())

    def forcase_statement(self):
        self.match('KEYWORD', 'forcase')
        id_name = self.current_token[1]
        self.match('ID')
        self.match('EQUAL') 
        val = self.current_token[1]
        self.match('NUMBER')
        
        genquad(':=', 1, '_', id_name)
        cond_quad = nextquad()
        
        genquad('>', id_name, val, '_') 
        exit_quad = nextquad() - 1 

        while self.current_token[1] == 'when':
            self.match('KEYWORD', 'when')
            b_true, b_false = self.condition()
            self.match('COLON')
            backpatch(b_true, nextquad())
            self.statements()
            backpatch(b_false, nextquad())
            
        w = newtemp()
        genquad('+', id_name, 1, w)
        genquad(':=', w, '_', id_name)
        genquad('jump', '_', '_', cond_quad)
        
        backpatch(makelist(exit_quad), nextquad())


    def switchcase_statement(self):
        self.match('KEYWORD', 'switchcase')
        exit_list = emptylist()
        
        while self.current_token[1] == 'when':
            self.match('KEYWORD', 'when')
            b_true, b_false = self.condition()
            self.match('COLON')
            backpatch(b_true, nextquad())
            self.statements()
            exit_list = merge(exit_list, makelist(nextquad()))
            genquad('jump', '_', '_', '_')
            backpatch(b_false, nextquad())
            
        self.match('KEYWORD', 'default')
        self.match('COLON')
        self.statements()
        backpatch(exit_list, nextquad())

    def whilecase_statement(self):
        self.match('KEYWORD', 'whilecase')
        cond_quad = nextquad()
        
        while self.current_token[1] == 'when':
            self.match('KEYWORD', 'when')
            b_true, b_false = self.condition()
            self.match('COLON')
            backpatch(b_true, nextquad())
            self.statements()
            genquad('jump', '_', '_', cond_quad)
            backpatch(b_false, nextquad())
            
        self.match('KEYWORD', 'default')
        self.match('COLON')
        self.statements()

    def incase_statement(self):
        self.match('KEYWORD', 'incase')
        flag = newtemp()
        first_quad = nextquad()
        genquad(':=', 0, '_', flag) 
        
        while self.current_token[1] == 'when':
            self.match('KEYWORD', 'when')
            b_true, b_false = self.condition()
            self.match('COLON')
            backpatch(b_true, nextquad())
            self.statements()
            genquad(':=', 1, '_', flag) 
            backpatch(b_false, nextquad())
            
        genquad('=', 1, flag, first_quad) 

    def untilcase_statement(self):
        self.match('KEYWORD', 'untilcase')
        start_quad = nextquad()
        
        while self.current_token[1] == 'when':
            self.match('KEYWORD', 'when')
            b_true, b_false = self.condition()
            self.match('COLON')
            backpatch(b_true, nextquad())
            self.statements()
            backpatch(b_false, nextquad())
            
        self.match('KEYWORD', 'until')
        u_true, u_false = self.condition()
        backpatch(u_false, start_quad)
        backpatch(u_true, nextquad())


asm_file = None

def emit(instr):
    global asm_file
    asm_file.write(f"    {instr}\n")

def emit_label(label):
    global asm_file
    asm_file.write(f"{label}:\n")

def get_scope_by_name(name):
    for s in all_completed_scopes_for_printing:
        if s.name_hint == name:
            return s
    return None

def find_entity_in_scope_hierarchy(name, start_scope):
    
    curr = start_scope
    while curr:
        for e in curr.entityList:
            if e.name == name:
                return e, curr.level
        
        parent_scope = None
        if curr.level > 0:
          
            for s in all_completed_scopes_for_printing:
                for ent in s.entityList:
                    if isinstance(ent, Function) and ent.name == curr.name_hint:
                        parent_scope = s
                        break
                if parent_scope: break
        curr = parent_scope
    return None, -1

def gnlvcode(v_name, current_scope):
    e, e_level = find_entity_in_scope_hierarchy(v_name, current_scope)
    emit(f"lw t0, 4(fp)")
    for _ in range(current_scope.level - e_level - 1):
        emit(f"lw t0, 4(t0)")
    return e

def loadvr(v, reg, current_scope):
    if str(v).isdigit() or (str(v).startswith('-') and str(v)[1:].isdigit()):
        emit(f"li {reg}, {v}")
    else:
        e, e_level = find_entity_in_scope_hierarchy(v, current_scope)
        if not e: return
        
        if e_level == 0:
            emit(f"lw {reg}, -{e.offset}(gp)")
        elif e_level == current_scope.level:
            if isinstance(e, Parameter) and e.mode == 'inout':
                emit(f"lw t0, -{e.offset}(fp)")
                emit(f"lw {reg}, (t0)")
            else:
                emit(f"lw {reg}, -{e.offset}(fp)")
        else:
            gnlvcode(v, current_scope)
            if isinstance(e, Parameter) and e.mode == 'inout':
                emit(f"lw t0, (t0)")
                emit(f"lw {reg}, (t0)")
            else:
                emit(f"lw {reg}, (t0)")

def storevr(reg, v, current_scope):
    e, e_level = find_entity_in_scope_hierarchy(v, current_scope)
    if not e: return
    
    if e_level == 0:
        emit(f"sw {reg}, -{e.offset}(gp)")
    elif e_level == current_scope.level:
        if isinstance(e, Parameter) and e.mode == 'inout':
            emit(f"lw t0, -{e.offset}(fp)")
            emit(f"sw {reg}, (t0)")
        else:
            emit(f"sw {reg}, -{e.offset}(fp)")
    else:
        gnlvcode(v, current_scope)
        if isinstance(e, Parameter) and e.mode == 'inout':
            emit(f"lw t0, (t0)")
            emit(f"sw {reg}, (t0)")
        else:
            emit(f"sw {reg}, (t0)")

def generate_final_riscv():
    global asm_file, asm_filename
    asm_file = open(asm_filename, 'w', encoding='utf-8')
    
    emit_label("L_main")
    emit("la sp, stack_end")
    emit("addi gp, sp, 0") 
    
    if not all_completed_scopes_for_printing: return
    main_prog = all_completed_scopes_for_printing[-1]
    emit(f"j L_{main_prog.name_hint}")
    
    current_scope = None
    par_count = 0
    
    jump_targets = set()
    for q in quad_list:
        if q[1] in ['jump', '<', '>', '<=', '>=', '=', '<>']:
            try: jump_targets.add(int(q[4]))
            except: pass

    for q in quad_list:
        q_idx, op, x, y, z = q
        if q_idx in jump_targets: emit_label(f"L{q_idx}")
            
        if op == 'begin_block':
            current_scope = get_scope_by_name(x)
            emit_label(f"L_{x}")
            emit(f"sw ra, 0(sp)")
            emit(f"addi fp, sp, 0")
            emit(f"addi sp, sp, -{current_scope.offset}")
            
        elif op == 'end_block':
            emit(f"lw ra, 0(fp)")
            emit(f"jr ra")
            
        elif op == ':=':
            loadvr(x, "t1", current_scope)
            storevr("t1", z, current_scope)
            
        elif op in ['+', '-', '*', '/']:
            loadvr(x, "t1", current_scope)
            loadvr(y, "t2", current_scope)
            if op == '+': emit(f"add t0, t1, t2")
            elif op == '-': emit(f"sub t0, t1, t2")
            elif op == '*': emit(f"mul t0, t1, t2")
            elif op == '/': emit(f"div t0, t1, t2")
            storevr("t0", z, current_scope)
            
        elif op == 'jump':
            emit(f"j L{z}")
            
        elif op in ['<', '>', '<=', '>=', '=', '<>']:
            loadvr(x, "t1", current_scope)
            loadvr(y, "t2", current_scope)
            instr = {"<":"blt", ">":"bgt", "<=":"ble", ">=":"bge", "=":"beq", "<>":"bne"}[op]
            emit(f"{instr} t1, t2, L{z}")
            
        elif op == 'out':
            loadvr(x, "a0", current_scope)
            emit("li a7, 1")
            emit("ecall")
            emit("li a0, 10")
            emit("li a7, 11")
            emit("ecall")
            
        elif op == 'in':
            emit("li a7, 5")
            emit("ecall")
            storevr("a0", x, current_scope)
            
        elif op == 'ret':
            loadvr(x, "t1", current_scope)
            # Find the hidden _ret_ parameter
            e_ret, _ = find_entity_in_scope_hierarchy("_ret_", current_scope)
            if e_ret:
                emit(f"lw t0, -{e_ret.offset}(fp)") 
                emit(f"sw t1, (t0)")
            
        elif op == 'par':
            next_f_len = 0
            for i in range(q_idx, len(quad_list)):
                if quad_list[i][1] == 'call':
                    f_name = quad_list[i][2]
                    s_target = get_scope_by_name(f_name)
                    if s_target: next_f_len = s_target.offset
                    break
            offset = 12 + 4 * par_count
            if y == 'CV':
                loadvr(x, "t1", current_scope)
                emit(f"sw t1, -{offset + next_f_len}(sp)")
            elif y == 'REF':
                e, e_level = find_entity_in_scope_hierarchy(x, current_scope)
                if e_level == current_scope.level:
                    if isinstance(e, Parameter) and e.mode == 'inout':
                        emit(f"lw t1, -{e.offset}(fp)")
                        emit(f"sw t1, -{offset + next_f_len}(sp)")
                    else:
                        emit(f"addi t1, fp, -{e.offset}")
                        emit(f"sw t1, -{offset + next_f_len}(sp)")
                else:
                    gnlvcode(x, current_scope)
                    if isinstance(e, Parameter) and e.mode == 'inout':
                        emit(f"lw t1, (t0)")
                        emit(f"sw t1, -{offset + next_f_len}(sp)")
                    else:
                        emit(f"addi t1, t0, 0")
                        emit(f"sw t1, -{offset + next_f_len}(sp)")
            elif y == 'RET':
                e, e_level = find_entity_in_scope_hierarchy(x, current_scope)
                emit(f"addi t1, fp, -{e.offset}")
                emit(f"sw t1, -{offset + next_f_len}(sp)")
            par_count += 1
            
        elif op == 'call':
            f_name = x
            f_ent, f_def_level = find_entity_in_scope_hierarchy(f_name, current_scope)
            s_target = get_scope_by_name(f_name)
            
     
            if f_def_level == current_scope.level:
      
                emit("addi t0, fp, 0")
                emit(f"sw t0, -{4 + s_target.offset}(sp)")
            else:
          
                emit("lw t0, 4(fp)")
                for _ in range(current_scope.level - f_def_level - 1):
                    emit("lw t0, 4(t0)")
                emit(f"sw t0, -{4 + s_target.offset}(sp)")
            
    
            emit("addi t0, fp, 0")
            emit(f"sw t0, -{8 + s_target.offset}(sp)")
            
            emit(f"addi sp, sp, -{s_target.offset}")
            emit(f"jal L_{f_name}")
            emit(f"addi sp, sp, {s_target.offset}")
            par_count = 0
            
        elif op == 'halt':
            emit("li a0, 0")
            emit("li a7, 93")
            emit("ecall")

    asm_file.write("\n.data\nstack: .space 10240\nstack_end:\n")
    asm_file.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compiler_phase2.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    base_name = filename.split('.')[0]
    
    sym_filename = base_name + '.symb'
    int_filename = base_name + '.int'
    asm_filename = base_name + '.asm'
    
    open(sym_filename, 'w', encoding='utf-8').close()
    open(int_filename, 'w', encoding='utf-8').close()
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        
        my_lexer = LexicalAnalyzer(code)
        my_parser = SyntaxAnalyzer(my_lexer)
        
        my_parser.start_program()
        
        with open(int_filename, 'w', encoding='utf-8') as iter_f:
            for q in quad_list:
                iter_f.write(f"{q[0]}: {q[1]}, {q[2]}, {q[3]}, {q[4]}\n")
                
       
        generate_final_riscv()
        print(f"Final RISC-V code generated in {asm_filename}")
                
       
        print("\n============================================================")
        print("  ΕΝΔΙΑΜΕΣΟΣ ΚΩΔΙΚΑΣ (Quads)")
        print("============================================================")
        for q in quad_list:
            print(f"{q[0]:6}: ({q[1]}, {q[2]}, {q[3]}, {q[4]})")
        print("============================================================\n\n")

        print("============================================================")
        print("  ΠΙΝΑΚΑΣ ΣΥΜΒΟΛΩΝ (όλα τα scopes)")
        print("============================================================")
        for scope in reversed(all_completed_scopes_for_printing):
            name = getattr(scope, 'name_hint', 'unknown')
            print(f"\n  Scope '{name}' (level={scope.level}, framelength={scope.offset}):")
            if not scope.entityList:
                print("    (κενό)")
            for e in scope.entityList:
                if isinstance(e, Variable):
                    print(f"    SymbolEntry(name='{e.name}', kind=variable, scope={scope.level}, offset={e.offset})")
                elif isinstance(e, Parameter):
                    print(f"    SymbolEntry(name='{e.name}', kind=parameter, scope={scope.level}, mode={e.mode}, offset={e.offset})")
                elif isinstance(e, TempVariable):
                    print(f"    SymbolEntry(name='{e.name}', kind=temp, scope={scope.level}, offset={e.offset})")
                elif isinstance(e, Function):
                    print(f"    SymbolEntry(name='{e.name}', kind=function, scope={scope.level}, start_quad={e.startQuad})")
        print("============================================================\n")
                
    except FileNotFoundError:
        print("File not found.")