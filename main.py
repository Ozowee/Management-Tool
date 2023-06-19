import discord
import json
from discord import app_commands,InteractionType,InteractionResponse
from discord.ui import Button,View
from utils import Check,Add,Remove,ClearQuery,CheckAll,ReadCSV,Setup,SetupCheck,getDB,CheckByName,RemoveByName
from logs import log_info

with open("access.json",'r') as accessFile:
    jsonFile = json.load(accessFile)
    DiscordClientToken = jsonFile['Keys']['DiscordClientToken']
    DiscordGuildID = jsonFile['Keys']['DiscordGuildID']

guild_id = DiscordGuildID

class client(discord.Client):
    async def on_ready(self):
        await self.wait_until_ready()
        await user.sync(guild=discord.Object(id = guild_id))
        log_info("Stock Management Tool succesfully launched!")

client = client(intents=discord.Intents.all())
user = app_commands.CommandTree(client)

async def sku_autocomplete(
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        choices = [element['SKU'] for element in getDB()[str(interaction.user)].find()]
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices if current.lower() in choice.lower()
        ]

@user.command(guild=discord.Object(id=guild_id), name='check_by_sku',description='check stock numbers for desired SKU')
@app_commands.autocomplete(sku=sku_autocomplete)
async def CheckSKU(interaction: discord.Interaction, sku:str):
    user = str(interaction.user)
    view1 = View()

    await interaction.response.send_message("⚙️ Working on it...")
    await interaction.followup.send(embed=Check(sku,user),view=view1)
    log_info(str(interaction.user)+" sprawdził listę")

async def name_autocomplete(
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        choices = [name_find["Info"]["shoe_name"] for name_find in getDB()[str(interaction.user)].find()]
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices if current.lower() in choice.lower()
        ]

@user.command(guild=discord.Object(id=guild_id), name='check_by_name',description='check stock numbers for desired shoe name')
@app_commands.autocomplete(name=name_autocomplete)
async def slashCheckName(interaction: discord.Interaction, name:str):
    user = str(interaction.user)
    view1 = View()

    await interaction.response.send_message("⚙️ Working on it...")
    await interaction.followup.send(embed=CheckByName(user,name),view=view1)
    log_info(str(interaction.user)+" sprawdził listę")


@user.command(guild=discord.Object(id=guild_id),name='add',description="add sneaker to your database")
async def Add_product(interaction: discord.Integration,sku:str,size:str,quantity:int):
    user = str(interaction.user)
    view1 = View()
    await interaction.response.send_message("⚙️ Working on it...")
    await interaction.followup.send(embed=Add(sku,size,quantity,user),view=view1)
    log_info(str(interaction.user)+" uzył komendy ADD")



async def sku_autocomplete_remove(
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        choices = [element['SKU'] for element in getDB()[str(interaction.user)].find()]
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices if current.lower() in choice.lower()
        ]

@user.command(guild=discord.Object(id=guild_id),name='remove_by_sku',description="remove sneaker from your database")
@app_commands.autocomplete(sku=sku_autocomplete_remove)
async def Remove_product(interaction: discord.Integration,sku:str,size:str,quantity:int):
    user = str(interaction.user)
    view1 = View()
    await interaction.response.send_message("⚙️ Working on it...")
    await interaction.followup.send(embed=Remove(sku,size,quantity,user),view=view1)
    log_info(str(interaction.user)+" uzył komendy REMOVE")

@user.command(guild=discord.Object(id=guild_id),name='remove_by_name',description="remove sneaker from your database")
@app_commands.autocomplete(name=name_autocomplete)
async def Remove_product(interaction: discord.Integration,name:str,size:str,quantity:int):
    user = str(interaction.user)
    view1 = View()
    await interaction.response.send_message("⚙️ Working on it...")
    await interaction.followup.send(embed=RemoveByName(name,size,quantity,user),view=view1)
    log_info(str(interaction.user)+" uzył komendy REMOVE")

@user.command(guild=discord.Object(id=guild_id),name='drop',description="drop all records for desired sku")
async def Drop(interaction: discord.Integration,sku:str):
    user = str(interaction.user)
    view1 = View()
    await interaction.response.send_message("⚙️ Working on it...")
    await interaction.followup.send(embed=ClearQuery(sku,user),view=view1)
    log_info(str(interaction.user)+" uzył komendy DROP")


@user.command(guild=discord.Object(id=guild_id),name='checkall',description="check all data in your DB")
async def CheckInfoAll(interaction: discord.Integration):
    user = str(interaction.user)
    page = 0

    class Buttons(discord.ui.View):
        def __init__(self,*,timeout=None):
            self.page = 0
            super().__init__(timeout=timeout)
            

        @discord.ui.button(label='Previous Page',style=discord.ButtonStyle.red)
        async def red_button(self,interaction:discord.Interaction,button:discord.ui.Button):
            self.page -= 1

            await interaction.response.edit_message(content=f"Processing on next page: **{self.page+1}**",embed=None)
            msg = await interaction.original_response()
            await interaction.followup.edit_message(content="",embed=CheckAll(user,self.page),message_id=msg.id)

        @discord.ui.button(label='Next Page',style=discord.ButtonStyle.green)
        async def green_button(self,interaction:discord.Interaction,button:discord.ui.Button):
            self.page += 1
            await interaction.response.edit_message(content=f"Processing on next page: **{self.page+1}**",embed=None)
            msg = await interaction.original_response()
            await interaction.followup.edit_message(content="",embed=CheckAll(user,self.page),message_id=msg.id)

    view1 = Buttons()
    await interaction.response.send_message("⚙️ Working on it...")
    await interaction.followup.send(embed=CheckAll(user,page),view=view1)
    log_info(str(interaction.user)+" uzył komendy CheckAll")


@user.command(guild=discord.Object(id=guild_id),name='addcsv',description="upload your products from csv file!")
async def csv(interaction: discord.Integration,file: discord.Attachment):
    
    user = str(interaction.user)
    view1 = View()
    await interaction.response.send_message("⚙️ Working on it...")
    await interaction.followup.send(embed=ReadCSV(user,file),view=view1)


async def level_autocomplete(
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        choices = ["1","2","3","4","5"]
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices if current.lower() in choice.lower()
        ]
async def type_autocomplete(
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        choices = ["Private","B2B"]
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices if current.lower() in choice.lower()
        ]
async def successfulship_autocomplete(
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        choices = ["Yes","No"]
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices if current.lower() in choice.lower()
        ]
async def quick_ship_autocomplete(
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        choices = ["Yes","No"]
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices if current.lower() in choice.lower()
        ]


@user.command(guild=discord.Object(id=guild_id),name='setup_stockx',description="setup your stockx account info")
@app_commands.autocomplete(level=level_autocomplete,accounttype=type_autocomplete,successful_ship=successfulship_autocomplete,quick_ship=quick_ship_autocomplete)
async def slash(interaction: discord.Integration,level:str,accounttype:str,successful_ship:str,quick_ship:str):
    user = str(interaction.user)
    view1 = View()
    await interaction.response.send_message(embed=Setup(user,level,accounttype,successful_ship,quick_ship),view=view1)
    log_info(str(interaction.user)+" uzył komendy Setup")


@user.command(guild=discord.Object(id=guild_id),name='check_setup',description="check your stockx account settings")
async def slash(interaction: discord.Integration):
    user = str(interaction.user)
    view1 = View()
    await interaction.response.send_message(embed=SetupCheck(user),view=view1)
    log_info(str(interaction.user)+" uzył komendy SetupCheck")


    

client.run(DiscordClientToken)