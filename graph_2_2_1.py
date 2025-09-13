from tangle import *

# given a 5 tuple of weights (a,b,c,d,e) such that a,b,c,d,e correspond to the left, second to left, second to right, right, and bottom tangle counts respectively
# returns true if the tuple satisfies a condition i believe to be necessary and sufficient for the Jones polynomial to have leading and falling coefficient not 1
# this condition is checked to be necessary and sufficient for |a|,|b|,|c|,|d|,|e|<=7, and sufficient for <=13 
def is_valid_5_tuple(l):
    [a, b, c, d, e] = l
    if not (a < 0 and a % 2 == 1 and b < 0 and b % 2 == 1 and c < 0 and c % 2 == 0 and d > 0 and d % 2 == 1 and e > 0 and e % 2 == 1):
        return None
    [a, b, c, d, e] = [abs(x) for x in [a, b, c, d, e]]
    match [a, b, c, d, e]:
        case [v, w, x, y, z] if w == v and x > (v + 1) / 2 and (v - 1) / 2 < y == z < x:
            return True
        case [v, w, x, y, z] if w == v and x == (v + 1) / 2 and y == z == x - 1:
            return True
        case [v, w, x, y, z] if w == v and x > (v - 3) / 2 and y == z + 2 == x + 3:
            return True
        case [v, w, x, y, z] if x == (v - 1) / 2 and w > v and y == z + 2 == x + 3:
            return True
        case [v, w, x, y, z] if x == (w - 1) / 2 and w < v and y == z + 2 == x + 3:
            return True
        case _:
            return False

# representation of the 2-2-1 triangle graph in my weird format
(e010,e011,e020,e021,e12) = ((0,1,0), (0, 1, 1), (0, 2, 0), (0, 2, 1), (1, 2))
g = [[e010, e011, e020, e021], [e12, e011, e010], [e12, e021, e020]] 
# by current evidence, the following parity (with signs) is necessary for the Jones polynomial to have leading and falling coef not 1 (up to mirror image)
parities = [-1, -1, -2, 1, 1]


# example of a set of working weights (w0, w1, ..., w4). the second and third line convert the weights to the graph form that gauss_from_weighted_graph accepts and prints the gauss code of the graph
'''
(w0, w1, w2, w3, w4) = [-3, -3, -10, 13, 11]
(e010,e011,e020,e021,e12) = (((0,1),w0,0),((0,1),w1,1),((0,2),w2,0),((0,2),w3,1),((1, 2),w4)) 
print(gauss_from_weighted_graph([[e010, e011, e020, e021], [e12, e011, e010], [e12, e021, e020]]))
'''

#check which parity assignments to g give a connected link
print(check_all_parity(g))

#generate the gauss codes of all weight assignments such that the maximum weight is 20, then copies the list to clipboard using the pbcopy command in a Mathematica pasteable format
'''
gauss_codes_up_to_20 = generate_up_to_k_with_sign(g, parities, 20, predicate=is_valid_5_tuple)
subprocess.run("pbcopy", text=True, input=format_mathematica([b for (_, b) in gauss_codes_up_to_20]))
print(len(gauss_codes_up_to_20))
'''

# stuff i don't want to try to understand
'''
ouch = generate_up_to_k_with_sign(g, parities, 18)
interesting = sorted([ouch[i-1][0] for i in [1, 10, 19, 28, 37, 46, 55, 64, 4225, 4234, 4243, 4252, 4261, 4270, \
4279, 4288, 4609, 4618, 4627, 4636, 4645, 4654, 4663, 4672, 4673, \
4682, 4691, 4700, 4709, 4718, 4727, 4736, 8897, 8906, 8915, 8924, \
8933, 8942, 8951, 8960, 9217, 9226, 9235, 9244, 9253, 9262, 9271, \
9280, 9281, 9290, 9299, 9308, 9317, 9326, 9335, 9344, 9345, 9354, \
9363, 9372, 9381, 9390, 9399, 9408, 13569, 13578, 13587, 13596, \
13605, 13614, 13623, 13632, 13825, 13834, 13843, 13852, 13861, 13870, \
13879, 13888, 13889, 13898, 13907, 13916, 13925, 13934, 13943, 13952, \
13953, 13962, 13971, 13980, 13989, 13998, 14007, 14016, 14017, 14026, \
14035, 14044, 14053, 14062, 14071, 14080, 18241, 18250, 18259, 18268, \
18277, 18286, 18295, 18304, 18433, 18442, 18451, 18460, 18469, 18478, \
18487, 18496, 18497, 18506, 18515, 18524, 18533, 18542, 18551, 18560, \
18561, 18570, 18579, 18588, 18597, 18606, 18615, 18624, 18625, 18634, \
18643, 18652, 18661, 18670, 18679, 18688, 18689, 18698, 18707, 18716, \
18725, 18734, 18743, 18752, 22915, 22923, 22929, 22930, 22931, 22940, \
22949, 22958, 22967, 22976, 23059, 23068, 23077, 23086, 23095, 23104, \
23123, 23132, 23141, 23150, 23159, 23168, 23187, 23196, 23205, 23214, \
23223, 23232, 23251, 23260, 23269, 23278, 23287, 23296, 23315, 23324, \
23333, 23342, 23351, 23360, 23370, 23379, 23388, 23397, 23406, 23415, \
23424, 27589, 27597, 27605, 27613, 27617, 27618, 27619, 27620, 27621, \
27630, 27639, 27648, 27685, 27694, 27703, 27712, 27749, 27758, 27767, \
27776, 27813, 27822, 27831, 27840, 27877, 27886, 27895, 27904, 27941, \
27950, 27959, 27968, 28005, 28014, 28023, 28032, 28060, 28069, 28078, \
28087, 28096, 32311, 32320, 32375, 32384, 32439, 32448, 32503, 32512, \
32567, 32576, 32631, 32640, 32695, 32704, 32750, 32759, 32768]])

#[print([a, b, c, d, e]) for [a, b, c, d, e] in interesting if [-e, -d, c, -b, -a] not in interesting]

#17 -> 8
#15 -> 8
#13 -> 6
#11 -> 6


out = {}
for t in temp:
    p = []
    for v in t:
        p.append((2 - (v % 2)) * (1 if v > 0 else -1))
    out[tuple(p)] = out.get(tuple(p), []) + [t]
[print(i, ":", out[i]) for i in out]

for (i, _) in ouch:
    x = is_valid_5_tuple(*i)
    if (x != None):
        if (not x) and i in interesting:
            print("False negative for:", i)
        elif x and i not in interesting:
            print("False positive for", i)
'''
