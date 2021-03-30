
from discord.ext import commands
from discord.ext import tasks
import discord
import os
import traceback
import requests
import time
import json
import copy
from datetime import datetime, timedelta, timezone

Hololive = {
    "UChAnqc_AY5_I3Px5dig3X1Q": [
        "戌神ころね",
        "https://yt3.ggpht.com/ytc/AAUvwnimjdERaJDGopfH8UaB0r9tr_p8uyuEWWyYVkAd5Q=s88-c-k-c0x00ffffff-no-rj"
    ],
    "UCCzUftO8KOVkV4wQG1vkUvg": [
        "宝鐘マリン",
        "https://yt3.ggpht.com/ytc/AAUvwnjPuFWs42Vx2yIhK7z1w4L-e1GIpHn_5R1uknbS=s88-c-k-c0x00ffffff-no-rj"
    ],
    "UC1DCedRgGHBdm81E1llLhOQ": [
        "兎田ぺこら",
        "https://yt3.ggpht.com/ytc/AAUvwnjvkyPGzOmEXZ34mEFPlwMKTbCDl1ZkQ_HkxY-O5Q=s88-c-k-c0x00ffffff-no-rj"
    ],
    "UC5CwaMl1eIgY8h02uZw7u8A": [
        "星街すいせい",
        "https://yt3.ggpht.com/ytc/AAUvwnjdAl5rn3IjWzl55_0-skvKced7znPZRuPC5xLB=s88-c-k-c0x00ffffff-no-rj"
    ],
    "UCdn5BQ06XqgXoAxIhbqw5Rg": [
        "白上フブキ",
        "https://yt3.ggpht.com/ytc/AAUvwniEQsukDZoC-l8zchhRzpraxcH7Fyq9amrj2980Aw=s88-c-k-c0x00ffffff-no-rj"
    ],
    "UC1opHUrw8rvnsadT-iGp7Cg": [
        "湊あくあ",
        "https://yt3.ggpht.com/ytc/AAUvwngM9Jmc29dvbOY43w7RWFbOZLU4tGtOkEwtt-g7PA=s88-c-k-c0x00ffffff-no-rj"
    ],
    "UCvzGlP9oQwU--Y0r9id_jnA": [
        "大空スバル",
        "https://yt3.ggpht.com/ytc/AAUvwniCgko15I_x5bYWm0G2vnf5hZqD5hLOtLEDw0Na=s88-c-k-c0x00ffffff-no-rj"
    ],
    "UCQ0UDLQCjY0rmuxCDE38FGg": [
        "夏色まつり",
        "https://yt3.ggpht.com/ytc/AAUvwni8cjtyc08E7rocvO9_gR1b5BhO1O6O1VreDxMW=s176-c-k-c0x00ffffff-no-rj"
    ],
    "UCdyqAaZDKHXg4Ahi7VENThQ": [
        "白銀ノエル",
        "https://yt3.ggpht.com/ytc/AAUvwnijLF2X1YBVQo3rClt7ub29cYM7OzpmRmliaGbw=s88-c-k-c0x00ffffff-no-rj"
    ],
    "UCajhBT4nMrg3DLS-bLL2RCg": [
        "天野ピカミィ",
        "https://yt3.ggpht.com/ytc/AAUvwnjfPSGerlUwIcpujHs9De6IZYRuH_H2v1heW48b=s88-c-k-c0x00ffffff-no-rj"
    ],
    "UC3vzVK_N_SUVKqbX69L_X4g": [
        "緋笠トモシカ",
        "https://yt3.ggpht.com/ytc/AAUvwnhSyw72yPqDbQMSNN6RBJ0nAHa7wmMl-5etY8Bs=s88-c-k-c0x00ffffff-no-rj"
    ],
} #配信者のチャンネルID, 配信者名, アイコン画像のURLのリスト
webhook_url_Hololive = 'https://discord.com/api/webhooks/814627315048906802/mast3_S-vt3V0R_fwVhzgrKmWD3H4fYAD9XZQiTuSWKFEupE2aRou24yWiYM6Jtksdjd' #ホロライブ配信開始
webhook_url_Hololive_yotei = 'https://discord.com/api/webhooks/814626994296979456/IisxTTZqQXTvM569Z4TVFYSEqdxEriwt_M9XX_IEEiDsNNqG991tyZr94VOOfjAsBpeJ' #ホロライブ配信予定
broadcast_data = {} #配信予定のデータを格納
tmp = {}

YOUTUBE_API_KEY = ["AIzaSyD1v807Gio9K4GVjKVjdRVgw0_kMip7z8Y","AIzaSyDYbIaTUq3yipQrOHncHhHjKDxVRZDZE5s","AIzaSyACZwmWNAyT5w2Spzm3_61Rw0GiH33utRU","AIzaSyDR5AhxSeIKsvIMJDqhsMTfh_fvo6DLR3o","AIzaSyCbmIAmPpKnLMrM2vEGg8MoqTyHgTVMAOM","AIzaSyDE9i7mg0ruYaISi8MPVH-tMd8LE4B_kNg","AIzaSyA2x_6iFWJHDlxjYAq4-ekMz9lHnlgZcAA","AIzaSyDi-PwXFxb9XuQN-SvSWc9fO0vMdWzCaAI","AIzaSyCqydt1Dlwdx-J9FVt8GGWjEJKtj_zYe9I","AIzaSyAxSNNHLlW8S4t4t52azdYaXsUc2Y5nxG0"]

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

def replace_JST(s):
    a = s.split("-")
    u = a[2].split(" ")
    t = u[1].split(":")
    time = [int(a[0]), int(a[1]), int(u[0]), int(t[0]), int(t[1]), int(t[2])]
    if(time[3] >= 15):
      time[2] += 1
      time[3] = time[3] + 9 - 24
    else:
      time[3] += 9
    return (str(time[0]) + "/" + str(time[1]).zfill(2) + "/" + str(time[2]).zfill(2) + " " + str(time[3]).zfill(2) + "-" + str(time[4]).zfill(2) + "-" + str(time[5]).zfill(2))


# 起動時に動作する処理
@bot.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    broadcast_data = {} #配信予定のデータを格納
    tmp = {}
    #get_information.start()
    #time.sleep(120)
    #check_schedule.start()
    
@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format()) + "エラー\n"
    await ctx.send(error_msg)
    
@bot.command()
async def ping(ctx):
    await ctx.send("pong\n")


bot.run(token)




