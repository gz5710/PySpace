from wxpy import *

# Login (store in the cache)
bot = Bot(cache_path=True)

# Send message by File_Helper
bot.file_helper.send("Hello, wechat")

# Reply to message
@bot.register()
def print_message(msg):
    print('[Received Message] ' + msg.text)
    return '[Auto Reply]\nThanks your kind message. Unfortunately Mr Bruce GONG is unable to answered right now. He will contact you once available. Thanks.' + '\n感谢您的消息，但很可惜，Bruce GONG先生无法立刻回复，稍后他会尽快联系您，谢谢。'


# Group message transfert
group = bot.groups().search('Test')[0]


# Keep program running
embed()