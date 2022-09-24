from myutil import *

## Prepare:
## Reset Multichain.
## Create 3 new addresses.
# [api.getnewaddress() for _ in range(3)]

addrs = api.getaddresses()
# print(addrs)
## Create setaddr.bat to set Windows Environment variables:
def set_addr():
    with open('setaddr.bat', 'w') as f:
        for i in range(4):
            f.write('set addr{}={}\n'.format(i, addrs[i]))
# set_addr()

## Grant 'receive,send' permissions to the addresses.
def grant_perm():
    a = '{},{},{}'.format(addrs[1], addrs[2], addrs[3])
    api.grant(a, 'receive,send')
# grant_perm()
#---------------------------------------------------------

# List assets:  (all issued assets)
#      multichain-cli chain1 listassets
## Try:     mc listassets
def list_assets():
    for j in api.listassets():
        print(j['name'] , j['issueqty'])
# list_assets()         ## Initially there is no assets.

''' Issue: asset to address
     multichain-cli chain1 issue <addr> <asset> <amount> <subdivide>
The issuer must be the 'root' or has 'admin' permission.
<addr> is address of the receiver that has 'receive' permission.
Return the 'txid' that issues the asset if success.
By default the asset is 'closed', that means cannot be issued more.
Issuing a closed asset more than once would fail.
Try:       mc issue %addr1% as1 100 1
    'add0' issues 100 'as1' asset to 'add1' with subdivide 1.
'''
def issue(recv, asset, amount, subd=1):
    print(api.issue(recv, asset, amount, subd))
# issue(addrs[2], 'as2', 1000, 0.01)
# Try: list_assets() again.

## Get Asset Info of an asset:
#      multichain-cli chain1 getassetinfo <asset> <versbose>=false
# Try:
#      mc getassetinfo as1
#      mc getassetinfo as2 true
def get_asset_info(asset, versbose=False):
    r = api.getassetinfo(asset, versbose)
    print(r['name'], r['issueqty'])
# get_asset_info('as1')

## Get Address Balance of an address:
#      multichain-cli chain1 getaddressbalances <addr>
## Try:     mc getaddressbalances %addr1%
def get_addr_bal(addr):
    for x in api.getaddressbalances(addr):
        print(x['name'], x['qty'])
# get_addr_bal(addrs[2])

## Issue Form: allows issuing from an address that is
#   'non-root' nor 'admin' but have 'issue' permission.
#   multichain-cli chain1 issuefrom <from_addr> <to_addr> <asset> <amount> <subdivide>
# Try:
#       mc grant %addr1% issue
#       mc issuefrom %addr1% %addr2% as3 3000 1
# get_addr_bal(addrs[2])

## Initially 'root' and 'admin' has 'issue' premission but does not own any asset.
## It is possible that they issue assets to themself.
# get_addr_bal(addrs[0])         # empty
# issue(addrs[0], 'as0', 100)
# get_addr_bal(addrs[0])         # as0 100

## Get Total Balances of all addresses in the node:
#     multichain-cli chain1 gettotalbalances
## Try:    mc gettotalbalances
def get_total_balances():
    for j in api.gettotalbalances():
        print(j['name'], j['qty'])
# get_total_balances()

#-------------------------------------------------------

''' Send Asset:
     multichain-cli chain1 sendasset <receiver_addr> <asset> <amount>
<addr> is address of the receiver and must has 'receive' permission.
The sender is the 'root' or 'admin' and must have enough asset.
Return 'txid' that send the asset if success.
Try:    mc sendasset %addr1% as0 1
'''
def send_asset(recv, asset, amount):
    print(api.sendasset(recv, asset, amount))
# send_asset(addrs[2], 'as0', 2)

''' Multichain handles the balances for both sender and receiver.
The wallet take cares of sign and verify transactions.  '''
# get_addr_bal(addrs[0])
# get_addr_bal(addrs[1])
# get_addr_bal(addrs[2])

''' Send Asset Form: non 'root' or 'admin' addresses but have 'send' permission.
   multichain-cli chain1 sendassetfrom <from_addr> <to_addr> <asset> <amount>
Try:    mc sendassetfrom %addr1% %addr2% as0 1
'''
def send_asset_form(from_addr, to_addr, asset, amount):
    print(api.sendassetfrom(from_addr, to_addr, asset, amount))
