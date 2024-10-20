import sys

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from twisted.application import service
from twisted.internet.endpoints import serverFromString
from twisted.internet.protocol import ServerFactory
from twisted.python.components import registerAdapter
from twisted.python import log
from ldaptor.inmemory import fromLDIFFile
from ldaptor.interfaces import IConnectedLDAPEntry
from ldaptor.protocols.ldap.ldapserver import LDAPServer

LDIF = b'''\
dn: dc=org
dc: org
ObjectClass: dcObject

dn: dc=example,dc=org
dc: example
ObjectClass: dcObject
ObjectClass: organization

dn: ou=people, dc=example,dc=org
ObjectClass: organizationUnit
ou: people

dn: cn=bob,ou=people, dc=example,dc=org
cn: bob
gn: Bob
mail: bob@example.org
ObjectClass: person
ObjectClass: inetOrgPerson
telephoneNumber: 555-9999
uid: bob
sn: Roberts
userPassword: asecret

dn: cn=John,ou=people, dc=example,dc=org
ObjectClass: addressbookPerson
cn: john
sn: Doe
street: Back alley
postOfficeBox: 123
postalCode: 54321
postalAddress: Backstreet
st: NY
I: New York City
c: US
userPassword: terces

'''

'''
The main class of the LDAPServer.py is defined here.
'''

class Tree(object):

    def __init__(self):
        global LDIF
        self.f = BytesIO(LDIF)
        d= fromLDIFFile(self.f)
        d.addCallback(self.ldifRead)

    def ldifRead(self, result):
        self.f.close()
        self.db = result

class LDAPServerFactory(ServerFactory):

    protocol = LDAPServer

    def __init__(self, root):
      self.root = root

    def buildProtocol(self, addr):
        proto = self.protocol()
        proto.debug = self.debug
        proto.factory = self
        return proto

'''
Here the main function is defined.

The LDAP server will listen for incoming connections on port
8080 of the localhost or a command-line specified port.
'''

if __name__ == "__main__":
    from twisted.internet import reactor
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    else:
        port = 8080
    log.startLogging(sys.stderr)
    tree= Tree()
    registerAdapter(
        lambda x: x.root,
        LDAPServerFactory,
        IConnectedLDAPEntry
    )
    factory = LDAPServerFactory(tree.db)
    factory.debug = True
    application = service.Application("ldapptor-server")
    myService = service.IServiceCollection(application)
    serverEndpointStr = "tcp:{0}".format(port)
    e = serverFromString(reactor, serverEndpointStr)
    d = e.listen(factory)
    reactor.run()
