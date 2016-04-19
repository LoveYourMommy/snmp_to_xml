from pysnmp.entity.rfc3413.oneliner import cmdgen

import time
import sys
import operator
# import shutil
from copy import deepcopy

import onevalue
import xml_body


DATE = time.strftime('%Y-%m-%d %H-%M')
IP = input('IP: ')
community = input('Community (default: 3.1415926535): ') or '3.1415926535'
Group = input('Group: ')

sysname = onevalue.get_value(ip=IP, comm=community, oid='1.3.6.1.2.1.1.5.0')

oids_value = {}

cmdGen = cmdgen.CommandGenerator()
errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
    cmdgen.CommunityData(community),
    cmdgen.UdpTransportTarget((str(IP), 161)),
    '1.3.6.1.2.1.2.2.1.2'
)

if errorIndication:
    print(errorIndication)
    sys.exit()
else:
    for varBindTableRow in varBindTable:
        for name, val in varBindTableRow:
            a = name.prettyPrint().replace("SNMPv2-SMI::mib-2.2.2.1.2.", '')
            oids_value[a] = val.prettyPrint()

print('There are next interfaces:')
sorted_oids_value = sorted(oids_value.items(), key=operator.itemgetter(1))
for k, v in sorted_oids_value:
    print(k, ' = ', v)






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

def set_for_name(string):
    res = ''
    if 'FastEthernet' in string:
        res = string.replace('FastEthernet', 'Fa')
    elif 'GigabitEthernet' in string:
        res = string.replace('GigabitEthernet', 'Gi')
    return res


def set_for_keys(string):
    res = ''
    if 'FastEthernet' in string:
        res = string.replace('FastEthernet', 'Fa')
        res = res.replace('/', '-')
    elif 'GigabitEthernet' in string:
        res = string.replace('GigabitEthernet', 'Gi')
        res = res.replace('/', '-')
    return res


while True:
    filter_choosing = input('grep[1] or grep -v [2] [default: without]: ') or 'without'
    if filter_choosing == 'without':
        print('No filters applied')
        break
    if filter_choosing == 'end':
        print('Applying filter')
        break
    elif filter_choosing == '1':
        Filter = input('Filter: ') or 'disabled'
        inputs = Filter.split(' ')
        oids_value = grep(oids_value, inputs)
        for i in oids_value:
            print(oids_value[i])
    elif filter_choosing == '2':
        Filter = input('Filter: ') or 'disabled'
        inputs = Filter.split(' ')
        oids_value = grepv(oids_value, inputs)
        for i in oids_value:
            print(oids_value[i])
    else:
        print('Wrong choice')
        break



srt = list(oids_value.keys())
srt.sort()


file_name = IP + ' ' + DATE + '.xml'
print('Next interfaces added to' + file_name)
sorted_oids_value = sorted(oids_value.items(), key=operator.itemgetter(1))
for k, v in sorted_oids_value:
    print(k, ' = ', v)


f = open(file_name, 'w')

f.write(xml_body.header % (Group, sysname, sysname, Group, IP))

for i in srt:
    data = {'hostname': sysname, 'interface_key': set_for_keys(oids_value[i]),
            'interface_name': (set_for_name(oids_value[i])), 'interface_oid': i, 'comm': community}
    f.write(xml_body.items % data)

f.write(xml_body.items_triggers)

for i in srt:
    data = {'hostname': sysname, 'interface_key': set_for_keys(oids_value[i]),
            'interface_name': (set_for_name(oids_value[i]))}
    if 'Fast' in oids_value[i]:
        f.write(xml_body.triggers_fa % data)
    elif 'Giga' in oids_value[i]:
        f.write(xml_body.triggers_gi % data)

f.write(xml_body.triggers_graphs)

for i in srt:
    data = {'hostname': sysname, 'interface_key': set_for_keys(oids_value[i]),
            'interface_name': (set_for_name(oids_value[i]))}
    f.write(xml_body.graph % data)

f.write(xml_body.end_of_xml)
f.close()
# shutil.move(file_name, '/home/sgalay/')

