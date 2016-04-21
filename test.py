import requests
from pprint import pprint
import json

ZABIX_ROOT = '**********'
url = ZABIX_ROOT + '/api_jsonrpc.php'

########################################
# user.login
########################################
payload = {
    "jsonrpc" : "2.0",
    "method" : "user.login",
    "params": {
      'user': '*******',
      'password': '******',
    },
    "auth" : None,
    "id" : 0,
}
headers = {
    'content-type': 'application/json',
}
res  = requests.post(url, data=json.dumps(payload), headers=headers)
res = res.json()
print ('user.login response')
pprint(res)

########################################
# host.get
########################################
payload = {
    "jsonrpc": "2.0",
    "method": "item.get",
    "params": {
        "output": "extend",
        "hostids": "10105",
        "search": {
            "key_": "StatusBE1"
        },
        "sortfield": "name"
    },
    "auth" : res['result'],
    "id" : 2,
}
res2 = requests.post(url, data=json.dumps(payload), headers=headers)
res2 = res2.json()
print ('host.get response')
pprint(res2['result'])
print(type(res2['result'][0]))
for i, v in res2['result'][0].items():
    if 'snmp' in i:
        print(i, v)
