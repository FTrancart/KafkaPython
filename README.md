# KafkaPython

Please launch the zookeeper and the kafka server before using the Python file, plus create a topic called 'ArbitrageCryptos' : 
 
 WINDOWS
 - .\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
 - .\bin\windows\kafka-server-start.bat .\config\server.properties
 - .\bin\windows\kafka-topics.bat --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic ArbitrageCryptos
 
 
 
 Three crypto exchanges are used to compare the bid and ask prices of a specified asset pair, chosen because of their API : 
 - Binance, 
 - Coinbase, 
 - Kraken.
 
For each asset asked (example BTCEUR for the Bictoin price in Euro), the script compares the BTCEUR bid price of the exchanges and writes 
the one whose bid is the more expensive with the differences compared to the other exchanges.

Then it does the same for the ask prices by writing in the topic whose ask price is the cheapest as the differences compared to other exchanges.

Finally, the script computes if there is a possible arbitrage for this asset in the three exchanges by comparing if the maximum of the bid prices is superior
to the cheapest ask price, what would mean we could sell more BTCEUR than what we would have bought. If there is one, the script writes the beneficiary combination with the gain amount.

If, for BTCEUR : BidPrice(Binance) > AskPrice(Coinbase) 

Then : I buy BTCEUR on Coinbase and resell it on Binance and earn BidPrice(Binance) - AskPrice (Coinbase)
  

 
