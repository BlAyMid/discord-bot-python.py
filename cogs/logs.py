import discord
from discord.ext import commands
from discord import utils
import config


class Logs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Module {} is loaded'.format(self.__class__.__name__))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        msg = f"{member.name} joined the server."
        await self.bot.get_channel(config.channel_logs_system).send(msg)
        role = discord.utils.get(member.guild.roles, id=config.role_id_noname)
        await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        msg = f"{member.name} left the server."
        await self.bot.get_channel(config.channel_logs_system).send(msg)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        msg = f"Message before changes {before.content}\n"f"Message after changes {after.content}"
        msg_1 = f"Reddit"
        if before.content != after.content:
            await self.bot.get_channel(config.channel_logs_message).send(msg)
        if before.content == after.content:
            await self.bot.get_channel(config.channel_logs_message).send(msg_1)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        author = message.author
        msg = f"Deleted message: {message.content}\n"f"Name author {author}"
        await self.bot.get_channel(config.channel_logs_message).send(msg)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if before.channel is None:
            msg = f"{member.display_name} joined the channel {after.channel.mention}"
            await self.bot.get_channel(config.channel_logs_voice_state).send(msg)
        elif after.channel is None:
            msg = f"{member.display_name} left the channel {before.channel.mention}"
            await self.bot.get_channel(config.channel_logs_voice_state).send(msg)
        elif before.channel != after.channel:
            msg = f"{member.display_name} moved from the channel {before.channel.mention}" \
                  f" into the channel {after.channel.mention}"
            await self.bot.get_channel(config.channel_logs_voice_state).send(msg)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == config.POST_ID:
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            member = utils.get(message.guild.members, id=payload.user_id)

            try:
                emoji = str(payload.emoji)
                role = utils.get(message.guild.roles, id=config.ROLES[emoji])

                if (len([i for i in member.roles if i.id not in config.EXCROLES]) <= config.MAX_ROLES_PER_USER):
                    await member.add_roles(role)
                    msg = ('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
                    await self.bot.get_channel(config.channel_logs_rols).send(msg)
                else:
                    await message.remove_reaction(payload.emoji, member)
                    msg = ('[ERROR] Too many roles for user {0.display_name}'.format(member))
                    await self.bot.get_channel(config.channel_logs_rols).send(msg)

            except KeyError as e:
                print('[ERROR] KeyError, no role found for ' + emoji)
            except Exception as e:
                print(repr(e))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = utils.get(message.guild.members, id=payload.user_id)

        try:
            emoji = str(payload.emoji)
            role = utils.get(message.guild.roles, id=config.ROLES[emoji])

            await member.remove_roles(role)
            msg = ('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))
            await self.bot.get_channel(config.channel_logs_rols).send(msg)

        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))


def setup(bot):
    bot.add_cog(Logs(bot))