# from PyQt5 import Qt
# import sys
# import socket

# IPPORT = ("",5002)

# Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Socket.bind(IPPORT)

# def DisplayNot(text):
# 	#print(text)
# 	data = text.split(" ")
# 	if len(data)>6 :
# 		return data[6][:-1]
# 	return 0
# otp=0
# while True:
# 	data = Socket.recv(1024)
# 	otp=DisplayNot(data.decode("utf-8"))
# 	if otp!=0:
# 		break
# 	pass

# print(otp)


from PyQt5 import Qt
import sys
import socket

IPPORT = ("",5002)

Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Socket.bind(IPPORT)

def DisplayNot(text):
	#print(text)
	data = text.split(" ")
	if len(data)>6 :
		return data[6][:-1]
	# if data:
	# 	return data

	return 0

otp=0

while True:
	data = Socket.recv(1024)
	otp=DisplayNot(data.decode("utf-8"))
	if otp!=0:
		break
	pass

print(otp)


