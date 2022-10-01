from myutil import *

# Reset and prepare.
## Reset Multichain and prepare.
def prepare():
    ## Create 3 new addresses.
    [api.getnewaddress() for _ in range(3)]
    global addrs
    addrs = api.getaddresses()
    ## Create setaddr.bat to set Windows Environment variables:
    with open('setaddr.bat', 'w') as f:
        for i in range(4):
            f.write('set addr{}={}\n'.format(i, addrs[i]))

    ## Grant 'receive,send' permissions to the addresses.
    a = '{},{},{}'.format(addrs[1], addrs[2], addrs[3])
    api.grant(a, 'receive,send')
    print('Prepare Ok.')
# prepare()
addrs = api.getaddresses()
# print(addrs)
#---------------------------------------------------------

''' List Streams:
        multichain-cli chain1 liststreams
Try:    mc liststreams
The 'root' stream is created when the first node is started. '''
def list_streams():
    for s in api.liststreams():
        print(s['name'])
# list_streams()

''' Create Stream:
   multichain-cli chain1 create stream <name> <open>=true
   multichain-cli chain1 createfrom <from_addr> stream <name> <open>=true
The creater is the 'root' or 'admin' which has 'create' permission.
An <open> stream allows anyone with 'send' permission to publish to the stream.
Return the 'txid' that creates the stream if success.
Try:
      mc create stream s1 true            '''
# print(api.create('stream', 's2', True))

''' Grant stream permission to address to allow a 'non-root'
  to be a creater.
Try:
   mc grant %addr1% create
   mc createfrom %addr1% stream s3 false

Stream info:
  multichain-cli chain1 getstreaminfo <stream_name>
'''
def get_stream_info(name):
    s = api.getstreaminfo(name)
    # print(s)
    print('name: ', s['name'])
    print('restrict: ', s['restrict'])
# get_stream_info('s1')     ## 'open' streams have 'write' is False.
# get_stream_info('s3')


''' 'write' Permission:
'root' has all permissions, but 'write' permission is not listed.
'''
def list_perms():
    for j in api.listpermissions():
        print(j['address'] , j['type'])
# list_perms()

''' List addresses that have some permissions to a stream:
      multichain-cli chain1 listpermissions <stream_name>.*
Try:
          mc listpermissions s1.*
The 'root' has 'write' permission to all streams.
A stream permission is for a particular stream and belong to an address.
'''
def list_permissions(sname):
    for j in api.listpermissions(sname+'.*'):
        print(j.get('address'), ': ', j.get('type'))
# list_permissions('s1')

''' Close Stream:
Open stream: 'write' is false.
Close stream: 'write' is true.
Alternatively, a close stream can be created with restrict: write.
Try:
   mc create stream s4 "{\"restrict\":\"write\"}"
'''
# get_stream_info('s1')     ## 'write' is false
# get_stream_info('s3')     ## 'write' is True
# get_stream_info('s4')     ## 'write' is True

#-----------------------------------------------------------

## Create hex strings.
hello_hex = str_hex('hello');   ## print(hello_hex)  ## 68656c6c6f
hi_hex = str_hex('hi');         ## print(hi_hex)     ## 6869
whatup_hex = str_hex('whatup'); ## print(whatup_hex) ## 776861747570

''' Publish hex string:
A stream item may contain <key>/<value>, where <value> is a hex string.
  multichain-cli chain1 publish <stream_name> <key> <value>
  multichain-cli chain1 publishfrom <from_addr> <stream_name> <key> <value>
For open streams the publisher must have 'send' permission.
<key> must be string, <value> may be hex-string or json.
Return the 'txid' that publishs to the stream if success.
Try:
           mc publish s1 k1 68656c6c6f
           mc publishfrom %addr1% s1 k2 6869
More than one items may have the same key.
'''
def pub_hex(sname, key, value):
    print(api.publish(sname, key, value))
# pub_hex('s2', 'key1', hello_hex)
# pub_hex('s2', 'key1', hi_hex)

''' Publishing to a closed stream requires 'send' and 'write' permissions.
Try:
     mc publishfrom %addr1% s3 key1 68656c6c6f      ## falis.
Grant 'add1' the 'write' permission to 's3' stream.
     mc grant %add1% s3.write
Try again:
     mc publishfrom %addr1% s4 key1 68656c6c6f
'''
#-----------------------------------------------------------------

''' Subscribe to a stream:
To start tracking a stream, the node must subscribe to the stream.
     multichain-cli chain1 subscribe <stream_name>
Try:
     mc subscribe s1
Nothings returned if success.

List Items of a stream:
  multichain-cli chain1 liststreamitems <stream_name>
Try:    mc liststreamitems s1
'''
def list_stream_items(sname):
    for js in api.liststreamitems(sname):
        print(js['keys'], hex_str(js['data']))
# list_stream_items('s1')

''' List Items by Stream and Key:
 multichain-cli chain1 liststreamkeyitems <stream_name> <key>
'''
def list_stream_key_items(sname, key):
    for r in api.liststreamkeyitems(sname, key):
        print(hex_str(r['data']))
