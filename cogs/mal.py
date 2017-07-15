from discord.ext import commands
from enum import Enum
from requests.auth import HTTPBasicAuth
import discord, requests, json
#import xmltodict
from bs4 import BeautifulSoup

class EntryType(Enum):
    ANIME = 'anime'
    MANGA = 'manga'

    def __str__(self):
        return str(self.value)

class MalEntry:
    def __init__(self, data, entry_type):
        self.id = data.find('id').text
        self.title = data.find('title').text
        self.desc = data.find('synopsis').text.replace('<br />', '').replace('[i]', '*').replace('[/i]', '*')
        self.image_url = data.find('image').text
        self.score = data.find('score').text
        self.type = data.find('type').text
        self.entry_type = str(entry_type)

        if entry_type is EntryType.ANIME:
            self.episodes = data.find('episodes').text
        else:
            self.chapter = data.find('chapters').text
            self.volume = data.find('volumes').text
            
def entry_search(name, entry_type, username, password):
    url = 'https://myanimelist.net/api/{}/search.xml'.format(entry_type)
    resp = requests.get(url, params=(('q', name),), auth=HTTPBasicAuth(username, password))
    soup = BeautifulSoup(resp.content, 'lxml')
    entry = soup.find(str(entry_type)).find('entry')
    return MalEntry(entry, entry_type)

class MyAnimeList:
    def __init__(self, bot):
        self.bot = bot
        with open('mal.json', 'r') as credsfile:
            self.creds = json.load(credsfile)

    @commands.command(pass_context=True)
    async def anime(self, ctx, *, name: str):
        entry = entry_search(name, EntryType.ANIME, self.creds['user'], self.creds['pass'])
        entry_embed = discord.Embed(title=entry.title, 
                description=entry.desc, 
                url='https://myanimelist.net/anime/{}'.format(entry.id))
        entry_embed.set_thumbnail(url=entry.image_url)
        entry_embed.add_field(name='Score', value=entry.score)
        entry_embed.add_field(name='Type', value=entry.type)
        entry_embed.add_field(name='Episodes', value=entry.episodes)
        await self.bot.send_message(ctx.message.channel, embed=entry_embed)

    @commands.command(pass_context=True)
    async def manga(self, ctx, *, name: str):
        entry = entry_search(name, EntryType.MANGA, self.creds['user'], self.creds['pass'])
        entry_embed = discord.Embed(title=entry.title,
                description=entry.desc,
                url='https://myanimelist.net/manga/{}'.format(entry.id))
        entry_embed.set_thumbnail(url=entry.image_url)
        entry_embed.add_field(name='Score', value=entry.score)
        entry_embed.add_field(name='Type', value=entry.type)
        entry_embed.add_field(name='Chapter', value=entry.chapter)
        entry_embed.add_field(name='Volume', value=entry.volume)
        await self.bot.send_message(ctx.message.channel, embed=entry_embed)

def setup(bot):
    bot.add_cog(MyAnimeList(bot))
