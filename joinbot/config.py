import os
import shutil
import traceback
import configparser


class Config:
    def __init__(self, config_file):
        config = configparser.ConfigParser()

        if not config.read(config_file, encoding='utf-8'):
            print('[config] Config file not found')

        config = configparser.ConfigParser(interpolation=None)
        config.read(config_file, encoding='utf-8')

        self.auth = None

        self._login_token = config.get('Credentials', 'Token', fallback=ConfigDefaults.token)
        self.owner_id = config.get('Credentials', 'OwnerID', fallback=ConfigDefaults.owner_id)
        self.command_prefix = config.get('Credentials', 'CommandPrefix', fallback=ConfigDefaults.command_prefix)

        self.rules_channel = config.get('Channels', 'RulesChannel', fallback=ConfigDefaults.rules_channel)
        self.new_member_channel = config.get('Channels', 'NewMemberChannel', fallback=ConfigDefaults.new_member_channel)

        self.new_member_role = config.get('Roles', 'NewMemberRole', fallback=ConfigDefaults.new_member_role)


class ConfigDefaults:
    token = None    # This is not where you put your login info, go away.

    command_prefix = '.'
    rules_channel = None
    new_member_role = None
    new_member_channel = None
    owner_id = None

    options_file = 'config/options.ini'


