import discord
from discord.ext import commands
import asyncio
import asyncpraw
import config


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('Module {} is loaded'.format(self.__class__.__name__))

    @commands.Cog.listener()
    async def on_ready(self):
        reddit = asyncpraw.Reddit(
            client_id=config.client_id,
            client_secret=config.client_secret,
            user_agent=config.user_agent,
        )
        while True:
            await asyncio.sleep(config.timeout)
            channel = self.bot.get_channel(config.id_channel_first)
            first_submissions = await reddit.subreddit(config.subbreddit_name_first)
            first_submissions = first_submissions.new(limit=config.post_limit)
            item = await first_submissions.__anext__()
            if item.title not in config.first:
                config.first.append(item.title)
                await channel.send(item.url)
            channel = self.bot.get_channel(config.id_channel_second)
            second_submssions = await reddit.subreddit(config.subbreddit_name_second)
            second_submssions = second_submssions.new(limit=config.post_limit)
            item = await second_submssions.__anext__()
            if item.title not in config.second:
                config.second.append(item.title)
                await channel.send(item.url)
            channel = self.bot.get_channel(config.id_channel_three)
            three_submssions = await reddit.subreddit(config.subbreddit_name_three)
            three_submssions = three_submssions.new(limit=config.post_limit)
            item = await three_submssions.__anext__()
            if item.title not in config.three:
                config.three.append(item.title)
                await channel.send(item.url)
            channel = self.bot.get_channel(config.id_channel_four)
            four_submssions = await reddit.subreddit(config.subbreddit_name_four)
            four_submssions = four_submssions.new(limit=config.post_limit)
            item = await four_submssions.__anext__()
            if item.title not in config.four:
                config.four.append(item.title)
                await channel.send(item.url)

    @commands.command(usage="kick <@user> <aurgument>")
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

    @commands.command(usage="kick <@user> <reason=None>")
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.send(f"You was kick from server")
        await ctx.send(f"Member {member.mention} was kicked from this server", delete_after=5)
        await member.kick(reason=reason)

    @commands.command(usage="ban <@user> <reason=None>")
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.send(f"You was banned on server")
        await ctx.send(f"Member {member.mention} was banned on this server", delete_after=5)
        await member.ban(reason=reason)

    @commands.command(usage="ver <@user>")
    @commands.has_role("noname")
    async def ver(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit=1)
        verification_role = discord.utils.get(ctx.message.guild.roles, name=config.verification_role)
        noname_role = discord.utils.get(ctx.message.guild.roles, name=config.noname_role)
        await member.add_roles(verification_role)
        await member.remove_roles(noname_role)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def info(self, ctx):
        region = ctx.guild.region
        owner = ctx.guild.owner.mention
        all = len(ctx.guild.members)
        members = len(list(filter(lambda m: not m.bot, ctx.guild.members)))
        bots = len(list(filter(lambda m: m.bot, ctx.guild.members)))
        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]
        channels = [len(list(filter(lambda m: str(m.type) == "text", ctx.guild.channels))),
                    len(list(filter(lambda m: str(m.type) == "voice", ctx.guild.channels)))]
        embed = discord.Embed(title=f"{ctx.guild} information")
        embed.add_field(name="Statuses",
                        value=f"Online: {statuses[0]}\n Idle: {statuses[1]}\n DND: {statuses[2]}\n Offline: {statuses[3]}")
        embed.add_field(name="Members", value=f"All: {all}\n Humans: {members}\n Bots: {bots}")
        embed.add_field(name="Channels",
                        value=f"All: {channels[0] + channels[1]}\n Text: {channels[0]}\n Voice: {channels[1]}")
        embed.add_field(name="Members", value=f"All: {all}\n Humans: {members}\n Bots: {bots}")
        embed.add_field(name="Region", value=region)
        embed.add_field(name="Owner", value=owner)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Admin(bot))
