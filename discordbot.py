

from discord.ext import commands
from discord.ext import tasks
import tweepy
import discord
import os
import traceback
import requests
import time
import json
import copy
from datetime import datetime, timedelta, timezone
import re
import sys, codecs

Streamer = {
    "UChAnqc_AY5_I3Px5dig3X1Q": [
        "戌神ころね",
        "https://yt3.ggpht.com/ytc/AAUvwnimjdERaJDGopfH8UaB0r9tr_p8uyuEWWyYVkAd5Q=s88-c-k-c0x00ffffff-no-rj",
        "Hololive",
        "戌神ころね"
    ],
    "UCCzUftO8KOVkV4wQG1vkUvg": [
        "宝鐘マリン",
        "https://yt3.ggpht.com/ytc/AAUvwnjPuFWs42Vx2yIhK7z1w4L-e1GIpHn_5R1uknbS=s88-c-k-c0x00ffffff-no-rj",
        "Hololive",
        "宝鐘マリン"
    ],
    "UC1DCedRgGHBdm81E1llLhOQ": [
        "兎田ぺこら",
        "https://yt3.ggpht.com/ytc/AAUvwnjvkyPGzOmEXZ34mEFPlwMKTbCDl1ZkQ_HkxY-O5Q=s88-c-k-c0x00ffffff-no-rj",
        "Hololive",
        "兎田ぺこら"
    ],
    "UC5CwaMl1eIgY8h02uZw7u8A": [
        "星街すいせい",
        "https://yt3.ggpht.com/ytc/AAUvwnjdAl5rn3IjWzl55_0-skvKced7znPZRuPC5xLB=s88-c-k-c0x00ffffff-no-rj",
        "Hololive",
        "星街すいせい"
    ],
    "UCdn5BQ06XqgXoAxIhbqw5Rg": [
        "白上フブキ",
        "https://yt3.ggpht.com/ytc/AAUvwniEQsukDZoC-l8zchhRzpraxcH7Fyq9amrj2980Aw=s88-c-k-c0x00ffffff-no-rj",
        "Hololive",
        "白上フブキ"
    ],
    "UC1opHUrw8rvnsadT-iGp7Cg": [
        "湊あくあ",
        "https://yt3.ggpht.com/ytc/AAUvwngM9Jmc29dvbOY43w7RWFbOZLU4tGtOkEwtt-g7PA=s88-c-k-c0x00ffffff-no-rj",
        "Hololive",
        "湊あくあ"
    ],
    "UCvzGlP9oQwU--Y0r9id_jnA": [
        "大空スバル",
        "https://yt3.ggpht.com/ytc/AAUvwniCgko15I_x5bYWm0G2vnf5hZqD5hLOtLEDw0Na=s88-c-k-c0x00ffffff-no-rj",
        "Hololive",
        "大空スバル"
    ],
    "UCt30jJgChL8qeT9VPadidSw": [
        "しぐれうい",
        "https://yt3.ggpht.com/ytc/AAUvwniuo8k4PtT6z_AsalVyQbz6BUpTebJVt22kZDw8Ig=s88-c-k-c0x00ffffff-no-rj",
        "Hololive",
        "しぐれうい"
    ],
    "UCQ0UDLQCjY0rmuxCDE38FGg": [
        "夏色まつり",
        "https://yt3.ggpht.com/ytc/AAUvwni8cjtyc08E7rocvO9_gR1b5BhO1O6O1VreDxMW=s176-c-k-c0x00ffffff-no-rj",
        "Hololive",
        "夏色まつり"
    ],
    "UCdyqAaZDKHXg4Ahi7VENThQ": [
        "白銀ノエル",
        "https://yt3.ggpht.com/ytc/AAUvwnijLF2X1YBVQo3rClt7ub29cYM7OzpmRmliaGbw=s88-c-k-c0x00ffffff-no-rj",
        "Hololive",
        "白銀ノエル"
    ],
    "UCajhBT4nMrg3DLS-bLL2RCg": [
        "天野ピカミィ",
        "https://yt3.ggpht.com/ytc/AAUvwnjfPSGerlUwIcpujHs9De6IZYRuH_H2v1heW48b=s88-c-k-c0x00ffffff-no-rj",
        "VOMS",
        "VOMS"
    ],
    "UC3vzVK_N_SUVKqbX69L_X4g": [
        "緋笠トモシカ",
        "https://yt3.ggpht.com/ytc/AAUvwnhSyw72yPqDbQMSNN6RBJ0nAHa7wmMl-5etY8Bs=s88-c-k-c0x00ffffff-no-rj",
        "VOMS",
        "VOMS"
    ],
    "UC0Owc36U9lOyi9Gx9Ic-4qg": [
        "因幡はねる【あにまーれ】",
        "https://yt3.ggpht.com/ytc/AAUvwngvgRbvQSxZHcosptXrl6PO3djyKHY7ZLIGbQHo=s176-c-k-c0x00ffffff-no-rj",
        "Animale",
        "774inc"
    ],
    "UC2kyQhzGOB-JPgcQX9OMgEw": [
        "宗谷いちか【あにまーれ】",
        "https://yt3.ggpht.com/ytc/AAUvwnj2XS4F6MS5aaKGDaQ4mcrPlW44lEN-p9oXqj9x=s176-c-k-c0x00ffffff-no-rj",
        "Animale",
        "【あにまーれ】"
    ],
    "UCRvpMpzAXBRKJQuk-8-Sdvg": [
        "日ノ隈らん【あにまーれ】",
        "https://yt3.ggpht.com/ytc/AAUvwnit824wjmPA7AE7LDtG0EVjmutNl4-sICtStfTh=s176-c-k-c0x00ffffff-no-rj",
        "Animale",
        "【あにまーれ】"
    ],
    "UCXp7sNC0F_qkjickvlYkg-Q": [
        "風見くく【あにまーれ】",
        "https://yt3.ggpht.com/ytc/AAUvwngUM0DtcqRxbIHvfd8t3D-YEFLudJbN29dpdy44=s176-c-k-c0x00ffffff-no-rj",
        "Animale",
        "【あにまーれ】"
    ],
    "UCW8WKciBixmaqaGqrlTITRQ": [
        "柚原いづみ【あにまーれ】",
        "https://yt3.ggpht.com/ytc/AAUvwnhkL2lOLKPB4cqpPgqjHDV9AVypXtkNt10Eqm0=s176-c-k-c0x00ffffff-no-rj",
        "Animale",
        "【あにまーれ】"
    ],
    "UCtzCQnCT9E4o6U3mHHSHbQQ": [
        "白宮みみ【あにまーれ】",
        "https://yt3.ggpht.com/ytc/AAUvwnh5PNIZ9uxa95u863cHH2MYouiMqeau7SMPMgIM2g=s176-c-k-c0x00ffffff-no-rj",
        "Animale",
        "【あにまーれ】"
    ],
    "UC_BlXOQe5OcRC7o0GX8kp8A": [
        "羽柴なつみ【あにまーれ】",
        "https://yt3.ggpht.com/ytc/AAUvwnhnPVaFf9fcrI0-QGkOQ-qSEz2jx0KI8VdkdzGc=s176-c-k-c0x00ffffff-no-rj",
        "Animale",
        "【あにまーれ】"
    ],
    "UC_WOBIopwUih0rytRnr_1Ag": [
        "瀬島るい【あにまーれ】",
        "https://yt3.ggpht.com/ytc/AAUvwniT9Kk84h82ycAnKFqBNqWSb6GYU9msUCuICnU1=s176-c-k-c0x00ffffff-no-rj",
        "Animale",
        "【あにまーれ】"
    ],
    "UCFsWaTQ7kT76jNNGeGIKNSA": [
        "飛良ひかり【あにまーれ】",
        "https://yt3.ggpht.com/ytc/AAUvwnggEiqlVN2rxQJAOdr_FDt5FxmAc_zqTKT-Jo1L=s176-c-k-c0x00ffffff-no-rj",
        "Animale",
        "【あにまーれ】"
    ],
    "UC3xG1XWzAKt5dxSxktJvtxg": [
        "大浦るかこ【あにまーれ】",
        "https://yt3.ggpht.com/ytc/AAUvwni5YbJevR91U1BH8ZnAht-KGKlfR9qQ0mq--Ms-=s176-c-k-c0x00ffffff-no-rj",
        "Animale",
        "【あにまーれ】"
    ],
    "UC4PrHgUcAtOoj_LKmUL-uLQ": [
        "湖南みあ【あにまーれ】",
        "https://yt3.ggpht.com/ytc/AAUvwnhx0c80q3E3hw9sh-DaAcCdJzQwoj-RGacvGKCr=s176-c-k-c0x00ffffff-no-rj",
        "Animale",
        "【あにまーれ】"
    ],
    "UCqskJ0nmw-_eweWfsKvbrzQ": [
        "月野木ちろる【あにまーれ】",
        "https://yt3.ggpht.com/ytc/AAUvwnjuOZitdf-fShd8pKRuJphKOBul_WJ9ikhVJC0t=s176-c-k-c0x00ffffff-no-rj",
        "Animale",
        "【あにまーれ】"
    ],
    "UCwePpiw1ocZRSNSkpKvVISw": [
        "西園寺メアリ【ハニスト】",
        "https://yt3.ggpht.com/ytc/AAUvwnhhEokdfq1Mo2x7_TmP2AU-v0nqHFchVBNWqay_=s176-c-k-c0x00ffffff-no-rj",
        "774inc",
        "【ハニスト】"
    ],
    "UCeLzT-7b2PBcunJplmWtoDg": [
        "周防パトラ 【ハニスト】",
        "https://yt3.ggpht.com/ytc/AAUvwni3K3HvrlssJykNA7cE68zGcO4xZPF5k3XLE9sO=s176-c-k-c0x00ffffff-no-rj",
        "774inc",
        "【ハニスト】"
    ],
    "UCYTz3uIgwVY3ZU-IQJS8r3A": [
        "島村シャルロット【ハニスト】",
        "https://yt3.ggpht.com/ytc/AAUvwnjfBbGgsin15WvNkf1f1KvMA956OOECN8FswkYU=s176-c-k-c0x00ffffff-no-rj",
        "774inc",
        "【ハニスト】"
    ],
    "UCDh2bWI5EDu7PavqwICkVpA": [
        "堰代ミコ【ハニスト】",
        "https://yt3.ggpht.com/ytc/AAUvwnj3utKMlGG9fe71Ti1JfPMohMvO_gT_oSCdGC51=s176-c-k-c0x00ffffff-no-rj",
        "774inc",
        "【ハニスト】"
    ],
    "UCzUNASdzI4PV5SlqtYwAkKQ": [
        "小森めと 【ブイアパ】",
        "https://yt3.ggpht.com/ytc/AAUvwngcfYNy2eRoiQds8qhnxWohjghC3WcxLBtOX5Kg=s176-c-k-c0x00ffffff-no-rj",
        "774inc",
        "【ブイアパ】"
    ],
    "UC3EhsuKdEkI99TWZwZgWutg": [
        "杏戸ゆげ 【ブイアパ】",
        "https://yt3.ggpht.com/ytc/AAUvwnhldEYLmpc864v-XQDKTryZmS33CK_91Wf2Iwb1=s176-c-k-c0x00ffffff-no-rj",
        "774inc",
        "【ブイアパ】"
    ],
    "UChXm-xAYPfygrbyLo2yCASQ": [
        "季咲あんこ 【ブイアパ】",
        "https://yt3.ggpht.com/ytc/AAUvwnguDljqOoJWknfaN1vN3F8NPPPBMydXFK-ljH05=s176-c-k-c0x00ffffff-no-rj",
        "774inc",
        "【ブイアパ】"
    ],
    "UCV4EoK6BVNl7wxuxpUvvSWA": [
        "不磨わっと 【ブイアパ】",
        "https://yt3.ggpht.com/ytc/AAUvwnghel9DJYtFb6bSWzpybgFvZVXW5JVewnf7t3X-=s176-c-k-c0x00ffffff-no-rj",
        "774inc",
        "【ブイアパ】"
    ],
    "UCmqrvfLMws-GLGHQcB5dasg": [
        "花奏 かのん 【ブイアパ】",
        "https://yt3.ggpht.com/ytc/AAUvwngyYdZqbOy-sD-6uapvOvPFivU6Aizkkjkz0lWqbg=s176-c-k-c0x00ffffff-no-rj",
        "774inc",
        "【ブイアパ】"
    ],
    "UCvPPBoTOor5gm8zSlE2tg4w": [
        "虎城アンナ 【シュガリリ】",
        "https://yt3.ggpht.com/ytc/AAUvwng3pwz9U-DRhU-oVEo42HFGbzOElFOMHZ532dlV=s176-c-k-c0x00ffffff-no-rj",
        "774inc",
        "【シュガリリ】"
    ],
    "UC2hc-00y-MSR6eYA4eQ4tjQ": [
        "龍ヶ崎リン 【シュガリリ】",
        "https://yt3.ggpht.com/ytc/AAUvwnhPqY2LTUK6Eo6Fl1ZH_kL-Z9QhjDl9a46iwRH-=s176-c-k-c0x00ffffff-no-rj",
        "774inc",
        "【シュガリリ】"
    ],
    "UC--A2dwZW7-M2kID0N6_lfA": [
        "獅子王クリス 【シュガリリ】",
        "https://yt3.ggpht.com/ytc/AAUvwngzuEXJ6hxBH1uZtz_iJv1VRC8mMGlqEOXojp9f=s176-c-k-c0x00ffffff-no-rj",
        "774inc",
        "【シュガリリ】"
    ],
    "UC2GuoutVyegg6PUK88lLpjw": [
        "兄者弟者",
        "https://yt3.ggpht.com/ytc/AAUvwniy1ARFkKvn9C681YgHkjsPjuPxrkYshOGvEZ7D_A=s88-c-k-c0x00ffffff-no-rj",
        "DBD",
        "DBD"
    ],
    "UCpXHIKytmA2RIHpDF3rp9EA": [
        "べるくら企画",
        "https://yt3.ggpht.com/ytc/AAUvwngKckKiJXKa0Zcur2AfNK87SmfnyjEjKn_H8Ogvww=s88-c-k-c0x00ffffff-no-rj",
        "DBD",
        "DBD"
    ],
    "UCDn8Lqf-x0zD8hmFUg08f6w": [
        "狩野英孝【公式チャンネル】EIKO!GO!!",
        "https://yt3.ggpht.com/ytc/AAUvwnhNDtCn0kpzANQ89q9UDFL04ytW32eYXodrysaI=s88-c-k-c0x00ffffff-no-rj",
        "DBD",
        "DBD"
    ],
    "UCz0aC9z3kXruRHULDqFRuVA": [
        "あっさりしょこ",
        "https://yt3.ggpht.com/ytc/AAUvwniV_ALSL7vMEX9wgVI4Je2KWb3jtntzi94iNyWPGQ=s88-c-k-c0x00ffffff-no-rj",
        "DBD",
        "DBD"
    ],
    "UCY5M1FeR1BQNsnumsJA1epA": [
        "れぷちん",
        "https://yt3.ggpht.com/ytc/AAUvwnhEhvtgRPYbyulaH2SKyVYTdMcsPYlECaRCIGL3Zg=s88-c-k-c0x00ffffff-no-rj",
        "DBD",
        "DBD"
    ],
    "UCH4fJJRV2UzgEpurjm9AiGw": [
        "柚子木しろ",
        "https://yt3.ggpht.com/ytc/AAUvwnhQkyw5DWx_1hZoHrQVF73SscIZKmfUJRVVwIXljQ=s88-c-k-c0x00ffffff-no-rj",
        "DBD",
        "DBD"
    ],
    "UC0VoI57B2_63MErt_1QBpxA": [
        "EXAM",
        "https://yt3.ggpht.com/ytc/AAUvwngTAeWz5Hw53R8yVMIm3cc5XBygvo4qGtu6B0O6hw=s88-c-k-c0x00ffffff-no-rj",
        "DBD",
        "DBD"
    ],
} #配信者のチャンネルID, 配信者名, アイコン画像のURLのリスト
webhook_url = "https://discord.com/api/webhooks/814627315048906802/mast3_S-vt3V0R_fwVhzgrKmWD3H4fYAD9XZQiTuSWKFEupE2aRou24yWiYM6Jtksdjd" #配信開始
webhook_url_yotei = {"Hololive": ['https://discord.com/api/webhooks/814626994296979456/IisxTTZqQXTvM569Z4TVFYSEqdxEriwt_M9XX_IEEiDsNNqG991tyZr94VOOfjAsBpeJ'],
                    "VOMS": ['https://discord.com/api/webhooks/838761972651655208/Kf3CGJ4ILSOgnQSm-gSEvtck2-Ug7clLCoQNr5HANyELXjxgffAseMr_j9qjiMxmvi0S'],
                     "Animale": ['https://discord.com/api/webhooks/839456091549073478/7EOanYAZaCsDWiiBTpqoOaTsmMg6VwhdCXpAvIs-GFWmEv5aqrGsg5v2mdNwqRbuLndu'],
                     "774inc": ['https://discord.com/api/webhooks/839456401164075019/647cX72CzfwUQA1YoYAE4plZ-pzHLftVSjr3N2Ap_rauabzqRjFUD_wBH3fHeCBw3U6i'],
                     "DBD": ['https://discord.com/api/webhooks/853051395140485120/LcdvLRUFrCEAMfUFeelxtlebhLJ4hXij4d994L3hB1CU0v2NazkjKZpr_lcP5zjUUdGK']                     
                    }#配信予定
