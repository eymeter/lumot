import discord
import json
import re

bot = discord.Bot(intents=discord.Intents.all())
token = None
activated = False
customization = {
    "name": "lumot",
    "ephemerality": False,
    "staff": []
}

with open('config.json', 'r') as file:
    data = json.load(file)
    token = data['token']

@bot.event
async def on_ready():
    print(f"Using Bot: {bot.user.name}")
    print("Use activate command to activate.")
    print("Use edit command to customize.")

@bot.event
async def on_message(message):
    if not activated:
        return
    
    if message.author.bot:
        return

    pattern = re.compile(r"(i'm|im|i\s*am)\s*(.+)", re.IGNORECASE)
    match = re.search(pattern, message.content)
    
    if match:
        print("Detected.")
        
        if customization["ephemerality"] == False:
            await message.channel.send(f"Hello {match.group(2)}, I am {customization['name']}!")
        else:
            await message.author.send(f"Hello {match.group(2)}, I am {customization['name']}!")

            

@bot.command(description="Activates Lumot. Edit it first.")
async def activate(ctx):
    global activated
    activated = True
    await ctx.respond("Activated bot!", ephemeral=True)

@bot.command(description="Lumot Commands")
async def help(ctx):
    await ctx.respond("Lumot Bot Commands:\n/activate - Activates the bot\n/deactivate - Deactivates the bot\n/help - Gives you the commands\n/edit - Customize your Lumot.", ephemeral=True)

@bot.command(description="Deactivate Lumot.")
async def deactivate(ctx):
    global activated
    activated = False
    await ctx.respond("Deactivated the bot!", ephemeral=True)

@bot.command(description="Customize Lumot.")
async def edit(ctx, name: discord.Option(str), ephemerality: discord.Option(bool)):
    if not name and ephemerality:
        await ctx.respond("Missing values!", ephemeral=True)
        return
    if ctx.author != ctx.guild.owner:
        if customization["staff"].clear() == customization["staff"]:
            await ctx.respond("The owner of this server has not defined staff ranks that can use this bot, or you are just not a staff.", ephemeral=True)
            return
        else:
            for role in ctx.author.roles:
              if not role in customization["staff"]:
                  await ctx.respond("You have to have a defined staff rank to use this!",ephemeral=True)

    customization["name"] == name
    customization["ephemerality"] == ephemerality
    await ctx.respond("Modification successful", ephemeral=True)

@bot.command(description="Add a staff role name that can modify Lumot.")
async def addstaff(ctx, rankname: discord.Option(str)):
    if not rankname:
        await ctx.respond("You have to enter a rank name.", ephemeral=True)
        return

    if ctx.author != ctx.guild.owner:
        await ctx.respond("You have to be the owner to use this command.", ephemeral=True)
        return
    
    customization["staff"].append(rankname)
    await ctx.respond(f"Successfully added: {rankname}", ephemeral=True)

@bot.command(description="Remove a staff role name that can modify Lumot.")
async def delstaff(ctx, rankname: discord.Option(str)):
    if not rankname:
        await ctx.respond("You have to enter a rank name.", ephemeral=True)
        return

    if ctx.author != ctx.guild.owner:
        await ctx.respond("You have to be the owner to use this command.", ephemeral=True)
        return
    
    customization["staff"].remove(rankname)
    await ctx.respond(f"Successfully deleted: {rankname}", ephemeral=True)

bot.run(token)
