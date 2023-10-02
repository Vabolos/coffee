import discord
import random
import sys
import os
import datetime
import asyncio
import wavelink

from discord import app_commands, Interaction
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from datetime import datetime, timedelta, time
from discord.ui import Button, View

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
bot = discord.Client(intents=intents)
TOKEN = 'TOKEN HERE'
command = app_commands.CommandTree(bot)
start_time = datetime.now().replace(microsecond=0)




#-------------------------------------------------CODE START-------------------------------------------------#

# sync commands
@command.command(name='sync', description='Owner only')
async def sync(interaction: discord.Interaction):
    if interaction.user.id == userID here:
        await command.sync()
        print('Command tree synced.')
    else:
        await interaction.response.send_message('You must be the owner to use this command!')

#bot is ready for combat
@bot.event
async def on_ready():
    await command.sync(guild=discord.Object(id=serverID here))
    user_id = bot.user.id
    embed = discord.Embed(title="I'm ready!", description="Bot is ready to serve the coffee shop!", color=0x6a4a3a)
    embed.set_footer(text="ID: " + str(user_id) + " • " + str(datetime.now().strftime("%H:%M")))
    await bot.get_channel(channelID here).send(embed=embed)
        # Setting `Watching ` status
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the guests!"))
    print("\nReady for reservations!")
    bot.loop.create_task(node_connect())

async def node_connect():
    await bot.wait_until_ready()
    await wavelink.NodePool.create_node(bot=bot, host='127.0.0.1', port=2300, password='youshallnotpass', https=False)

@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
    channel = bot.get_channel(channelID here)
    await channel.send(f':arrow_forward: `Lavalink` - Node, ID= **{node.identifier}** is ready!')
    print(f"Node {node.identifier} is ready!") 

# restarts the bot
@command.command(description="Restart bot!", guild=discord.Object(id=serverID here))
@app_commands.default_permissions(administrator=True)
async def restart(interaction: discord.Interaction):
    if interaction.user.id == userID here:
        await interaction.response.send_message("Restarting...")
        now = datetime.now()
        current_time = now.strftime("%d %B - %H:%M:%S")
        channel = bot.get_channel(channelID here)
        await channel.send(f"> `{current_time}` - Bot is restarting...")
        print("Bot is restarting...")
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        await interaction.response.send_message("You don't have permission to use this command!")
        now = datetime.now()
        current_time = now.strftime("%d %B - %H:%M:%S")
        channel = bot.get_channel(channelID here)
        await channel.send(f"> `{current_time}` - {interaction.user.mention} tried to restart the bot!")
        print("Unauthorized access attempt by " + str(interaction.user))

# shuts down the bot
@command.command(description="Shuts down the bot!", guild=discord.Object(id=serverID here))
@app_commands.default_permissions(administrator=True)
async def shutdown(interaction: discord.Interaction):
    if interaction.user.id == userID here:
        await interaction.response.send_message("shutting down...")
        now = datetime.now()
        current_time = now.strftime("%d %B - %H:%M:%S")
        channel = bot.get_channel(channelID here)
        await channel.send(f"❗ `{current_time}` - Bot is shutting down...")
        print("Bot is shutting down...")
        sys.exit()
    else:
        await interaction.response.send_message("You are not allowed to shut down the bot!")
        now = datetime.now()
        current_time = now.strftime("%d %B - %H:%M:%S")
        channel = bot.get_channel(channelID here)
        await channel.send(f"❗ `{current_time}` - {interaction.user.mention} tried to shut down the bot!")
        print("Unauthorized access attempt by " + str(interaction.user))

@bot.event
async def on_member_join(member: discord.Member):
    channel = bot.get_channel(channelID here)
    message_content = f"Welcome {member.mention} to the Coffee Shop!"
    embed = discord.Embed(
        title="Enjoy your stay!",
        description=f"Thank you for joining! Please make sure to read the <#rulechannelD here> and have a great time! :coffee: \n \n You can chat both here and in channelLINK \n",
        color=0x6a4a3a
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1034538860165730376/1112840193477726339/5650-marshmallow-pusheen.gif")
    embed.set_image(url="https://cdn.discordapp.com/attachments/1008706439310753832/1028539043518103562/IMG_0443.jpg")
    embed.set_footer(text="The Coffee Shop")
    role = discord.utils.get(member.guild.roles, id=roleID here)
    await member.add_roles(role)

    # Create custom button linked to a custom VC
    custom_vc_button = Button(style=discord.ButtonStyle.grey, label="☕ Join Custom VC", url="channelLINK here")

    # Create normal button linked to a normal VC
    normal_vc_button = Button(style=discord.ButtonStyle.grey, label="🍵 Join Normal VC", url="channelLINK here")

    # Add buttons to the view
    view = View()
    view.add_item(custom_vc_button)
    view.add_item(normal_vc_button)

    # Send the message with embed and buttons
    message = await channel.send(content=message_content, embed=embed, view=view)
    await asyncio.sleep(300)  # Delay for 5 minutes (300 seconds)
    await message.delete()  # Delete the message and embed

# snipe messages
snipe_message_content = None
snipe_message_author = None

@bot.event
async def on_message_delete(message):
    global snipe_message_content
    global snipe_message_author

    snipe_message_content = message.content
    snipe_message_author = message.author.name
    await asyncio.sleep(60)
    snipe_message_author = None
    snipe_message_content = None

@command.command(description="Snipes the last deleted message!", guild=discord.Object(id=serverID here))
async def snipe(interaction: discord.Interaction):
    if snipe_message_content == None:
        await interaction.response.send_message("There is nothing to snipe!")
    else:
        userAvatar = interaction.user.display_avatar
        embed = discord.Embed(description=f"{snipe_message_content}", color=0x6a4a3a)
        embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}", icon_url=userAvatar)
        embed.set_author(name=f"Sniped a message deleted by {snipe_message_author}")
        await interaction.response.send_message(embed=embed)
        return


