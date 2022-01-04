from bluetooth import *

socket = BluetoothSocket(RFCOMM)
socket.connect(("98:DA:40:00:E8:89", 1))
print("bluetooth connected!")

while True:
    data = socket.recv(1024)
    print(data)
    if (data == "q"):
        print("Quit")
        break

socket.close()