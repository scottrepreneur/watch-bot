import pandas as pd

currency = '$'

_arb_markets = pd.DataFrame([{'exchange': 'bitfinex', 'pair': 'btcusd', 'lowest_ask_quote': 10061, 'lowest_ask_base': 4.19231838, 'highest_bid_quote': 10060, 'highest_bid_base': 0.91112082}, {'exchange': 'coinbase-pro', 'pair': 'btcusd', 'lowest_ask_quote': 10035.88, 'lowest_ask_base': 0.36846605, 'highest_bid_quote': 10035.87, 'highest_bid_base': 8.99429223}, {'exchange': 'bitstamp', 'pair': 'btcusd', 'lowest_ask_quote': 10039.32, 'lowest_ask_base': 0.80460934, 'highest_bid_quote': 10027.22, 'highest_bid_base': 0.5}, {'exchange': 'kraken', 'pair': 'btcusd', 'lowest_ask_quote': 10043.5, 'lowest_ask_base': 0.8, 'highest_bid_quote': 10040, 'highest_bid_base': 0.211}, {'exchange': 'cexio', 'pair': 'btcusd', 'lowest_ask_quote': 10050.4, 'lowest_ask_base': 0.02, 'highest_bid_quote': 10032.3, 'highest_bid_base': 0.163}, {'exchange': 'gemini', 'pair': 'btcusd', 'lowest_ask_quote': 10038.2, 'lowest_ask_base': 0.08075183, 'highest_bid_quote': 10030.37, 'highest_bid_base': 0.1638662}, {'exchange': 'quoine', 'pair': 'btcusd', 'lowest_ask_quote': 10037.25587, 'lowest_ask_base': 0.002, 'highest_bid_quote': 10035.75893, 'highest_bid_base': 0.002482}, {'exchange': 'okcoin', 'pair': 'btcusd', 'lowest_ask_quote': 10031.93, 'lowest_ask_base': 0.2349, 'highest_bid_quote': 10031.76, 'highest_bid_base': 0.027}, {'exchange': 'bisq', 'pair': 'btcusd', 'lowest_ask_quote': 10096.3236, 'lowest_ask_base': 0.0879, 'highest_bid_quote': 9996.36, 'highest_bid_base': 0.1423}, {'exchange': 'bitflyer', 'pair': 'btcusd', 'lowest_ask_quote': 10036.2, 'lowest_ask_base': 0.01, 'highest_bid_quote': 10023, 'highest_bid_base': 0.01}, {'exchange': 'bitbay', 'pair': 'btcusd', 'lowest_ask_quote': 10046.18, 'lowest_ask_base': 2, 'highest_bid_quote': 10026.67, 'highest_bid_base': 2}, {'exchange': 'bittrex', 'pair': 'btcusd', 'lowest_ask_quote': 10040.219, 'lowest_ask_base': 0.0005898, 'highest_bid_quote': 10032.215, 'highest_bid_base': 0.44684805}, {'exchange': 'liquid', 'pair': 'btcusd', 'lowest_ask_quote': 10037.25587, 'lowest_ask_base': 0.002, 'highest_bid_quote': 10035.75893, 'highest_bid_base': 0.002482}])


