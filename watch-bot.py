import os
from flask import Flask, request, jsonify
import discord
import requests_async as requests
import cryptowatcher

client = discord.Client()

# colors
teal = discord.Colour(0x00AE86)
orange = discord.Colour(0xFF4500)
lime = discord.Colour(0x00FF00)
blue = discord.Colour(0x00BFFF)
red = discord.Colour(0x8B0000)

currency = '$'
cryptowatch_domain = 'https://api.cryptowat.ch/'


app = Flask(__name__)

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

# TODO: SET colors based on up or down market
# TODO: CHECK active markets & exchanges
# TODO: SET Currency Symbol based on ticker

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
		commands_help(message, teal)

	# Exchanges command
	# @param [ids] - returns the symbols for the exchanges used in the URLs
	#
	elif watch_command.split(' ')[0] == 'exchanges':
		await cryptowatcher.get_exchanges(message, watch_command)

	# Markets command
	# @param first parameter should be an [exchange]
	# @param second parameter should be [symbol] of the coin looking for markets
	elif watch_command.split(' ')[0] == 'markets':
		await cryptowatcher.get_markets(message, watch_command)

	# Prices commands
	# @param first parameter is a [trading pair]
	# @param (optional) an [exchange], defaults to kraken if left off
	elif watch_command.split(' ')[0] == 'price':
		await cryptowatcher.get_price(message, watch_command)

	# Summary commands
	# @param first parameter is a [trading pair]
	# @param (optional) an [exchange], defaults to kraken if left off
	elif watch_command.split(' ')[0] == 'summary':
		await cryptowatcher.get_market_summary(message, watch_command)

	# Orderbook command
	# @param
	# 
	elif watch_command.split(' ')[0] == 'orders':
		await cryptowatcher.get_orderbook(message, watch_command)

	# Arbitrage command 
	# @param
	# 
	elif watch_command.split(' ')[0] == 'arb':
		await cryptowatcher.get_arb_opp(message, watch_command)

	# Recent trades command
	# @param
	# 
	elif watch_command.split(' ')[0] == 'recent':
		await discord_send(message, "Recent")

	else:
		await commands_help(message, red)

# help helper function
async def commands_help(message, color):
	embed = discord.Embed(
		title= 'Bot Commands Help',
		description= '''Commands available:\n```$watch [command] help\n$watch exchanges [ids]\n$watch markets [exchange] [ticker (single coin)]\n$watch price [pair] [exchange default=kraken]\n$watch summary [trading pair] [exchange default=kraken]\n$watch arb [trading pair]```''',
		color= color
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