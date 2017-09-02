from __future__ import absolute_import
import json
import time

from . import __version__


def dumps_json(symtab, strategy):
    outs = '{'+('"version": 1,\n'
            ' "gr1py": "{version}",\n'
            ' "date": "{date}",\n'
            ' "extra": "",\n').format(version=__version__,
                                     date=time.strftime("%Y-%m-%d %H:%M:%S",
                                                        time.gmtime()))
    outs += ' "ENV": ['+', '.join([('{"'+str(v['name'])+'": '
                                    +(('['+str(v['domain'][0])
                                       +','+str(v['domain'][1])+']')
                                      if v['type'] == 'int'
                                      else '"'+str(v['type'])+'"')
                                    +'}') for v in symtab
                                    if v['uncontrolled']])+'],\n'
    outs += ' "SYS": ['+', '.join([('{"'+str(v['name'])+'": '
                                    +(('['+str(v['domain'][0])
                                       +','+str(v['domain'][1])+']')
                                      if v['type'] == 'int'
                                      else '"'+str(v['type'])+'"')
                                    +'}') for v in symtab
                                    if not v['uncontrolled']])+'],\n'
    outs += ' "nodes": {\n'
    first = True
    for nd, attr in strategy.nodes(data=True):
        if first:
            first = False
        else:
            outs += ','
        outs += '"'+str(nd)+'": {\n'
        for key in ['state', 'mode', 'initial']:
            outs += '\t"'+key+'": '+json.dumps(attr[key])+',\n'
        outs += '\t"trans": '+json.dumps([str(next_nd) for next_nd
                                          in strategy.successors(nd)])
        outs += ' }\n'

    return outs+'}}'

def dumps_gr1caut(symtab, strategy):
    node_mapping = dict(zip(strategy.nodes(), range(strategy.number_of_nodes())))
    outs = '1\n'  # version 1
    for nd, attr in strategy.nodes(data=True):
        outs += str(node_mapping[nd])+' ' + ' '.join([str(val) for val in attr['state']])
        outs += ' ' + str(1 if attr['initial'] else 0)
        outs += ' ' + str(attr['mode'])
        outs += ' -1'  # rgrad not implemented yet
        outs += ' ' + ' '.join([str(node_mapping[next_nd]) for next_nd in strategy.successors(nd)])
        outs += '\n'
    return outs

def dumps_dot(symtab, strategy):
    idt = 4*' '
    outs = '/* created using gr1py, version {v} */\n'.format(v=__version__)
    outs += 'digraph A {\n'+idt+'"" [shape=none]\n'
    node_strings = dict()
    for nd, attr in strategy.nodes(data=True):
        node_strings[nd] = ('"'+str(nd)+';\\n'
                            +', '.join([sym['name']+'='+str(attr['state'][i])
                                       for (i,sym) in enumerate(symtab)])
                            +'"')
        outs += idt+node_strings[nd]+'\n'
        if attr['initial']:
            outs += '"" -> '+idt+node_strings[nd]+'\n'
    for (u, v) in strategy.edges():
        outs += idt+node_strings[u]+' -> '+node_strings[v]+'\n'
    return outs+'}'
