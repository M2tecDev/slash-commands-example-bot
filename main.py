import asyncio
import discord, os
from discord.ext import commands
from dislash import (
    InteractionClient,
    SlashInteraction,
    Option,
    OptionChoice,
    OptionType,
    ActionRow,
    Button,
    SelectMenu,
    SelectOption,
    ButtonStyle,
    ResponseType,
    application_commands
)
# A local file for cool menus
from pagination import *


client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
inter_client = InteractionClient(client)
token = str(os.environ.get('bot_token'))


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
@inter_client.slash_command(description="Says Hello")
@application_commands.cooldown(1, 3, application_commands.BucketType.member)
async def hello(ctx):
    await ctx.reply('Hello!')


@inter_client.slash_command(description="Wanna see it?")
async def secret(ctx):
    await ctx.reply("Confidential message 😓😲😔🥱😒😖", ephemeral=True)


@inter_client.slash_command(
    description="Creates an embed",
    options=[
        Option("title", "Creates a title", OptionType.STRING),
        Option("description", "Creates a description", OptionType.STRING),
        Option("color", "Colors the embed", OptionType.STRING),
        Option("image_url", "URL of the embed's image", OptionType.STRING),
        Option("footer", "Creates a footer", OptionType.STRING),
        Option("footer_url", "URL of the footer image", OptionType.STRING)
    ]
)
async def embed(
    inter: SlashInteraction,
    title: str = None,
    description: str = None,
    color: str = None,
    image_url: str = None,
    footer: str = None,
    footer_url: str = None
):
    if color is not None:
        try:
            color = await commands.ColorConverter().convert(inter, color)
        except:
            color = discord.Color.default()
    else:
        color = discord.Color.default()
    reply = discord.Embed(color=color)
    if title is not None:
        reply.title = title
    if description is not None:
        reply.description = description
    if image_url is not None:
        reply.set_image(url=image_url)
    pl = {}
    if footer is not None:
        pl['text'] = footer
    if footer_url is not None:
        pl['icon_url'] = footer_url
    if len(pl) > 0:
        reply.set_footer(**pl)
    await inter.create_response(embed=reply)

#--------------------------+
# Command with subcommands |
#--------------------------+
@inter_client.slash_command(description="Sends a picture")
async def pic(inter: SlashInteraction):
    # The basae command for subcommands
    pass

@pic.sub_command(
    description="Pictures of animals",
    options=[
        Option("choice", "Choose on of them", OptionType.STRING, True, choices=[
            OptionChoice("Cat", "cat"),
            OptionChoice("Dog", "dog"),
            OptionChoice("Parrot", "parrot")
        ])
    ]
)
async def animal(inter: SlashInteraction, choice: str):
    # This command is visivle as "/pic animal"
    pics = {
        "cat": "https://cdn.discordapp.com/attachments/642107341868630024/810550425735790602/Depositphotos_9979039_xl-2015.png",
        "dog": "https://cdn.discordapp.com/attachments/642107341868630024/810550486482681856/51525059_401.png",
        "parrot": "https://cdn.discordapp.com/attachments/642107341868630024/810550543884746762/popugaj_d_850.png"
    }
    reply = discord.Embed(
        title="Adorable animal",
        color=discord.Color.from_rgb(200, 200, 200)
    )
    reply.set_image(url=pics[choice])
    await inter.create_response(embed=reply)

@pic.sub_command(
    description="Pictures os cars",
    options=[
        Option("choice", "Choose one of these", OptionType.STRING, True, choices=[
            OptionChoice("F1", "f1"),
            OptionChoice("Dragster", "dragster"),
            OptionChoice("Monstertruck", "monstertruck")
        ])
    ]
)
async def car(inter: SlashInteraction, choice: str):
    # This command is visivle as "/pic car"
    pics = {
        "f1": "https://cdn.discordapp.com/attachments/642107341868630024/810550602304061470/141385-27.png",
        "dragster": "https://cdn.discordapp.com/attachments/642107341868630024/810550764438552576/swamp-rat-37_1.png",
        "monstertruck": "https://cdn.discordapp.com/attachments/642107341868630024/810550863856140338/-5f8PdoTxji0w6-VGoHDTBicP2Zdc9tFUIomBtdzwl5PebWq7JZ74I0WOos6CY13ldpCILhGKodFZUjRS5eLPNjYOwBMjK0HgCzV.png"
    }
    reply = discord.Embed(
        title="Cool car",
        color=discord.Color.from_rgb(200, 200, 200)
    )
    reply.set_image(url=pics[choice])
    await inter.create_response(embed=reply)