# edit snipe messages before and after content
edit_snipe_message_before = None
edit_snipe_message_after = None
edit_snipe_message_author = None

@bot.event
async def on_message_edit(before, after):
    global edit_snipe_message_before
    global edit_snipe_message_after
    global edit_snipe_message_author

    edit_snipe_message_before = before.content
    edit_snipe_message_after = after.content
    edit_snipe_message_author = after.author.name
    await asyncio.sleep(60)
    edit_snipe_message_author = None
    edit_snipe_message_before = None
    edit_snipe_message_after = None

@command.command(description="Snipes the last edited message!", guild=discord.Object(id=serverID here))
async def editsnipe(interaction: discord.Interaction):
    if edit_snipe_message_before == None:
        await interaction.response.send_message("There is nothing to snipe!")
    else:
        userAvatar = interaction.user.display_avatar
        embed = discord.Embed(description=f"**Before:** {edit_snipe_message_before} \n \n **After:** {edit_snipe_message_after}", color=0x6a4a3a)
        embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}", icon_url=userAvatar)
        embed.set_author(name=f"Sniped a message edited by {edit_snipe_message_author}")
        await interaction.response.send_message(embed=embed)
        return


# /showavatar command
@command.command(description="Show avatar!", guild=discord.Object(id=serverID here))    
@app_commands.describe(show='Input username')
async def avatar(interaction: discord.Interaction, show: discord.User):
    userAvatar = show.display_avatar
    embed = discord.Embed(title=f"Avatar",description=f"")
    embed.set_image(url=userAvatar)
    embed.set_author(name=show, icon_url=userAvatar)
    await interaction.response.send_message(embed=embed)


#purge command
@command.command(description="Purge messages!", guild=discord.Object(id=serverID here))
@app_commands.default_permissions(manage_messages=True)
@app_commands.describe(amount='Input amount')
async def purge(interaction: discord.Interaction, amount: int):
    await interaction.response.defer(ephemeral=False)
    await interaction.channel.purge(limit=amount+1)

# bot events
# blob 
@bot.event
async def on_message(message):
    if message.content.startswith('blob'):
        await message.reply('https://tenor.com/view/fell-down-catscafecomics-cute-penguin-blob-gif-16020602')
    if message.content.startswith('coffee'):
       await message.reply('https://tenor.com/view/cup-coffee-anime-pink-cute-gif-17759667')
    if message.content.startswith('shark'):
         await message.reply('https://images-ext-1.discordapp.net/external/wZUrV164mYoJLm510WHkHNGBbULCCg8fab-sk5Ue_pM/https/i.natgeofe.com/n/aa12774c-6281-4f96-988e-b9be88deaf88/hammerhead-sharks_3x4.jpg?width=527&height=702') 


#play music command
@command.command(description="Play Music!", guild=discord.Object(id=serverID here))
async def play(interaction: discord.Interaction, song: str):
    guild = interaction.guild
    tracks = await wavelink.YouTubeTrack.search(query=song, return_first=False)
    Str = ""
    var = "**Choose a track:**"
    backslash = '\n'
    for count, track in enumerate(tracks[:5], start=1):
        Str += f"\n**{count}: **{track.title}"
    embed = discord.Embed(color=0xb000c7)
    embed.add_field(name=var + backslash, value=Str, inline=False)
    await interaction.response.send_message(embed=embed)

    if not guild.voice_client:
        vc: wavelink.Player = guild.voice_client or await interaction.user.voice.channel.connect(cls=wavelink.Player)

    else:
        vc: wavelink.Player = guild.voice_client

    def trackcheck(message):
        return message.author == message.author and message.content.isdigit() and int(message.content) in range(6)
    try:
        message = await bot.wait_for("message", timeout=30, check=trackcheck,)
    except asyncio.TimeoutError:
        await interaction.response.send_message("This command can only be used for 30 seconds!", delete_after=10)

    else:
        if vc.queue.is_empty and not vc.is_playing():
                td_str = str(timedelta(seconds=tracks[int(message.content)-1].length))
                x = td_str.split(':')
                await vc.play(tracks[int(message.content)-1])
                embed=discord.Embed(title="Song", url=f"{track.uri}", color=0xF1C8F6)
                embed.add_field(name="**Now playing:**", value=f"`{tracks[int(message.content)-1]}`", inline=True)
                embed.add_field(name="**Song duration:**", value=f"`{x[1]}:{x[2]}`", inline=True)
                embed.add_field(name="\u200b", value="\u200b", inline=False)
                embed.set_footer(text=f"Requested by: {interaction.user.name}")
                embed.set_image(url = track.thumbnail)
                await interaction.followup.send(embed=embed)
        else:
                await vc.queue.put_wait((tracks[int(message.content)-1]))
                embed = discord.Embed(color=0xF1C8F6)
                embed.add_field(name="**Added to queue:**", value=tracks[int(message.content)-1], inline=False)
                await interaction.followup.send(embed=embed)

    vc.ctx = guild
    vc.loop = False


