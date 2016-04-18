header = '''<?xml version="1.0" encoding="UTF-8"?>
    <zabbix_export>
    <version>2.0</version>
    <date>2015-02-22T12:42:58Z</date>
    <groups>
        <group>
            <name>%s</name>
        </group>
    </groups>
    <hosts>
        <host>
            <host>%s</host>
             <name>%s</name>
            <description/>
            <proxy>
            </proxy>
            <status>0</status>
            <ipmi_authtype>-1</ipmi_authtype>
            <ipmi_privilege>2</ipmi_privilege>
            <ipmi_username/>
            <ipmi_password/>
            <templates/>
            <groups>
                <group>
                    <name>%s</name>
                </group>
            </groups>
            <interfaces>
                <interface>
                    <default>1</default>
                    <type>2</type>
                    <useip>1</useip>
                    <ip>%s</ip>
                    <dns/>
                    <port>161</port>
                    <bulk>1</bulk>
                    <interface_ref>if1</interface_ref>
                </interface>
            </interfaces>
            <applications/>
            <items> '''


items = '''
 <item>
     <name>Traffic In %(interface_name)s</name>
     <type>4</type>
     <snmp_community>%(comm)s</snmp_community>
     <multiplier>1</multiplier>
     <snmp_oid>IF-MIB::ifHCInOctets.%(interface_oid)s</snmp_oid>
     <key>TrafficIn%(interface_key)s</key>
     <delay>90</delay>
     <history>7</history>
     <trends>365</trends>
     <status>0</status>
     <value_type>0</value_type>
     <allowed_hosts/>
     <units>b</units>
     <delta>1</delta>
     <snmpv3_contextname/>
     <snmpv3_securityname/>
     <snmpv3_securitylevel>0</snmpv3_securitylevel>
     <snmpv3_authprotocol>0</snmpv3_authprotocol>
     <snmpv3_authpassphrase/>
     <snmpv3_privprotocol>0</snmpv3_privprotocol>
     <snmpv3_privpassphrase/>
     <formula>8</formula>
     <delay_flex/>
     <params/>
     <ipmi_sensor/>
     <data_type>0</data_type>
     <authtype>0</authtype>
     <username/>
     <password/>
     <publickey/>
     <privatekey/>
     <port/>
     <description/>
     <inventory_link>0</inventory_link>
     <applications/>
     <valuemap/>
     <logtimefmt/>
     <interface_ref>if1</interface_ref>
 </item>
 <item>
     <name>Traffic Out %(interface_name)s</name>
     <type>4</type>
     <snmp_community>%(comm)s</snmp_community>
     <multiplier>1</multiplier>
     <snmp_oid>IF-MIB::ifHCOutOctets.%(interface_oid)s</snmp_oid>
     <key>TrafficOut%(interface_key)s</key>
     <delay>90</delay>
     <history>7</history>
     <trends>365</trends>
     <status>0</status>
     <value_type>0</value_type>
     <allowed_hosts/>
     <units>b</units>
     <delta>1</delta>
     <snmpv3_contextname/>
     <snmpv3_securityname/>
     <snmpv3_securitylevel>0</snmpv3_securitylevel>
     <snmpv3_authprotocol>0</snmpv3_authprotocol>
     <snmpv3_authpassphrase/>
     <snmpv3_privprotocol>0</snmpv3_privprotocol>
     <snmpv3_privpassphrase/>
     <formula>8</formula>
     <delay_flex/>
     <params/>
     <ipmi_sensor/>
     <data_type>0</data_type>
     <authtype>0</authtype>
     <username/>
     <password/>
     <publickey/>
     <privatekey/>
     <port/>
     <description/>
     <inventory_link>0</inventory_link>
     <applications/>
     <valuemap/>
     <logtimefmt/>
     <interface_ref>if1</interface_ref>
 </item>
 <item>
     <name>Status %(interface_name)s</name>
     <type>4</type>
     <snmp_community>%(comm)s</snmp_community>
     <multiplier>0</multiplier>
     <snmp_oid>1.3.6.1.2.1.2.2.1.8.%(interface_oid)s</snmp_oid>
     <key>Status%(interface_key)s</key>
     <delay>90</delay>
     <history>7</history>
     <trends>365</trends>
     <status>0</status>
     <value_type>0</value_type>
     <allowed_hosts/>
     <units/>
     <delta>0</delta>
     <snmpv3_contextname/>
     <snmpv3_securityname/>
     <snmpv3_securitylevel>0</snmpv3_securitylevel>
     <snmpv3_authprotocol>0</snmpv3_authprotocol>
     <snmpv3_authpassphrase/>
     <snmpv3_privprotocol>0</snmpv3_privprotocol>
     <snmpv3_privpassphrase/>
     <formula>1</formula>
     <delay_flex/>
     <params/>
     <ipmi_sensor/>
     <data_type>0</data_type>
     <authtype>0</authtype>
     <username/>
     <password/>
     <publickey/>
     <privatekey/>
     <port/>
     <description/>
     <inventory_link>0</inventory_link>
     <applications/>
     <valuemap>
         <name>SNMP interface status (ifOperStatus)</name>
     </valuemap>
     <logtimefmt/>
     <interface_ref>if1</interface_ref>
 </item>'''

