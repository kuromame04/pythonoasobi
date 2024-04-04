import requests
import urllib
import discord
import json
from discord.ext import commands
import discord.app_commands
from discord import Webhook
from discord.utils import get
from discord.ext import tasks
import aiohttp
import ast
import time
from bs4 import BeautifulSoup
# 昔書いたこーどだからあんまり見ないでほしいな
TOKEN="MTE1MDc5MDI3NTcxMTYzMTQ5Mg.GqppS5.xinOuemeOFiLw1_rYxKMpR_XWpSZogB_PrUXcA"
client=discord.Client(intents=discord.Intents.all())
cmd=discord.app_commands.CommandTree(client)
# 今度作る翻訳機能にいる奴
API_KEY="e00e4bf9-a28a-5e60-25d8-3ef004714fcb:fx"

channelid={}
banlist=[]
webhooks={} # webhookのアドレスを置いておく場所
enable=None
channelname=[] # チャンネル名
starttime={} # TO機能の時間置き場
timeadd=[]
# Webhook送るやつ
async def sendwebhook(msg,whurl):
    try:                            
        if msg.attachments:
            async with aiohttp.ClientSession() as session:
                webhook=Webhook.from_url(whurl,session=session)
                await webhook.send(
                content=msg.content,
                username=str(msg.author)+f" from {msg.guild.name}",
                avatar_url=str(msg.author.avatar),
                files=[await i.to_file() for i in msg.attachments]
                )
        else:
            async with aiohttp.ClientSession() as session:
                webhook=Webhook.from_url(whurl,session=session)
                await webhook.send(
                content=msg.content,
                username=str(msg.author)+f" from {msg.guild.name}",
                avatar_url=str(msg.author.avatar),
                )
    except discord.app_commands.errors.CommandInvokeError:
        await msg.channel.send(f"恐らくWHが上限{e}")
        
async def sendwebhook2(msg,whurl,userid):
    try:                            
        if msg.attachments:
            async with aiohttp.ClientSession() as session:
                webhook=Webhook.from_url(whurl,session=session)
                await webhook.send(
                content="_リプライ "+f"<@{userid}>",
                username=str(msg.author)+f" from {msg.guild.name}",
                avatar_url=str(msg.author.avatar),
                files=[await i.to_file() for i in msg.attachments]
                )
        else:
            async with aiohttp.ClientSession() as session:
                webhook=Webhook.from_url(whurl,session=session)
                await webhook.send(
                content="_リプライ "+f"<@{userid}>",
                username=str(msg.author)+f" from {msg.guild.name}",
                avatar_url=str(msg.author.avatar),
                )
    except discord.app_commands.errors.CommandInvokeError:
        await msg.channel.send(f"恐らくWHが上限{e}")
@cmd.command(
    name="join",
    description="グロチャに入室"
)
# 入室してwhurlの取得
async def join(ctx:discord.Integration,channel:discord.TextChannel):
    await ctx.response.defer()
    global enable; global channelname; global webhooks
    enable=True
    channelname.append(channel)
    print(channelname)
    webhook = await ctx.channel.create_webhook(name="MAMEchat")
    webhooks[ctx.guild.id]=webhook.url
    await ctx.followup.send("完了✅")
@cmd.command(
    name="exit",
    description="退出するやつ 実行したチャンネルで必ず行ってください。"
)
async def exit(ctx:discord.Integration):
    await ctx.response.defer()
    global enable; global webhooks
    enable=False
    del webhooks[ctx.guild.id]
    await ctx.followup.send("完了✅")

@cmd.command(
    name="ban",
    description="出禁に出来ん"
)
async def ban(ctx:discord.Integration,menber:discord.Member):
    print(menber)
    global banlist
    banlist.append(str(menber))
    await ctx.response.send_message(f"userをBANしました。{menber}")
@cmd.command(
    name="banoff",
    description="挽回所"
)
async def banoff(ctx:discord.Integration,menber:discord.Member):
    global banlist
    if str(menber) in banlist:
        await ctx.response.send_message(f"挽回所するよ{menber}")
        if menber in banlist:
            for i in banlist:
                if banlist[i]==menber:
                    del banlist[i]
                    break
        else:
            await ctx.response.send_message(f"こいつはまだBANしていません。{menber}")
        
