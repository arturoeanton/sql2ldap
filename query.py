import argparse
import ldap
from in2pos import makeQuery

parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('-u','--url', default="ldap://127.0.0.1", help='url example ldap://127.0.0.1')
parser.add_argument('-b','--bind', default="cn=admin,dc=planetexpress,dc=com", help='example cn=admin,dc=planetexpress,dc=com')
parser.add_argument('-p','--password',default="GoodNewsEveryone",  help='example GoodNewsEveryone')
parser.add_argument('-ba','--base',  default="dc=planetexpress,dc=com",help='example dc=planetexpress,dc=com')
parser.add_argument('-q','--query', default="select  title,mail    from person ",  help='example "[n]select * from person where mail=a* or mail=h* or mail=b*"')
parser.add_argument('-v','--verbose', default=False,  help='example False')
parser.add_argument('-po','--politic', default='d',  help='example d|r|n|o')

# select  jpegPhoto from person
# employeeType,description, title, objectClass, userPassword, sn, mail, ou , givenName cn, displayName, uid

args = parser.parse_args()

########## initialize connection ###############################################
con = ldap.initialize(args.url)
con.simple_bind_s(args.bind, args.password)
########## performing a simple ldap query ######################################

query = makeQuery (args.query)
if (args.verbose):
    print args.query
    print query

attr = map(str.strip,args.query.split("select")[-1].split("from")[0].split(","))


politic = args.politic

result = con.search_s(args.base, ldap.SCOPE_SUBTREE, query)
for r in result:
    row =r[1]
    if politic == 'r':
        print row
        continue
    if politic == 'o':
        for a in attr:
            if row.has_key(a):
                print a,":",row[a]
            else:
                print a,": NULL"
        continue

    for field in row:
        if politic == 'd':
            if (field in attr) or attr[0]=="*":
                print field, ":", row[field]
        elif politic == 'n':
            if not (field in attr):
                print field, ":", row[field]
    print "-"
