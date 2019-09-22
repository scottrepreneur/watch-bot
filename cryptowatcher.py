import discord
import requests_async as requests
import pandas as pd
from arb_check import arb_check

currency = '$'
cryptowatch_domain = 'https://api.cryptowat.ch/'
no_orderbook_data = ['binance-us']

# colors
teal = discord.Colour(0x00AE86)
orange = discord.Colour(0xFF4500)
lime = discord.Colour(0x00FF00)
blue = discord.Colour(0x00BFFF)
red = discord.Colour(0x8B0000)

# Exchanges command
# @param [ids] - returns the symbols for the exchanges used in the URLs
#
async def get_exchanges(message, watch_command):
	try:
		if watch_command.split(' ')[1] == 'help':
			embed = discord.Embed(
				title='Exchanges Command | `$watch exchanges [ids, optional] `',
				description='The Exchanges Command will provide all the exchanges available in Watcher.\nOptionally, include `ids` to retrieve the exchange symbols used in the market & pricing commands',
				color= teal
				)
			embed.set_author(name='CryptoWat.ch', url='https://cryptowat.ch', icon_url= 'https://static.cryptowat.ch/static/images/cryptowatch.png')
			await discord_embed(message, embed)
			return
	except:
		url = cryptowatch_domain + 'exchanges'
		response = await requests.get(url)
		exchanges = response.json()['result']
		_exchanges = []

		try: 
			if watch_command.split(' ')[1] == 'ids':
				for e in exchanges:
					_exchanges.append(e['symbol'])
		except:
			for e in exchanges:
				_exchanges.append(e['name'])
		
		# print(_exchanges)
		embed = discord.Embed(
			title = 'Exchanges',
			description = (', ').join(_exchanges),
			color= orange
		)
		embed.set_author(name='CryptoWat.ch', url='https://cryptowat.ch', icon_url= 'https://static.cryptowat.ch/static/images/cryptowatch.png')
		await discord_embed(message, embed)

# Markets command
# @param first parameter should be an [exchange]
# @param second parameter should be [symbol] of the coin looking for markets
async def get_markets(message, watch_command):
	

	if len(watch_command.split(' ')) < 2 or watch_command.split(' ')[1] == 'help':
		embed = discord.Embed(
			title='Markets Command | `$watch markets [exchange] [symbol] `',
			description='Trading Pair: base and quote all lowercase, no space. ex. `btcusd`\nExchange: optionally, include an exchange. Kraken is used by default.',
			color= teal
			)
		embed.set_author(name='CryptoWat.ch', url='https://cryptowat.ch', icon_url= 'https://static.cryptowat.ch/static/images/cryptowatch.png')
		await discord_embed(message, embed)
		return

	try:
		if watch_command.split(' ')[1]:
			try:
				if watch_command.split(' ')[2]:
					url = cryptowatch_domain + 'markets/' + watch_command.split(' ')[1]
					response = await requests.get(url)
					# print(response.json())
					markets = response.json()['result']
					_markets = []
					for m in markets:
						if watch_command.split(' ')[2] in m['pair']:
							_markets.append(str(m['pair']).upper())

					embed = discord.Embed(
						title = '{} Markets at {}'.format(str(watch_command.split(' ')[2]).upper(), str(watch_command.split(' ')[1]).capitalize()),
						description = (', ').join(_markets),
						color= lime
					)
					embed.set_author(name='CryptoWat.ch', url='https://cryptowat.ch', icon_url= 'https://static.cryptowat.ch/static/images/cryptowatch.png')
					await discord_embed(message, embed)

			except:
				print('inner except')
				await discord_send(message, 'Please include an exchange and coin with markets request `$watch markets [kraken] [btc]`')
	except:
		print('outer except')
		await discord_send(message, 'Please include an exchange and coin with markets request `$watch markets [kraken] [btc]`')


