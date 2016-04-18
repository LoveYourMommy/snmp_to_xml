from pysnmp.hlapi import *
def get_value(ip, comm, oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
           getCmd(SnmpEngine(),
           CommunityData(comm),
           UdpTransportTarget((ip, 161)),
           ContextData(),
           ObjectType(ObjectIdentity(oid)))
    )

    if errorIndication:
        print(errorIndication)
        sys.exit()
    else:
        for x in varBinds:
            return str(x).replace('SNMPv2-MIB::sysName.0 = ', '')