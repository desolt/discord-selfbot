from discord.ext import commands
import discord

class Profile:
    def __init__(self, bot):
        self.bot = bot

    async def get_random_quote(member: discord.Member):
        pass

    @commands.command(pass_context=True, no_pm=True)
    async def profile(self, ctx, *, member : discord.Member=None):
        if member is None: member = ctx.message.server.me

        prof_pic = lambda: member.default_avatar_url if len(member.avatar_url) == 0 else member.avatar_url

        embed = discord.Embed(title='{}#{}'.format(member.name, member.discriminator), 
                color=member.top_role.color,
                type='rich')
        embed.set_thumbnail(url=prof_pic())
        embed.add_field(name='Name', value=member.name)
        embed.add_field(name='Nickname', value=member.display_name)
        embed.add_field(name='Role', value=member.top_role.name)
        embed.add_field(name='Joined', value=member.joined_at.strftime('%m/%d/%Y'))
        await self.bot.send_message(ctx.message.channel, embed=embed)

def setup(bot):
    bot.add_cog(Profile(bot))

