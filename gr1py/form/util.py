"""

Various routines for checking consistency, converting among formats,
and preparing for use elsewhere in the package.
"""
import copy


def gr1c_to_python(ast, symtable=None):
    """Create new AST that uses Python from one having gr1c syntax.

    If symtable is not None, it will be used to ensure primed
    variables get unique names. Else, every primed variable is named
    as the original variable with the suffix '_next'.
    """
    if isinstance(ast, tuple):
        if len(ast) == 2 and ast[1] == "'":
            return ast[0]+'_next'
        elif len(ast) == 3 and ast[0] == '<->':
            return (' or ',
                    (' and ',
                     gr1c_to_python(ast[1], symtable=symtable),
                     gr1c_to_python(ast[2], symtable=symtable)),
                    (' and ',
                     ('not ', gr1c_to_python(ast[1], symtable=symtable)),
                     ('not ', gr1c_to_python(ast[2], symtable=symtable))))
        elif len(ast) == 3 and ast[0] == '->':
            return (' or ',
                    ('not ', gr1c_to_python(ast[1], symtable=symtable)),
                    gr1c_to_python(ast[2], symtable=symtable))
        else:
            return tuple([gr1c_to_python(sub, symtable=symtable) for sub in ast])
    else:
        if ast == '&':
            return ' and '
        elif ast == '|':
            return ' or '
        elif ast == '!':
            return 'not '
        else:
            return ast

def flatten(ast):
    if isinstance(ast, tuple):
        output = ''
        if len(ast) == 2:
            output += '(' + flatten(ast[0]) + flatten(ast[1]) + ')'
        elif len(ast) == 3:
            output += '(' + flatten(ast[1]) + flatten(ast[0]) + flatten(ast[2]) + ')'
        else:
            raise ValueError('Unexpected 4-tuple in AST')
    else:
        if ast == '=':
            output = '=='
        else:
            output = str(ast)
    return output

def get_support(symtab, ast):
    """Get set of variables occurring in parse tree.

    symtab is an object that defines __contains__(), i.e., for which
    the expression `x in symtab` is defined, where `x` is a variable
    name (type str). ast is a tree represented as tuples, e.g., as
    obtained from form.gr1c.parse().
    """
    pass

def gen_expr(asd, informat='gr1c'):
    assert informat == 'gr1c', 'Only the gr1c input format is supported.'
    if 'ENV' in asd:
        symtab = [dict([('name', x[0]), ('type', x[1]),
                        ('domain', x[2]), ('uncontrolled', True)])
                  for x in asd['ENV']]
    else:
        symtab = []
    if 'SYS' in asd:
        symtab += [dict([('name', x[0]), ('type', x[1]),
                        ('domain', x[2]), ('uncontrolled', False)])
                   for x in asd['SYS']]

    exprtab = dict()
    for k in asd:
        if k in ['ENV', 'SYS']:
            continue
        if k in ['ENVINIT', 'SYSINIT']:
            exprtab[k] = flatten(gr1c_to_python(asd[k]))
        else:
            exprtab[k] = []
            for subform in asd[k]:
                exprtab[k].append(flatten(gr1c_to_python(subform)))

    return symtab, exprtab

def fill_empty(exprtab):
    """

    Empty implies True.
    """
    exprtab = copy.deepcopy(exprtab)
    for subformula in ['ENVINIT', 'SYSINIT']:
        if ((subformula not in exprtab)
            or len(exprtab[subformula].strip()) == 0):
            exprtab[subformula] = 'True'
    for subformula in ['ENVTRANS', 'SYSTRANS', 'ENVGOAL', 'SYSGOAL']:
        if subformula not in exprtab or len(exprtab[subformula]) == 0:
            exprtab[subformula] = ['True']
        else:
            for k in range(len(exprtab[subformula])):
                if len(exprtab[subformula][k].strip()) == 0:
                    exprtab[subformula][k] = 'True'
    return exprtab
