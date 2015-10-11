from __future__ import absolute_import
import json
import time

from . import __version__


def dump_json(symtab, strategy):
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
    for nd, attr in strategy.nodes_iter(data=True):
        if first:
            first = False
        else:
            outs += ','
        outs += '"'+str(nd)+'": {\n'
        for key in ['state', 'mode', 'initial']:
            outs += '\t"'+key+'": '+json.dumps(attr[key])+',\n'
        outs += '\t"trans": '+json.dumps([str(next_nd) for next_nd
                                          in strategy.successors_iter(nd)])
        outs += ' }\n'
        
    return outs+'}}'

def dump_gr1caut(symtab, strategy):
    outs = '1\n'  # version 1
    for nd, attr in strategy.nodes_iter(data=True):
        outs += str(nd)+' ' + ' '.join([str(val) for val in attr['state']])
        outs += ' ' + str(1 if attr['initial'] else 0)
        outs += ' ' + str(attr['mode'])
        outs += ' -1'  # rgrad not implemented yet
        outs += ' ' + ' '.join([str(next_nd) for next_nd in strategy.successors(nd)])
        outs += '\n'
    return outs
