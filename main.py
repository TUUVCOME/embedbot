import asyncio
from urllib import response
from asyncio import sleep
import disnake
from tabulate import tabulate
import datetime
from config import *

from disnake.ext import commands

bot = commands.Bot(
    command_prefix=PREFIX,
    sync_commands_debug=True,
)

@bot.event
async def on_ready():
  guilds = len(bot.guilds)
  info = "/"
  print("[{}] Бот готов к работе.".format(info)) #в командную строку идёт инфа о запуске
  while True:
    await bot.change_presence(status = disnake.Status.online, activity = disnake.Activity(name = f'/help', type = disnake.ActivityType.playing)) #Идёт инфа о команде помощи (префикс изменить)
    await asyncio.sleep(15)
    await bot.change_presence(status = disnake.Status.online, activity = disnake.Activity(name = f'за {len(bot.guilds)} серверами', type = disnake.ActivityType.watching)) #Инфа о количестве серверов, на котором находится бот.
    await asyncio.sleep(15)
    members = 0
    for guild in bot.guilds:
      for member in guild.members:
        members += 1
    await bot.change_presence(status = disnake.Status.idle, activity = disnake.Activity(name = f'за {members} участниками', type = disnake.ActivityType.watching)) #Общее количество участников, за которыми следит бот (Находятся на серверах)
    await asyncio.sleep(15)

@bot.slash_command(description="Пингануть бота")
async def ping(inter):
  ping_start = datetime.datetime.now()
  ping_end = datetime.datetime.now()
  response_time = ping_end - ping_start
  response_time_in_ms = response_time.total_seconds() * 1000
  await inter.response.send_message(f"Бот ответил за: {response_time_in_ms} мс")

@bot.slash_command(description="Создаёт EMBED")
@commands.has_guild_permissions(administrator=True)
async def createembed(inter, name: str, description: str, author: str, footer: str = " ", urlphoto: str = "https://cdn.discordapp.com/attachments/1020625502064607232/1021760499899187250/standard_1.gif"):
    embed = disnake.Embed(
        title= name,
        description=description,
        color=disnake.Colour.dark_teal(),
    )

    embed.set_author(
    name=author,
    )

    embed.set_footer(
    text=footer,
    )

    embed.set_image(url=urlphoto)

    await inter.send(embed=embed)

@bot.slash_command(description="Показывает информацию о сервере.")
async def server(inter):
    owner = await inter.guild.fetch_member(inter.guild.owner_id) if inter.guild.owner_id else None
    owner_mention = owner.mention if owner else "Unknown"

    embed2 = disnake.Embed(
        title = "Информация о сервере.",
        description = f"Название сервера: {inter.guild.name}\nУчастников: {inter.guild.member_count}\nВладелец: {owner_mention}\n",
        color = disnake.Colour.dark_teal(),
    )

    embed2.set_image(inter.guild.banner)
    embed2.set_thumbnail(inter.guild.icon)
    await inter.send(embed=embed2)

@bot.slash_command(description="Показывает информацию о человеке.")
async def infop(inter, ping: disnake.Member):
    created_at = ping.created_at.strftime("%d.%m.%Y")
    member = disnake.Embed(
        title="Информация о человеке.",
        description=f"Настоящее имя: {ping.name}\nВысвеченное имя: {ping.display_name}\nКогда аккаунт был создан: {created_at}",
        color=disnake.Colour.dark_teal(),
    )
    member.set_image(url=ping.avatar.url)
    await inter.send(embed=member)

@bot.slash_command(description="Показывает все доступные команды в боте.")
async def help(inter):
    embed1 = disnake.Embed(
        title= "Команды и их описание",
        description= "Описание функций\n\n- /createembed позволяет сделать EMBED сообщение.\n\n- /server показывает информацию о сервере.\n\n- /help показывает информацию о командах и их назначении.",
        color= disnake.Colour.dark_teal(),
    )

    await inter.send(embed=embed1)


bot.run(TOKEN)
