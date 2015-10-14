import gr1py.cli
from gr1py.solve import check_realizable


ARBITER1_SPC_GR1C = """
ENV: r1;
SYS: g1;

ENVINIT: !r1;
ENVTRANS:
[](((r1 & !g1) | (!r1 & g1)) -> ((r1' & r1) | (!r1' & !r1)));
ENVGOAL:
[]<>!(r1 & g1);

SYSINIT: !g1;
SYSTRANS:
[](((r1 & g1) | (!r1 & !g1)) -> ((g1 & g1') | (!g1 & !g1')));
SYSGOAL:
[]<>((r1 & g1) | (!r1 & !g1));
"""


def check_check_realizable(tsys, exprtab, expected):
    assert check_realizable(tsys, exprtab) == expected

def test_check_realizable():
    for spcstr, expected in [(ARBITER1_SPC_GR1C, True),
                             ('SYS:x;', True),
                             ('SYS: x;\nSYSGOAL: []<>False;', False)]:
        tsys, exprtab = gr1py.cli.loads(spcstr)
        yield check_check_realizable, tsys, exprtab, expected
