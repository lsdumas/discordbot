import discord
from discord.ext import commands
from discord import app_commands

import refs
import requests
import json

bot = commands.Bot(command_prefix='!',intents=discord.Intents.default())

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(e)

@bot.tree.command(name = 'metar', description = 'Recherche le dernier METAR disponible d\'un aéroport.')
@app_commands.describe(icao = 'ICAO de l\'aérport')
async def metar(interaction: discord.Interaction, icao:str):
    icao = icao
    url = f'https://api.checkwx.com/metar/{icao}/decoded?x-api-key={refs.apiKey}'
    response = requests.get(url)
    metarjson = response.json()
    valide = metarjson['results']
    if valide == 1:
        airport = metarjson["data"][0]['station']['name']
        metarraw = metarjson["data"][0]['raw_text']   
        embed = discord.Embed(color = 0x2483c5)
        embed.set_author(name = f'{airport}', icon_url = f'{refs.icon}')
        embed.add_field(name = 'METAR', value = f'`{metarraw}`')
        embed.set_footer(text = 'Source: CheckWX')
        await interaction.response.send_message(embed = embed)
    else:     
        url = f'https://api.checkwx.com/metar/{icao}/nearest/decoded?x-api-key={refs.apiKey}'
        response = requests.get(url)
        metarjson = response.json()
        valide2 = metarjson['results']
        if valide2 == 1:
            airport = metarjson["data"][0]['station']['name']
            metarraw = metarjson["data"][0]['raw_text']
            embed = discord.Embed(description = f'METAR le plus proche de {icao.upper()}', color = 0x2483c5)
            embed.set_author(name = 'Pas de METAR disponible', icon_url = f'{refs.icon}')
            embed.add_field(name = f'{airport}', value = f'`{metarraw}`')
            embed.set_footer(text = 'Source: CheckWX')
            await interaction.response.send_message(embed = embed) 
        else:            
            embed = discord.Embed(title = 'Pas de METAR disponible', color = 0x2483c5)
            embed.set_author(name = 'Oups', icon_url = f'{refs.icon}')
            embed.set_footer(text = 'Source: CheckWX')
            await interaction.response.send_message(embed = embed)

@bot.tree.command(name = 'taf', description = 'Recherche le TAF d\' un aéroport')
@app_commands.describe(icao = 'ICAO de l\'aéroport')
async def taf(interaction: discord.Interaction, icao:str):
    icao = icao
    url = f'https://api.checkwx.com/taf/{icao}/decoded?x-api-key={refs.apiKey}'
    response = requests.get(url)
    tafjson = response.json()
    valide = tafjson['results']
    if valide == 1:
        airport = tafjson["data"][0]['station']['name']
        tafraw = tafjson["data"][0]['raw_text']   
        embed = discord.Embed(color = 0x2483c5)
        embed.set_author(name = f'{airport}',icon_url = f'{refs.icon}')
        embed.add_field(name = 'TAF', value = f'`{tafraw}`')
        embed.set_footer(text = 'Source: CheckWX')
        await interaction.response.send_message(embed = embed)
    else:     
        url = f'https://api.checkwx.com/taf/{icao}/nearest/decoded?x-api-key={refs.apiKey}'
        response = requests.get(url)
        tafjson = response.json()
        valide2 = tafjson['results']
        if valide2 == 1:
            airport = tafjson["data"][0]['station']['name']
            tafraw = tafjson["data"][0]['raw_text']
            embed = discord.Embed(description = f'TAF le plus proche de {icao.upper()}', color = 0x2483c5)
            embed.set_author(name = 'Pas de TAF disponible', icon_url = f'{refs.icon}')
            embed.add_field(name = f'{airport}', value = f'`{tafraw}`')
            embed.set_footer(text = 'Source: CheckWX')
            await interaction.response.send_message(embed = embed)
        else:            
            embed = discord.Embed(title = 'Pas de TAF disponible', color = 0x2483c5)
            embed.set_author(name = 'Oups', icon_url = f'{refs.icon}')
            embed.set_footer(text = 'Source: CheckWX')
            await interaction.response.send_message(embed = embed)

bot.run(refs.TOKEN)