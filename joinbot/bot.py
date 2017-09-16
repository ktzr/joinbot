import discord

from joinbot.config import Config, ConfigDefaults


class JoinBot(discord.Client):
    def __init__(self):
        super().__init__()

        self.config = Config(ConfigDefaults.options_file)

    # noinspection PyMethodOverriding
    def run(self):
        super().run(self.config._login_token)

    async def on_ready(self):
        print('Connected!\n')
        print('Username: ' + self.user.name)
        print('ID: ' + self.user.id)

    async def on_member_join(self, member):
        try:
            self.send_message(member, 'Hey! and welcome to the %s Discord Server!\n'
                                  'Please make sure you read <#%s> and set a nickname so people '
                                  'can identify you and you can post in all the channels!' % (
                              member.server.name, self.config.rules_channel))
        except:
            print("failed to send msg to new member: %s" % member.name)
        try:
            await self.add_roles(member, discord.utils.get(member.server.roles, id=self.config.new_member_role))
        except:
            print("failed to add role to new member: %s" % member.name)
        print('New guest %s' % member.name)

    async def on_message(self, message):

        if message.author == self.user:
            return
        if message.channel.id == self.config.new_member_channel:
            delete = True

            if self.config.command_prefix + "join" in message.content.lower():
                print('User Joining %s' % message.author.name)
                try:
                    await self.remove_roles(message.author,discord.utils.get(message.server.roles, id=self.config.new_member_role))
                except:
                    print("failed to remove role from new member: %s" % message.author.name)

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
            return

    async def on_message_delete(self, message):
        try:
            if message.channel.id not in (self.config.new_member_channel, 296099129199689738):
                print("Message deleted in %s author %s :'%s'"%(message.channel.name,message.author.name,message.content))
        except Exception:
            print("failed to log message deletion")


if __name__ == '__main__':
    bot = JoinBot()
    bot.run()
