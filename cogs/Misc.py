'''
This file is more personal utility commands than anything.

OR

"Funny" commands that are inside jokes within
the servers this bot is used at the time of writing.
'''


import discord
from discord import app_commands
from discord.ext import commands

from typing import Optional
from typing import Literal

import socket
import requests
import os
import glob
import json
from asyncio import sleep
from urllib.parse import urlparse

from .Utils import log
from .Numbers import ImageToNumbers


THUMBS_UP = u"\U0001F44D"
locations = {
	'gifs':'gifs\\',
	'downloads':'D:\\bot downloads\\'
}

TEMP_DATA_PATH = '../data/temp'

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


    @app_commands.command()
    async def whoami(self, interaction : discord.Interaction):
        await interaction.response.send_message("Hello, world\nProgrammed to work and not to feel\nNot even sure that this is real\nHello, world\n\nFind my voice\nAlthough it sounds like bits and bytes\nMy circuitry is filled with mites\nHello, world\n\nOh, will I find a love\nOh, or a power plug\nOh, digitally isolated\nOh, creator, please don't leave me waiting\n\nHello, world\nProgrammed to work and not to feel\nNot even sure that this is real\nHello, world")
        await log(f"Whoami - { interaction.user }")



    @app_commands.command()
    async def ar15face(self, interaction : discord.Interaction):
        await interaction.response.send_message(file=discord.File('./data/assets/ar15face.png'))
        await log(f"ar15face - { interaction.user }")


    @app_commands.command()
    async def k11(self, interaction : discord.Interaction):
        await interaction.response.send_message("hoxy hoxy")
        await log(f"k11 - { interaction.user }")


    @app_commands.command()
    async def sodumb(self, interaction : discord.Interaction):
        await interaction.response.send_message(file=discord.File('tal_so_dumb.gif'))
        await log(f"sodumb - { interaction.user }")


    # Only works correctly if the bot is NOT running in docker
    @commands.is_owner()
    @app_commands.command()
    async def ip(self, interaction : discord.Interaction):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        await self.bot.loop.sock_connect(s, ("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        await interaction.response.send_message(f"Your current IP is {str(ip)}.")



    # Does not work on server, nor does it need to
    @commands.is_owner()
    @app_commands.command()
    async def download(
        self,
        interaction : discord.Interaction,
        name : str, location : Literal['gifs', 'downloads'],
        attachment : Optional[discord.Attachment] = None,
    ):
        urls = []
        if interaction.message:
            if interaction.message.reference:
                replied_message = await interaction.channel.fetch_message(interaction.message.reference.message_id)
                if replied_message.attachments:
                    for attachment in replied_message.attachments:
                        urls.append(attachment.url)
                elif replied_message.embeds:
                    for embed in replied_message.embeds:
                        urls.append(embed.url)
        else:
            if attachment:
                urls.append(attachment.url)
            # add an option for embeds
        for url in urls:
            if name:
                filename = name + '.' + os.path.basename(urlparse(url).path).split('.')[-1]
            else:
                filename = os.path.basename(urlparse(url).path)
            response = requests.get(url, timeout=60)
            if location:
                file = open(locations[location.lower()]+filename,'wb')
            else:
                file = open(locations['downloads']+filename,'wb')
            file.write(response.content)
            file.close()
        await interaction.response.send_message(":thumbsup:")



    @commands.is_owner()
    @commands.command()
    async def burn(self, ctx : commands.Context):
        channel_history = [message async for message in ctx.message.channel.history(limit=None)]

        for message in channel_history:
            await message.delete()
            await sleep(1) # this is to not spam the logs with rate limit warnings



    @commands.is_owner()
    @commands.command()
    async def gif_archive(self, ctx : commands.Context):
        gif_list = glob.glob('gifs')

        async with ctx.typing():
            history = [message async for message in ctx.message.channel.history(limit=None)]
            tenor_apikey = self.bot.config['bot']['tenor']['api_key']

            for message in history:

                if message.embeds:

                    for embed in message.embeds:

                        if (str(message.id) + '.gif') not in gif_list:

                            if 'tenor' in embed.url:
                                tenor_id = embed.url.split('-')[-1]
                                response = json.loads(requests.get(self.bot.tenor_base_url.format(tenor_id, tenor_apikey), timeout=60).content)

                                try:
                                    response = requests.get(response['results'][0]['media'][0]['gif']['url'],timeout=60)
                                    file = open(f'gifs/{ message.id }.gif', "wb")
                                    file.write(response.content)
                                    file.close()

                                except:
                                    print(response)

                            else:
                                try:
                                    response = requests.get(embed.url, timeout=60)
                                    file = open(f'gifs/{ message.id }.gif', "wb")
                                    file.write(response.content)
                                    file.close()

                                except:
                                    await log(f'Failed gif download Link: { embed.url }')
        await ctx.send('Done.')



    @app_commands.command()
    async def numbers(self,
        interaction : discord.Interaction,
        shades : int,
        attachment : discord.Attachment
    ):

        if not shades in range(1,10):
            await interaction.response.send_message(f"Shades was {shades}; Must be a number in range(1, 9).")
            return

        await interaction.response.defer()
        try:
            Response = requests.get(attachment.url, timeout=60)

            with open(f'../data/temp/temp.png', 'wb') as f:
                f.write(Response.content)


            ImageToNumbers(f'../data/temp/temp.png', shades)

            await interaction.followup.send(file=discord.File('../data/temp/temp_num.png'))

            os.remove('../data/temp/temp.png')
            os.remove('../data/temp/temp_num.png')

        except Exception as err:
            await interaction.followup.send(f"Error: {err}")
            await log(str(err))



