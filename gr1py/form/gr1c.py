"""Parser for gr1c input format

gr1c can be found at http://scottman.net/2012/gr1c
A description of the input format is available at
http://slivingston.github.io/gr1c/md_spc_format.html
"""

tokens = (
    'AND_LIVENESS_OP', 'AND_SAFETY_OP',
    'LIVENESS_OP', 'SAFETY_OP', 'EVENTUALLY_OP',
    'EQUIV', 'IMPLIES',
    'LE_OP', 'GE_OP', 'NOT_EQUALS',
    'TRUE_CONSTANT', 'FALSE_CONSTANT', 'PRIME',
    'E_VARS', 'E_INIT', 'E_TRANS', 'E_GOAL',
    'S_VARS', 'S_INIT', 'S_TRANS', 'S_GOAL',
    'IDENTIFIER', 'NUMBER', 'COMMENT',
    'newline'
    )

def t_TRUE_CONSTANT(t):
    r'True'
    return t

def t_FALSE_CONSTANT(t):
    r'False'
    return t

def t_PRIME(t):
    r'\''
    return t

def t_E_VARS(t):
    r'ENV:'
    return t

def t_E_INIT(t):
    r'ENVINIT:'
    return t

def t_E_TRANS(t):
    r'ENVTRANS:'
    return t

def t_E_GOAL(t):
    r'ENVGOAL:'
    return t

def t_S_VARS(t):
    r'SYS:'
    return t

def t_S_INIT(t):
    r'SYSINIT:'
    return t

def t_S_TRANS(t):
    r'SYSTRANS:'
    return t

def t_S_GOAL(t):
    r'SYSGOAL:'
    return t

def t_NUMBER(t):
    r'(\d+)(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

def t_COMMENT(t):
    r'\#.*\n'
    pass

t_ignore = "  \t\r"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

literals = ['(', ')', '&', '|', '!', '=', ';', ',', '<', '>', '[', ']']
t_IDENTIFIER = r'[a-zA-Z_]\w*'
t_AND_LIVENESS_OP = r'&[ \t]*\[\]<>'
t_AND_SAFETY_OP = r'&[ \t]*\[\]'
t_LIVENESS_OP = r'\[\]<>'
t_SAFETY_OP = r'\[\]'
t_EVENTUALLY_OP = r'<>'

t_LE_OP = r'<='
t_GE_OP = r'>='
t_NOT_EQUALS = r'!='

t_EQUIV = r'<->'
t_IMPLIES = r'->'

def t_error(t):
    pass

import ply.lex as lex
lex.lex()

precedence = (
     ('left', '|'),
     ('left', '&'),
     ('left', '!'),
     ('left', 'PRIME'),
     ('right', '='),
     ('nonassoc', 'NUMBER', 'IDENTIFIER')
     )

def p_input(p):
    """input : input exp
             | exp
    """
    if len(p) == 2:
        if p[1] != ';':
            p[0] = p[1]
    elif p[2] != ';':
        p[0] = p[1]
        p[0].update(p[2])
    else:
        p[0] = p[1]

def p_exp(p):
    """exp : E_VARS ';'
           | E_VARS evar_list ';'
           | S_VARS ';'
           | S_VARS svar_list ';'
           | E_INIT ';'
           | E_INIT propformula ';'
           | E_TRANS ';'
           | E_TRANS etransformula ';'
           | E_GOAL ';'
           | E_GOAL egoalformula ';'
           | S_INIT ';'
           | S_INIT propformula ';'
           | S_TRANS ';'
           | S_TRANS stransformula ';'
           | S_GOAL ';'
           | S_GOAL sgoalformula ';'
    """
    if p[1] == t_E_INIT.__doc__:
        if len(p) == 3:
            p[0] = {'ENVINIT': ''}
        else:
            p[0] = {'ENVINIT': p[2]}
    elif p[1] == t_S_INIT.__doc__:
        if len(p) == 3:
            p[0] = {'SYSINIT': ''}
        else:
            p[0] = {'SYSINIT': p[2]}
    elif p[1] == t_E_VARS.__doc__ and len(p) == 3:
        p[0] = {'ENV': []}
    elif p[1] == t_S_VARS.__doc__ and len(p) == 3:
        p[0] = {'SYS': []}
    else:
        p[0] = p[2]

def p_evar_list(p):
    """evar_list : evar_list IDENTIFIER
                 | evar_list IDENTIFIER '[' NUMBER ',' NUMBER ']'
                 | IDENTIFIER
                 | IDENTIFIER '[' NUMBER ',' NUMBER ']'
    """
    if len(p) == 2:
        p[0] = {'ENV': [(p[1], 'boolean', None)]}
    elif len(p) == 3:
        p[0] = p[1]
        p[0]['ENV'].append((p[2], 'boolean', None))
    elif len(p) == 7:
        p[0] = {'ENV': [(p[1], 'int', (p[3], p[5]))]}
    else:
        p[0] = p[1]
        p[0]['ENV'].append((p[2], 'int', (p[4], p[6])))