webhook_url_tw = "https://discord.com/api/webhooks/853479874038595604/w_qUk4c_yx_8QDrd6uWKYsk6LYMyJug9rWsyDy7r6gyLRgQUCTRkKMB9qKY-mKTlS8uG"

webhook_url = "https://discord.com/api/webhooks/815378597640273950/n4lBhc1Xeh7NHD7YuEocX_Vwxg4tKml5tsZSV10eshXmUu_OCHJuce1ft77GJ_cvUt3j" #配信開始
webhook_url_yotei = {"Hololive": ['https://discord.com/api/webhooks/815378597640273950/n4lBhc1Xeh7NHD7YuEocX_Vwxg4tKml5tsZSV10eshXmUu_OCHJuce1ft77GJ_cvUt3j'],
                     "VOMS": ['https://discord.com/api/webhooks/815378597640273950/n4lBhc1Xeh7NHD7YuEocX_Vwxg4tKml5tsZSV10eshXmUu_OCHJuce1ft77GJ_cvUt3j'],
                     "Animale": ['https://discord.com/api/webhooks/815378597640273950/n4lBhc1Xeh7NHD7YuEocX_Vwxg4tKml5tsZSV10eshXmUu_OCHJuce1ft77GJ_cvUt3j'],
                     "774inc": ['https://discord.com/api/webhooks/815378597640273950/n4lBhc1Xeh7NHD7YuEocX_Vwxg4tKml5tsZSV10eshXmUu_OCHJuce1ft77GJ_cvUt3j'],
                     "DBD": ['https://discord.com/api/webhooks/815378597640273950/n4lBhc1Xeh7NHD7YuEocX_Vwxg4tKml5tsZSV10eshXmUu_OCHJuce1ft77GJ_cvUt3j']                     
                    }#配信予定
