from discord.ext import commands
from discord.commands import slash_command


class FreeFolkSimulator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def init_master(self,ctx,bot,channel=None):

        # Grab the webhooks for that channel
        webhooks = await ctx.channel.webhooks()

        # Get the name of the channel.
        if channel:
            channelStr = str(channel)
        else:
            channelStr = str(ctx.channel)

        # Get the name of the guild
        guild = str(ctx.guild)

        # Add channel to guild config list if it doesn't exist
        if channelStr not in self.bot.local_data['guilds'][guild].keys():
            self.bot.local_data['guilds'][guild][channelStr] = {}
            print(f"Initialized {channelStr}")
        else:
            print(f"Found {channelStr} in data.")

        # If the bot is already initialized for this channel:
        if bot in self.bot.local_data['guilds'][guild][channelStr].keys():

            # Grab the URL / ID for the webhook that is stored in the config
            url = self.bot.local_data['guilds'][guild][channelStr][bot]

            # Parse out the ID
            id = url.split("webhooks/")[1].split("/")[0]

            # Remove the bot from that channel's keys
            self.bot.local_data['guilds'][guild][channelStr].pop(bot)

            # Iterate through webhooks in that channel, delete matching one
            for webhook in webhooks:
                if webhook.id == id:
                    webhook.delete()

            # Notify
            await ctx.respond(f"{bot} was already active here, it's been deactivated.")

            self.bot.save_config()

        else:

            # Gotta check into this, boosting probably changes.
            if len(webhooks) > 9:
                await ctx.respond("I don't think we can have more than ten webhooks.")

            else:

                # Grab the picture of the bot for the webhook
                with open(f'pics/{bot}.jpeg','rb') as image:
                    f = image.read()

                # Create a new webhook for the bot in that channel
                data = await ctx.channel.create_webhook(name=bot, avatar=f)

                # Record webhook URL
                self.bot.local_data['guilds'][guild][channelStr][bot] = data.url

                self.bot.save_config()

                await ctx.respond("Activated!  Trigger words are {}".format(", ".join(self.bot.bot_data[bot]['keywords'])))


    @slash_command(name='init_vizzy', description='Activate Vizzy T for a channel.')
    async def init_vizzy(self, ctx):
        bot = "vizzy-t-bot"
        await self.init_master(ctx,bot)


    @slash_command(name='init_bobby', description='Activate Bobby B for a channel.')
    async def init_bobby(self, ctx):
        bot = "bobby-b-bot"
        await self.init_master(ctx,bot)


    @slash_command(name='init_mannis', description='Activate Stannis Mannis for a channel.')
    async def init_mannis(self, ctx):
        bot = "stannis-mannis-bot"
        await self.init_master(ctx,bot)


    @slash_command(name='init_caraxes', description='Activate Caraxes for a channel.')
    async def init_caraxes(self, ctx):
        bot = "caraxes-bot"
        await self.init_master(ctx,bot)


    @slash_command(name='init_aeggy', description='Activate Aeggy III for a channel.')
    async def init_aeggy(self, ctx):
        bot = "aeggy-3-bot"
        await self.init_master(ctx,bot)


    @slash_command(name='init_jon', description='Activate Jon Snow for a channel.')
    async def init_jon(self, ctx):
        bot = "Jon Snow"
        await self.init_master(ctx,bot)


    @slash_command(name='init_hound', description='Activate the Hound for a channel.')
    async def init_hound(self, ctx):
        bot = "The Hound"
        await self.init_master(ctx,bot)


    @slash_command(name='init_olenna', description='Activate Olenna for a channel.')
    async def init_olenna(self, ctx):
        bot = "olenna-bot"
        await self.init_master(ctx,bot)


    @slash_command(name='init_karl', description='Activate Karl Tanner for a channel.')
    async def init_karl(self, ctx):
        bot = "karlbot"
        await self.init_master(ctx,bot)


    @slash_command(name='init_tormund', description='Activate TormundBot for a channel.')
    async def init_tormund(self, ctx):
        bot = "tormund-bot"
        await self.init_master(ctx,bot)


    @slash_command(name='init_tyrion', description='Activate Tyrion for a channel.')
    async def init_tyrion(self, ctx):
        bot = "tyrion-bot"
        await self.init_master(ctx,bot)


    @slash_command(name='init_nightking', description='Activate the Night King for a channel.')
    async def init_nightking(self, ctx):
        bot = "night-king-bot"
        await self.init_master(ctx,bot)


    @slash_command(name='init_cersei', description='Activate Cersei for a channel.')
    async def init_cersei(self, ctx):
        bot = "cersei-l-bot"
        await self.init_master(ctx,bot)


    @slash_command(name='init_tywin', description='Activate Tywin for a channel.')
    async def init_tywin(self, ctx):
        bot = "tywin-l-bot"
        await self.init_master(ctx,bot)


    @slash_command(name='init_jaime', description='Activate Jaime for a channel.')
    async def init_jaime(self, ctx):
        bot = "jaime-l-bot"
        await self.init_master(ctx,bot)


    @slash_command(name='init_gimli', description='Activate Gimli for a channel.')
    async def init_gimli(self, ctx):
        bot = "gimli-bot"
        await self.init_master(ctx,bot)


    @slash_command(name='init_arya', description='Activate Arya Stark for a channel.')
    async def init_arya(self, ctx):
        bot = "arya-bot"
        await self.init_master(ctx,bot)


    @slash_command(name='init_bran', description='Activate Bran Stark for a channel.')
    async def init_bran(self, ctx):
        bot = "bran-bot"
        await self.init_master(ctx,bot)


    @slash_command(name='init_ned', description='Activate Ned Stark for a channel.')
    async def init_ned(self, ctx):
        bot = "ned-bot"
        await self.init_master(ctx,bot)

    '''
    @slash_command(name='init_all', description='Activate everyone for a channel.')
    async def init_all(self, ctx):
        for bot in self.bot.bot_data.keys():
            await self.init_master(ctx,bot)


    @slash_command(name='thelongnight', description='Active all bots everywhere.  Run and hide.')
    async def thelongnight(self, ctx):
        for channel in ctx.guild.channels:
            for bot in self.bot.bot_data.keys():
                await self.init_master(ctx,bot,channel)
    '''

def setup(bot):
    bot.add_cog(FreeFolkSimulator(bot))
