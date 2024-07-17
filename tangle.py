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


#(e01, e02, e03, e12, e13, e23) = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
#g = [[e01, e02, e03], [e01, e13, e12], [e02, e12, e23], [e03, e23, e13]]
#edges = [e01, e02, e03, e12, e13, e23]
#parities = [1, 1, 1, 2, 1, 2]

(e010,e011,e020,e021,e12) = ((0,1,0), (0, 1, 1), (0, 2, 0), (0, 2, 1), (1, 2))
g = [[e010, e011, e020, e021], [e12, e011, e010], [e12, e021, e020]]
parities = [[1, 1, 1, 2, 2], [1, 1, 2, 1, 2], [1, 2, 1, 2, 1], [2, 1, 1, 2, 1], [1, 1, 1, 2, 1], [1, 2, 2, 1, 1], [1, 1, 2, 1, 1]]

print(check_all_parity(g))
ouch = [element for p in parities for element in generate_up_to_k(g, p, 8)]
subprocess.run("pbcopy", text=True, input=format_mathematica([b for (_, b) in ouch]))
print(len(ouch))

temp = sorted([ouch[i - 1][0] for i in [877, 884, 891, 1012, 1019, 1026, 1768, 1775, 1782, 1903, 1910, 1917, \
    1930, 1937, 1944, 3739, 3746, 3753, 3928, 3935, 3942, 4414, 4421, \
    4428, 4603, 4610, 4617, 4765, 4772, 4779, 10381, 10388, 10395, 10867, \
    10874, 10881, 11056, 11063, 11070, 11218, 11225, 11232, 11731, 11738, \
    11745, 11893, 11900, 11977, 11982, 12055, 12062, 12141, 12150, 14674, \
    14681, 14688, 15430, 15437, 15444, 15565, 15572, 15579, 15592, 15599, \
    15606, 16456, 16463, 16470, 16483, 16490, 16510, 16517, 16972, 16977, \
    17001, 17010]])
[print(i) for i in temp]

out = {}
for t in temp:
    p = []
    for v in t:
        p.append((2 - (v % 2)) * (1 if v > 0 else -1))
    out[tuple(p)] = out.get(tuple(p), []) + [t]
[print(i, ":", out[i]) for i in out]

print(ouch[876][1])

for p, g in ouch:
    if (p == [-3, -3, -4, 3, 3]):
        print(g)
#interesting_parities = [[1, 1, 1, 2, 2], [1, 1, 2, 1, 2], [1, 1, 1, 2, 1], [1, 2, 2, 1, 1], [1, 1, 2, 1, 1]]

#print(gauss_from_weighted_graph([[((a, b), parities[edges.index((a, b))]) for (a, b) in v] for v in g]))
#print(format_mathematica([gauss_from_weighted_graph(generate_k4(-4, -4, 4, 3, -3, -3)) for k in range(8)]))
#print(format_mathematica([gauss_from_weighted_graph(x) for x in generate_all_sign_two(3, 3, 4, 3)]))

#{175, 180, 219, 224, 551, 556, 611, 616, 1399, 1404, 1523, 1528, 1571, 1576, 1947, 1952, 2127, 2132, 2139, 2144}