@pic.sub_command(
    description="Pictures of aircrafts",
    options=[
        Option("choice", "Choose one of these", OptionType.STRING, True, choices=[
            OptionChoice("Airbus", "airbus"),
            OptionChoice("Helicopter", "helicopter"),
            OptionChoice("Supersonic Jet", "jet")
        ])
    ]
)
async def aircraft(inter: SlashInteraction, choice: str):
    # This command is visivle as "/pic aircraft"
    pics = {
        "airbus": "https://cdn.discordapp.com/attachments/642107341868630024/810551182153089044/42199782_401.png",
        "helicopter": "https://cdn.discordapp.com/attachments/642107341868630024/810551295185256489/2983453.png",
        "jet": "https://cdn.discordapp.com/attachments/642107341868630024/810551664771072020/images.png"
    }
    reply = discord.Embed(
        title="Modern aircraft",
        color=discord.Color.from_rgb(200, 200, 200)
    )
    reply.set_image(url=pics[choice])
    await inter.create_response(embed=reply)

#--------------------------+
#      Other commands      |
#--------------------------+
@inter_client.slash_command(
    description="Say something",
    options=[Option("text", "Type anything", OptionType.STRING, True)]
)
async def say(inter: SlashInteraction, text: str):
    await inter.create_response(text)


@inter_client.slash_command(
    name="user-info",
    description="Shows user profile",
    options=[Option("user", "Which user to inspect", OptionType.USER)]
)
async def user_info(inter: SlashInteraction, user: discord.User = None):
    badges = {
        "staff": "<:staff:812692120049156127>",
        "partner": "<:partner:812692120414322688>",
        "hypesquad": "<:hypesquad_events:812692120358879262>",
        "bug_hunter": "<:bug_hunter:812692120313266176>",
        "hypesquad_bravery": "<:bravery:812692120015339541>",
        "hypesquad_brilliance": "<:brilliance:812692120326373426>",
        "hypesquad_balance": "<:balance:812692120270798878>",
        "verified_bot_developer": "<:verified_bot_developer:812692120133042178>"
    }
    user = user or inter.author
    badge_string = ' '.join(badges[pf.name] for pf in user.public_flags.all() if pf.name in badges)
    created_at = str(user.created_at)[:-7]
    reply = discord.Embed(color=discord.Color.blurple())
    reply.title = str(user)
    reply.set_thumbnail(url=user.avatar_url)
    reply.add_field(
        name="Registration",
        value=(
            f"⌚ **Created at:** `{created_at}`\n"
            f"📋 **ID:** `{user.id}`"
        ),
        inline=False
    )
    if len(badge_string) > 1:
        reply.add_field(
            name="Badges",
            value=f"`->` {badge_string}"
        )
    await inter.create_response(embed=reply)


@inter_client.slash_command(
    description="Choose which notifications you want to get",
    options=[
        Option("updates", "Update pings", OptionType.BOOLEAN),
        Option("news", "News pings", OptionType.BOOLEAN)
    ]
)
async def notifications(inter: SlashInteraction, updates: bool = False, news: bool = False):
    if inter.guild is None:
        return
    # Get roles
    updates_role = discord.utils.get(inter.guild.roles, name="Updates")
    news_role = discord.utils.get(inter.guild.roles, name="News")
    # Which roles to add / remove
    to_add = []
    to_remove = []
    if updates:
        to_add.append(updates_role)
    else:
        to_remove.append(updates_role)
    if news:
        to_add.append(news_role)
    else:
        to_remove.append(news_role)
    # Add / remove the roles
    try:
        roles = [role for role in to_remove if role in inter.author.roles]
        if to_add:
            await inter.author.add_roles(*to_add)
        if roles:
            await inter.author.remove_roles(*roles)
    except Exception:
        pass
    # Build the tables
    list_of_added = '\n'.join(f"> <@&{role.id}>" for role in to_add)
    list_of_removed = '\n'.join(f"> <@&{role.id}>" for role in to_remove)
    # Send an embed
    emb = discord.Embed(
        title="🔔 | Notifications",
        color=discord.Color.gold()
    )
    if list_of_added:
        emb.add_field(name="Added:", value=list_of_added, inline=False)
    if list_of_removed:
        emb.add_field(name="Removed:", value=list_of_removed, inline=False)
    emb.set_footer(text=inter.author, icon_url=inter.author.avatar_url)
    await inter.create_response(embed=emb)

#--------------------------+
#         Buttons          |
#--------------------------+
@inter_client.slash_command(description="Play with buttons")
async def buttons(ctx: SlashInteraction):
    pages = [
        "This is page 1.\n"\
        "It has some content.\n"\
        "It even does have 3rd line",

        "This is page 2.\n"\
        "You definitely pressed a button.\n"\
        "Which is cool, but, there's page 3",

        "This is page 3.\n"\
        "As I promised"
    ]
    page = 0
    
    emb = discord.Embed(
        title="Tiny book",
        description=pages[page],
        color=discord.Color.green()
    )
    # Create some buttons
    row_of_buttons = ActionRow(
        Button(
            style=ButtonStyle.green,
            label="<-",
            custom_id="prev"
        ),
        Button(
            style=ButtonStyle.green,
            label="->",
            custom_id="next"
        )
    )
    # Send a message
    msg = await ctx.reply(
        embed=emb,
        components=[row_of_buttons]
    )

    def check(inter):
        return inter.author.id == ctx.author.id
    # One of the ways to process commands
    # See also an example below
    for _ in range(100): # Max 100 clicks per command
        try:
            inter = await msg.wait_for_button_click(check, timeout=60)
        except asyncio.TimeoutError:
            await msg.edit(components=[])
            return
        # inter is instance of ButtonInteraction
        # Get the clicked button id
        ID = inter.clicked_button.custom_id
        # Maybe change the page
        if ID == "prev":
            if page > 0:
                page -= 1
        elif ID == "next":
            if page + 1 < len(pages):
                page += 1
        # Update the message
        emb.description = pages[page]
        await inter.reply(embed=emb, type=ResponseType.UpdateMessage)
    
    await msg.edit(components=[])


