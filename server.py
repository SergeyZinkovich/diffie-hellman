import socket
import random
from Crypto import Random
from Crypto.Cipher import AES

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
conn, addr = sock.accept()



p = random.getrandbits(256)
g = random.getrandbits(256)
sessionkey = Random.new().read(32) # 256 bit
conn.send(str(p).encode())
conn.send(str(g).encode())
a = random.getrandbits(256)
A = pow(g, a, p)
conn.send(str(A).encode())
B = int(conn.recv(1024).decode())
K = pow(B, a, p)

input = open("text.txt")

iv = Random.new().read(16)  # 128 bit
kek = K.to_bytes((K.bit_length() + 7) // 8, 'big')
obj = AES.new(kek, AES.MODE_CFB, iv)
ciphertext = iv + obj.encrypt(input.read())

conn.send(ciphertext)

conn.close()

