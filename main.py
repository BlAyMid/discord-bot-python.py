import discord                                                                                                          #Importing the discord library to advertise the bot.(1 line).
from discord.ext import commands                                                                                        #Importing commands from the library module.(2 line).
import sqlite3                                                                                                          #Importing the sqlite3 module to work with the database.(3 line).
import os                                                                                                               #Importing the os module to work with cogs in the future.(4 line).
import config                                                                                                           #Import the config file. The most useful thing.(5 line).

bot = commands.Bot(config.command_prefix, intents=discord.Intents.all())                                                #I don't like to call this variable a client. The bot is a good replacement. All intentions simplify interaction with the bot.(7 line).
bot.remove_command("help")                                                                                              #This is necessary to create your custom "help" command.(8 line).


@bot.event                                                                                                              #This type of function is needed for constant passive startup.(11 line).
async def on_ready():                                                                                                   #The event is needed to launch the function when the bot is launched.(12 line).
    print("Bot connected")                                                                                              #when the bot starts it will write to you about it in the terminal.(13 line).
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Dota 2"))                            #I like the custom status of my bot and the fact that it can use this to play.(14 line).
                                                                                                                        #You can change its activity and game, see the documentation. In normal times, you can put the *prefix* help like this(activity=discord.Game(f"{config.command_prefix}help")).(14 line).
    global base, cur                                                                                                    #I'm going to use this database to implement server statistics.Check it later maybe. (16 line).
    base = sqlite3.connect("bot.db")                                                                                    #Connecting to the database.(17 line).
    cur = base.cursor()                                                                                                 #Creating a cursor inside the database.(18 line).
    if base:                                                                                                            #If the database exists then the connection has been made.(21 line).
        print("Database connected")                                                                                     #We output a message to ourselves to make it calmer.(22 line).

@bot.event
async def on_command_error(ctx, error):                                                                                 #A function for handling some errors. Ctx is an argument for sending information back to the author. Error is an argument passing the error function.(23 line).
    pass
    if isinstance(error, commands.MissingPermissions):                                                                  #If something refers to errors and there are no rights then...(25 line).
        await ctx.send(f"{ctx.author.name}, you don't have enough permissions to execute this command", delete_after=5) #Sending the author directly what he is missing (MissingPermissions). Deletion after 5 seconds, so as not to clutter up the chat.(26 line).
    if isinstance(error, commands.MissingRequiredArgument):                                                             #If something refers to errors and there is no argument then...(27 line).
        await ctx.send(f"{ctx.author.name}, be sure to specify an argument", delete_after=5)                            #Sending the author directly what he is missing (MissingRequiredArgument). Deletion after 5 seconds, so as not to clutter up the chat.(28 line).
    if isinstance(error, commands.MissingRole):                                                                         #If something refers to errors, and then there are no rights (roles)...(29 line).
        await ctx.send(f"{ctx.author.name}, you don't have enough permissions to execute this command", delete_after=5) #Sending the author directly what he is missing (MissingRole). The text is the same as with a lack of permissions, in fact, a lack of role = insufficient permissions. Deletion after 5 seconds, so as not to clutter up the chat.(30 line).

@bot.command()                                                                                                          #The type of function for creating a team in the bot.(32 line).
async def check_cogs(ctx, extension):                                                                                   #Asynchronous function with arguments for checking the operation of cogs.(33 line).
    try:
        bot.load_extension(f"cogs.{extension}")                                                                         #Loading a specific extension(cog).(35 line).
    except commands.ExtensionAlreadyLoaded:                                                                             #The extension is already loaded.(36 line).
        await ctx.send(f"Cog is loaded...{extension}")                                                                  #Then in this case send "Cog is loaded...".(37 line).
    except commands.ExtensionNotFound:                                                                                  #Extension not found.(38 line).
        await ctx.send("Cog not found")                                                                                 #Then in this case send "Cog not found".(39 line).
    else:
        await ctx.send(f"Cog is unloaded...{extension}")
        bot.unload_extension(f"cogs.{extension}")                                                                       #Disable the cog.(42 line).

@bot.command()                                                                                                          #I will prescribe in advance that I will not comment on repeated lines of code now, so look in the code.(all code).
@commands.has_permissions(administrator=True)                                                                           #In order to use this command, you need to have administrator permissions.(45,52...line).
async def load(ctx, extension):                                                                                         #Asynchronous function with arguments for sending back and extending via cogs.(46 line).
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Cogs is loaded...{extension}")


@bot.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):                                                                                       #Asynchronous function with arguments to disable a specific cog.(53 line).
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Cogs is unloaded...{extension}")


@bot.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):                                                                                       #Asynchronous function with arguments for reboot the specific cogs you choose.(60 line).
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Cogs is loaded...{extension}")


for filename in os.listdir("./cogs"):                                                                                   #Search for the /logs folder using the os module.(66 line).
    if filename.endswith(".py"):                                                                                        #Search in this folder for files ending with .py.(67 line).
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(config.token_bot)