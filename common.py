def edge_list(gauss):
    out = []
    for i in range(len(gauss)):
        out.append((gauss[i], gauss[(i + 1) % len(gauss)]))
    return out

def reverse(edge):
    (a, b) = edge
    return (b, a)

#return edge in forward direction if it exists, otherwise return None
def is_edge(gauss, edge):
    edges = edge_list(gauss)
    (a, b) = edge
    if (a, b) in edges:
        return (a, b)
    if (b, a) in edges:
        return (b, a)
    return None

#very unoptimized code for finding regions
#returns a list of lists of edges which form the boundary of each region
def find_regions(gauss):
    regions = []
    temp = gauss.copy()

    #preprocessing to remove loops, i.e. edges of the form (n, -n)
    for i in range(len(gauss)):
        if gauss[i - 1] == -1 * gauss[i]:
            #temp.remove(gauss[i - 1])
            #temp.remove(gauss[i])
            #regions.append([gauss[i - 1], gauss[i]])
            raise Exception("Unhandled, not unique")

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

    #print(edge_pairs, "\n")
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
                        #print("1history:", history, "x,y:", (x, y), "a,b,c,d:", ((a, b), (c, d)))
                        break
                    elif x == d and y == c:
                        history += [b, a]
                        edge_pairs.remove(((a, b), (c, d)))
                        #print("2history:", history, "x,y:", (x, y), "a,b,c,d:", ((a, b), (c, d)))
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
            if (i != 0):
                edge_pairs.append(((history[i - 2], history[i - 1]), (history[i], history[i + 1])))
            regions.append(history[i:])
            history = history[:i]

    out = []
    for region in regions:
        post = []
        for i in range(len(region)):
            if i % 2 == 1:
                post.append((region[i - 1], region[i]))
        out.append(post)
    return out