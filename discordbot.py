
from discord.ext import commands
import os
import traceback
import time
import requests
import json
import copy
from datetime import datetime, timedelta, timezone


webhook_url_Hololive = 'https://discord.com/api/webhooks/814455705607077928/7GHQbsP_NNHR9uZ78CzVmiQwyCajJEdRpqI8hRDD-yKy87evrNnkEmJDiIOCT2nLMjHn' #ホロライブ配信開始
webhook_url_Hololive_yotei = 'https://discord.com/api/webhooks/814455705607077928/7GHQbsP_NNHR9uZ78CzVmiQwyCajJEdRpqI8hRDD-yKy87evrNnkEmJDiIOCT2nLMjHn' #ホロライブ配信予定
broadcast_data = {} #配信予定のデータを格納

YOUTUBE_API_KEY = ["AIzaSyD1v807Gio9K4GVjKVjdRVgw0_kMip7z8Y","AIzaSyDYbIaTUq3yipQrOHncHhHjKDxVRZDZE5s","AIzaSyACZwmWNAyT5w2Spzm3_61Rw0GiH33utRU","AIzaSyDR5AhxSeIKsvIMJDqhsMTfh_fvo6DLR3o","AIzaSyCbmIAmPpKnLMrM2vEGg8MoqTyHgTVMAOM","AIzaSyDE9i7mg0ruYaISi8MPVH-tMd8LE4B_kNg","AIzaSyA2x_6iFWJHDlxjYAq4-ekMz9lHnlgZcAA"]

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


bot.run(token)

