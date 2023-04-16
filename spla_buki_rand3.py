import discord
from discord.commands import Option
import csv
import random
import sys
import asyncio
import os
import subprocess

#https://qiita.com/melonade/items/25c038e8e4e6800aa639

bot = discord.Bot()

with open('buki3.csv',encoding="utf-8") as f:
    reader = csv.reader(f)
    all_list = [row for row in reader]

WEAPONS = {i[3] for i in all_list}
SUBS = {i[1] for i in all_list}
SPECIALS = {i[2] for i in all_list}

async def get_weapons(ctx):
    return [weapon for weapon in WEAPONS if weapon.startswith(ctx.value)]

async def get_subs(ctx):
    return [sub for sub in SUBS if sub.startswith(ctx.value)]

async def get_specials(ctx):
    return [special for special in SPECIALS if special.startswith(ctx.value)]

@bot.slash_command(description="ブキ種を選択しないと全てのブキから選ばれます")
async def buki(
    ctx,
    ブキ種: Option(str, 'ブキ種で絞れます', autocomplete=get_weapons, required=False, default=''),
    サブ: Option(str, 'サブで絞れます', autocomplete=get_subs, required=False, default=''),
    スペシャル: Option(str, 'スペシャルで絞れます', autocomplete=get_specials, required=False, default='')
):
    #await ctx.respond(f'{weapon}が選択されました')
    alist = [i for i in all_list if (i[3]==ブキ種)] if ブキ種!="" else all_list
    blist = [i for i in alist if (i[1]==サブ)] if サブ!="" else alist
    clist = [i[0] for i in blist if (i[2]==スペシャル)] if スペシャル!="" else [i[0] for i in blist]
    if clist == []:
        dlist = [i[0] for i in all_list]
        await ctx.respond(f'該当するブキはありませんでした。全ブキから：**__{random.choice(dlist)}__**', delete_after=90)
    else:
        await ctx.respond(f'**__{random.choice(clist)}__**(該当数:{len(clist)})', delete_after=90)

TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)