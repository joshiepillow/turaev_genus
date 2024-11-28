import subprocess
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
def generate_up_to_k(g, parities, k, predicate=lambda _: True):
    edges = []
    for v in g:
        for e in v:
            if e not in edges:
                edges.append(e)
    
    parities = [x + k - 2 for x in parities]

    def valid():
        while True:
            if parities[-1] < 3: #skip mirror images so no need to check negative values on the last element 
                return False
            for i in range(len(parities) - 1):
                if (-3 < parities[i] < 3):
                    parities[i] -= 2
                    break
                if (parities[i] < -k):
                    parities[i] = k - parities[i] % 2
                    parities[i + 1] -= 2
                    break
            else:
                count = 0
                for p in parities:
                    count += 1 if p < 0 else 0
                if (count < 2 or len(parities) - count < 2):
                    parities[0] -= 2
                    continue
                if not predicate(parities):
                    parities[0] -= 2
                    continue
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
    
def generate_up_to_k_with_sign(g, parities, k, predicate=lambda _: True):
    edges = []
    for v in g:
        for e in v:
            if e not in edges:
                edges.append(e)
    signs = [1 if x > 0 else -1 for x in parities]
    parities = [abs(x) + k - 2 for x in parities]

    def prod():
        return [signs[i] * parities[i] for i in range(len(signs))]

    def valid():
        while True:
            if parities[-1] < 3: 
                return False
            for i in range(len(parities) - 1):
                if (parities[i] < 3):
                    parities[i] = k - parities[i] % 2
                    parities[i + 1] -= 2
                    break
            else: 
                if not predicate(prod()):
                    parities[0] -= 2
                    continue
                return True

    out = []
    while valid():
        temp = []
        for v in g:
            acc = []
            for e in v:
                (a, b, *rest) = e
                acc.append(((a, b), prod()[edges.index(e)], *rest))
            temp.append(acc)
        out.append((prod(), gauss_from_weighted_graph(temp)))
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