import discord, os
from discord.ext import commands
from dislash import slash_commands
from dislash.interactions import *


client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
slash = slash_commands.SlashClient(client)
token = str(os.environ.get('bot_token'))
guild_ids = [
    808030843078836254
]


class CE:
    vbd = "<:verified_bot_developer:812692120133042178>"
    staff = "<:staff:812692120049156127>"
    partner = "<:partner:812692120414322688>"
    nitro = "<:nitro:812692119990566933>"
    events = "<:hypesquad_events:812692120358879262>"
    hunter = "<:bug_hunter:812692120313266176>"
    brilliance = "<:brilliance:812692120326373426>"
    bravery = "<:bravery:812692120015339541>"
    balance = "<:balance:812692120270798878>"


#--------------------------+
#        Commands          |
#--------------------------+
@commands.cooldown(1, 5, commands.BucketType.member)
@client.command()
async def ping(ctx):
    await ctx.send(f"Pong: {client.latency * 1000:.0f}")


#--------------------------+
#     Slash-Commands       |
#--------------------------+
@slash.command(description="Says Hello")
async def hello(ctx):
    await ctx.reply('Hello!')


@slash.command(description="Wanna see it?")
async def secret(ctx):
    await ctx.reply("Confidential message 😓😲😔🥱😒😖", hide_user_input=True, ephemeral=True)


@slash.command(
    description="Creates an embed",
    options=[
        Option("title", "Creates a title", Type.STRING),
        Option("description", "Creates a description", Type.STRING),
        Option("color", "Colors the embed", Type.STRING),
        Option("image_url", "URL of the embed's image", Type.STRING),
        Option("footer", "Creates a footer", Type.STRING),
        Option("footer_url", "URL of the footer image", Type.STRING)
    ])
async def embed(ctx: Interaction):
    title = ctx.data.get('title')
    desc = ctx.data.get('description')
    color = ctx.data.get('color')
    image_url = ctx.data.get('image_url')
    footer = ctx.data.get('footer')
    footer_url = ctx.data.get('footer_url')
    if color is not None:
        try:
            color = await commands.ColorConverter().convert(ctx, color)
        except:
            color = discord.Color.default()
    else:
        color = discord.Color.default()
    reply = discord.Embed(color=color)
    if title is not None:
        reply.title = title
    if desc is not None:
        reply.description = desc
    if image_url is not None:
        reply.set_image(url=image_url)
    pl = {}
    if footer is not None:
        pl['text'] = footer
    if footer_url is not None:
        pl['icon_url'] = footer_url
    if len(pl) > 0:
        reply.set_footer(**pl)
    await ctx.send(embed=reply)


@slash.command(
    description="Sends a picture",
    options=[
        Option("animal", "Pictures of animals", Type.SUB_COMMAND, options=[
            Option("choice", "Choose on of them", Type.STRING, True, choices=[
                OptionChoice("Cat", "cat"),
                OptionChoice("Dog", "dog"),
                OptionChoice("Parrot", "parrot")
            ])
        ]),
        Option("car", "Pictures os cars", Type.SUB_COMMAND, options=[
            Option("choice", "Choose one of these", Type.STRING, True, choices=[
                OptionChoice("F1", "f1"),
                OptionChoice("Dragster", "dragster"),
                OptionChoice("Monstertruck", "monstertruck")
            ])
        ]),
        Option("aircraft", "Pictures of aircrafts", Type.SUB_COMMAND, options=[
            Option("choice", "Choose one of these", Type.STRING, True, choices=[
                OptionChoice("Airbus", "airbus"),
                OptionChoice("Helicopter", "helicopter"),
                OptionChoice("Supersonic Jet", "jet")
            ])
        ])
    ])
async def pic(ctx: Interaction):
    subcmd = ctx.data.options.values()[0]
    choice = subcmd.get("choice")
    pics = {
        "cat": "https://cdn.discordapp.com/attachments/642107341868630024/810550425735790602/Depositphotos_9979039_xl-2015.png",
        "dog": "https://cdn.discordapp.com/attachments/642107341868630024/810550486482681856/51525059_401.png",
        "parrot": "https://cdn.discordapp.com/attachments/642107341868630024/810550543884746762/popugaj_d_850.png",
        "f1": "https://cdn.discordapp.com/attachments/642107341868630024/810550602304061470/141385-27.png",
        "dragster": "https://cdn.discordapp.com/attachments/642107341868630024/810550764438552576/swamp-rat-37_1.png",
        "monstertruck": "https://cdn.discordapp.com/attachments/642107341868630024/810550863856140338/-5f8PdoTxji0w6-VGoHDTBicP2Zdc9tFUIomBtdzwl5PebWq7JZ74I0WOos6CY13ldpCILhGKodFZUjRS5eLPNjYOwBMjK0HgCzV.png",
        "airbus": "https://cdn.discordapp.com/attachments/642107341868630024/810551182153089044/42199782_401.png",
        "helicopter": "https://cdn.discordapp.com/attachments/642107341868630024/810551295185256489/2983453.png",
        "jet": "https://cdn.discordapp.com/attachments/642107341868630024/810551664771072020/images.png"
    }
    titles = {
        "animal": "Adorable animal",
        "car": "Coolset car",
        "aircraft": "Coolest aircraft"
    }
    reply = discord.Embed(
        title=titles[subcmd.name],
        color=discord.Color.from_rgb(200, 200, 200)
    )
    reply.set_image(url=pics[choice])
    await ctx.send(embed=reply)


@slash.command(
    description="Say something",
    options=[Option("text", "Type anything", Type.STRING, True)])
async def say(ctx):
    await ctx.send(ctx.data.get('text'))


@slash.command(
    name="user-info",
    description="Shows user profile",
    options=[Option("user", "Which user to inspect", Type.USER)] )
async def user_info(ctx: Interaction):
    badges = {
        "staff": CE.staff,
        "partner": CE.partner,
        "hypesquad": CE.events,
        "bug_hunter": CE.hunter,
        "hypesquad_bravery": CE.bravery,
        "hypesquad_brilliance": CE.brilliance,
        "hypesquad_balance": CE.balance,
        "verified_bot_developer": CE.vbd
    }
    user = ctx.data.get("user", ctx.author)
    badge_string = ' '.join(badges[pf.name] for pf in user.public_flags.all() if pf.name in badges)
    reply = discord.Embed(color=discord.Color.blurple())
    reply.title = str(user)
    reply.set_thumbnail(url=user.avatar_url)
    reply.add_field(
        name="Registration",
        value=(
            f"⌚ **Created at:** `{user.created_at}`\n"
            f"📋 **ID:** `{user.id}`"
        )
    )
    reply.add_field(
        name="Badges",
        value=f"`->` {badge_string}"
    )
    await ctx.send(embed=reply)


#--------------------------+
#         Events           |
#--------------------------+
async def _on_ready():
    print("Client is ready")
client.add_listener(_on_ready, 'on_ready')


@slash.event
async def on_ready():
    print("Slash client is ready")

#--------------------------+

client.run(token)