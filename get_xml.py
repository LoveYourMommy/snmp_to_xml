from pysnmp.entity.rfc3413.oneliner import cmdgen

import time
import sys
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
for i in oids_value:
    print(i, ' = ', oids_value[i])
print('Choose filter')

Filter = input('Filter: ') or 'disabled'
values = Filter.split(' ')



def grep(oidlist, keyword):
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


list_of_oids = grep(oids_value, values)
print(list_of_oids)
srt = list(list_of_oids.keys())
srt.sort()
print('Filtered')
for i in srt:
    print(i, ' = ', list_of_oids[i])

file_name = IP + ' ' + DATE + '.xml'
print('Next interfaces added to' + file_name)
for i in srt:
    print(i + '=' + list_of_oids[i])

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

