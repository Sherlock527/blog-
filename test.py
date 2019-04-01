import jwt
import datetime
import threading


event = threading.Event()
key = 'magedu'

# 在jwt的payload中增加exp claim
data = jwt.encode({'name':'tom', 'age':20, 'exp':int(datetime.datetime.now().timestamp())+10}, key)
print(jwt.get_unverified_header(data))  # {'typ': 'JWT', 'alg': 'HS256'}
try:
    while not event.wait(1):  # 过期校验就会抛出异常，10s后直接打印e
        print(jwt.decode(data, key))  # {'name': 'tom', 'age': 20, 'exp': 1552664023}
        print(datetime.datetime.now().timestamp())  # 1552664014.58518
except jwt.ExpiredSignatureError as e:
    print(e)  # Signature has expired