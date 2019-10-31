import socket
import random
from Crypto.Cipher import AES

sock = socket.socket()
sock.connect(('localhost', 9090))
p = int(sock.recv(256).decode())
g = int(sock.recv(256).decode())

b = random.getrandbits(256)
B = pow(g, b, p)
sock.send(str(B).encode())
A = int(sock.recv(1024).decode())
K = pow(A, b, p)

ciphertext = bytes()
while True:
    data = sock.recv(1024)
    if not data:
        break
    ciphertext += data

ciphertext = bytes(ciphertext)
iv = ciphertext[:16]
kek = K.to_bytes((K.bit_length() + 7) // 8, 'big')
obj = AES.new(kek, AES.MODE_CFB, iv)
plaintext = obj.decrypt(ciphertext[16:])

output = open("decoded.txt", "wb")
output.write(plaintext)

sock.close()














