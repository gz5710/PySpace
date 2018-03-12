from wxpy import *
import operator

bot = Bot(cache_path=True)
my_friends = bot.friends()
# print(type(my_friends))

friend_loc = {} # 每一个元素是一个二元列表，分别存储地区和人数信息

for f in my_friends:
    # print(f"{f.name} - {f.province} - {f.city}")
    if f.province != "":
        if f.province in friend_loc:
            friend_loc[f.province] += 1
        else:
            friend_loc[f.province] = 1
    else:
        try:
            friend_loc["无"] += 1
        except KeyError:
            friend_loc.setdefault("无", 1)
        
friend_loc_sorted = sorted(friend_loc.items(),key = operator.itemgetter(1),reverse = True)

# for key, val in friend_loc.items():
#     print(f"{key} - {val}")
print(f"您共有 {sum(friend_loc.values())} 位微信好友")
print(friend_loc_sorted)