items_triggers = '''
                </items>
            <discovery_rules/>
            <macros/>
            <inventory/>
        </host>
    </hosts>
        <triggers>
        '''

triggers_fa = '''
         <trigger>
            <expression>({TRIGGER.VALUE}=0 and {%(hostname)s:Status%(interface_key)s.change(0)}&gt;0)|\
({TRIGGER.VALUE}=1 and {%(hostname)s:Status%(interface_key)s.last(0)}&gt;1)</expression>
            <name>Problem with %(interface_name)s</name>
            <url/>
            <status>0</status>
            <priority>3</priority>
            <description/>
            <type>0</type>
            <dependencies/>
        </trigger>

        <trigger>
            <expression>(({TRIGGER.VALUE}=0 and {%(hostname)s:TrafficIn%(interface_key)s.avg(5m)}&gt;0 and \
{%(hostname)s:TrafficIn%(interface_key)s.last()}=0)|({TRIGGER.VALUE}=1 and \
{%(hostname)s:TrafficIn%(interface_key)s.last()}=0))|(({TRIGGER.VALUE}=0 and \
{%(hostname)s:TrafficOut%(interface_key)s.avg(5m)}&gt;0 and \
{%(hostname)s:TrafficOut%(interface_key)s.last()}=0)|({TRIGGER.VALUE}=1 and \
{%(hostname)s:TrafficOut%(interface_key)s.last()}=0))</expression>
            <name>Too little traffic %(interface_name)s</name>
            <url/>
            <status>0</status>
            <priority>2</priority>
            <description/>
            <type>0</type>
            <dependencies/>
        </trigger>

        <trigger>
            <expression>(({TRIGGER.VALUE}=0 and {%(hostname)s:TrafficOut%(interface_key)s.last()}&gt;91268055) or \
({TRIGGER.VALUE}=1 and {%(hostname)s:TrafficOut%(interface_key)s.last()}&gt;90000000)) or (({TRIGGER.VALUE}=0 and \
{%(hostname)s:TrafficIn%(interface_key)s.last()}&gt;91268055) or ({TRIGGER.VALUE}=1 and \
{%(hostname)s:TrafficIn%(interface_key)s.last()}&gt;90000000))</expression>
            <name>Too much traffic %(interface_name)s</name>
            <url/>
            <status>0</status>
            <priority>2</priority>
            <description/>
            <type>0</type>
            <dependencies/>
        </trigger> '''
