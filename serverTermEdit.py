import random
import time


salary = 300  # $
flag_cost = 100  # BTC
bot_time = 0.07
acceptable_time = 15*60
flag = 'zssoib{PyTh0n_15_a_B1g_Th1nG_4_U}'
greeting = ['Welcome to the server!',
            'To get the flag, you have to pay 100 BTC. You have the opportunity to earn dollars and exchange them for BTC at a certain rate. Keep in mind that overflowing the balance will lead to a breakdown of the banking system and reset the account!',
            '',
            'Available commands:',
            f'1 -get {salary}$',
            '2 -exchange $ for BTC',
            f'3 -buy a flag for {flag_cost} BTC']


# приветствие нового клиента и доступные команды
for msg in greeting:
    print(msg)

# счета клиента
currencies = {'Dollar score': 0,
              'BTC score': 0,
              'BTC rate': 0}

tic = 10
start_time = time.time()
while True:
    #  курс Btc и диапазон
    currencies['BTC rate'] = random.randint(20000, 60000)

    overflow_dollar_score = random.randint(70000, 7200000)
    overflow_btc_score = random.randint(105, 130)

    # счета клиента
    for key, value in currencies.items():
        print(f'{key}: {value}')


    # получение данных от клиента
    try:
        data = input()
        execution_time = float(f'{time.perf_counter() - tic:0.4f}')
        tic = time.perf_counter()
    except:
        break
    else:
        # декодирование данных
        try:
            msg = data
        except:
            print('decode error, try again')
            break

        # отключение клиента, посылающего пустые сообщения
        if msg == '':
            print('disabling')
            break

        # обработка команд клиента
        if msg == '1':
            currencies['Dollar score'] += salary
            print('You got paid!')
        elif msg == '2':
            if currencies['Dollar score'] < currencies['BTC rate']:
                print('Not enough funds to exchange!')
            else:
                currencies['BTC score'] += (currencies['Dollar score'] // currencies['BTC rate'])
                currencies['Dollar score'] = currencies['Dollar score'] % currencies['BTC rate']
                print('Successful exchange!')
        elif msg == '3':
            if currencies['BTC score'] >= flag_cost:
                print(flag)
                break
            else:
                print('insufficient funds, try again')
        else:
            print('Command error')
            break


        # 'поломка' банковской системы при переполнении счетов
        if currencies['Dollar score'] > overflow_dollar_score:
            currencies['Dollar score'] = 0
            print('The banking system was broken. Hacker stole your money')
        elif currencies['BTC score'] > overflow_btc_score:
            currencies['BTC score'] = 0
            print('The blockchain system was broken. Hacker stole your BTC')

        # проверка на бота
        if execution_time < bot_time:
            print('You are a bot')
            break

        # ограничение времени сеанса
        stop_time = time.time()
        all_time = stop_time - start_time
        if all_time > acceptable_time:
            print('Your time is over')
            break
