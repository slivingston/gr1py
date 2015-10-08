"""Solve various problems concerning the formula
"""
from __future__ import absolute_import

from .tstruct import stategen


def forallexists_pre(tsys, A):
    tmp = set()
    for s in A:
        for pre_s in tsys.G.predecessors_iter(s):
            for envpost in tsys.envtrans[pre_s]:
                canreach = False
                for post_pre_s in tsys.G.successors(pre_s):
                    if tuple([post_pre_s[i] for i in tsys.ind_uncontrolled]) != envpost:
                        continue
                    if post_pre_s in A:
                        canreach = True
                        break
                if not canreach:
                    break
            if canreach:
                tmp.add(pre_s)
    return tmp

def get_winning_set(tsys):
    S = set(tsys.G.nodes_iter())
    Z = [S.copy() for i in range(tsys.num_sgoals)]
    change_among_Z = True
    while change_among_Z:
        change_among_Z = False
        Z_prev = [this_Z.copy() for this_Z in Z]
        for i in range(len(Z)):
            this_Z_prev = Z[i].copy()
            Y = set()
            goal_progress = forallexists_pre(tsys, Z_prev[(i+1) % tsys.num_sgoals])
            goal_progress &= set([s for s in S if 'SYSGOAL'+str(i) in tsys.G.node[s]['sat']])
            while True:
                Y_prev = Y.copy()
                Y = set()
                Y_exmodal = forallexists_pre(tsys, Y_prev)
                reach_goal_progress = goal_progress.union(Y_exmodal)
                for j in range(tsys.num_egoals):
                    X = S.copy()
                    while True:
                        X_prev = X.copy()
                        X = forallexists_pre(tsys, X_prev)
                        X &= set([s for s in S if 'ENVGOAL'+str(j) not in tsys.G.node[s]['sat']])
                        X |= reach_goal_progress
                        if X == X_prev:
                            break
                        X &= X_prev
                    Y |= X

                if Y == Y_prev:
                    break
                Y |= Y_prev
            Z[i] = Y
            if Z[i] != this_Z_prev:
                change_among_Z = True
                Z[i] &= this_Z_prev
    return Z[0]

def check_realizable(tsys, exprtab, init_flags='ALL_ENV_EXIST_SYS_INIT'):
    assert init_flags.upper() == 'ALL_ENV_EXIST_SYS_INIT', 'Only the initial condition interpretation ALL_ENV_EXIST_SYS_INIT is supported.'

    W = get_winning_set(tsys)

    evalglobals = {'__builtins__': None, 'True': True, 'False': False}
    identifiers = [v['name'] for v in tsys.symtab]

    for state in stategen([v for v in tsys.symtab if v['uncontrolled']]):
        stated = dict(zip(identifiers, state))
        if not eval(exprtab['ENVINIT'], evalglobals, stated):
            continue
        found_match = False
        for s in W:
            if (tuple([s[i] for i in tsys.ind_uncontrolled]) == state
                and 'SYSINIT' in tsys.G.node[s]['sat']):
                found_match = True
                break
        if not found_match:
            return False

    return True
