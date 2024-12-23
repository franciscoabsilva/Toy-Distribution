\* Toy_Distribution *\
Minimize
OBJ: Factory_1 + Factory_2 + Factory_3
Subject To
_C1: Factory_2 + Factory_3 >= 1
_C2: Factory_1 + Factory_2 >= 1
_C3: Factory_1 + Factory_2 >= 1
_C4: Factory_1 <= 1
_C5: Factory_2 <= 1
_C6: Factory_3 <= 1
Bounds
 0 <= Factory_1
 0 <= Factory_2
 0 <= Factory_3
Generals
Factory_1
Factory_2
Factory_3
End
