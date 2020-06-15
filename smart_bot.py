import discord
from smart_gen_2 import SmartBot
import re
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
Token = os.getenv('DISCORD_TOKEN')
client = discord.Client()

file = pd.read_csv('smart_sticky.csv')
region_big = {'EU': ['es', 'nl', 'pt', 'se', 'de', 'it', 'pl', 'gr', 'be', 'ua', 'gb', 'ru', 'fr'],
              'US': ['us', 'mx', 'ca']
              }

country_key = []
country_value = []
for i in range(file.shape[0]):
    m = re.compile(r'([^@]+).smartproxy.com').search(str(file['Proxy address'][i]))
    country_key.append(m.groups()[0])
    country_value.append([m.groups()[0]])

country = dict(zip(country_key, country_value))
country_all = dict(region_big, **country)


@client.event
async def on_ready():
    print(f'{client.user} has connected to discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    mm = re.compile(r'!gen ([^:]+) ([\d]+) ([^:]+:[^:]+)').search(message.content)
    if int(mm.groups()[1]) <= 10000:
        bot = SmartBot(country_all.get(mm.groups()[0]), mm.groups()[2], int(mm.groups()[1]))
        bot.proxy_gen()
        with open('proxy.txt', 'rb') as f:
            await message.channel.send(file=discord.File(f, f'Smart_{mm.groups()[0]}_{mm.groups()[1]}.txt'))
    else:
        await message.channel.send('proxies are too much! Please gen proxies below 10000!')


client.run(Token)
