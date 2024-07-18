import subprocess

def generate_k4(a, b, c, d, e, f):
    (e01, e02, e03, e12, e13, e23) = (((0, 1), a), ((0, 2), b), ((0, 3), c), ((1, 2), d), ((1, 3), e), ((2, 3), f))
    return [[e01, e02, e03], [e01, e13, e12], [e02, e12, e23], [e03, e23, e13]]

def generate_two(a, b, c, d):
    (e0, e1, e2, e3) = (((0, 1), a, 0), ((0, 1), b, 1), ((0, 1), c, 2), ((0, 1), d, 3))
    return [[e0, e1, e2, e3], [e3, e2, e1, e0]]

def generate_all_sign_two(a, b, c, d):
    return [generate_two(a, b, -c, -d),
        generate_two(a, -b, c, -d),
        generate_two(a, -b, -c, d),
        generate_two(-a, b, c, -d),
        generate_two(-a, b, -c, d),
        generate_two(-a, -b, c, d)]

def format_mathematica(l):
    return str(l).replace("[", "{").replace("]", "}")

#takes a graph spec of form [[(v1, v2, (optional) id), (v1, v2, (optional) id), ...], [...], [...], ...]
#returns a list of parities that give valid knots (i.e. not links)
def check_all_parity(g):
    edges = []
    for v in g:
        for e in v:
            if e not in edges:
                edges.append(e)
    
    out = []
    for i in range(2**len(edges)):
        e_map = {}
        for e in edges:
            e_map[e] = 2 - (i % 2)
            i >>= 1

        temp = []
        for v in g:
            acc = []
            for e in v:
                (a, b, *rest) = e
                acc.append(((a, b), e_map[e], *rest))
            temp.append(acc)
        if (gauss_from_weighted_graph(temp)):
            out.append(list(e_map.values()))
    return out

#k must be at least 4
def generate_up_to_k(g, parities, k):
    edges = []
    for v in g:
        for e in v:
            if e not in edges:
                edges.append(e)
    
    parities = [x + k - 2 for x in parities]

    def valid():
        if parities[-1] < 3: #skip mirror images so no need to check negative values on the last element 
            return False
        for i in range(len(parities) - 1):
            if (-3 < parities[i] < 3):
                parities[i] -= 2
                return valid()
            if (parities[i] < -k):
                parities[i] = k - parities[i] % 2
                parities[i + 1] -= 2
                return valid()
            
        count = 0
        for p in parities:
            count += 1 if p < 0 else 0
        if (count < 2 or len(parities) - count < 2):
            parities[0] -= 2
            return valid()
        return True


    out = []
    while valid():
        temp = []
        for v in g:
            acc = []
            for e in v:
                (a, b, *rest) = e
                acc.append(((a, b), parities[edges.index(e)], *rest))
            temp.append(acc)
        out.append((parities.copy(), gauss_from_weighted_graph(temp)))
        parities[0] -= 2
    
    return out
    
def generate_up_to_k_with_sign(g, parities, k):
    edges = []
    for v in g:
        for e in v:
            if e not in edges:
                edges.append(e)
    signs = [1 if x > 0 else -1 for x in parities]
    parities = [abs(x) + k - 2 for x in parities]

    def valid():
        if parities[-1] < 3: 
            return False
        for i in range(len(parities) - 1):
            if (parities[i] < 3):
                parities[i] = k - parities[i] % 2
                parities[i + 1] -= 2
                return valid()
        return True


    out = []
    while valid():
        temp = []
        for v in g:
            acc = []
            prod = [signs[i] * parities[i] for i in range(len(signs))]
            for e in v:
                (a, b, *rest) = e
                acc.append(((a, b), prod[edges.index(e)], *rest))
            temp.append(acc)
        out.append((prod.copy(), gauss_from_weighted_graph(temp)))
        parities[0] -= 2
    
    return out
    



#gives gauss code after replacing each edge with `edge_weight` tangles
def gauss_from_weighted_graph(g):
    edges = []
    for v in g:
        for e in v:
            if e not in edges:
                edges.append(e)
    
    assoc_crossings = {}
    count = 1
    for e in edges:
        (_, w, *_) = e
        assoc_crossings[e] = list(range(count, count + abs(w)))
        count += abs(w)
    #print(assoc_crossings)
    #takes (edge, 0 if "foward direction" else 1, 0 if "starting left" else 1) and returns (gauss, next input)
    def inner(edge, direction, parity):
        ((a, b), w, *_) = edge
        small = assoc_crossings[edge].copy()

        if (direction):
            small = small[::-1]
        if (parity == (w > 0)):
            small[0] *= -1
        for i in range(1, len(small)):
            small[i] *= -1 if small[i - 1] > 0 else 1
        x = a if direction else b
        mod = -1 if parity == (w % 2) else 1
        next = g[x][(g[x].index(edge) + mod) % len(g[x])]
        next_direction = 0 if next[0][0] == x else 1
        next_parity = 0 if parity == (w % 2) else 1
        return small, (next, next_direction, next_parity)


    gauss = []
    visited = []
    current_v = (g[0][0], 0, 0)
    #print(inner(*current_v))
    while current_v not in visited:
        #print(gauss, "\n", current_v)
        visited.append(current_v)
        small, current_v = inner(*current_v)
        gauss += small
    if len(visited) != 2 * len(edges):
        return None
    return gauss

#(e010,e011,e020,e021,e12) = ((0,1,0), (0, 1, 1), (0, 2, 0), (0, 2, 1), (1, 2))
#g = [[e010, e011, e020, e021], [e12, e011, e010], [e12, e021, e020]]
#parities = [-1, -1, -2, 1, 1]

(w0, w1, w2, w3, w4) = (-3, -3, -4, 3, 3)
(e010,e011,e020,e021,e12) = (((0,1),w0,0),((0,1),w1,1),((0,2),w2,0),((0,2),w3,1),((1, 2),w4))
print(gauss_from_weighted_graph([[e010, e011, e020, e021], [e12, e011, e010], [e12, e021, e020]]))

#print(check_all_parity(g))
#ouch = generate_up_to_k_with_sign(g, parities, 18)
#subprocess.run("pbcopy", text=True, input=format_mathematica([b for (_, b) in ouch]))
#print(len(ouch))

'''
print(sorted([ouch[i-1][0] for i in [1, 10, 19, 28, 37, 46, 55, 64, 4225, 4234, 4243, 4252, 4261, 4270, \
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
32567, 32576, 32631, 32640, 32695, 32704, 32750, 32759, 32768]]))




out = {}
for t in temp:
    p = []
    for v in t:
        p.append((2 - (v % 2)) * (1 if v > 0 else -1))
    out[tuple(p)] = out.get(tuple(p), []) + [t]
[print(i, ":", out[i]) for i in out]
'''