def p_svar_list(p):
    """svar_list : svar_list IDENTIFIER
                 | svar_list IDENTIFIER '[' NUMBER ',' NUMBER ']'
                 | IDENTIFIER
                 | IDENTIFIER '[' NUMBER ',' NUMBER ']'
    """
    if len(p) == 2:
        p[0] = {'SYS': [(p[1], 'boolean', None)]}
    elif len(p) == 3:
        p[0] = p[1]
        p[0]['SYS'].append((p[2], 'boolean', None))
    elif len(p) == 7:
        p[0] = {'SYS': [(p[1], 'int', (p[3], p[5]))]}
    else:
        p[0] = p[1]
        p[0]['SYS'].append((p[2], 'int', (p[4], p[6])))

def p_etransformula(p):
    """etransformula : SAFETY_OP tpropformula
                     | etransformula AND_SAFETY_OP tpropformula
    """
    if len(p) == 3:
        p[0] = {'ENVTRANS': [p[2]]}
    else:
        p[0] = p[1]
        p[0]['ENVTRANS'].append(p[3])

def p_stransformula(p):
    """stransformula : SAFETY_OP tpropformula
                     | stransformula AND_SAFETY_OP tpropformula
    """
    if len(p) == 3:
        p[0] = {'SYSTRANS': [p[2]]}
    else:
        p[0] = p[1]
        p[0]['SYSTRANS'].append(p[3])

def p_egoalformula(p):
    """egoalformula : LIVENESS_OP propformula
                    | egoalformula AND_LIVENESS_OP propformula
    """
    if len(p) == 3:
        p[0] = {'ENVGOAL': [p[2]]}
    else:
        p[0] = p[1]
        p[0]['ENVGOAL'].append(p[3])

def p_sgoalformula(p):
    """sgoalformula : LIVENESS_OP propformula
                    | sgoalformula AND_LIVENESS_OP propformula
    """
    if len(p) == 3:
        p[0] = {'SYSGOAL': [p[2]]}
    else:
        p[0] = p[1]
        p[0]['SYSGOAL'].append(p[3])

def p_propformula(p):
    """propformula : TRUE_CONSTANT
                   | FALSE_CONSTANT
                   | IDENTIFIER
                   | '!' propformula
                   | propformula '&' propformula
                   | propformula '|' propformula
                   | propformula IMPLIES propformula
                   | propformula EQUIV propformula
                   | IDENTIFIER '=' NUMBER
                   | IDENTIFIER '>' NUMBER
                   | IDENTIFIER '<' NUMBER
                   | IDENTIFIER LE_OP NUMBER
                   | IDENTIFIER GE_OP NUMBER
                   | IDENTIFIER NOT_EQUALS NUMBER
                   | '(' propformula ')'
    """
    if len(p) == 2:
        p[0] = p[1]
    elif p[1] == '!':
        p[0] = ('!', p[2])
    elif (p[2] == '&' or p[2] == '|' or p[2] == '->' or p[2] == '<->'
          or p[2] == '=' or p[2] == '>' or p[2] == '<' 
          or p[2] == '!=' or p[2] == '>=' or p[2] == '<='):
        p[0] = (p[2], p[1], p[3])
    else:  # ( subformula )
        p[0] = p[2]

def p_tpropformula(p):
    """tpropformula : TRUE_CONSTANT
                    | FALSE_CONSTANT
                    | IDENTIFIER
                    | IDENTIFIER PRIME
                    | '!' tpropformula
                    | tpropformula '&' tpropformula
                    | tpropformula '|' tpropformula
                    | tpropformula IMPLIES tpropformula
                    | tpropformula EQUIV tpropformula
                    | IDENTIFIER '=' NUMBER
                    | IDENTIFIER PRIME '=' NUMBER
                    | IDENTIFIER '>' NUMBER
                    | IDENTIFIER PRIME '>' NUMBER
                    | IDENTIFIER '<' NUMBER
                    | IDENTIFIER PRIME '<' NUMBER
                    | IDENTIFIER LE_OP NUMBER
                    | IDENTIFIER PRIME LE_OP NUMBER
                    | IDENTIFIER GE_OP NUMBER
                    | IDENTIFIER PRIME GE_OP NUMBER
                    | IDENTIFIER NOT_EQUALS NUMBER
                    | IDENTIFIER PRIME NOT_EQUALS NUMBER
                    | '(' tpropformula ')'
    """
    if len(p) == 2:
        p[0] = p[1]
    elif p[1] == '!':
        p[0] = ('!', p[2])
    elif (p[2] == '&' or p[2] == '|' or p[2] == '->' or p[2] == '<->'
          or p[2] == '=' or p[2] == '>' or p[2] == '<'
          or p[2] == '!=' or p[2] == '>=' or p[2] == '<='):
        p[0] = (p[2], p[1], p[3])
    elif (p[2] == '\'' and len(p) >= 5
          and (p[3] == '=' or p[3] == '>' or p[3] == '<'
               or p[3] == '!=' or p[3] == '>=' or p[3] == '<=')):
        p[0] = (p[3], (p[1], '\''), p[4])
    elif p[2] == '\'':
        p[0] = (p[1], '\'')
    else:  # ( subformula )
        p[0] = p[2]


import ply.yacc as yacc
from os.path import dirname
PWD = dirname(__file__)
lexer = lex.lex()
parser = yacc.yacc(tabmodule='gr1py.form.parsetab', outputdir=PWD)
parse = lambda x: parser.parse(x, lexer=lexer)
