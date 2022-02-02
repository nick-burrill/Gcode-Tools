O100 (G84 R.H. Tapping Cycle)
(http://www.helmancnc.com/g84-tapping-cycle-example-cnc-program/)
N1 T18 M06
N2 G90 G54 G00 X0.625 Y0.625
N3 S500 M03
N4 G43 H18 Z1. M08
N5 G84 G99 Z-0.65 R0.1 F35.7143
N6 X-0.625 Y-0.625
N7 G80 G00 Z1. M09
N8 G53 G49 Z0. M05
N9 M30