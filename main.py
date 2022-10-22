import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import json
import random
import requests
from data import config

load_dotenv()
token = os.getenv('token')

intents = discord.Intents.all()

class CustomClient(commands.Bot):
    def __init__(self, command_prefix, self_bot):

        commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents, self_bot=self_bot)
        self.bot = commands.Bot(command_prefix=command_prefix, intents=intents, owner_id=851635355974369281, description="FreeFolkSimulatorBot")

        # Empty dict for local data
        self.local_data = {}

        # Load in bot config / lines
        self.bot_data = config

        # Set local config file path
        self.config_path = "data.json"

        # Load in config data
        self.load_config()

    def inGuild(self,guild):
        """
        Check if the bot is in a guild.

        :param guild: str
        :return:
        """

        if guild in self.local_data['guilds']:
            return True
        else:
            return False

    def load_config(self):
        """
        Loads in config from local json file

        :return:
        """

        # Create an empty config file if it doesn't exist
        if not os.path.exists(self.config_path):
            self.local_data = {'guilds': {}}
            self.save_config()
        else:
            # Load in config from an existing file
            with open(self.config_path,"r") as config:
                data = config.read()
                self.local_data = json.loads(data)

    def save_config(self):
        """
        Dump config to a local file.

        :return:
        """

        dumping = json.dumps(self.local_data)
        with open(self.config_path, 'w') as file:
            file.write(dumping)
            file.close()


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
        When the bot is added to a guild, add the guild to local data.

        :param guild:
        :return:
        """

        self.local_data['guilds'][str(guild)] = {}
        self.save_config()

    def send_webhook(self, url, body, username):
        """
        Send a webhook.

        :param url: Webhook URL
        :param body: Primary content
        :param username: Associated user with webhook
        :return:
        """

        data = {'content': body, 'username': username}
        requests.post(url, data=data)

    async def on_message(self, message):
        guild = str(message.guild)
        channel = str(message.channel)

        # For shortening the code a little bit.
        g = self.local_data['guilds'][guild]

        # Check to see if the channel is configured to be watched
        if channel in g:

            # Iterate through bots that are assigned to that channel
            for bot in g[channel]:

                # Iterate through each trigger word for each bot
                for keyword in self.bot_data[bot]['keywords']:

                    # If there's a trigger word, respond
                    if keyword in message.content.lower():

                        # Get a random number to choose the quote with
                        num = random.randint(0,len(self.bot_data[bot]['quotes'])-1)

                        # Choose the quote
                        response = self.bot_data[bot]['quotes'][num]

                        # Grab the URL for the webhook
                        webhook_url = self.local_data['guilds'][guild][channel][bot]

                        # Send the message
                        self.send_webhook(webhook_url, response, bot)

                        # Break out of the bot's for loop, so we don't send more than one message
                        break

    async def on_ready(self):
        print(f'{self.user.name} is connected to Discord.')

        # Make sure all the guilds are added to local data
        for guild in self.guilds:
            if not self.inGuild(str(guild)):
                self.local_data['guilds'][str(guild)] = {}

        self.save_config()



bot = CustomClient(command_prefix="!", self_bot=False)

# Load in those cogs
cogs = os.listdir('cogs')

print("Loading in cogs.")
for file in cogs:
    if ".py" in file:
        bot.load_extension("cogs."+file.replace(".py", ""))

print("Done loading cogs.")

bot.run(token)