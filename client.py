import socket
import json

comSocket = socket.socket()

svrIP = ""
comSocket.connect((svrIP,2500))
print('Connected to '+svrIP)

while True:
   sendData = '라즈베리파이 데이터'
   comSocket.send(sendData.encode()) #bytes형으로 변환하여 전송

   #bytes형으로 수신된 데이터를 문자열로 변환 출력
   print('Received message: {0}'.format(json.loads(comSocket.recv(1024).decode())))