from os import environ
from pprint import pprint


def foo():
    print('foo')


def bar(x):
    if callable(x):
        x()
    else:
        print('Not callable')


bar(foo)

s = []
print(type(s))

if type(s) is str:
    print('string')
else:
    print('not string')

d = {'username': 'a', 'password': 'b', 'url': 'u'}
e = dict(d, url='new')

pprint(d)
pprint(e)

print(environ['JENKINS_USERNAME'])