def arb_check(arb_markets):
	# arb_markets = pd.DataFrame([{'exchange': 'bitfinex', 'pair': 'btcusd', 'lowest_ask_quote': 10061, 'lowest_ask_base': 4.19231838, 'highest_bid_quote': 10060, 'highest_bid_base': 0.91112082}, {'exchange': 'coinbase-pro', 'pair': 'btcusd', 'lowest_ask_quote': 10035.88, 'lowest_ask_base': 0.36846605, 'highest_bid_quote': 10035.87, 'highest_bid_base': 8.99429223}, {'exchange': 'bitstamp', 'pair': 'btcusd', 'lowest_ask_quote': 10039.32, 'lowest_ask_base': 0.80460934, 'highest_bid_quote': 10027.22, 'highest_bid_base': 0.5}, {'exchange': 'kraken', 'pair': 'btcusd', 'lowest_ask_quote': 10043.5, 'lowest_ask_base': 0.8, 'highest_bid_quote': 10040, 'highest_bid_base': 0.211}, {'exchange': 'cexio', 'pair': 'btcusd', 'lowest_ask_quote': 10050.4, 'lowest_ask_base': 0.02, 'highest_bid_quote': 10032.3, 'highest_bid_base': 0.163}, {'exchange': 'gemini', 'pair': 'btcusd', 'lowest_ask_quote': 10038.2, 'lowest_ask_base': 0.08075183, 'highest_bid_quote': 10030.37, 'highest_bid_base': 0.1638662}, {'exchange': 'quoine', 'pair': 'btcusd', 'lowest_ask_quote': 10037.25587, 'lowest_ask_base': 0.002, 'highest_bid_quote': 10035.75893, 'highest_bid_base': 0.002482}, {'exchange': 'okcoin', 'pair': 'btcusd', 'lowest_ask_quote': 10031.93, 'lowest_ask_base': 0.2349, 'highest_bid_quote': 10031.76, 'highest_bid_base': 0.027}, {'exchange': 'bisq', 'pair': 'btcusd', 'lowest_ask_quote': 10096.3236, 'lowest_ask_base': 0.0879, 'highest_bid_quote': 9996.36, 'highest_bid_base': 0.1423}, {'exchange': 'bitflyer', 'pair': 'btcusd', 'lowest_ask_quote': 10036.2, 'lowest_ask_base': 0.01, 'highest_bid_quote': 10023, 'highest_bid_base': 0.01}, {'exchange': 'bitbay', 'pair': 'btcusd', 'lowest_ask_quote': 10046.18, 'lowest_ask_base': 2, 'highest_bid_quote': 10026.67, 'highest_bid_base': 2}, {'exchange': 'bittrex', 'pair': 'btcusd', 'lowest_ask_quote': 10040.219, 'lowest_ask_base': 0.0005898, 'highest_bid_quote': 10032.215, 'highest_bid_base': 0.44684805}, {'exchange': 'liquid', 'pair': 'btcusd', 'lowest_ask_quote': 10037.25587, 'lowest_ask_base': 0.002, 'highest_bid_quote': 10035.75893, 'highest_bid_base': 0.002482}])
	arb_markets = arb_markets.set_index('exchange')

	# print(arb_markets.at['kraken','lowest_ask_quote'])
	arbs = []
	for index, row in arb_markets.iterrows():
		exchangeA = {
			'name': index,
			'ask': row['lowest_ask_quote'],
			'base': row['lowest_ask_base'],
		}
		for index, row in arb_markets.iterrows():
			# print(exchangeA)
			# print(index)
			# print(row)
			if exchangeA['name'] == index:
				continue

			if int(row['highest_bid_quote']) > int(exchangeA['ask']):
				# print('bid: {} at {}, ask: {} at {}'.format(
				# 		row['highest_bid_quote'],
				# 		index,
				# 		exchangeA['ask'],
				# 		exchangeA['name']
				# 	))
				
				arb_amount_quote = currency + str(int(row['highest_bid_quote']) - int(exchangeA['ask']))
				arb_amount_base = int(arb_amount_quote.strip('$')) / exchangeA['ask']
				arb_percent = str((int(row['highest_bid_quote']) - int(exchangeA['ask'])) / int(exchangeA['ask']) *100) + '%'
				quote = 'usd'
				base = 'btc'
				
				new_arb = {
					'quote': quote,
					'base': base,
					'ask_exchange': exchangeA['name'],
					'ask_quote': exchangeA['ask'],
					'ask_base': exchangeA['base'],
					'bid_exchange': index,
					'bid_quote': row['highest_bid_quote'],
					'bid_base': row['highest_bid_base'],
					'arb_percent': arb_percent,
					'arb_amount_quote': arb_amount_quote,
					'arb_amount_base': arb_amount_base
				}
				arbs.append(new_arb)


	arbs.sort(key=lambda x: int(x['arb_amount_base']), reverse=True)
	arb = arbs[0]

	_new_title = 'a {} arbitrage opportunity!'.format(arb['arb_percent'])
	_new_description = '''

Buy {} {} with {} on {} for {}, Sell on {} for {}.
Potential Profit: {} {} ({})
	 	'''.format(
			arb['ask_base'],
			arb['base'],
			arb['quote'],
			arb['ask_exchange'],
			arb['ask_quote'],
			arb['bid_exchange'],
			arb['bid_quote'],
			arb['arb_amount_base'],
			arb['base'],
			arb['arb_amount_quote']
		)
	return({
		'title': _new_title,
		'description': _new_description
	})

# 				print(_new_description)
				# if row['highest_bid_base'] > exchangeA['base']:
				# 	_new_description = '''
						
				# 	'''
				# 	print(currency + str(exchangeA['base'] * exchangeA['ask']))
				# 	print(str(exchangeA['base'] * exchangeA['ask']/exchangeA['ask']*100)+ '%')
				# else: 
				# 	print(currency + str(row['highest_bid_base'] * row['highest_bid_quote']))
				# 	print(str(row['highest_bid_base'] * row['highest_bid_quote']/row['highest_bid_quote']*100)+ '%')



###
# arb = highest_bid is higher than lowest_ask
### ignoring withdrawal and exchange fees, for the moment

# for each exchangeA, get the other exchanges. iterate through those as well exchange[i]
# if exchange[i]['highest_bid_quote'] - exchangeA['lowest_ask_quote'] > 0:
# determine smaller of the two bases
# multiply the smaller base times the smaller quote
# divide ^ by the quote to get a percent

# [exchangeA] has low_ask
# [exchangeB] has high_bid
## message template:
# a(n) [arb_percent] arbitrage opportunity!
# Buy [quote] with [base] on [exchangeA] for [lowest_ask_quote] [], Sell on [exchangeB] for [highest_bid_quote].
# Potential Profit: [arb_amount] [base]

# test = '''🎊💯💯🎰 an extraordinary [5.79%] #arbitrage opportunity! 
# Buy [$ZRX] / [$ETH] on [DDEX] for [0.0011499], Sell on [Bittrex] for [0.0012164].
# \nPotential Profit: [0.005075] [ETH] (~1.058 DAI).\n\#DeFi 💰💰💰💰💰'''


# print(arb_markets.head())