# send_asset_form(addrs[2], addrs[1], 'as0', 3)
# get_addr_bal(addrs[1])
# get_addr_bal(addrs[2])

''' If the sender and receiver addresses are belong to the same node,
 the total balances of the node does not change.  '''
# get_total_balances()
#--------------------------------------------------------

''' Sending multiple assets in a tx.
The sent assets are represnted as json:
        {<asset1>:<amount1>, <asset2>:<amount2>, ...}
    multichain-cli chain1 send <receiver_addr> <json>
    multichain-cli chain1 sendfrom <from_addr> <to_addr> <json>
Try:
     mc sendfrom %addr1% %addr2% "{\"as0\":1, \"as1\":2}"     '''
# get_addr_bal(addrs[1])
def send_from(from_addr, to_addr, jsasset):
    print(api.sendfrom(from_addr, to_addr, jsasset))
# send_from(addrs[2], addrs[1], {"as0":1, "as1":2})
# get_addr_bal(addrs[1])
#----------------------------------------------------

## string <--> hex string:
# print(str_hex('Hello'))         ## 48656c6c6f
# print(hex_str('48656c6c6f'))    ## Hello
#----------------------------------------------------

''' Sending Asset with Metadata:
  multichain-cli chain1 sendwithdata <receiver_addr> <json_asset> <metadata>
  multichain-cli chain1 sendwithdatafrom <from_addr> <to_addr> <json_asset> <metadata>
If <metadata> is just a text it much be a hex-string:
Try:
  mc sendwithdata %addr2% "{\"as0\":1}" 48656c6c6f
'''
def send_with_data(recv, jsasset, mdata):
    print(api.sendwithdata(recv, jsasset, mdata))
# send_with_data(addrs[3], {'as0': 1}, str_hex('How do you do?'))

''' The metadata is stored in the tx of a receiver address.
List the last <n> transactions of an <addr>:
         multichain-cli chain1 listaddresstransactions <addr> <n>
Try:
          mc listaddresstransactions %addr1% 1
          mc listaddresstransactions %addr2% 2
'data' contains the metadata.
'''
def read_data(addr, n):
    for t in api.listaddresstransactions(addr, n):
        d = t['data'][0]
        if type(d) == str:
            print(hex_str(d))
        else:
            print(d)
# read_data(addrs[1], 1)
#---------------------------------------------------

''' Sending Text Metadata:
<metadata> may be a json in the form of:  {"text": "<str>"}
Try:
  mc sendwithdata %addr2% {\"as0\":1} "{\"text\": \"Hello\"}"
'''
# send_with_data(addrs[3], {'as0': 1}, {"text": "Hi how are you?"})
# read_data(addrs[3], 1)

''' <metadata> may be a json object:  {"json": {"id":"123", "name":"john"}}
Try:
  mc sendwithdata %addr2% "{\"as0\":1}" "{\"json\": {\"id\":\"123\", \"name\":\"john\"}}"
'''
# send_with_data(addrs[3], {'as0': 1}, {"json": {'id': 500, 'name': 'jack'}})
# read_data(addrs[3], 1)

#-----------------------------------------------------------------

''' Issuing 'open' asset:  (That can be reissued more.)
The asset is described as json, with 'open' is true.
  multichain-cli chain1 issue <recv> "{\"name\":<asset_name>, \"open\": true }" <amount> <subdivide>
  multichain-cli chain1 issueform <form_addr> <to_addr> "{\"name\":<asset_name>, \"open\": true }" <amount> <subdivide>
Try: Issue 'ax' asset to addr1 as an opened asset:
  mc issue %addr1% "{\"name\":\"ax\", \"open\":true}" 100 1

Issuing More:
     multichain-cli chain1 issuemore <recv> <asset> <amount>
     multichain-cli chain1 issuemoreform <form_addr> <to_addr> <asset> <amount>
Try:
         mc issuemore %addr1% ax 200
Check:
         mc getaddressbalances %addr1%
'''
