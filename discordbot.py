import time
import requests
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
    ]
} #配信者のチャンネルID, 配信者名, アイコン画像のURLのリスト

webhook_url_Hololive = 'https://discord.com/api/webhooks/814455705607077928/7GHQbsP_NNHR9uZ78CzVmiQwyCajJEdRpqI8hRDD-yKy87evrNnkEmJDiIOCT2nLMjHn' #ホロライブ配信開始
webhook_url_Hololive_yotei = 'https://discord.com/api/webhooks/814455705607077928/7GHQbsP_NNHR9uZ78CzVmiQwyCajJEdRpqI8hRDD-yKy87evrNnkEmJDiIOCT2nLMjHn' #ホロライブ配信予定
broadcast_data = {} #配信予定のデータを格納

YOUTUBE_API_KEY = ["AIzaSyD1v807Gio9K4GVjKVjdRVgw0_kMip7z8Y","AIzaSyDYbIaTUq3yipQrOHncHhHjKDxVRZDZE5s","AIzaSyACZwmWNAyT5w2Spzm3_61Rw0GiH33utRU","AIzaSyDR5AhxSeIKsvIMJDqhsMTfh_fvo6DLR3o","AIzaSyCbmIAmPpKnLMrM2vEGg8MoqTyHgTVMAOM","AIzaSyDE9i7mg0ruYaISi8MPVH-tMd8LE4B_kNg","AIzaSyA2x_6iFWJHDlxjYAq4-ekMz9lHnlgZcAA"]

def dataformat_for_python(at_time): #datetime型への変換
    at_year = int(at_time[0:4])
    at_month = int(at_time[5:7])
    at_day = int(at_time[8:10])
    at_hour = int(at_time[11:13])
    at_minute = int(at_time[14:16])
    at_second = int(at_time[17:19])
    return datetime(at_year, at_month, at_day, at_hour, at_minute, at_second)

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

def post_to_discord(userId, videoId):
    haishin_url = "https://www.youtube.com/watch?v=" + videoId #配信URL
    content = "配信中！\n" + haishin_url #Discordに投稿される文章
    main_content = {
        "username": Hololive[userId][0], #配信者名
        "avatar_url": Hololive[userId][1], #アイコン
        "content": content #文章
    }
    requests.post(webhook_url_Hololive, main_content) #Discordに送信
    broadcast_data.pop(videoId)

def get_information():
    tmp = copy.copy(broadcast_data)
    api_now = 0 #現在どのYouTube APIを使っているかを記録
    for idol in Hololive:
        api_link = "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=" + idol + "&key=" + YOUTUBE_API_KEY[api_now] + "&eventType=upcoming&type=video"
        api_now = (api_now + 1) % len(YOUTUBE_API_KEY) #apiを1つずらす
        aaa = requests.get(api_link)
        v_data = json.loads(aaa.text)
        try:
            for item in v_data['items']:#各配信予定動画データに関して
                broadcast_data[item['id']['videoId']] = {'channelId':item['snippet']['channelId']} #channelIDを格納
            for video in broadcast_data:
                try:
                    a = broadcast_data[video]['starttime'] #既にbroadcast_dataにstarttimeがあるかチェック
                except KeyError:#なかったら
                    aaaa = requests.get("https://www.googleapis.com/youtube/v3/videos?part=liveStreamingDetails&id=" + video + "&key=" + YOUTUBE_API_KEY[api_now])
                    api_now = (api_now + 1) % len(YOUTUBE_API_KEY) #apiを1つずらす
                    vd = json.loads(aaaa.text)
                    print(vd)
                    broadcast_data[video]['starttime'] = vd['items'][0]['liveStreamingDetails']['scheduledStartTime']
        except KeyError: #配信予定がなくて403が出た
            continue
    for vi in broadcast_data:
        if(not(vi in tmp)):
            print(broadcast_data[vi])
            try:
                post_broadcast_schedule(broadcast_data[vi]['channelId'], vi, broadcast_data[vi]['starttime'])
            except KeyError:
                continue

def check_schedule(now_time, broadcast_data):
    for bd in list(broadcast_data):
        try:
            # RFC 3339形式 => datetime
            sd_time = datetime.strptime(broadcast_data[bd]['starttime'], '%Y-%m-%dT%H:%M:%SZ') #配信スタート時間をdatetime型で保管
            sd_time += timedelta(hours=9)
            if(now_time >= sd_time):#今の方が配信開始時刻よりも後だったら
                post_to_discord(broadcast_data[bd]['channelId'], bd) #ツイート
        except KeyError:
            continue

def post_broadcast_schedule(userId, videoId, starttime):
    st = starttime.replace('T', ' ')
    sst = st.replace('Z', '')
    ssst = replace_JST(sst)
    haishin_url = "https://www.youtube.com/watch?v=" + videoId #配信URL
    content = ssst + "に配信予定！\n" + haishin_url #Discordに投稿される文章
    main_content = {
        "username": Hololive[userId][0], #配信者名
        "avatar_url": Hololive[userId][1], #アイコン
        "content": content #文章
    }
    requests.post(webhook_url_Hololive_yotei, main_content) #Discordに送信


while True:
    now_time = datetime.now() + timedelta(hours=9)
    if(((now_time.year > 2020) or ((now_time.year == 2020) and (now_time.month >= 6) and (now_time.day >= 22))) and (now_time.minute == 0) and (now_time.hour %  == 0)):
        get_information()
    check_schedule(now_time, broadcast_data)
    time.sleep(60)
