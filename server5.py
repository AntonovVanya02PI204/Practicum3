import socket, getpass, sys, random, csv
'''
Модуль random используем для генерации случайных чисел. Модуль socket включает в себя функции создания объекта сокета Socket, который и обрабатывает канал данных, а также функции,
связанных с сетевыми задачами, такими как преобразование имени сервера в IP адрес и форматирование данных для отправки по сети.
Модуль sys обеспечивает доступ к некоторым переменным и функциям, взаимодействующим с интерпретатором python.
Функция getpass() модуля getpass печатает подсказку и запрашивает у пользователя 
пароль без повторения. Входные данные возвращаются в качестве строки для вызывающей стороны.
Модуль csv понадобится в дальнейшем для записи необходимых данный в csv файл
'''
def sendmsg(sock, data):
    # функция отвечает за красивое отображение длины сообщения ( в сообщении 7 символов - перед значащей цифрой стоят незначащие нули)
    length = "0"*(7-len(str(len(data)))) + str(len(data))
    data = bytearray((f'{length}{data}').encode())
    sock.send(data)

def recvmsg(sock, zn):
    # Выводим длину сообщения
    data = sock.recv(zn).decode()
    print("Длина сообщения:", data[:7])
    return data[7:]

socket.socket.sendmsg = sendmsg
socket.socket.recvmsg = recvmsg

main_stdout = sys.stdout
# Открываем файл msg.txt на запись необходимых данных
sys.stdout = open('msg.txt', 'w')
print("Осуществляется запуск сервера")
sock = socket.socket()
port=getpass.getpass(prompt = 'Введите имя порта: ')
if not port:
        port = 8083
else:
    port = int(port)
# по умолчанию имя порта 8083  (port = 8083)

while True:
    '''
    Теперь свяжем наш сокет с данными хостом и портом с помощью метода bind,
    которому передается кортеж, первый элемент (или нулевой, если считать от нуля) которого — хост, а второй — порт:
        '''
    try:
        sock.bind(('', port))
        print(f"Порт {port}")
        break
    # Иначе вызываем ошибку - данный порт нам недоступен
    except OSError as oserr:
        print(f"порт {port} недоступен")
        # генерация(random) - имени порта
        port = random.randint(1024,65535)
'''
Теперь у нас все готово, чтобы принимать соединения. С помощью метода listen мы запустим для данного сокета режим прослушивания. 
Метод принимает один аргумент — максимальное количество подключений в очереди.
'''

sock.listen(0)
print("Начало прослушивания порта")

def listening():
        while True: 
                print("Осуществляется прием данных от клиента")
                '''
                Чтобы получить данные нужно воспользоваться методом recv, который в качестве аргумента принимает количество байт для чтения. 
                Мы будем читать порциями по 1024 байт (или 1 кб):
                    '''
                data = conn.recvmsg(1024)
                if not data:
                        print(f"Выполняется отключение клиента {addr}")
                        return False

                msg = data
                if msg == "выход":
                        print(f"Клиент попросил отключения {addr}")
                        return True
                print(msg)
                print("Введите сообщение для отправления необходимых данных клиенту")
                data = input()
                conn.sendmsg(data)
                
sys.stdout.close()
sys.stdout = main_stdout 

const = False
while not const:
        conn, addr = sock.accept()
        print(f"Выполняется подключение клиента {addr}")
        #создаем файл для записи данных 
        total = "total.csv"
        #a+ - Открывает файл для добавления и чтения
        with open(total, 'a+', newline = '') as login:
                login.seek(0,0)
                reader = csv.reader(login, delimiter = ';')
                for row in reader:
                        if row[0] == addr[0]:
                            #Записываем в разные ячейки адрес, имя и пароль
                                password = row[2]
                                name = row[1]
                                break
                else:
                        conn.sendmsg("Введите Ваше имя")
                        name = conn.recvmsg(1024)
                        conn.sendmsg("Введите пароль")
                        password = conn.recvmsg(1024)
                        writer = csv.writer(login, delimiter = ';')
                        writer.writerow([addr[0], name, password])

        while True:
                conn.sendmsg("Введите пароль для начала диалога")
                password1 = conn.recvmsg(1024)
                if password1 == password:
                        conn.sendmsg((f"Начинаем наше общение, {name}"))
                        break
                else:
                        conn.sendmsg("Введен неверный пароль")
        try:
                const = listening()
        except (ConnectionAbortedError, ConnectionResetError) as error:
                print(error)
        conn.close() 

print("Произведена остановка сервера")