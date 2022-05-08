from itertools import count
from pwn import *
import time

HOST = '127.0.0.1'
PORT = 9090

s = connect(HOST, PORT)
for i in range(7):
    print(s.recvline().decode()[:-1])

Dollar_score = 0
BTC_score = 0
BTC_rate = 0

for j in count():
    Dollar_score = int(s.recvline().decode()[14:-1])
    BTC_score = int(s.recvline().decode()[11:-1])
    BTC_rate = int(s.recvline().decode()[10:-1])
    print(f'{j}: {Dollar_score}     {BTC_score}     {BTC_rate}')

    if BTC_score >= 100:
        s.sendline('3'.encode())
        flag = s.recvline().decode()[:-1]
        break
    if Dollar_score < BTC_rate:
        s.sendline('1'.encode())
        print(s.recvline().decode()[:-1])
    elif Dollar_score >= BTC_rate:
        s.sendline('2'.encode())
        print(s.recvline().decode()[:-1])


    # time.sleep(0.08)
print(flag)
