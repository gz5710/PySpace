from urllib import request
from urllib import parse
from http import cookiejar
#Fiddler获得的真实登陆地址
login_url = 'https://www.googleadservices.com/pagead/conversion/1005888149/?random=1519684534120&cv=9&fst=1519684534120&num=1&value=0&label=ULE2CJvc4AIQlcXS3wM&bg=ffffff&hl=en&guid=ON&resp=GooglemKTybQhCsO&u_h=800&u_w=1280&u_ah=800&u_aw=1280&u_cd=24&u_his=8&u_tz=60&u_java=false&u_nplug=4&u_nmime=5&frm=0&url=http%3A%2F%2Fwww.seloger.com%2Flist.htm%3Fidtt%3D2%26naturebien%3D1%2C2%2C4%26idtypebien%3D1%26ci%3D780646%2C780686%2C920022%26tri%3Dd_px%26pxmax%3D270000%26nb_pieces%3D2%2C3%26nb_chambres%3D2&ref=http%3A%2F%2Fwww.seloger.com%2Flist.htm%3Forg%3Dadvanced_search%26idtt%3D2%26idtypebien%3D1%26ci%3D780646%2C780686%2C920022%26pxmax%3D270000%26tri%3Dinitial%26nb_pieces%3D2%2C3%26nb_chambres%3D2%26naturebien%3D1%2C2%2C4&tiba=Vente%20appartement%202%20ou%203%20pi%C3%A8ces%20Versailles%2C%20Viroflay%20ou%20Chaville%20(%2078%2C%2078%20ou%2092)%20%7C%20acheter%20appartements%20F2%2FT2%2F2%20pi%C3%A8ces%20ou%20F3%2FT3%2F3%20pi%C3%A8ces%20%C3%A0%20Versailles%2C%20Viroflay%20ou%20Cha&rfmt=3&fmt=4'
user_agent = r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
#Headers信息
headers = {'User-Agnet': user_agent, 'Connection': 'keep-alive'}
#登陆Form_Data信息
Login_Data = {}
# Login_Data['username'] = 'gz5710'
# Login_Data['password'] = '5710640'
# Login_Data['goto'] = 'http://bbs.xineurope.com'
# Login_Data['gotoOnFail'] = 'http: //baidu.com'
#使用urlencode方法转换标准格式
logingpostdata = parse.urlencode(Login_Data).encode('utf-8')
#声明一个CookieJar对象实例来保存cookie
cookie = cookiejar.CookieJar()
#利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
cookie_support = request.HTTPCookieProcessor(cookie)
#通过CookieHandler创建opener
opener = request.build_opener(cookie_support)
#创建Request对象
req1 = request.Request(url=login_url, data=logingpostdata, headers=headers)

#打开登陆界面
html1 = opener.open(req1)
print(html1.read().decode('utf-8'))
#查询成绩的页面
# grade_url = 'http://ssfw.xmu.edu.cn/cmstar/index.portal?.pn=p1201_p3535'
# req2 = request.Request(url=grade_url, headers=headers)
# html2 = opener.open(req2)
# html2 = html2.read().decode('utf-8')
# print(html2)