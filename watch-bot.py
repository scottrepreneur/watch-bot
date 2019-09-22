import os
from flask import Flask, request, jsonify
import discord
import requests_async as requests

client = discord.Client()

# colors
teal = discord.Colour(0x00AE86)
orange = discord.Colour(0xFF4500)
lime = discord.Colour(0x00FF00)
blue = discord.Colour(0x00BFFF)
red = discord.Colour(0x8B0000)

app = Flask(__name__)

cryptowatch_domain = 'https://api.cryptowat.ch/'

@client.event
async def on_ready():
    print('Bot logged in'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # say hello!
    if message.content.startswith('$hello'):
        await message.channel.send('Hello! :wave:')

    # get a cat image
    elif message.content.startswith('$cat'):
        await message.channel.send(requests.get('https://aws.random.cat/meow').json()['file'])

    # get cryptowat.ch
    elif message.content.startswith('$watch') or message.content.startswith('$w'):
    	await watcher_message(message)

# TODO: CHECK active markets & exchanges

async def watcher_message(message):
	if message.content.split(' ')[0] == '$w':
		watch_command = message.content[3:]
	else:
		watch_command = message.content[7:]
	print(watch_command.split(' '))

	# General Help command
	# no @params
	# Help is available for the other commands to get additional help
	if watch_command.split(' ')[0] == 'help':
		embed = discord.Embed(
			title= 'Bot Commands Help',
			description= '''Commands available: 
				```$watch [command] help\n$watch exchanges [ids]\n$watch markets [exchange] [ticker (single coin)]\n$watch price [pair] [exchange default=kraken]\n$watch summary [pair] [exchange default=kraken]\n$watch orderbook [pair] [exchange]```''',
			color= teal
		)
		embed.set_author(name='CryptoWat.ch', url='https://cryptowat.ch', icon_url= 'https://static.cryptowat.ch/static/images/cryptowatch.png')
		await discord_embed(message, embed)

	# Exchanges command
	# @param ids - returns the symbols for the exchanges used in the URLs
	#
	elif watch_command.split(' ')[0] == 'exchanges':
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
			
			print(_exchanges)
			embed = discord.Embed(
				title = 'Exchanges',
				description = (', ').join(_exchanges),
				color= orange
			)
			embed.set_author(name='CryptoWat.ch', url='https://cryptowat.ch', icon_url= 'https://static.cryptowat.ch/static/images/cryptowatch.png')
			await discord_embed(message, embed)

	# Markets command
	# @param first parameter should be an exchange
	# @param second parameter should be the coin looking for markets
	elif watch_command.split(' ')[0] == 'markets':
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
	# @param first parameter is a trading pair
	# @param (optional) the exchange, defaults to kraken if left off
	elif watch_command.split(' ')[0] == 'price':
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
						description=str(price),
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
					description=str(price),
					color= blue
				)
			embed.set_author(name='CryptoWat.ch', url='https://cryptowat.ch', icon_url= 'https://static.cryptowat.ch/static/images/cryptowatch.png')
			await discord_embed(message, embed)

	# Summary commands
	# @param 
	# 
	elif watch_command.split(' ')[0] == 'summary':
		await discord_send(message, "Summary")

	# Recent trades command
	# @param
	# 
	elif watch_command.split(' ')[0] == 'recent':
		await discord_send(message, "Recent")

	# Orderbook command
	# @param
	# 
	elif watch_command.split(' ')[0] == 'orderbook':
		await discord_send(message, "Orderbook")

	# Arbitrage command 
	# @param
	# 
	elif watch_command.split(' ')[0] == 'arb':
		await discord_send(message, 'checking for arb opportunities')

	else:
		embed = discord.Embed(
			title= 'No Command Found!',
			description= '''Commands available: 
				```$watch [command] help\n$watch exchanges [ids]\n$watch markets [exchange] [ticker (single coin)]\n$watch price [pair] [exchange default=kraken]```''',
			color= red
		)
		embed.set_author(name='CryptoWat.ch', url='https://cryptowat.ch', icon_url= 'https://static.cryptowat.ch/static/images/cryptowatch.png')
		await discord_embed(message, embed)


async def discord_send(message, _message):
	await  message.channel.send(_message)

async def discord_embed(message, _embed):
	await  message.channel.send(embed=_embed)


client.run(os.environ.get("DISCORD_API_KEY"))

if __name__ == '__main__':
	app.run()