# Prices commands
# @param first parameter is a [trading pair]
# @param (optional) an [exchange], defaults to kraken if left off
async def get_price(message, watch_command):
	if len(watch_command.split(' ')) < 2 or watch_command.split(' ')[1] == 'help':
		embed = discord.Embed(
			title='Price Command | `$watch price [trading pair] [exchange]`',
			description='Trading Pair: base and quote all lowercase, no space. ex. `btcusd`\nExchange: optionally, include an exchange. Kraken is used by default.',
			color= teal
			)
		embed.set_author(name='CryptoWat.ch', url='https://cryptowat.ch', icon_url= 'https://static.cryptowat.ch/static/images/cryptowatch.png')
		await discord_embed(message, embed)
		return

	try:
		if watch_command.split(' ')[2]:
			url = cryptowatch_domain + 'markets/{}/{}/price'.format(str(watch_command.split(' ')[2]).lower(),str(watch_command.split(' ')[1]).lower())
			response = await requests.get(url)
			if response.status_code == 404:
				embed = discord.Embed(
					title='Not Found',
					description=response.json()['error'],
					color= red
					)
				embed.set_author(name='CryptoWat.ch', url='https://cryptowat.ch', icon_url= 'https://static.cryptowat.ch/static/images/cryptowatch.png')
				await discord_embed(message, embed)
				return
			price = response.json()['result']['price']
			embed = discord.Embed(
					title='{} Price on {} '.format(str(watch_command.split(' ')[1]).upper(), str(watch_command.split(' ')[2]).capitalize()),
					description=currency + str(price),
					color= blue
				)
			embed.set_author(name='CryptoWat.ch', url='https://cryptowat.ch', icon_url= 'https://static.cryptowat.ch/static/images/cryptowatch.png')
			await discord_embed(message, embed)
	except:
		url = cryptowatch_domain + 'markets/kraken/{}/price'.format(str(watch_command.split(' ')[1]).lower())
		response = await requests.get(url)
		price = response.json()['result']['price']
		embed = discord.Embed(
				title='{} Price on {} '.format(str(watch_command.split(' ')[1]).upper(), "Kraken").capitalize(),
				description=currency + str(price),
				color= blue
			)
		embed.set_author(name='CryptoWat.ch', url='https://cryptowat.ch', icon_url= 'https://static.cryptowat.ch/static/images/cryptowatch.png')
		await discord_embed(message, embed)

async def get_market_summary(message, watch_command):
	if len(watch_command.split(' ')) < 2 or watch_command.split(' ')[1] == 'help':
		embed = discord.Embed(
			title='Price Summary Command | `$watch summary [trading pair] [exchange]`',
			description='Trading Pair: base and quote all lowercase, no space. ex. `btcusd`\nExchange: optionally, include an exchange. Kraken is used by default.',
			color= teal
			)
		embed.set_author(name='CryptoWat.ch', url='https://cryptowat.ch', icon_url= 'https://static.cryptowat.ch/static/images/cryptowatch.png')
		await discord_embed(message, embed)
		return

	try:
		if watch_command.split(' ')[2]:
			url = cryptowatch_domain + 'markets/{}/{}/summary'.format(str(watch_command.split(' ')[2]).lower(),str(watch_command.split(' ')[1]).lower())
			response = await requests.get(url)
			if response.status_code == 404:
				embed = discord.Embed(
					title='Not Found',
					description=response.json()['error'],
					color= red
					)
				embed.set_author(name='CryptoWat.ch', url='https://cryptowat.ch', icon_url= 'https://static.cryptowat.ch/static/images/cryptowatch.png')
				await discord_embed(message, embed)
				return
			price = response.json()['result']['price']
			embed = discord.Embed(
					title='{} Summary on {} '.format(str(watch_command.split(' ')[1]).upper(), str(watch_command.split(' ')[2]).capitalize()),
					color= blue
				)
			embed.add_field(name='Last Price', value=currency + str(price['last']), inline=True)
			embed.add_field(name='Volume (24h)', value=currency + str(response.json()['result']['volumeQuote']), inline=True)
			embed.add_field(name='High (24h)', value=currency + str(price['high']), inline=True)
			embed.add_field(name=currency + ' Change', value=currency + str(price['change']['absolute']), inline=True)
			embed.add_field(name='% Change', value=currency + str(price['change']['percentage']), inline=True)
			embed.add_field(name='Low (24h)', value=currency + str(price['low']), inline=True)
			embed.set_author(name='CryptoWat.ch', url='https://cryptowat.ch', icon_url= 'https://static.cryptowat.ch/static/images/cryptowatch.png')
			await discord_embed(message, embed)
	except:
		url = cryptowatch_domain + 'markets/kraken/{}/summary'.format(str(watch_command.split(' ')[1]).lower())
		response = await requests.get(url)
		price = response.json()['result']['price']
		embed = discord.Embed(
				title='{} Summary on {} '.format(str(watch_command.split(' ')[1]).upper(), 'Kraken'),
				color= blue
			)
		embed.add_field(name='Last Price', value=currency + str(price['last']), inline=True)
		embed.add_field(name='Volume (24h)', value=currency + str(response.json()['result']['volumeQuote']), inline=True)
		embed.add_field(name='High (24h)', value=currency + str(price['high']), inline=True)
		embed.add_field(name=currency + ' Change', value=currency + str(price['change']['absolute']), inline=True)
		embed.add_field(name='% Change', value=currency + str(price['change']['percentage']), inline=True)
		embed.add_field(name='Low (24h)', value=currency + str(price['low']), inline=True)
		embed.set_author(name='CryptoWat.ch', url='https://cryptowat.ch', icon_url= 'https://static.cryptowat.ch/static/images/cryptowatch.png')
		await discord_embed(message, embed)

