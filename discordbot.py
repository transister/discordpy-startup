
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

Streamer = {
    "UChAnqc_AY5_I3Px5dig3X1Q": [
        "戌神ころね",
        "https://yt3.ggpht.com/ytc/AAUvwnimjdERaJDGopfH8UaB0r9tr_p8uyuEWWyYVkAd5Q=s88-c-k-c0x00ffffff-no-rj",
        "Hololive"
    ],
    "UCCzUftO8KOVkV4wQG1vkUvg": [
        "宝鐘マリン",
        "https://yt3.ggpht.com/ytc/AAUvwnjPuFWs42Vx2yIhK7z1w4L-e1GIpHn_5R1uknbS=s88-c-k-c0x00ffffff-no-rj",
        "Hololive"
    ],
    "UC1DCedRgGHBdm81E1llLhOQ": [
        "兎田ぺこら",
        "https://yt3.ggpht.com/ytc/AAUvwnjvkyPGzOmEXZ34mEFPlwMKTbCDl1ZkQ_HkxY-O5Q=s88-c-k-c0x00ffffff-no-rj",
        "Hololive"
    ],
    "UC5CwaMl1eIgY8h02uZw7u8A": [
        "星街すいせい",
        "https://yt3.ggpht.com/ytc/AAUvwnjdAl5rn3IjWzl55_0-skvKced7znPZRuPC5xLB=s88-c-k-c0x00ffffff-no-rj",
        "Hololive"
    ],
    "UCdn5BQ06XqgXoAxIhbqw5Rg": [
        "白上フブキ",
        "https://yt3.ggpht.com/ytc/AAUvwniEQsukDZoC-l8zchhRzpraxcH7Fyq9amrj2980Aw=s88-c-k-c0x00ffffff-no-rj",
        "Hololive"
    ],
    "UC1opHUrw8rvnsadT-iGp7Cg": [
        "湊あくあ",
        "https://yt3.ggpht.com/ytc/AAUvwngM9Jmc29dvbOY43w7RWFbOZLU4tGtOkEwtt-g7PA=s88-c-k-c0x00ffffff-no-rj",
        "Hololive"
    ],
    "UCvzGlP9oQwU--Y0r9id_jnA": [
        "大空スバル",
        "https://yt3.ggpht.com/ytc/AAUvwniCgko15I_x5bYWm0G2vnf5hZqD5hLOtLEDw0Na=s88-c-k-c0x00ffffff-no-rj",
        "Hololive"
    ],
    "UCQ0UDLQCjY0rmuxCDE38FGg": [
        "夏色まつり",
        "https://yt3.ggpht.com/ytc/AAUvwni8cjtyc08E7rocvO9_gR1b5BhO1O6O1VreDxMW=s176-c-k-c0x00ffffff-no-rj",
        "Hololive"
    ],
    "UCdyqAaZDKHXg4Ahi7VENThQ": [
        "白銀ノエル",
        "https://yt3.ggpht.com/ytc/AAUvwnijLF2X1YBVQo3rClt7ub29cYM7OzpmRmliaGbw=s88-c-k-c0x00ffffff-no-rj",
        "Hololive"
    ],
    "UCajhBT4nMrg3DLS-bLL2RCg": [
        "天野ピカミィ",
        "https://yt3.ggpht.com/ytc/AAUvwnjfPSGerlUwIcpujHs9De6IZYRuH_H2v1heW48b=s88-c-k-c0x00ffffff-no-rj",
        "VOMS"
    ],
    "UC3vzVK_N_SUVKqbX69L_X4g": [
        "緋笠トモシカ",
        "https://yt3.ggpht.com/ytc/AAUvwnhSyw72yPqDbQMSNN6RBJ0nAHa7wmMl-5etY8Bs=s88-c-k-c0x00ffffff-no-rj",
        "VOMS"
    ],
} #配信者のチャンネルID, 配信者名, アイコン画像のURLのリスト
webhook_url = "https://discord.com/api/webhooks/814627315048906802/mast3_S-vt3V0R_fwVhzgrKmWD3H4fYAD9XZQiTuSWKFEupE2aRou24yWiYM6Jtksdjd" #配信開始
webhook_url_yotei = {"Hololive": ['https://discord.com/api/webhooks/814626994296979456/IisxTTZqQXTvM569Z4TVFYSEqdxEriwt_M9XX_IEEiDsNNqG991tyZr94VOOfjAsBpeJ'],
                     "VOMS": ['https://discord.com/api/webhooks/838761972651655208/Kf3CGJ4ILSOgnQSm-gSEvtck2-Ug7clLCoQNr5HANyELXjxgffAseMr_j9qjiMxmvi0S']
                    }#配信予定
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
    return (str(time[0]) + "/" + str(time[1]).zfill(2) + "/" + str(time[2]).zfill(2) + " " + str(time[3]).zfill(2) + ":" + str(time[4]).zfill(2))

