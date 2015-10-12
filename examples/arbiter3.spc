# The "arbiter" example for 3 input lines from
# N. Piterman, A. Pnueli, and Y. Sa'ar (2006). Synthesis of Reactive(1)
# Designs. *In Proc. 7th International Conference on Verification, Model
# Checking and Abstract Interpretation*.
#
# A Python script for generating an arbitrary size instance (i.e., for
# any number of input lines) is available in the examples directory of
# gr1c (http://scottman.net/2012/gr1c).

ENV: r1 r2 r3;
SYS: g1 g2 g3;

ENVINIT: !r1 & !r2 & !r3;
ENVTRANS:
  [](((r1 & !g1) | (!r1 & g1)) -> ((r1' & r1) | (!r1' & !r1)))
& [](((r2 & !g2) | (!r2 & g2)) -> ((r2' & r2) | (!r2' & !r2)))
& [](((r3 & !g3) | (!r3 & g3)) -> ((r3' & r3) | (!r3' & !r3)));
ENVGOAL:
  []<>!(r1 & g1)
& []<>!(r2 & g2)
& []<>!(r3 & g3);

SYSINIT: !g1 & !g2 & !g3;
SYSTRANS:
  [](!g1' | !g2')
& [](!g1' | !g3')
& [](!g2' | !g3')
& [](((r1 & g1) | (!r1 & !g1)) -> ((g1 & g1') | (!g1 & !g1')))
& [](((r2 & g2) | (!r2 & !g2)) -> ((g2 & g2') | (!g2 & !g2')))
& [](((r3 & g3) | (!r3 & !g3)) -> ((g3 & g3') | (!g3 & !g3')));
SYSGOAL:
  []<>((r1 & g1) | (!r1 & !g1))
& []<>((r2 & g2) | (!r2 & !g2))
& []<>((r3 & g3) | (!r3 & !g3));
