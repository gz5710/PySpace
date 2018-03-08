# -*- coding: utf-8 -*-
import json
import requests
from urllib import request
from urllib import parse
from datetime import datetime
from wxpy import *

# 调用图灵机器人API，发送消息并获得机器人的回复
def auto_reply(text):     
    url = "http://www.tuling123.com/openapi/api"
    api_key = "2c044484ce66456588a9d5640ba6d0ec"    
    payload = {
        "key": api_key,
        "info": text,
        "userid": "123456"
    }
    r = requests.post(url, data=json.dumps(payload))     
    result = json.loads(r.content)   
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '[Got a response from Tuling] '+ result["text"])
    return "[Bruce的聊天机器人] " + result["text"]

bot = Bot(console_qr=True, cache_path=True)

@bot.register()
def forward_message(msg):     
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '[Received Message] ' + msg.text)
    return auto_reply(msg.text)

embed()