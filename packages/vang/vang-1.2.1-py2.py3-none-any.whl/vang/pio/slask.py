import hashlib
from json import dumps

data = {
    'foo': 'bar'
}


hash_object = hashlib.md5(dumps(data).encode('utf-8'))
print(hash_object.hexdigest())

