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
welcome = f'[{startWord}] : 终于等到您翻牌子了，我是小哲\n\n[ 如想结束对话，请输入“{endWord}” ]'
bye = f'[{startWord}] : 小哲很高兴与您交流，希望下次再见！'

@bot.register()
def forward_message(msg):     
    if msg.text.startswith(startWord):
        # print(f'[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [Received Message] {msg.text}')
        white_list.append(msg.sender.name)
        print(f"[{msg.sender.name}] joining the chat {white_list}")
        if msg.text == startWord:
            return welcome
        else:
            return auto_reply(msg.text)
    elif msg.text.startswith(endWord):
        white_list.remove(msg.sender.name)
        print(f"[{msg.sender.name}] leaving the chat {white_list}")
        return bye
    else:
        try:
            b=white_list.index(msg.sender.name)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [Received Message] {msg.sender.name}: {msg.text}")
            res = auto_reply(msg.text)
            if res == endWord:
                white_list.remove(msg.sender.name)
                print(f"[{msg.sender.name}] leaving the chat {white_list}")
            else:
                return res
        except ValueError:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] The user[{msg.sender.name}] is not in the white list {white_list}")
            return ''
        


embed()