#skip music command
@command.command(description="Skip the song!", guild=discord.Object(id=serverID here))
async def skip(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    guild = interaction.guild
    vc: wavelink.Player = guild.voice_client
    if not vc.queue.is_empty:
        embed = discord.Embed(color=0xF1C8F6)
        embed.add_field(name="**Skip!**", value="\n Skipped the song!", inline=False)
        await vc.stop()
        await interaction.followup.send(embed=embed)

#resume music command
@command.command(description="Resume the song!", guild=discord.Object(id=serverID here))
async def resume(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    guild = interaction.guild
    vc: wavelink.Player = guild.voice_client
    await vc.set_pause(False)
    embed = discord.Embed(color=0xF1C8F6)
    embed.add_field(name="**Resume!**", value="\n The song has been resumed!", inline=False)
    await interaction.followup.send(embed=embed)

#pause music command
@command.command(description="Pause the song!", guild=discord.Object(id=serverID here))
async def pause(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    guild = interaction.guild
    vc: wavelink.Player = guild.voice_client
    await vc.set_pause(True)
    embed = discord.Embed(color=0xF1C8F6)
    embed.add_field(name="**Pause!**", value="\n The song has been paused!", inline=False)
    await interaction.followup.send(embed=embed)

#stop music command
@command.command(description="Stop the song!", guild=discord.Object(id=serverID here))
async def stop(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    guild = interaction.guild
    vc: wavelink.Player = guild.voice_client
    await vc.stop()
    embed = discord.Embed(color=0xF1C8F6)
    embed.add_field(name="**Stop!**", value="\n The song has been stopped!", inline=False)
    await interaction.followup.send(embed=embed)

#queue music command
@command.command(description="Show the queue!", guild=discord.Object(id=serverID here))
async def queue(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    guild = interaction.guild
    vc: wavelink.Player = guild.voice_client
    queue = vc.queue
    Str = ""
    var = "**Queue:**"
    backslash = '\n'
    for count, track in enumerate(queue[:10], start=1):
        Str += f"\n**{count}: **{track.title}"
    embed = discord.Embed(color=0xF1C8F6)
    embed.add_field(name=var + backslash, value=Str, inline=False)
    await interaction.followup.send(embed=embed)

#now playing music command
@command.command(description="Show the now playing song!", guild=discord.Object(id=serverID here))
async def nowplaying(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    guild = interaction.guild
    vc: wavelink.Player = guild.voice_client
    queue = vc.queue
    Str = ""
    var = "**Now playing:**"
    backslash = '\n'
    for count, track in enumerate(queue[:1], start=1):
        Str += f"\n**{count}: **{track.title}"
    embed = discord.Embed(color=0xF1C8F6)
    embed.add_field(name=var + backslash, value=Str, inline=False)
    await interaction.followup.send(embed=embed)

#leave music command
@command.command(description="Leave the voice channel!", guild=discord.Object(id=serverID here))
async def leave(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    guild = interaction.guild
    vc: wavelink.Player = guild.voice_client
    await vc.disconnect()
    embed = discord.Embed(color=0xF1C8F6)
    embed.add_field(name="**Leave!**", value="\n I have left the voice channel!", inline=False)
    await interaction.followup.send(embed=embed)

#volume music command
@command.command(description="Change the volume!", guild=discord.Object(id=serverID here))
async def volume(interaction: discord.Interaction, volume: int):
    await interaction.response.defer(ephemeral=False)
    guild = interaction.guild
    vc: wavelink.Player = guild.voice_client
    await vc.set_volume(volume)
    embed = discord.Embed(color=0xF1C8F6)
    embed.add_field(name="**Volume!**", value=f"\n The volume has been set to {volume}!", inline=False)
    await interaction.followup.send(embed=embed)


# message counter command
@command.command(description="Message counter!", guild=discord.Object(id=serverID here))
async def messages(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    channel = interaction.channel
    counter = 0
    async for message in channel.history(limit=None):
        if message.author == interaction.user:
            counter += 1
    embed = discord.Embed(color=0x6a4a3a)
    embed.add_field(name="**Messages!**", value=f"\n You have sent {counter} messages!", inline=False)
    await interaction.followup.send(embed=embed)

bot.run(TOKEN)