# list_stream_key_items('s1', 'k1')

''' Stream items may have duplicated key.
Try:
     mc publish s1 k1 776861747570   ## whatup
'''
# list_stream_key_items('s1', 'k1')

## If there is no duplicate keys, the result can be found at the first item.
def non_duplicate_key(key):
    r = api.liststreamkeyitems('s1', key)
    print(hex_str(r[0].get('data')))
# non_duplicate_key('k1')
# non_duplicate_key('k2')
#--------------------------------------------------------------
''' Publish Text:
The published value may be a json of the from:  {'text': <txt>}
'''
# print(api.publish('s1', 'kt', {'text': 'How do you do?'}))
def read_txt(key):
    for j in api.liststreamkeyitems('s1', key):
        d = j['data']
        if type(d) is dict:     ## json
            print(d['text'])
# read_txt('kt')
#------------------------------------------------------------
''' Publish Json:
The published value may be a json of the from:
              {'json': <json>}
Try:
 mc publish s1 kj "{\"json\":{\"id\":\"1\", \"gpa\":\"3.8\", \"name\":\"John\"}}"
'''
def pub_student(key, id, name, gpa):
    json = {'json': {'id': id, 'name': name, 'gpa': gpa}}
    print(api.publish('s1', key, json))
# pub_student('cs', 1, 'John', 2.1)
# pub_student('cs', 2, 'Jack', 3.8)
# pub_student('ee', 3, 'Joe', 4.0)

## Read json:
def read_student(key):
    for j in api.liststreamkeyitems('s1', key):
        student =j['data']['json']
        print(student['id'], student['name'], student['gpa'])
# read_student('cs')
# read_student('ee')

## Find gpa by key and name:
def get_gpa(key, name):
    for js in api.liststreamkeyitems('s1', key):
        s = js['data']['json']
        if s['name'] == name:
            print(s['gpa'])
# get_gpa('cs', 'Jack')
##------------------------------------------------------------------------

def add_more_students():
    pub_student('it', 4, 'Jame', 1.2)
    pub_student('cs', 5, 'Jim', 3.1)
    pub_student('ce', 6, 'Jody', 2.1)
# add_more_students()
# read_student('cs')

''' List Command Options:
  multichain-cli chain1 liststreamkeyitems <sname> <key> <verbose>=False, <count>=10, <start>=0
<verbose> if True contains info about tx.
<count> number of items to be listed (from the first).
<start> (from 0 based position), if negative start from the end.
Try:
     mc liststreamkeyitems s1 cs
     mc liststreamkeyitems s1 cs true
'''
def list_keyitems(key, count=10, start=0):
    for j in api.liststreamkeyitems('s1', key, False, count, start):
        print(j['keys'], j['data'])
# list_keyitems('cs')
# list_keyitems('ce')
# list_keyitems('cs', 3)
# list_keyitems('cs', 3, 1)
# list_keyitems('cs', 2, 2)
# list_keyitems('cs', 1, 1)      ## one from the first
# list_keyitems('cs', 1, -1)     ## the last

''' Keys List:
    multichain-cli chain1 liststreamqueryitems <sname> <json>
List all items by a keys list that specified by a <json>.
<json> defines keys list in the form: ["key1", "key2", ...]
Try:
    mc liststreamqueryitems s1 "{\"keys\":[\"cs\"]}"
'''
def list_queryitems(keys):
    for j in api.liststreamqueryitems('s1', keys):
        print(j['keys'], j['data'])
# list_queryitems({'keys': ['cs']})
# list_queryitems({'keys': ['it']})
# list_queryitems({'keys': ['cs', 'it']}) ## no items with the list of keys

## Add more examples with key list:
def pub_items_with_keylist():
    print(api.publish('s1', 'cs', {'json': {'dep': 'Computer Science'}}))
    print(api.publish('s1', ['cs','oo'], {'json':{'dep':'Computer Science','title':'OO Programming'}}))
    print(api.publish('s1', ['cs','oo'], {'json':{'dep':'Computer Science','title':'OO Design and Analysis'}}))
    print(api.publish('s1', ['cs','dm'], {'json':{'dep':'Computer Science','title':'Discrete Math'}}))
    print(api.publish('s1', 'ee', {'text': 'Electrical Engineer'}))
    print(api.publish('s1', ['ee','dm'], {'json':{'dep':'Electrical Engineer','title':'Discrete Math'}}))
# pub_items_with_keylist()

##  Query by Keys List:
def query_keys():
    for js in api.liststreamkeyitems('s1', 'cs'):
    # for js in api.liststreamqueryitems('s1', {'keys':['cs']}):
    # for js in api.liststreamqueryitems('s1', {'keys':['oo']}):
    # for js in api.liststreamqueryitems('s1', {'keys':['dm', 'cs']}):
    # for js in api.liststreamqueryitems('s1', {'keys':['ee']}):
    # for js in api.liststreamqueryitems('s1', {'keys':['dm']}):
    # for js in api.liststreamqueryitems('s1', {'keys':['ee','cs']}):  ## not intersect
        print(js['keys'], js['data'])
# query_keys()

#################################################################