# Orderbook command
# @param
# 
async def get_orderbook(message, watch_command):
	if len(watch_command.split(' ')) < 2 or watch_command.split(' ')[1] == 'help':
		embed = discord.Embed(
			title='Orderbook Command | `$watch orders [trading pair] [exchange]`',
			description='Trading Pair: base and quote all lowercase, no space. ex. `btcusd`\nExchange: optionally, include an exchange. Kraken is used by default.',
			color= teal
			)
		embed.set_author(name='CryptoWat.ch', url='https://cryptowat.ch', icon_url= 'https://static.cryptowat.ch/static/images/cryptowatch.png')
		await discord_embed(message, embed)
		return

	try:
		print(watch_command.split(' '))
		if watch_command.split(' ')[2]:
			url = cryptowatch_domain + 'markets/{}/{}/orderbook'.format(str(watch_command.split(' ')[2]).lower(),str(watch_command.split(' ')[1]).lower())
			response = await requests.get(url)
			if response.status_code == 404:
				embed = discord.Embed(
					title='Not Found',
					description=response.json()['error'],
					color= red
					)
				embed.set_author(name='CryptoWat.ch', url='https://cryptowat.ch', icon_url= 'https://static.cryptowat.ch/static/images/cryptowatch.png')
				await discord_embed(message, embed)
				return
			orderbook = response.json()['result']
			print(orderbook)
			embed = discord.Embed(
					title='{} Orderbook on {} '.format(str(watch_command.split(' ')[1]).upper(), str(watch_command.split(' ')[2]).capitalize()),
					color= blue
				)
			await discord_embed(message, embed)

	except:
		url = cryptowatch_domain + 'markets/kraken/{}/orderbook'.format(str(watch_command.split(' ')[1]).lower())
		response = await requests.get(url)
		orderbook = response.json()['result']
		print(orderbook)
		embed = discord.Embed(
				title='{} Orderbook on {} '.format(str(watch_command.split(' ')[1]).upper(), 'Kraken'),
				color= blue
			)
		await discord_embed(message, embed)

# Arbitrage command 
# @param [trading pair] 
# 
async def get_arb_opp(message, watch_command):
	print(watch_command)
	if len(watch_command.split(' ')) < 2 or watch_command.split(' ')[1] == 'help':
		embed = discord.Embed(
			title='Arbitrage Opportunity Command | `$watch arb [trading pair]`',
			description='Trading Pair: base and quote all lowercase, no space. ex. `btcusd`',
			color= teal
			)
		embed.set_author(name='CryptoWat.ch', url='https://cryptowat.ch', icon_url= 'https://static.cryptowat.ch/static/images/cryptowatch.png')
		await discord_embed(message, embed)
		return

	markets_url = cryptowatch_domain + 'markets'
	response = await requests.get(markets_url)
	markets = response.json()['result']
	_markets = []

	for m in markets:
		if m['active'] == True and str(m['pair']) == str(watch_command.split(' ')[1]) and not m['exchange'] in no_orderbook_data:
			orders_url = cryptowatch_domain + 'markets/{}/{}/orderbook'.format(str(m['exchange']), str(m['pair']))
			print(orders_url)
			r = await requests.get(orders_url)
			orderbook = r.json()['result']
			market = {
				'exchange': m['exchange'],
				'pair': m['pair'],
				'lowest_ask_quote': orderbook['asks'][0][0],
				'lowest_ask_base': orderbook['asks'][0][1],
				'highest_bid_quote': orderbook['bids'][0][0],
				'highest_bid_base': orderbook['bids'][0][1]
				}
			_markets.append(market)
	
	print(_markets)
	arb_markets = pd.DataFrame(_markets)
	# print(arb_markets.head(10))
	best_arb = arb_check(arb_markets)
	embed = discord.Embed(
			title=best_arb['title'],
			description=best_arb['description']
		)
	embed.set_author(name='CryptoWat.ch', url='https://cryptowat.ch', icon_url= 'https://static.cryptowat.ch/static/images/cryptowatch.png')
	await discord_embed(message, embed)
		
	# print(arb_markets.at['kraken','lowest_ask_quote'])
	# for index, row in arb_markets.iterrows():
	# 	print(abs(arb_markets.at['kraken','lowest_ask_quote'] - row['lowest_ask_quote']) / arb_markets.at['kraken','lowest_ask_quote'])
	# 	if abs(arb_markets.at['kraken','lowest_ask_quote'] - row['lowest_ask_quote']) / arb_markets.at['kraken','lowest_ask_quote'] > 0.001:
	# 		print(str(abs(arb_markets.at['kraken','lowest_ask_quote'] - row['lowest_ask_quote'])) + ' against ' + index)

async def discord_send(message, _message):
	await  message.channel.send(_message)

async def discord_embed(message, _embed):
	await  message.channel.send(embed=_embed)
