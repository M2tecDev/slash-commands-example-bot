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
@slash.command(guild_ids=guild_ids, description="Says Hello")
async def hello(ctx):
    await ctx.reply('Hello!')


@slash.command(guild_ids=guild_ids, description="Wanna see it?")
async def secret(ctx):
    await ctx.reply("Confidential message 😓😲😔🥱😒😖", hide_user_input=True, ephemeral=True)


@slash.command(
    guild_ids=guild_ids,
    description="Creates an embed",
    options=[
        Option("title", "Creates a title", Type.STRING),
        Option("description", "Creates a description", Type.STRING),
        Option("color", "Colors the embed", Type.STRING),
        Option("image_url", "URL of the embed's image", Type.STRING),
        Option("footer", "Creates a footer", Type.STRING),
        Option("footer_url", "URL of the footer image", Type.STRING)
    ])
async def embed(ctx):
    title = ctx.data.get_option('title')
    desc = ctx.data.get_option('description')
    color = ctx.data.get_option('color')
    image_url = ctx.data.get_option('image_url')
    footer = ctx.data.get_option('footer')
    footer_url = ctx.data.get_option('footer_url')
    if color is not None:
        try:
            color = await commands.ColorConverter().convert(ctx, color.value)
        except:
            color = discord.Color.default()
    else:
        color = discord.Color.default()
    reply = discord.Embed(color=color)
    if title is not None:
        reply.title = title.value
    if desc is not None:
        reply.description = desc.value
    if image_url is not None:
        reply.set_image(url=image_url.value)
    pl = {}
    if footer is not None:
        pl['text'] = footer.value
    if footer_url is not None:
        pl['icon_url'] = footer_url.value
    if len(pl) > 0:
        reply.set_footer(**pl)
    await ctx.send(embed=reply)


@slash.command(
    guild_ids=guild_ids,
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
async def pic(ctx):
    subcmd = ctx.data.options[0]
    choice = subcmd.get_option("choice").value
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
    guild_ids=guild_ids,
    description="Say something",
    options=[Option("text", "Type anything", Type.STRING, True)])
async def say(ctx):
    await ctx.send(ctx.data.get_option('text').value)


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