@cmd.command(
    name="timeout",
    description="タイムアウト"
)
async def timeout(ctx:discord.Integration,menber:discord.Member,timehour:int,timemin:int,timesec:int):
    global timeadd
    timeadd[str(menber)]=timehour*3600+timemin*60+timesec
    global starttime
    starttime[str(menber)]=time.time()
    await ctx.response.send_message(f"こいつをタイムアウトしました: {menber} 時間:{timehour}時間,{timemin}分,{timesec}秒")
    
@client.event
async def on_message(msg: discord.Message):
    now=time.time()
    print(msg.id)
    print(f"送信者{msg.author.name}")
    # yahoonewsbot用のやつ
    if msg.content=="joinnews":
        if not msg.channel.id in channelid:
            channelid[msg.channel.id]=msg.channel.id
            print(channelid[msg.channel.id])
    else:
        pass
    if  msg.author.bot:
        return
    if enable == False:
        return
    if  msg.channel.name in str(channelname):
        print("OK")
        if not  "_グローバルチャット" in msg.channel.name: # チャンネル名の処理
            await msg.channel.edit(name=msg.channel.name+"_グローバルチャット")
        if  msg.author.name in banlist:
            await msg.channel.send(f"お前さんの発言権ないよ(笑) <@{msg.author.id}>")
            await msg.delete()
            print("BANED")
        elif msg.author.name in timeadd: 
            print(f"TO{msg.author.name}")
            if starttime[msg.author.name]+timeadd[msg.author.name] >= now:
                now=starttime[msg.author.name]+timeadd[msg.author.name]-now
                await msg.channel.send(f"お前さんの発言権ないよ(笑) <@{msg.author.id}>完了まで,{now}")  
            elif starttime[msg.author.name]+timeadd[msg.author.name] <= now:
                print(f"TO終わり{msg.author.name}"); del starttime[msg.author.name]; del timeadd[msg.author.name]
                await msg.channel.send(f"タイムアウト解除されたぞ良かったな <@{msg.author.name}>")
        elif msg.content[:6] in "reply ":            # 返信機能を実装したい    なんか違うなぁ
            if len(msg.content)>=30:
                msg.channel.send(f"文法ミス;{msg.content}")
            else:
                user=msg.content[6:30]
                await msg.delete(); print(f"reply:{user}")
                for whurl in webhooks.values():
                    await sendwebhook2(msg,whurl,userid=user)
        elif msg.content[:6] in "remove":
            message=msg.content
        else:
            await msg.delete()
            for whurl in webhooks.values():
                await sendwebhook(msg,whurl)
            print(f"wh作成完了✅:{msg.content}")  
        return
    
@client.event
async def on_ready():
    await cmd.sync()
    loop.start()
    
@tasks.loop(minutes=60)
async def loop():
    global channelid
    filename ="yahoonewslist.txt"
    filename2="yahoolinklist.txt"
    load_url = "https://yahoo.co.jp"
    html = requests.get(load_url)
    html.encoding = html.apparent_encoding
# 美しいスープでHTMLを解析(htmlパース)
    soup = BeautifulSoup(html.text,'html.parser')
# 開く
    f = open(filename, mode="w",encoding="utf-8")
    f2 =open(filename2,mode="w",encoding="utf-8")
    topic = soup.find_all("a")
    for element in topic:
        url = element.get("href")
        link_url = urllib.parse.urljoin(load_url, url) 
        f.write(element.text) # 書き込み
        f.write("\n")
        f2.write(link_url)
        f2.write("\n")
# 適当正規表現 エラー対策のためUTF-8
    f2=open(filename2,mode="r",encoding="utf-8")
    linkline=f2.readlines()
    factlinkline=linkline[30:37]
    print(factlinkline)
    f2.close()
    f=open(filename,mode="r",encoding="utf-8")
    newsline=f.readlines()
    factnewsline=newsline[30:38]
    print(factnewsline)
    f.close()
    embed=discord.Embed(
        title="ニュース",
        color=0x00ff00,#<=緑色
        description="1時間に一回NEWSを提供"
    )
    embed.add_field(name=factnewsline[0],value=factlinkline[0])
    embed.add_field(name=factnewsline[1],value=factlinkline[1])
    embed.add_field(name=factnewsline[2],value=factlinkline[2])
    embed.add_field(name=factnewsline[3],value=factlinkline[3])
    embed.add_field(name=factnewsline[4],value=factlinkline[4])
    for i in channelid.values():
        try:
            print(type(i)is str)
            channel=client.get_channel(i)
            await channel.send(embed=embed)
        except:
            print("このチャンネルないみたい")
            continue

client.run(TOKEN)


    
    
    



