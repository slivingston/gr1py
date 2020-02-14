"""Solve various problems concerning the formula
"""
from __future__ import absolute_import
import copy

try:
    from networkx import DiGraph
except ImportError:
    from .minnx import DiGraph

from .tstruct import stategen


def forallexists_pre(tsys, A):
    tmp = set()
    for s in A:
        for pre_s in tsys.G.predecessors(s):
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

def get_winning_set(tsys, return_intermediates=False):
    S = set(tsys.G.nodes())
    Z = [S.copy() for i in range(tsys.num_sgoals)]
    change_among_Z = True
    while change_among_Z:
        change_among_Z = False
        Z_prev = [this_Z.copy() for this_Z in Z]
        if return_intermediates:
            Y_list = [[] for i in range(len(Z))]
            X_list = [[] for i in range(len(Z))]
        for i in range(len(Z)):
            this_Z_prev = Z[i].copy()
            Y = set()
            if return_intermediates:
                num_sublevels = 0
            goal_progress = forallexists_pre(tsys, Z_prev[(i+1) % tsys.num_sgoals])
            goal_progress &= set([s for s in S if 'SYSGOAL'+str(i) in tsys.G.nodes[s]['sat']])
            while True:
                Y_prev = Y.copy()
                if return_intermediates:
                    Y_list[i].append(Y_prev)
                    num_sublevels += 1
                Y = set()
                Y_exmodal = forallexists_pre(tsys, Y_prev)
                reach_goal_progress = goal_progress.union(Y_exmodal)
                if return_intermediates:
                    X_list[i].append([])
                for j in range(tsys.num_egoals):
                    X = S.copy()
                    while True:
                        X_prev = X.copy()
                        X = forallexists_pre(tsys, X_prev)
                        X &= set([s for s in S if 'ENVGOAL'+str(j) not in tsys.G.nodes[s]['sat']])
                        X |= reach_goal_progress
                        if X == X_prev:
                            break
                        X &= X_prev
                    if return_intermediates:
                        X_list[i][num_sublevels-1].append(X)
                    Y |= X

                if Y == Y_prev:
                    if return_intermediates:
                        num_sublevels -= 1
                        X_list[i].pop()
                    break
                Y |= Y_prev
            Z[i] = Y
            if Z[i] != this_Z_prev:
                change_among_Z = True
                Z[i] &= this_Z_prev
    if return_intermediates:
        return Z[0], Y_list, X_list
    else:
        return Z[0]

def get_initial_states(W, tsys, exprtab, init_flags='ALL_ENV_EXIST_SYS_INIT'):
    """

    If initial conditions are not satisfied on the winning set, return None.
    """
    assert init_flags.upper() == 'ALL_ENV_EXIST_SYS_INIT', 'Only the initial condition interpretation ALL_ENV_EXIST_SYS_INIT is supported.'

    evalglobals = {'__builtins__': None, 'True': True, 'False': False}
    identifiers = [v['name'] for v in tsys.symtab]

    initial_states = list()

    for state in stategen([v for v in tsys.symtab if v['uncontrolled']]):
        stated = dict(zip(identifiers, state))
        if not eval(exprtab['ENVINIT'], evalglobals, stated):
            continue
        found_match = False
        for s in W:
            if (tuple([s[i] for i in tsys.ind_uncontrolled]) == state
                and 'SYSINIT' in tsys.G.nodes[s]['sat']):
                initial_states.append(copy.deepcopy(s))
                found_match = True
                break
        if not found_match:
            return None

    return initial_states

def check_realizable(tsys, exprtab, init_flags='ALL_ENV_EXIST_SYS_INIT'):
    W = get_winning_set(tsys)
    if get_initial_states(W, tsys, exprtab, init_flags) is None:
        return False
    else:
        return True

