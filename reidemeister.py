from functools import lru_cache

gauss = [1, -2, 3, -1, 2, -3]

#return edge in forward direction if it exists, otherwise return None
def is_edge(gauss, edge):
    edges = edge_list(gauss)
    (a, b) = edge
    if (a, b) in edges:
        return (a, b)
    if (b, a) in edges:
        return (b, a)
    return None

def reverse(edge):
    (a, b) = edge
    return (b, a)

def reverse_edge(gauss, edge):
    edge = is_edge(edge)
    if not gauss or not edge:
        return None
    (a, b) = edge
    out = gauss.copy()
    out[gauss.index(a)] = b
    out[gauss.index(b)] = a
    return out

#@lru_cache(maxsize=1)
def edge_list(gauss):
    out = []
    for i in range(len(gauss)):
        out.append((gauss[i], gauss[(i + 1) % len(gauss)]))
    return out

def find_connected(edges, value):
    for edge in edges:
        (a, b) = edge
        if a == value:
            return b
        if b == value:
            return a
    return None

#@lru_cache(maxsize=1)
def find_regions(gauss):
    edges = edge_list(gauss)
    edges += edges
    out = []
    while len(edges):
        current = list(edges.pop())
        while len(current):
            last = -1 * current[-1]
            while -1 * current[-1] not in current:
                next = find_connected(edges, last)
                current += [last, next]
                edges.remove(is_edge(gauss, (last, next)))
                last = -1 * current[-1]
            i = current.index(last)
            out.append(current[i:])
            current = current[:i]
    return out

    


'''
def all_type_1(gauss):
    n = max(gauss) + 1
    out = []
    for i in range(len(gauss)):
        out += [gauss[:i] + [n, -n] + gauss[i:], gauss[:i] + [-n, n] + gauss[i:]]
    return out
'''
def type_1(gauss, edge):
    edge = is_edge(gauss, edge)
    if not edge:
        return None
    
    n = max(gauss) + 1
    (_, b) = edge
    i = gauss.index(b)
    return gauss[:i] + [n, -n] + gauss[i:], gauss[:i] + [-n, n] + gauss[i:]

def type_3(gauss, crossing, edge):
    edge = is_edge(gauss, edge)
    if not edge:
        return None
    
    (a, b) = edge
    if (a * b < 0): #a and b have to have the same sign (i.e both under or both over)
        return None
    crossing_to_a = is_edge(crossing, -1 * a) or is_edge(-1 * crossing, -1 * a) 
    crossing_to_b = is_edge(crossing, -1 * b) or is_edge(-1 * crossing, -1 * b)
    return reverse_edge(reverse_edge(reverse_edge(gauss, (a, b)), (crossing_to_a)), crossing_to_b)
'''
def type_2(gauss, over_edge, under_edge):
    regions = find_regions(gauss)
    for region in regions:
        is_edge
'''

print(find_regions(gauss))
