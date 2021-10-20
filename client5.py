import socket, getpass, threading # импортируем необходимые модули.Модуль threading использовался как главный способ достижения параллельности.
from time import sleep

def sendmsg(sock, data):
    # функция отвечает за красивое отображение длины сообщения ( в сообщении 7 символов - перед значащей цифрой стоят незначащие нули)
    length = "0"*(7-len(str(len(data)))) + str(len(data))
    data = bytearray((f'{length}{data}').encode())
    sock.send(data)

def recvmsg(sock, zn):
    data = sock.recv(zn).decode()
    print("Длина сообщения:", data[:7])
    return data[7:]
# вывод длины сообщения
socket.socket.sendmsg = sendmsg
socket.socket.recvmsg = recvmsg

def reciv():
    while True:
        # считывем данные небольшими порциями 
        data = sock.recvmsg(1024)
        with LOCK:
            print("Осуществляем прием данных от сервера")
            print(data)

LOCK = threading.Lock()
sock = socket.socket()
#Это нужно для того, чтобы сокет не блокировался
sock.setblocking(1)
port = getpass.getpass(prompt = 'Введите порт: ')
host = getpass.getpass(prompt = 'Введите хост: ')
if not port:
    # Порт по умолчанию
    port = 8083
else:
    port = int(port)
if not host:
    host = 'localhost'

# host, port = 'localhost', 8083 - по умолчанию
print("Выполняется Соединение с сервером")
sock.connect((host, port))
print("Соединение с сервером установлено")

#Thread.daemon сообщает, является ли поток демоническим
threading.Thread(target = reciv, daemon = True).start()
while True:
    msg = input()
    #  по умолчанию msg = "Hello!"
    print("Осуществляется отправка данных серверу")
    sock.sendmsg(msg)
    if msg == "выход":
        break
        

print("Разрыв соединения с сервером")

sock.close() 