def synthesize(tsys, exprtab, init_flags='ALL_ENV_EXIST_SYS_INIT'):
    assert init_flags.upper() == 'ALL_ENV_EXIST_SYS_INIT', 'Only the initial condition interpretation ALL_ENV_EXIST_SYS_INIT is supported.'

    W, Y_list, X_list = get_winning_set(tsys, return_intermediates=True)
    initial_states = get_initial_states(W, tsys, exprtab, init_flags)
    if initial_states is None:
        return None

    goalnames = ['SYSGOAL'+str(i) for i in range(tsys.num_sgoals)]

    for goalmode in range(tsys.num_sgoals):
        Y_list[goalmode][0] = set([s for s in W if goalnames[goalmode] in tsys.G.nodes[s]['sat']])

    strategy = DiGraph()
    next_id = len(initial_states)
    workset = list(range(next_id))
    strategy.add_nodes_from([(i, {'state': s, 'mode': 0, 'initial': True})
                             for (i,s) in enumerate(initial_states)])
    while len(workset) > 0:
        nd = workset.pop()

        j = 0
        while j < len(Y_list[strategy.nodes[nd]['mode']]):
            if strategy.nodes[nd]['state'] in Y_list[strategy.nodes[nd]['mode']][j]:
                break
            j += 1
        if j == 0:
            assert goalnames[strategy.nodes[nd]['mode']] in tsys.G.nodes[strategy.nodes[nd]['state']]['sat']
            original_mode = strategy.nodes[nd]['mode']
            while goalnames[strategy.nodes[nd]['mode']] in tsys.G.nodes[strategy.nodes[nd]['state']]['sat']:
                strategy.nodes[nd]['mode'] = (strategy.nodes[nd]['mode'] + 1) % tsys.num_sgoals
                if strategy.nodes[nd]['mode'] == original_mode:
                    break
            if strategy.nodes[nd]['mode'] != original_mode:
                repeat_found = False
                for possible_repeat, attr in list(strategy.nodes(data=True)):
                    if (possible_repeat != nd
                        and attr['mode'] == strategy.nodes[nd]['mode']
                        and attr['state'] == strategy.nodes[nd]['state']):
                        repeat_found = True
                        for (u,v) in strategy.in_edges(nd):
                            strategy.add_edge(u, possible_repeat)
                        strategy.remove_edges_from(
                            list(strategy.in_edges(nd)))
                        strategy.remove_node(nd)
                        break
                if repeat_found:
                    continue

            j = 0
            while j < len(Y_list[strategy.nodes[nd]['mode']]):
                if strategy.nodes[nd]['state'] in Y_list[strategy.nodes[nd]['mode']][j]:
                    break
                j += 1
            if j == 0:
                assert goalnames[strategy.nodes[nd]['mode']] in tsys.G.nodes[strategy.nodes[nd]['state']]['sat']

        for envpost in tsys.envtrans[strategy.nodes[nd]['state']]:
            next_state = None
            for succ_nd in tsys.G.successors(strategy.nodes[nd]['state']):
                if (tuple([succ_nd[i] for i in tsys.ind_uncontrolled]) == envpost
                    and ((j > 0 and succ_nd in Y_list[strategy.nodes[nd]['mode']][j-1])
                         or (j == 0 and succ_nd in W))):
                    next_state = succ_nd
                    break

            if next_state is None:
                assert j > 0
                if j == 0:
                    import pdb; pdb.set_trace()
                blocking_index = None
                blocking_sets = X_list[strategy.nodes[nd]['mode']][j-1]
                for k in range(len(blocking_sets)):
                    if strategy.nodes[nd]['state'] in blocking_sets[k]:
                        blocking_index = k
                        break
                assert blocking_index is not None
                for succ_nd in tsys.G.successors(strategy.nodes[nd]['state']):
                    if (tuple([succ_nd[i] for i in tsys.ind_uncontrolled]) == envpost
                        and succ_nd in blocking_sets[blocking_index]):
                        next_state = succ_nd
                        break
                assert next_state is not None

            foundmatch = False
            for candidate, cattr in strategy.nodes(data=True):
                if cattr['state'] == next_state and cattr['mode'] == strategy.nodes[nd]['mode']:
                    strategy.add_edge(nd, candidate)
                    foundmatch = True
                    break
            if not foundmatch:
                if j == 0:
                    new_mode = (strategy.nodes[nd]['mode'] + 1) % tsys.num_sgoals
                else:
                    new_mode = strategy.nodes[nd]['mode']

                workset.append(next_id)
                strategy.add_node(
                    next_id,
                    state=next_state,
                    mode=new_mode,
                    initial=False)
                strategy.add_edge(nd, next_id)
                next_id += 1

    return strategy