webhook_url_tw = 'https://discord.com/api/webhooks/815378597640273950/n4lBhc1Xeh7NHD7YuEocX_Vwxg4tKml5tsZSV10eshXmUu_OCHJuce1ft77GJ_cvUt3j'
def get_oauth():
    CONSUMER_KEY=os.environ['CONSUMER_KEY']
    CONSUMER_SECRET=os.environ['CONSUMER_SECRET']
    ACCESS_TOKEN_KEY=os.environ['ACCESS_TOKEN_KEY']
    ACCESS_TOKEN_SECRET=os.environ['ACCESS_TOKEN_SECRET']
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    return auth


broadcast_data = {} #配信予定のデータを格納
tweet_data = {}
tmp = {}

YOUTUBE_API_KEY = os.environ['YOUTUBE_APIKEY']
auth = get_oauth()
tw_api = tweepy.API(auth_handler=auth)

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



@tasks.loop(minutes=30)
async def get_information():
    tmp = copy.copy(broadcast_data)
    now_time = datetime.now() + timedelta(hours=9)
    queryWord = "戌神ころね"
    queryWord_buf = "戌神ころね"
    idList = []
    for idol in Streamer:
        if(queryWord_buf != Streamer[idol][3]):
            queryWord = queryWord + "|" + Streamer[idol][3]
            queryWord_buf = Streamer[idol][3]
        idList.append(idol)
    dtct_time = now_time - timedelta(days=7)
    api_link = "https://www.googleapis.com/youtube/v3/search?part=snippet&fields=items(id,snippet/title,snippet/channelId,snippet/publishedAt)&q=" + queryWord + "&key=" + YOUTUBE_API_KEY + "&eventType=upcoming&type=video&maxResults=50&" + dtct_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    aaa = requests.get(api_link)
    v_data = json.loads(aaa.text)
    api_link = "https://www.googleapis.com/youtube/v3/search?part=snippet&fields=items(id,snippet/title,snippet/channelId,snippet/publishedAt)&q=" + queryWord + "&key=" + YOUTUBE_API_KEY + "&eventType=live&type=video&maxResults=50"
    aaa = requests.get(api_link)
    #v_data.update(json.loads(aaa.text))
    for item in v_data['items']:#各配信予定動画データに関して
        try:
            if(item['snippet']['channelId'] in idList):
                broadcast_data[item['id']['videoId']] = {'channelId':item['snippet']['channelId']} #channelIDを格納
            if('dbd' in item['snippet']['title']):
                broadcast_data[item['id']['videoId']] = {'channelId':"UCaSgsFdGbwjfdawl3rOXiwQ"} #channelIDを格納
        except KeyError:
            continue
        
    for video in broadcast_data:
        try:
            a = broadcast_data[video]['starttime'] #既にbroadcast_dataにstarttimeがあるかチェック
        except KeyError:#なかったら
            aaaa = requests.get("https://www.googleapis.com/youtube/v3/videos?part=liveStreamingDetails&fields=items(liveStreamingDetails/scheduledStartTime)&id=" + video + "&key=" + YOUTUBE_API_KEY)
            vd = json.loads(aaaa.text)
            broadcast_data[video]['starttime'] = vd['items'][0]['liveStreamingDetails']['scheduledStartTime']
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
            if((sd_time + timedelta(minutes=1)) >= now_time >= sd_time):#今の方が配信開始時刻よりも後だったら
                post_to_discord(broadcast_data[bd]['channelId'], bd) 
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

