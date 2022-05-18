import discord
from discord.ext import commands
import config


class Member(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Module {} is loaded'.format(self.__class__.__name__))

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.command(usage="hello <@user> <reason=None>")
    async def hello(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit=1)
        await member.send(f'{member.name}, hello from {ctx.author.name}')

    @commands.command(usage="bitch <@user> <reason=None>")
    async def bitch(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit=1)
        await member.send(f'{ctx.author.name} says, you are  - {member.name} - son of a bitch))')

    @commands.command(usage="tip <@user> <reason=None>")
    async def tip(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit=1)
        await member.send(f'{ctx.author.name} slapped you, you are the best))))')

    @commands.command(usage="user <@user>")
    async def user(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        roles = [role for role in member.roles]
        embed = discord.Embed(title=f"Info {member.name}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Nickname", value=member.display_name, inline=True)
        embed.add_field(name="Created at", value=member.created_at.strftime("%d.%m.%Y %H:%M:%S"), inline=True)
        embed.add_field(name="Joined at", value=member.joined_at.strftime("%d.%m.%Y %H:%M:%S"), inline=True)
        embed.add_field(name="Roles", value="".join(role.mention for role in roles), inline=False)
        embed.add_field(name="Top role", value=member.top_role.mention, inline=True)
        embed.add_field(name="Bot?", value=member.bot, inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx):
        emb = discord.Embed(title="Навигация по командам")

        emb.add_field(name=f"{config.command_prefix}help_a", value="Help by commands (admin)")
        emb.add_field(name=f"{config.command_prefix}user @nickname", value="User Information")
        emb.add_field(name=f"{config.command_prefix}ping", value="Ping bot")
        emb.add_field(name=f"{config.command_prefix}hello @nickname", value="Send hello via bot")
        emb.add_field(name=f"{config.command_prefix}bitch @nickname", value="Tell your friend that he is the son of a bitch")
        emb.add_field(name=f"{config.command_prefix}tip @nickname", value="Slapped your friends")

        await ctx.send(embed=emb)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def help_a(self, ctx):
        emb = discord.Embed(title="All commands")

        emb.add_field(name=f"{config.command_prefix}ping", value="Ping bot")
        emb.add_field(name=f"{config.command_prefix}clear @arg(number)", value="Clearing the chat")
        emb.add_field(name=f"{config.command_prefix}kick @nickname", value="Kicking a member from the server")
        emb.add_field(name=f"{config.command_prefix}ban @nickname", value="Ban on the server")
        emb.add_field(name=f"{config.command_prefix}ver @nickname", value="Verification via role")
        emb.add_field(name=f"{config.command_prefix}user @nickname", value="User Information")
        emb.add_field(name=f"{config.command_prefix}info", value="Server Information")
        emb.add_field(name=f"{config.command_prefix}hello @nickname", value="Send hello via bot")
        emb.add_field(name=f"{config.command_prefix}bitch @nickname", value="Tell your friend that he is the son of a bitch")
        emb.add_field(name=f"{config.command_prefix}tip @nickname", value="Slapped your friends")
        emb.add_field(name=f"{config.command_prefix}help", value="Help by commands(no admin)")
        emb.add_field(name=f"{config.command_prefix}check_cogs @cog", value="Checking cog")
        emb.add_field(name=f"{config.command_prefix}load @cog", value="Loading of cog (it's better not to touch)")
        emb.add_field(name=f"{config.command_prefix}unload @cog", value="Shutdown of cog (it's better not to touch)")
        emb.add_field(name=f"{config.command_prefix}reload @cog", value="Reload of cog (it's better not to touch)")

        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Member(bot))