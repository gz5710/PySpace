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
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [Got a response from Tuling] {result['text']}")
    return f"[{startWord}] : {result['text']}"

bot = Bot(console_qr=True, cache_path=True)

# Create the lists
white_list = []
# Configs
startWord = '小哲同学'
endWord = '再见'
welcome = f'[{startWord}] : 终于等到您翻牌子了，我是小哲\n\n[ 结束对话时，请输入“{endWord}” ]'
bye = f'[{startWord}] : 小哲很高兴与您交流，希望下次再见'

@bot.register()
def forward_message(msg):     
    if msg.text.startswith(startWord):
        # print(f'[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [Received Message] {msg.text}')
        white_list.append(msg.member)
        print(f"[{msg.sender.name}] joining the chat")
        return welcome
    elif msg.text.startswith(endWord):
        white_list.remove(msg.member)
        print(f"[{msg.sender.name}] leaving the chat")
        return bye
    else:
        try:
            b=white_list.index(msg.member)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [Received Message] {msg.text}")
            return auto_reply(msg.text)
        except ValueError:
            print(f'The user[{msg.sender.name}] is not in the white list')
            return ''
        


embed()