@tasks.loop(seconds=60)
async def showTL():
    tweet_tmp = copy.copy(tweet_data)
    try:
        tl = tw_api.list_timeline(list_id='1402758087744712708', count=10)
        #tl = api.list_timeline(owner_screen_name='asuma_Noah', slug='774inc', count=10)
        tl.reverse()
        for status in tl:
            tweet_url = 'https://twitter.com/' + status.author.screen_name + '/status/' + status.id_str
            tweet_data[status.id] = {'text':status.text + '\n' + tweet_url}
            tweet_data[status.id]['icon_url'] =status.author.profile_image_url
            tweet_data[status.id]['name'] = status.author.name
            #main_content = {    
            #        "username": tweet_data[status.id]['name'],
            #        "avatar_url": tweet_data[status.id]['icon_url'],
            #        "content": tweet_data[status.id]['text']
            #}
            #requests.post(webhook_url, main_content)            
            #status.created_at += timedelta(hours=9) # add 9 hours for Japanese time
        for tw in list(tweet_data):
            if(not(tw in tweet_tmp)):
                main_content = {    
                    "username": tweet_data[tw]['name'],
                    "avatar_url": tweet_data[tw]['icon_url'],
                    "content": tweet_data[tw]['text']
                }
                requests.post(webhook_url_tw, main_content)#ツイート
            
    except Exception:
        time.sleep(1)
        pass

# 起動時に動作する処理
@bot.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    broadcast_data = {} #配信予定のデータを格納
    tweet_data = {}
    tmp = {}
    get_information.start()
    showTL.start()
    time.sleep(60)
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
