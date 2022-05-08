import socket
import random

HOST = '127.0.0.1'
PORT = 9090

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
print('сервер запущен...')

salary = 500 # $
flag_cost = 100 # BTC
overflow_dollar_score = 7200000
overflow_btc_score = 120
flag = b'zssoib{PyTh0N_15_C0OL}'

while True:
    # ожидание в очереди подключений 1 клиента, кроме текущего
    server.listen(1)
    client_socket, client_address = server.accept()
    print('Новое подключение: ', client_address)

    # приветствие нового клиента
    client_socket.send('Welcome to the server!\n'.encode())
    client_socket.send('To get the flag, you have to pay 100 BTC. You have the opportunity to earn dollars and exchange them for BTC at a certain rate. Keep in mind that overflowing the balance will lead to a breakdown of the banking system and reset the account!\n'.encode())
    client_socket.send('\n'.encode())

    # доступные команды
    client_socket.send('Available commands:\n'.encode())
    client_socket.send(f'1 -get {salary}$\n'.encode())
    client_socket.send('2 -exchange $ for BTC\n'.encode())
    client_socket.send(f'3 -buy a flag for {flag_cost} BTC\n'.encode())

    # счета клиента
    dollar_score = 0
    btc_score = 0

    while True:
        #  курс Btc
        btc_rate = random.randint(20000, 60000)

        # счета клиента
        client_socket.send(f'Dollar score: {dollar_score}\n'.encode())
        client_socket.send(f'BTC score: {btc_score}\n'.encode())
        client_socket.send(f'BTC exchange rate: {btc_rate}\n'.encode())


        # получение данных от клиента
        try:
            data = client_socket.recv(1024)
        except socket.error:
            print('client socket error')
            break
        else:
            # декодировка данных
            try:
                msg = data.decode()[:-1]
            except:
                print('decode error')
                client_socket.send('decode error, try again'.encode())
                client_socket.close()
                break

            # отключение клиента, посылающего пустые сообщения
            if msg == '':
                client_socket.send('disabling'.encode())
                print('Disabling')
                client_socket.close()
                break

            # обработка команд клиента
            if msg == '1':
                dollar_score += salary
                client_socket.send('You got paid!\n'.encode())
            elif msg == '2':
                if dollar_score < btc_rate:
                    client_socket.send('Not enough funds to exchange!\n'.encode())
                else:
                    btc_score += (dollar_score // btc_rate)
                    dollar_score = dollar_score % btc_rate
                    client_socket.send('Successful exchange!\n'.encode())
            elif msg == '3':
                if btc_score >= flag_cost:
                    client_socket.send(flag)
                    print('Disabling')
                    client_socket.close()
                    break
                else:
                    client_socket.send('insufficient funds, try again\n'.encode())
            else:
                client_socket.send('Command error\n'.encode())
                print('Disabling')
                client_socket.close()
                break

            # 'поломка' банковской системы при переполнении счетов
            if dollar_score > overflow_dollar_score:
                dollar_score = 0
                client_socket.send('The banking system was broken. Hacker stole your money\n'.encode())
            elif btc_score > overflow_btc_score:
                btc_score = 0
                client_socket.send('The blockchain system was broken. Hacker stole your BTC\n'.encode())
