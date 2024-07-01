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
'''
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

#very unoptimized code for finding regions
#returns a list of lists of edges which form the boundary of each region
def find_regions(gauss):
    regions = []
    temp = gauss.copy()

    #preprocessing to remove loops, i.e. edges of the form (n, -n)
    for i in range(len(gauss)):
        if gauss[i - 1] == -1 * gauss[i]:
            temp.remove(gauss[i - 1])
            temp.remove(gauss[i])
            regions.append([gauss[i - 1], gauss[i]])

    #generate every pair of edges that meet at perpendicularly at a crossing, i.e. ((x, y), (-y, z))
    edge_pairs = []
    for i in range(len(temp)):
        if (temp[i] < 0):
            continue
        j = temp.index(-1 * temp[i])
        l = len(temp)
        edge_pairs.append(((temp[i - 1], temp[i]), (temp[j], temp[j - 1])))
        edge_pairs.append(((temp[i - 1], temp[i]), (temp[j], temp[j + 1 - l])))
        edge_pairs.append(((temp[i + 1 - l], temp[i]), (temp[j], temp[j - 1])))
        edge_pairs.append(((temp[i + 1 - l], temp[i]), (temp[j], temp[j + 1 - l])))

    #repeat while there are edge pairs remaining to traverse
    while len(edge_pairs):
        ((a, b), (c, d)) = edge_pairs.pop()
        history = [a, b, c, d]

        #repeat while the current path history isn't empty
        while len(history):
            (x, y) = (history[-2], history[-1])

            #repeat while we haven't self intersected
            while -1 * y not in history:
                for ((a, b), (c, d)) in edge_pairs:
                    if x == a and y == b:
                        history += [c, d]
                        edge_pairs.remove(((a, b), (c, d)))
                        break
                    elif x == d and y == c:
                        history += [b, a]
                        edge_pairs.remove(((a, b), (c, d)))
                        break
                else:
                    print(edge_pairs, "\n", history, "\n", regions)
                    raise Exception(1)
                (x, y) = (history[-2], history[-1])

            #otherwise, remove self intersection and add to our list of
            i = history.index(-1 * y)
            if ((x, y), (history[i], history[i+1])) in edge_pairs:
                edge_pairs.remove(((x, y), (history[i], history[i+1])))
            elif ((history[i + 1], history[i]), (y, x)) in edge_pairs:
                edge_pairs.remove(((history[i + 1], history[i]), (y, x)))
            else:
                print(edge_pairs, "\n", history, "\n", regions)
                raise Exception(2)
            regions.append(history[i:])
            history = history[:i]

    return regions
            
'''
def all_type_1(gauss):
    n = max(gauss) + 1
    out = []
    for i in range(len(gauss)):
        out += [gauss[:i] + [n, -n] + gauss[i:], gauss[:i] + [-n, n] + gauss[i:]]
    return out
'''
def type_1(gauss, edge, parity):
    edge = is_edge(gauss, edge)
    if not edge:
        return None
    
    n = max(gauss) + 1
    (_, b) = edge
    i = gauss.index(b)
    return gauss[:i] + [n, -n] + gauss[i:] if parity else gauss[:i] + [-n, n] + gauss[i:]

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
print(type_1(gauss, (1, -2), True))
print(find_regions(type_1(gauss, (1, -2), True)))
