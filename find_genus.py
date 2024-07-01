gauss = [1, -2, 3, -1, 2, -3]

gauss_map = {}
for i in range(len(gauss)):
    gauss_map[gauss[i]] = (gauss[(i - 1 + len(gauss)) % len(gauss)], gauss[(i + 1) % len(gauss)])


a_switch = []
gauss_temp = gauss.copy()
while len(gauss_temp):
    loop = []
    key = gauss_temp[0]
    while key in gauss_temp:
        (_, after) = gauss_map[key]
        gauss_temp.remove(key)
        loop += [key, after]
        key = -1 * after
    a_switch.append(loop)

b_switch = []
gauss_temp = gauss.copy()
while len(gauss_temp):
    loop = []
    key = gauss_temp[0]
    backward = False
    while key in gauss_temp:
        print(key, " ", gauss_temp)

        (_, after) = gauss_map[key]
        gauss_temp.remove(key)
        if backward:
            loop += [after, key]
            key = -1 * key
        else:
            loop += [key, after]
            (key, _) = gauss_map[-1 * after]
        backward = not backward
    b_switch.append(loop)

print("A-switch:", a_switch)
print("B-switch:", b_switch)
print("Genus:", f"{(len(gauss) / 2 + 2 - len(a_switch) - len(b_switch)) / 2 : g}")