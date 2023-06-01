import discord
from discord.ext import commands
from discord import app_commands

import main
import requests
import json

bot = commands.Bot(command_prefix='!',intents=discord.Intents.default())

TOKEN = 'MTExMzY5Nzc1OTIzNzc2NzE4OA.GiXTy4.Mg9xdOPe8_VWpz1eHSluuvXSTaplBFLLDeC5bY'

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(e)

@bot.tree.command(name = 'metar', description = 'Recherche le dernier METAR disponible d\'un aéroport.')
@app_commands.describe(icao='ICAO')
async def metar(interaction: discord.Interaction, icao:str):

    url = f'https://api.checkwx.com/metar/{icao}/decoded?x-api-key=92da5b1db838401d8f67720db4'
    response = requests.get(url)
    metarjson = response.json()
    airport = metarjson["data"][0]['station']['name']
    metarraw = metarjson["data"][0]['raw_text']   
    print(airport)
    print(metarraw)
    embed = discord.Embed(title=f'{airport}', color=0x2483c5)
    embed.add_field(name='METAR', value=f'`{metarraw}`')
    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)