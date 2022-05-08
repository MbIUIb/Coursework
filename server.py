import socket
import random
import time

HOST = '127.0.0.1'
PORT = 9090

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
# print('сервер запущен...')

salary = 300 # $
flag_cost = 100 # BTC
overflow_dollar_score = 7200000
overflow_btc_score = 120
bot_time = 0.07
flag = 'zssoib{DunGe0N_Ma5T33Rs_The_B3sT}\n'
greeting = ['Welcome to the server!\n',
            'To get the flag, you have to pay 100 BTC. You have the opportunity to earn dollars and exchange them for BTC at a certain rate. Keep in mind that overflowing the balance will lead to a breakdown of the banking system and reset the account!\n',
            '\n',
            'Available commands:\n',
            f'1 -get {salary}$\n',
            '2 -exchange $ for BTC\n',
            f'3 -buy a flag for {flag_cost} BTC\n']

while True:
    # ожидание в очереди подключений 1 клиента, кроме текущего
    server.listen(5)
    client_socket, client_address = server.accept()
    # print('Новое подключение: ', client_address)

    # приветствие нового клиента и доступные команды
    for msg in greeting:
        client_socket.send(msg.encode())

    # счета клиента
    currencies ={'Dollar score': 0,
                 'BTC score': 0,
                 'BTC rate': 0}

    tic = 10
    while True:
        #  курс Btc
        currencies['BTC rate'] = random.randint(20000, 60000)

        # счета клиента
        for key, value in currencies.items():
            client_socket.send(f'{key}: {value}\n'.encode())


        # получение данных от клиента
        try:
            data = client_socket.recv(1024)
            execution_time = float(f'{time.perf_counter() - tic:0.4f}')
            tic = time.perf_counter()
        except socket.error:
            # print('client socket error')
            break
        else:
            # декодировка данных
            try:
                msg = data.decode()[:-1]
                # print(msg)
            except:
                # print('decode error')
                client_socket.send('decode error, try again'.encode())
                client_socket.close()
                break

            # отключение клиента, посылающего пустые сообщения
            if msg == '':
                client_socket.send('disabling'.encode())
                # print('Disabling')
                client_socket.close()
                break

            # обработка команд клиента
            if msg == '1':
                currencies['Dollar score'] += salary
                client_socket.send('You got paid!\n'.encode())
            elif msg == '2':
                if currencies['Dollar score'] < currencies['BTC rate']:
                    client_socket.send('Not enough funds to exchange!\n'.encode())
                else:
                    currencies['BTC score'] += (currencies['Dollar score'] // currencies['BTC rate'])
                    currencies['Dollar score'] = currencies['Dollar score'] % currencies['BTC rate']
                    client_socket.send('Successful exchange!\n'.encode())
            elif msg == '3':
                if currencies['BTC score'] >= flag_cost:
                    client_socket.send(flag.encode())
                    # print('task completed')
                    break
                else:
                    client_socket.send('insufficient funds, try again\n'.encode())
            else:
                client_socket.send('Command error\n'.encode())
                # print('Command error, disabling')
                client_socket.close()
                break


            # 'поломка' банковской системы при переполнении счетов
            if currencies['Dollar score'] > overflow_dollar_score:
                currencies['Dollar score'] = 0
                client_socket.send('The banking system was broken. Hacker stole your money\n'.encode())
            elif currencies['BTC score'] > overflow_btc_score:
                currencies['BTC score'] = 0
                client_socket.send('The blockchain system was broken. Hacker stole your BTC\n'.encode())

            # проверка на бота
            if execution_time < bot_time:
                client_socket.send('You are a bot\n'.encode())
                # print('Disabling')
                client_socket.close()
                break
