from kafka import KafkaConsumer, KafkaProducer
import requests, operator

def produce(data):
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    producer.send('ArbitrageCryptos', data)
    producer.close()

def consume():
    consumer = KafkaConsumer('ArbitrageCryptos', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest', enable_auto_commit=False)
    for message in consumer:
        print(message.value)
    consumer.close()

def compare(asset):
    asks = {'Coinbase' : 0, 'Kraken' : 0, 'Binance' : 0}
    bids = {'Coinbase' : 0, 'Kraken' : 0, 'Binance' : 0}
    
    #retrieve rating of asset bid and ask on each exchange platform KRAKEN/COINBASE/BINANCE
    kraken = requests.get("https://api.kraken.com/0/public/Ticker?pair=" + asset).json()
    asks['Kraken'] = kraken['result'][list(kraken['result'].keys())[0]]['a'][0]
    bids['Kraken'] = kraken['result'][list(kraken['result'].keys())[0]]['b'][0]
    
    asks['Binance'] = requests.get("https://api.binance.com/api/v3/ticker/bookTicker?symbol=" + asset).json()['askPrice']
    bids['Binance'] = requests.get("https://api.binance.com/api/v3/ticker/bookTicker?symbol=" + asset).json()['bidPrice']

    asks['Coinbase'] = requests.get("https://api.coinbase.com/v2/prices/" + asset[:3] + '-' + asset[3:] + "/buy").json()['data']['amount']
    bids['Coinbase'] = requests.get("https://api.coinbase.com/v2/prices/" + asset[:3] + '-' + asset[3:] + "/sell").json()['data']['amount']
    
    #sort dictionary to compare ratings
    askList = sorted(asks.items(), key=operator.itemgetter(1))
    bidList = sorted(bids.items(), key=operator.itemgetter(1))
    produce((asset + ' ask price : ' + askList[0][0] + ' (%f) ' %(float(askList[0][1])) + 'is cheaper than ' + askList[1][0] + ' by %f and cheaper than ' %(float(askList[1][1]) - float(askList[0][1])) + askList[2][0] + ' by %f' % (float(askList[2][1]) - float(askList[0][1]))).encode())
    produce((asset + ' bid price : ' + bidList[2][0] + ' (%f) ' %(float(bidList[2][1])) + 'is more expensive than ' + bidList[1][0] + ' by %f and more expensive than ' %(float(bidList[2][1]) - float(bidList[1][1])) + bidList[0][0] + ' by %f' % (float(bidList[2][1]) - float(bidList[0][1]))).encode())

    #search arbitrage between asks and bids
    if all(i[1] <= min(askList[j][1] for j in [0, 1, 2]) for i in bidList) == True:
        res = asset + ' arbitrage : No arbitrage possible'
        produce(res.encode())
    else: 
        for b in range(len(bidList)):
            for a in range(len(askList)):
                if bidList[b][1] > askList[a][1]:
                    res = asset + ' arbitrage : Buy %f from ' %(float(askList[a][1])) + askList[a][0] + ' and sell %f to ' %(float(bidList[b][1])) + bidList[b][0] + ', gain : %f' %(float(askList[a][1]) - float(bidList[b][1]))
                    produce(res.encode())

compare('ETHEUR')
consume()