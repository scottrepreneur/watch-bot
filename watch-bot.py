import os
from flask import Flask, request, jsonify
import discord
import requests

client = discord.Client()

app = Flask(__name__)

@client.event
async def on_ready():
    print('Bot logged in'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    # 
    elif message.content.startswith('$cat'):
        await message.channel.send(requests.get('https://aws.random.cat/meow').json()['file'])

    elif message.content.startswith('$hack'):
    	await message.channel.send(requests.get('https://api.cryptowat.ch/markets/kraken/btcusd/price').json()['result']['price'])

client.run(os.environ.get("DISCORD_API_KEY"))

if __name__ == '__main__':
	app.run()