from common import *

def region_contains_e(region, edge):
    (a, b) = edge
    for i in range(len(region)):
        if region[i] == (a, b):
            return region[i + 1 - len(region)]
        if region[i] == (b, a):
            return reverse(region[i - 1])
    return None

def region_contains_c(region, crossing):
    for i in range(len(region)):
        (a, b) = region[i]
        if (a == crossing or b == crossing):
            return True
    return False

def alternating_regions(gauss):
    '''
    def region_contains_ece(region, edge_crossing_edge):
        (a, b, c, d) = edge_crossing_edge
        for i in range(len(region)):
            if (region[i - 1] == (a, b) and region[i] == (c, d)):
                return True
            elif (region[i - 1] == (d, c) and region[i] == (b, a)):
                return True
        return False
    '''
    regions = find_regions(gauss)
    black = [regions[0]]
    crossings = []
    for i in range(len(black[-1])):
        ((a, b), (c, d)) = (black[-1][i - 1], black[-1][i])
        crossings.append((a, b, c, d))

    while len(crossings):
        #print("c:", crossings)
        crossing = crossings.pop()
        (a, b, c, d) = crossing
        for region in regions:
            if region_contains_c(region, b) and (not region_contains_e(region, (a, b))) and (not region_contains_e(region, (c, d))):
                if region in black: 
                    continue
                #print("r:", region)
                black.append(region)
                for i in range(len(black[-1])):
                    ((a, b), (c, d)) = (black[-1][i - 1], black[-1][i])
                    crossings.append((a, b, c, d))
                break
    return black

def turaev(gauss):
    black = alternating_regions(gauss)
    white = find_regions(gauss)
    for region in black:
        white.remove(region)
    regions = [black, white]

    def inner(temp, parity):
        out = []
        for i in range(len(temp)):
            (a, b) = (temp[i - 1], temp[i])
            for region in regions[0 if parity else 1]:
                e = region_contains_e(region, (a, b))
                if e:
                    (c, d) = e
                    out.append((a, b, c, d))
                    break
            parity = not parity
        return out
    
    left_hand = inner(gauss, True) + inner(gauss[::-1], False)
    right_hand = inner(gauss, False) + inner(gauss[::-1], True)
    turns = [left_hand, right_hand]
    #print("t:", turns)
    edges = edge_list(gauss)

    def inner_two(parity):
        out = []
        temp = edges.copy()
        while len(temp):
            history = []
            (x, y) = temp[0]
            while len(history) < 2 or history[0] != x or history[1] != y:
                #print("h:", history, "\nx:", (x, y))
                history += [x, y]
                temp.remove(is_edge(gauss, (x, y)))
                for (a, b, c, d) in turns[0 if (y > 0) == parity else 1]:
                    if (x, y) == (a, b):
                        (x, y) = (c, d)
                        break
            out.append(history)
        return out
    
    a_switch = inner_two(True)
    b_switch = inner_two(False)
    print("A-switch:", a_switch)
    print("B-switch:", b_switch)
    print("Genus:", f"{(len(gauss) / 2 + 2 - len(a_switch) - len(b_switch)) / 2 : g}")
        
'''
def turaev(gauss):
    edges = edge_list(gauss)

    def inner(parity):
        out = []
        temp = edges.copy()
        while len(temp):
            (x, y) = temp.pop()
            history = [x, y]
            backward = False
            while True:
                if parity == (history[-1] > 0):
                    backward = not backward
                for (a, b) in temp:
                    if (not backward) and a == -1 * history[-1]:
                        history += [a, b]
                        temp.remove((a, b))
                        break
                    if backward and b == -1 * history[-1]:
                        history += [b, a]
                        temp.remove((a, b))
                        break
                else:
                    out.append(history)
                    break

        return out

    a_switch = inner(True)
    b_switch = inner(False)
    print("A-switch:", a_switch)
    print("B-switch:", b_switch)
    print("Genus:", f"{(len(gauss) / 2 + 2 - len(a_switch) - len(b_switch)) / 2 : g}")
'''