@inter_client.slash_command(name="button-controls", description="Cool thing")
async def menu_example(ctx: SlashInteraction):
    # Build a menu
    menu = Element(
        header="Menu example",
        long_desc="Navigate through all the entries",
        elements=[
            Element(
                header="Chapter 1",
                long_desc="This is chapter 1 content. Truly entertaining stuff"
            ),
            Element(
                header="Chapter 2",
                long_desc="This is chapter 2 content. Cool"
            ),
            Element(
                header="Chapter 3",
                long_desc="This is chapter 3 content. Yo, look at this car: 🚕"
            ),
            Element(
                header="Super Chapter",
                long_desc="I have subchapters",
                elements=[
                    Element(
                        header="Penguins",
                        long_desc="They are cute, I guess"
                    ),
                    Element(
                        header="Crocodiles",
                        long_desc="Absolutely not cute creatures"
                    )
                ]
            )
        ]
    )
    # Build buttons
    button_row_1 = ActionRow(
        Button(
            style=ButtonStyle.blurple,
            emoji="⬆",
            custom_id="up"
        ),
        Button(
            style=ButtonStyle.green,
            label="Select",
            custom_id="select"
        )
    )
    button_row_2 = ActionRow(
        Button(
            style=ButtonStyle.blurple,
            emoji="⬇",
            custom_id="down"
        ),
        Button(
            style=ButtonStyle.red,
            label="Back",
            custom_id="back"
        )
    )
    # Send a message with buttons
    emb = discord.Embed(
        title=menu.header,
        description=f"{menu.long_desc}\n\n{menu.display_elements()}"
    )
    msg = await ctx.send(embed=emb, components=[button_row_1, button_row_2])

    # Click manager usage
    
    on_click = msg.create_click_listener(timeout=60)
    
    @on_click.not_from_user(ctx.author, cancel_others=True, reset_timeout=False)
    async def on_wrong_user(inter):
        await inter.reply("You're not the author", ephemeral=True)
    
    @on_click.matching_id("down")
    async def down(inter):
        menu.next_elem()
    
    @on_click.matching_id("up")
    async def up(inter):
        menu.prev_elem()
    
    @on_click.matching_id("select")
    async def select(inter):
        nonlocal menu
        menu = menu.element
    
    @on_click.matching_id("back")
    async def back(inter):
        nonlocal menu
        menu = menu.parent
    
    @on_click.no_checks()
    async def response(inter):
        emb.title = menu.header
        emb.description = f"{menu.long_desc}\n\n{menu.display_elements()}"
        await inter.reply(embed=emb, type=ResponseType.UpdateMessage)

    @on_click.timeout
    async def on_timeout():
        for button in button_row_1.components:
            button.disabled = True
        for button in button_row_2.components:
            button.disabled = True
        await msg.edit(embed=emb, components=[button_row_1, button_row_2])


@inter_client.slash_command(name="select-menu", description="Play with select menus")
async def select_menu(inter: SlashInteraction):
    emojis = {"r": "🔴", "g": "🟢", "b": "🔵"}
    menu = SelectMenu(
        custom_id="test_menu",
        placeholder="Select a couple of options",
        max_values=3,
        options=[
            SelectOption("Red", "r", "Represents red color", emojis['r']),
            SelectOption("Green", "g", "Represents green color", emojis['g']),
            SelectOption("Blue", "b", "Represents blue color", emojis['b'])
        ]
    )
    msg = await inter.reply("Choose your colors:", components=[menu])

    def check(menu_inter):
        return menu_inter.author == inter.author
    
    try:
        menu_inter = await msg.wait_for_dropdown(check, timeout=60)
    except asyncio.TimeoutError:
        await msg.delete()
    
    elems = [emojis[opt.value] for opt in menu_inter.select_menu.selected_options]
    await menu_inter.create_response(
        content=f"Your colors: {' '.join(elems)}",
        components=[],
        type=7
    )


#--------------------------+
#         Events           |
#--------------------------+
async def _on_ready():
    print("Client is ready")
client.add_listener(_on_ready, 'on_ready')


@inter_client.event
async def on_ready():
    print("Slash client is ready")

#--------------------------+

client.run(token)
