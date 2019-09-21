import os
from flask import Flask, request, jsonify
import discord
import requests_async as requests

client = discord.Client()

# colors
discord_teal = discord.Colour(0x00AE86)
discord_orange = discord.Colour(0xFF4500)
discord_lime = discord.Colour(0x00FF00)
discord_blue = discord.Colour(0x00BFFF)

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
    elif message.content.startswith('$watch'):
    	await watch_message(message)

async def watch_message(message):
	print(message.content)
	watch_command = message.content[7:]
	print(watch_command.split(' ')[0])

	# Help command
	# no @params
	# add help to other commands to get additional help
	if watch_command.split(' ')[0] == 'help':
		embed = discord.Embed(
			title = 'CryptoWatch Bot Commands',
			description = '''Commands available: 
				```$watch help
				$watch markets
				$watch price```''',
			color= discord_teal
		)
		await discord_embed(message, embed)

	# Exchanges command
	# @param ids - returns the symbols for the exchanges used in the URLs
	elif watch_command.split(' ')[0] == 'exchanges':
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
			title = 'CryptoWatch Exchanges',
			description = (', ').join(_exchanges),
			color= discord_orange
		)
		await discord_embed(message, embed)

	# Markets command
	# @param first parameter should be an exchange
	# @param second parameter should be the coin looking for markets
	elif watch_command.split(' ')[0] == 'markets':
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
							color= discord_lime
						)
						await discord_embed(message, embed)

				except:
					print('inner except')
					await discord_send(message, 'Please include an exchange and coin with markets request `$watch markets [kraken] [btc]`')
		except:
			print('outer except')
			await discord_send(message, 'Please include an exchange and coin with markets request `$watch markets [kraken] [btc]`')

	elif watch_command.split(' ')[0] == 'price':
		url = cryptowatch_domain + 'markets/kraken/{}/price'.format(str(watch_command.split(' ')[1]).lower())
		response = await requests.get(url)
		price = response.json()['result']['price']
		await discord_send(message, 'The Bitcoin price is: ' + str(price))

	elif watch_command.split(' ')[0] == 'summary':
		await discord_send(message, "Summary")

	elif watch_command.split(' ')[0] == 'recent':
		await discord_send(message, "Recent")

	elif watch_command.split(' ')[0] == 'orderbook':
		await discord_send(message, "Orderbook")

async def discord_send(message, _message):
	await  message.channel.send(_message)

async def discord_embed(message, _embed):
	await  message.channel.send(embed=_embed)


client.run(os.environ.get("DISCORD_API_KEY"))

if __name__ == '__main__':
	app.run()