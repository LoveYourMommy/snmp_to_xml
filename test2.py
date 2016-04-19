from copy import deepcopy


def grep(oidlist, keyword):
    if 'disabled' in keyword:
        return oidlist
    else:
        res = {}
        for k, v in oidlist.items():
            for i in keyword:
                if i in str(v):
                    res[k] = oidlist[k]
        oidlist = res
        return oidlist


def grepv(oidlist, keyword):
    res = deepcopy(oidlist)
    for k, v in res.items():
        for i in keyword:
            if i in str(v):
                del oidlist[k]
    return oidlist



dict = {'1321': 'Fa1', '1234': 'Fa2', '3123': 'Gi1', '23': 'Vlan3'}


while True:
    filter_choosing = input('grep[1] or grep -v [2] [default: without]: ') or 'without'
    if filter_choosing == 'without':
        print('No filters applied')
        break
    elif filter_choosing == '1':
        Filter = input('Filter: ') or 'disabled'
        inputs = Filter.split(' ')
        dict = grep(dict, inputs)
    elif filter_choosing == '2':
        Filter = input('Filter: ') or 'disabled'
        inputs = Filter.split(' ')
        grepv(dict, inputs)
    else:
        print('Wrong choice')
        break


print(dict)





'''

while True:
    Filter = input('Filter: ') or 'disabled'
    values = Filter.split(' ')
    grep(dict, values)
    print(dict)
    if 'disabled' in Filter:
        break

'''




