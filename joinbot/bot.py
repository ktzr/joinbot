import asyncio
import discord
import aiohttp

from joinbot.config import Config, ConfigDefaults


class JoinBot(discord.Client):
    def __init__(self):
        super().__init__()

        self.config = Config(ConfigDefaults.options_file)

    # noinspection PyMethodOverriding
    def run(self):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.start(self.config._login_token))
            loop.run_until_complete(self.connect())
        except Exception:
            loop.run_until_complete(self.close())
        finally:
            loop.close()

    async def on_ready(self):
        print('Connected!\n')
        print('Username: ' + self.user.name)
        print('ID: ' + self.user.id)

    async def on_member_join(self, member):
        self.send_message(member, 'Hey! and welcome to the %s Discord Server!\n'
                                  'Please make sure you read <#%s> and set a nickname so people '
                                  'can identify you and you can post in all the channels!' % (
                          member.server.name, self.config.rules_channel))
        await self.add_roles(member, discord.utils.get(member.server.roles, id=self.config.new_member_role))
        print('New guest %s' % member.name)

    async def on_message(self, message):

        if message.author == self.user:
            return
        if message.channel.id == self.config.new_member_channel:
            delete = True

            if self.config.command_prefix + "join" in message.content.lower():
                print('User Joining %s' % message.author.name)
                await self.remove_roles(message.author,
                                        discord.utils.get(message.server.roles, id=self.config.new_member_role))

            if self.config.command_prefix + 'setavi' in message.content.lower() and message.author.id == self.config.owner_id:
                string_avi = message.content[8:]
                async with aiohttp.get(string_avi) as r:
                    data = await r.read()
                    await self.edit_profile(avatar=data)

            if self.config.command_prefix + 'restart' in message.content.lower() and message.author.id == self.config.owner_id:
                self.logout()

            if self.config.command_prefix + 'keep' in message.content.lower() and message.author.id == self.config.owner_id:
                delete=False

            if delete:
                try:
                    print('deleting message from user: %s '
                          '"%s"' %(message.author.name,message.content))
                    await self.delete_message(message)
                except:
                    print("failed to delete message")
                    pass



if __name__ == '__main__':
    bot = JoinBot()
    bot.run()
