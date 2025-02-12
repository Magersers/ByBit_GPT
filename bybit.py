import random as rand
import time
import requests
from datetime import datetime
from pybit.unified_trading import HTTP

CHAD_API_KEY = '...'

session = HTTP(
    testnet=False,
    api_key="...",
    api_secret="...",
)

def prognos(message):
    request_json = {
    "message": f"Проанализируй криптовалюту {para} на основне предоставленных данных",
    "api_key": CHAD_API_KEY,
    "history": [
        { "role": "system", "content": message},
    ]
    }


    response = requests.post(url='https://ask.chadgpt.ru/api/public/gpt-4o-mini',
                         json=request_json)

    if response.status_code != 200:
        print(f'Ошибка! Код http-ответа: {response.status_code}')
    else:
        resp_json = response.json()

        if resp_json['is_success']:
            resp_msg = resp_json['response']
            used_words = resp_json['used_words_count']
            print(f'{resp_msg}')
            return resp_msg
        else:
            error = resp_json['error_message']
            print(f'Ошибка: {error}')

def Credit(session,symbol,buy,sell):
    print(session.set_leverage(
        category="linear",
        symbol=symbol,
        buyLeverage=str(buy),
        sellLeverage=str(sell),
    ))

def StartOrder(session,sumbol,side,qty,prise):
    order = str(rand.randint(1,9999999999))
    order_all = session.place_order(
        category="linear",
        symbol=sumbol,
        side=side,
        orderType="Limit",
        qty=str(qty),
        price=str(prise),
        orderLinkId=str(rand.randint(1,9999999999)),
        positionIdx='1',
    )
    return order_all['result']['orderId']
# Filled New Cancelled
def OrderStatus(session,orderId,para):
    status = session.get_open_orders(
        category="linear",
        symbol=para,
        openOnly=0,
        orderId=orderId,
        limit=1,
    )

    return status['result']['list'][0]['orderStatus']
         

para_mas=[
          {'para':'SOLUSDT','qvt':0.2,'order':0,'orderType':0,'exprise':''},
          {'para':'ETHUSDT','qvt':0.02,'order':0,'orderType':0,'exprise':''}
         ]
while 1 == 1 :
    i=0
    print("Начало паузы")
    time.sleep(10)  
    print("Пауза завершена")
    for par in para_mas :
        para = par['para']
        qvt = par['qvt']
        bad=0

        if par['order'] != 0:

            if(par['orderType'] == 0):
                result = OrderStatus(session,par['order'],para)
                print(result)
                if result == 'Filled':
                    order = StartOrder(session,para,'Sell',qvt,par['exprise'])
                    para_mas[i]['order'] = order
                    para_mas[i]['orderType'] = 1
            else:
                result = OrderStatus(session,par['order'],para)
                print(result)
                if result == 'Filled':
                    para_mas[i]['order'] = 0
                    para_mas[i]['orderType'] = 0
            i+=1
            continue

        svod = session.get_tickers(
            category="linear",
            symbol=para,
        )

        date_sena = session.get_kline(
            category="linear",
            symbol=para,
            interval=60,
        )

        kniga_zakazov = session.get_orderbook(
            category="linear",
            symbol=para,
        )

        limit_riska = session.get_risk_limit(
            category="linear",
            symbol=para,
        )

        dop_info = session.get_instruments_info(
            category="linear",
            symbol=para,
        )
        input_string =  prognos(f"""Используй метод технического анализа пары {para} и исходя из анализа напиши точку входа если она есть(цена должна быть ниже рынка чтобы сократить риски) и выхода в ином случае напиши переждать(тоесть если точка входа не выгодная на данный момент и возможно резкое падение), используя следюущие данные для анализа : исторические данные({date_sena}),
            актуальная книга заказов({kniga_zakazov}),лимит риска({limit_riska}),дополнительная информация({dop_info}),последняя сводка цен({svod}).ответ пиши по следующими шаблону(Цена входа: цена, цена выхода: цена) или пиши в случае если произошел резкий рост пиши переждать по шаблону(переждать время) время должно быть  в часах(не больше 2 часов)  и больше другого текста не надо только шаблон, это делается чтобы не уйти в убыток (и время ожидания) больше никакой информации не нужно писать  разница между ценой входа и продажи должна привышать 0.3%""" )
        try:
            prices = input_string.split(", ")
            entry_price = prices[0].split(": ")[1]
            exit_price = prices[1].split(": ")[1]
        except:
            bad = 1

        if bad != 1:
             order = StartOrder(session,para,'Buy',qvt,entry_price)
             para_mas[i]['order'] = order
             para_mas[i]['exprise'] = exit_price
        i+=1
# order = StartOrder(session,para,'Buy','0.01',2680.00)
# order2 = StartOrder(session,para,'Sell','0.01',exit_price)

# print("Вход", entry_price)
# print("выход", exit_price)