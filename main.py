import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import json
import random
import requests
from datetime import *

load_dotenv()
token = os.getenv('token')

intents = discord.Intents.all()

class CustomClient(commands.Bot):
    def __init__(self, command_prefix, self_bot):
        self.started = False

        commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents, self_bot=self_bot)
        self.bot = commands.Bot(command_prefix=command_prefix, intents=intents, owner_id=851635355974369281, description="FreeFolkSimulatorBot")

        # Empty dict for local data
        self.local_data = {'guilds': {}}

        self.used = []

        # Load in bot config / lines
        with open('bots.json','r') as file:
            data = file.read()
            file.close()

        self.bot_data = json.loads(data)

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

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
        When the bot is added to a guild, add the guild to local data.

        :param guild:
        :return:
        """

        self.local_data['guilds'][str(guild)] = {}
        for channel in guild.channels:
            self.local_data['guilds'][str(guild)][str(channel)] = {}

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

    async def get_webhooks(self):
        """
        Runs when the bot starts.  Iterates through guilds and gets all existing bot webhooks.  This is far more
        efficient than manually recording them.  However it's also slow initially, about 20 seconds.  Add
        threading in the future.

        :return:
        """
        start = datetime.now()

        # Iterate through bot guilds
        for guild in self.guilds:

            # Get guild name
            g = str(guild)

            # Add guild to local data
            self.local_data['guilds'][g] = {}

            # Iterate through channels
            for channel in guild.channels:

                # Get the channel name
                c = str(channel)

                # Only on text channels
                if str(channel.type) == "text":

                    # Erase all logged webhooks
                    self.local_data['guilds'][g][c] = {}


                    try:
                        # Load in existing webhooks
                        webhooks = await channel.webhooks()

                        # Iterate through webhooks
                        for webhook in webhooks:

                            # If a webhook's name is in the bot dict
                            if webhook.name in self.bot_data:

                                # If the webhook is already recorded, delete the extra one
                                if webhook.name in self.local_data['guilds'][str(guild)][str(channel)]:

                                    await webhook.delete()

                                # Add the webhook to local data
                                else:
                                    self.local_data['guilds'][str(guild)][str(channel)][webhook.name] = webhook.url
                    except Exception as e:
                        print(f"{channel.guild} had an error - {e}")

        print(f"Completed Webhook check in f{datetime.now() - start}")

    async def on_message(self, message):
        if self.started:
            # Get the guild name
            guild = str(message.guild)

            # Get the guild channel
            channel = str(message.channel)


            # Get the guild's data.  This shortens the code a little bit.
            g = self.local_data['guilds'][guild]


            try:

                # Iterate through bots that are assigned to that channel
                for bot in g[channel]:

                    # Iterate through each trigger word for each bot
                    for keyword in self.bot_data[bot]['keywords']:

                        # If there's a trigger word, respond
                        if keyword in message.content.lower():

                            # Make randomness
                            random.seed()

                            # Get a random number to choose the quote with
                            num = random.randint(0,len(self.bot_data[bot]['quotes'])-1)

                            # Choose the quote
                            response = self.bot_data[bot]['quotes'][num]

                            # Give the bot one shot to make a better quote, if it's used the one that it chose already
                            if response in self.used:
                                num = random.randint(0, len(self.bot_data[bot]['quotes']) - 1)
                                response = self.bot_data[bot]['quotes'][num]

                            # Make a user tag in case there's a spot for it
                            person = str(message.author).split("#")[0]

                            # Add user tag if there's a spot for it
                            if response.count("{}") == 1:
                                response = response.format(person)
                            elif response.count("{}") == 2:
                                response = response.format(person,person)

                            # Get the webhook URL
                            webhook_url = self.local_data['guilds'][guild][channel][bot]

                            # Send the message
                            self.send_webhook(webhook_url, response, bot)

                            # Add the response to used
                            self.used.append(response)

                            # Break out of the bot's for loop, so we don't send more than one message
                            break

            except Exception as e:
                print(e)

    async def on_ready(self):

        # Iterate through guilds and grab all webhooks to see which bots are active
        await self.get_webhooks()

        # For some reason
        self.started = True

        # Hello
        print(f'{self.user.name} is connected to Discord.')

        # Clear the used container every hour
        self.clear_used.start()



    @tasks.loop(hours=1)
    async def clear_used(self):

        # Clear the used container
        self.used = []




bot = CustomClient(command_prefix="!", self_bot=False)

# Load in those cogs
cogs = os.listdir('cogs')

print("Loading in cogs.")
for file in cogs:
    if ".py" in file:
        bot.load_extension("cogs."+file.replace(".py", ""))

print("Done loading cogs.")

bot.run(token)