from discord.ext import commands
import json, sys

try:
    with open('config.json', 'r') as cfgfile:
        config = json.load(cfgfile)
except IOError: 
    print('Please create a config.json file. ' \
          'See https://github.com/desolt/ for reference.')
    sys.exit(0)

bot = commands.Bot(command_prefix=config['prefix'], self_bot=True)

extensions = [
    'cogs.mal',
    'cogs.profile',
]

@bot.event
async def on_ready():
    print('Selfbot runing as {}!'.format(bot.user.name))

@bot.event
async def on_message(message):
    await bot.process_commands(message)

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)

    bot.run(config['token'], bot=False)
