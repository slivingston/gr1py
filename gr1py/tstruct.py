"""Temporal structures, e.g., transition system and game arena
"""
from __future__ import absolute_import
import itertools

try:
    from networkx import DiGraph
except ImportError:
    from .minnx import DiGraph


def stategen(symtab):
    statestab = []
    for v in symtab:
        if v['type'] == 'boolean':
            statestab.append(range(2))
        elif v['type'] == 'int':
            statestab.append(range(v['domain'][0], v['domain'][1]+1))
        else:
            raise TypeError('Unrecognized type "'+str(v['type'])
                            +'" of variable "'+str(v['name'])+'"')
    return itertools.product(*statestab)

def ts_from_expr(symtab, exprtab):
    """

    symtab and exprtab are as produced by form.util.gen_expr().
    """
    envtrans = dict()
    systrans = list()

    num_uncontrolled = len([i for i in range(len(symtab)) if symtab[i]['uncontrolled']])
    identifiers = [v['name'] for v in symtab]
    next_identifiers = [v['name']+'_next' for v in symtab]

    evalglobals = {'__builtins__': None, 'True': True, 'False': False}

    envtrans_formula = '(' + ') and ('.join(exprtab['ENVTRANS']) + ')'
    for state in stategen(symtab):
        stated = dict(zip(identifiers, state))
        envtrans[state] = []
        for next_state in stategen([v for v in symtab if v['uncontrolled']]):
            stated.update(dict(zip(next_identifiers, next_state)))
            if eval(envtrans_formula, evalglobals, stated):
                envtrans[state].append(next_state)

    systrans_formula = '(' + ') and ('.join(exprtab['SYSTRANS']) + ')'
    for state in stategen(symtab):
        stated = dict(zip(identifiers, state))
        for next_state in stategen(symtab):
            stated.update(dict(zip(next_identifiers, next_state)))
            if eval(systrans_formula, evalglobals, stated):
                systrans.append((state, next_state))

    G = DiGraph()
    G.add_edges_from(systrans)
    for nd in G.nodes():
        G.nodes[nd]['sat'] = list()
        stated = dict(zip(identifiers, nd))
        for subformula in ['ENVINIT', 'SYSINIT']:
            if eval(exprtab[subformula], evalglobals, stated):
                G.nodes[nd]['sat'].append(subformula)
        for subformula in ['ENVGOAL', 'SYSGOAL']:
            for (i, goalexpr) in enumerate(exprtab[subformula]):
                if eval(goalexpr, evalglobals, stated):
                    G.nodes[nd]['sat'].append(subformula+str(i))
                    
    return AnnTransitionSystem(symtab, G, envtrans,
                               num_egoals=len(exprtab['ENVGOAL']),
                               num_sgoals=len(exprtab['SYSGOAL']))

class AnnTransitionSystem(object):
    """Annotated transition system
    """
    def __init__(self, symtab, G, envtrans, num_egoals, num_sgoals):
        """

        Parameters are stored by reference, not copied.
        """
        self.G = G
        self.symtab = symtab
        self.envtrans = envtrans
        self.num_egoals = num_egoals
        self.num_sgoals = num_sgoals
        self.ind_uncontrolled = [i for i in range(len(symtab)) if symtab[i]['uncontrolled']]