@tasks.loop(hours=1)
async def get_information():
    tmp = copy.copy(broadcast_data)
    now_time = datetime.now() + timedelta(hours=9)
    api_now = 0 #現在どのYouTube APIを使っているかを記録
    for idol in Streamer:
        api_link = "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=" + idol + "&key=" + YOUTUBE_API_KEY[api_now] + "&eventType=upcoming&type=video"
        api_now = (api_now + 1)  #apiを1つずらす
        if(api_now >= 10):
            api_now = 0
        aaa = requests.get(api_link)
        time.sleep(1)
        v_data = json.loads(aaa.text)
        try:
            for item in v_data['items']:#各配信予定動画データに関して
                broadcast_data[item['id']['videoId']] = {'channelId':item['snippet']['channelId']} #channelIDを格納
            for video in broadcast_data:
                try:
                    a = broadcast_data[video]['starttime'] #既にbroadcast_dataにstarttimeがあるかチェック
                except KeyError:#なかったら
                    aaaa = requests.get("https://www.googleapis.com/youtube/v3/videos?part=liveStreamingDetails&id=" + video + "&key=" + YOUTUBE_API_KEY[api_now])
                    time.sleep(1)
                    api_now = (api_now + 1) #apiを1つずらす
                    if(api_now >= 10):
                        api_now = 0
                    vd = json.loads(aaaa.text)
                    print(vd)
                    broadcast_data[video]['starttime'] = vd['items'][0]['liveStreamingDetails']['scheduledStartTime']
        except KeyError: #配信予定がなくて403が出た
            continue
    for vi in list(broadcast_data):
        if(not(vi in tmp)):
            print(broadcast_data[vi])
            try:
                sd_time = datetime.strptime(broadcast_data[vi]['starttime'], '%Y-%m-%dT%H:%M:%SZ') #配信スタート時間をdatetime型で保管
                sd_time += timedelta(hours=9)
                if((now_time < sd_time) and ((now_time + timedelta(days=180)) > sd_time)):
                    post_broadcast_schedule(broadcast_data[vi]['channelId'], vi, broadcast_data[vi]['starttime'])
            except KeyError:
                continue

@tasks.loop(seconds=60)
async def check_schedule():
    now_time = datetime.now() + timedelta(hours=9)
    for bd in list(broadcast_data):
        try:
            sd_time = datetime.strptime(broadcast_data[bd]['starttime'], '%Y-%m-%dT%H:%M:%SZ') #配信スタート時間をdatetime型で保管
            sd_time += timedelta(hours=9)
            if((sd_time + timedelta(minutes=3)) >= now_time >= sd_time):#今の方が配信開始時刻よりも後だったら
                post_to_discord(broadcast_data[bd]['channelId'], bd) #ツイート
        except KeyError:
            continue

def post_to_discord(userId, videoId):
    haishin_url = "https://www.youtube.com/watch?v=" + videoId #配信URL
    content = "配信中！\n" + haishin_url #Discordに投稿される文章
    main_content = {
        "username": Streamer[userId][0], #配信者名
        "avatar_url": Streamer[userId][1], #アイコン
        "content": content #文章
    }
    requests.post(webhook_url, main_content) #Discordに送信
    broadcast_data.pop(videoId)
            
def post_broadcast_schedule(userId, videoId, starttime):
    st = starttime.replace('T', ' ')
    sst = st.replace('Z', '')
    ssst = replace_JST(sst)
    haishin_url = "https://www.youtube.com/watch?v=" + videoId #配信URL
    content = ssst + "に配信予定\n" + haishin_url #Discordに投稿される文章
    main_content = {
        "username": Streamer[userId][0], #配信者名
        "avatar_url": Streamer[userId][1], #アイコン
        "content": content #文章
    }
    requests.post(webhook_url_yotei[Streamer[userId][2]][0], main_content) #Discordに送信
    

# 起動時に動作する処理
@bot.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    broadcast_data = {} #配信予定のデータを格納
    tmp = {}
    get_information.start()
    time.sleep(120)
    check_schedule.start()
    
@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format()) + "エラー\n"
    await ctx.send(error_msg)
    
@bot.command()
async def ping(ctx):
    await ctx.send("pong\n")


bot.run(token)