triggers_gi = '''
         <trigger>
            <expression>({TRIGGER.VALUE}=0 and {%(hostname)s:Status%(interface_key)s.change(0)}&gt;0)|\
({TRIGGER.VALUE}=1 and {%(hostname)s:Status%(interface_key)s.last(0)}&gt;1)</expression>
            <name>Problem with %(interface_name)s</name>
            <url/>
            <status>0</status>
            <priority>3</priority>
            <description/>
            <type>0</type>
            <dependencies/>
        </trigger>

        <trigger>
            <expression>(({TRIGGER.VALUE}=0 and {%(hostname)s:TrafficIn%(interface_key)s.avg(5m)}&gt;0 and \
{%(hostname)s:TrafficIn%(interface_key)s.last()}=0)|({TRIGGER.VALUE}=1 and \
{%(hostname)s:TrafficIn%(interface_key)s.last()}=0))|(({TRIGGER.VALUE}=0 and \
{%(hostname)s:TrafficOut%(interface_key)s.avg(5m)}&gt;0 and \
{%(hostname)s:TrafficOut%(interface_key)s.last()}=0)|({TRIGGER.VALUE}=1 and \
{%(hostname)s:TrafficOut%(interface_key)s.last()}=0))</expression>
            <name>Too little traffic %(interface_name)s</name>
            <url/>
            <status>0</status>
            <priority>2</priority>
            <description/>
            <type>0</type>
            <dependencies/>
        </trigger>

        <trigger>
            <expression>(({TRIGGER.VALUE}=0 and {%(hostname)s:TrafficOut%(interface_key)s.last()}&gt;912680550) or \
({TRIGGER.VALUE}=1 and {%(hostname)s:TrafficOut%(interface_key)s.last()}&gt;900000000)) or (({TRIGGER.VALUE}=0 and \
{%(hostname)s:TrafficIn%(interface_key)s.last()}&gt;912680550) or ({TRIGGER.VALUE}=1 and \
{%(hostname)s:TrafficIn%(interface_key)s.last()}&gt;900000000))</expression>
            <name>Too much traffic %(interface_name)s</name>
            <url/>
            <status>0</status>
            <priority>2</priority>
            <description/>
            <type>0</type>
            <dependencies/>
        </trigger> '''

triggers_graphs = '''
    </triggers>
    <graphs>
    '''

graph = '''
    <graph>
            <name>Traffic %(interface_name)s</name>
            <width>900</width>
            <height>200</height>
            <yaxismin>0.0000</yaxismin>
            <yaxismax>100.0000</yaxismax>
            <show_work_period>1</show_work_period>
            <show_triggers>1</show_triggers>
            <type>0</type>
            <show_legend>1</show_legend>
            <show_3d>0</show_3d>
            <percent_left>0.0000</percent_left>
            <percent_right>0.0000</percent_right>
            <ymin_type_1>1</ymin_type_1>
            <ymax_type_1>0</ymax_type_1>
            <ymin_item_1>0</ymin_item_1>
            <ymax_item_1>0</ymax_item_1>
            <graph_items>
                <graph_item>
                    <sortorder>0</sortorder>
                    <drawtype>1</drawtype>
                    <color>000099</color>
                    <yaxisside>0</yaxisside>
                    <calc_fnc>2</calc_fnc>
                    <type>0</type>
                    <item>
                        <host>%(hostname)s</host>
                        <key>TrafficIn%(interface_key)s</key>
                    </item>
                </graph_item>
                <graph_item>
                    <sortorder>1</sortorder>
                    <drawtype>1</drawtype>
                    <color>990000</color>
                    <yaxisside>0</yaxisside>
                    <calc_fnc>2</calc_fnc>
                    <type>0</type>
                    <item>
                        <host>%(hostname)s</host>
                        <key>TrafficOut%(interface_key)s</key>
                    </item>
                </graph_item>
            </graph_items>
        </graph>
        '''
end_of_xml = '''
    </graphs>
</zabbix_export>
'''