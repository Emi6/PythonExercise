# 加注释
import requests
import re
import pymongo
import itchat
# connection = pymongo.MongoClient('127.0.0.1',27017)
# tdb = connection.MyData
# post = tdb.test
import pandas as pd
from PIL.PngImagePlugin import iTXt
from pandas import DataFrame
from lxml import etree
from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup
import psutil
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from collections import Counter
# from selenium import webdriver
# import sys
import json
# reload(sys)
# sys.setdefaultencoding('utf-8')
#https://www.jianshu.com/p/4c6387c650dc
def getcookie(filename):
    # cookie=open(r'filename','r')#打开所保存的cookies内容文件
    cookie = open(filename, 'r')
    cookies={}#初始化cookies字典变量
    for line in cookie.read().split(';'):   #按照字符：进行划分读取 #其设置为1就会把字符串拆分成2份

        name,value=line.strip().split('=',1)
        cookies[name]=value  #为字典cookies添加内容
    return cookies
def gethtml(url,filename):
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0column; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            }
    response = requests.get(url, headers=headers, cookies=getcookie(filename), timeout=30)
    return response
def init(i,User):
    url = 'https://xueqiu.com/v4/statuses/user_timeline.json?page={page}&user_id={user}'
    url=url.format(page=i,user=User)
    response = gethtml(url, 'cookie.txt')
    page = response.json()
    # print(page)
    return page
    # print(page)

def analyze(page):
    try:

    # print(page)
        statuses=page['statuses']
        count=page['count']
        # print(statuses[1]["text"])
        TimeUpper=statuses[1]["timeBefore"]
        TimeLower=statuses[count-1]["timeBefore"]
        TimeUpper = TimeUpper.replace('-', '')
        TimeUpper=TimeUpper.split()[0]
        TimeLower = TimeLower.replace('-', '')
        TimeLower = TimeLower.split()[0]
        if len(TimeLower) ==4:
            TimeLower='2018'+TimeLower
        if len(TimeUpper) == 4:
            TimeUpper = '2018' + TimeUpper
        # print(TimeUpper)
        special=str('今天')
        if TimeUpper==special:
            TimeUpper = datetime.now().strftime("%Y-%m-%d")
            TimeUpper = TimeUpper.replace('-', '')
        if TimeLower == special:
            TimeLower = datetime.now().strftime("%Y-%m-%d")
            TimeLower = TimeLower.replace('-', '')
            # TimeUpper = TimeUpper.split()[0]

        return TimeLower, TimeUpper,statuses
    except Exception as e:
        pass

def comparison(User,strday,TimeUpper,TimeLower,statuses,t,Name):
    d = list()
    print(TimeUpper,TimeLower)
    try:

        if strday>TimeUpper:
            print("it is a remark")
            return None
        elif TimeLower<strday<=TimeUpper:
            c=FindDay(User,statuses,strday,Name)
            d.extend(c)
            print('it is a remark2/3')
            print(2)
            print(d)
            return d
        elif strday<=TimeLower:
            c=FindDay(User,statuses,strday,Name)
            d=c
            print("d=")
            print(d)
            t=t+1
            # Read(t, User, strday, Name)
            page = init(t,User)
            TimeLower, TimeUpper, statuses=analyze(page)
            z=comparison(User,strday, TimeUpper, TimeLower, statuses, t,Name)
            print(z)
            if d is None:
                d=list()
                d.extend(z)
            else:
                d.extend(z)
            print('it is a remark3/3')
            print(3)
            return d
    except Exception as e:
         print('pass')
         pass

def FindDay(User,statuses,strday,Name):
    connection = pymongo.MongoClient('127.0.0.1', 27017)
    tdb = connection.MyData
    post = tdb.test
    c=list()
    for i in statuses:
       a=list()


       text=i["text"]
       timeBefore=i["timeBefore"]
       timeBefore_modify = timeBefore.replace('-', '')
       timeBefore_modify = timeBefore_modify.split()[0]
       if len(timeBefore_modify)==4:
           timeBefore_modify='2018'+timeBefore_modify
       # print(timeBefore_modify)
       if strday == timeBefore_modify and re.findall('\$(.*?)\$', text) :
           # print(timeBefore)
           l = len(re.findall('\$(.*?)\$', text))
           print(len(re.findall('\$(.*?)\$', text)))
           a.append(timeBefore)
           a.append(re.findall('\$(.*?)\$', text)[0:])
           print("a=")
           print(a)
           # c.append(a[1])
           # print(c)
           for num in range(0,l):
                post.insert({'名字':str(Name[User]), "时间": a[0], "股票代码": a[1][num]})
                c.append(a[1][num])

    if len(c):
        print(c)
        return c

    else:
        return None
           # itchat.send( '名字 '+str(Name[User])+'\n'+'时间 '+a[0]+'\n'+'股票代码 ' + a[1], 'filehelper')

def Read(t,User,strday,Name):
    try:
        page=init(t,User)
        print(User)
        TimeLower, TimeUpper, statuses=analyze(page)
        fan=comparison(User, strday, TimeUpper, TimeLower, statuses, t, Name)
        # print(d)
        print(fan)
        return fan
    except:
        pass
def job():
    # itchat.auto_login(hotReload=True)
    # connection = pymongo.MongoClient('127.0.0.1', 27017)
    # tdb = connection.MyData
    # post = tdb.test
    # post.insert({'name': "李白", "age": 1, "skill": 2})
    User = [5171159182, 'assistant', 'huodong', 'fangtan', 9485866208,
            8152922548, 'xueyingzhengquan', 2709857861, 5828665454, 3748823499,
            5964068708, 9887656769, 6785033954, 9528220473, 8255849716,
            3037882447, 'shilaomao', 'simon', 6424252664, 'Value_at_Risk',
            'david_freedom', 'TQ1024', 9650668145, 'funds', 2733321298,
            'lord', 8510627167, 'nysdy', 1512170192, 'caomaolufei',
            1175857472, 'backwasabi', 2340719306, 3491303582, 'etfs',
            9226205191, 'comy28', 8780033408, 'yanbao', 2439489334,
            9742512811, 'gtzhou', 'dean_li', 1062883669, 6254918995,
            'laogaowudao', 4111857140, 6146592061, 1102105103, 'traveller1985',
            1127205381, 6413254712, 'Mario', 'rickyzhong', 2164183023,
            'chrishine', 'zhuankan', 'elephant', 1538598451, 'earlzhang',
            'hljj', 1760673340, 'Thecherryking', 'tiandaoqiniu', 'michael_chen',
            1272530506, 9206125741, 'laobeiao', 'xykk', 'xqwy',
            1546206224, 4779794911, 'xingu', 9640778912, 8291461932,
            7355827634, 9905072371, 'wdx_1984', 8018540373, 4439117448,
            'yufu', 8240989798, 'zltz', 9813181917, 1324002892,
            1674117751, 'wpeak', 'zhongdaqi', 7610708650, 'conan',
            1662576529, 'jingchengjiushao', 'nick', 4877612337, 'congsky',
            'lyujz', 6049709616, 8780946767, 'AaronM', 1738642461,
            'chenda', 3464131377, 8064062857, 1373073106, 'xujiajie',
            2915442382, 9097259018, 3062205427, 9518372158, 'cozone',
            2785562330, 9586083092, 7953251915, 'aaatu', 4433867848,
            2308207656, 4106327074, 8029098291, 'investor', 8107212038,
            9396837428, 'olivia', 5190345050, 6981947864, 7351106301,
            9564664610, 'slowisquick', 5866067799, 4027447937, 9603722416,
            8315885552, 1339778771, 'AAA_3', 6867901973, 2959851771,
            4248906337, 6160258782, 'Lagom', 6832369826, 'guojingpu',
            9428236477, 6510147098, 'xuzhihong', 'linjun168', 'matias',
            4017847389, 3408310156, 'tianduo', 'farfromu', 9755618618,
            2033624326, 1683036638, 1906328753, 7315353232, 7592287001,
            3055849674, 6078380931, 1876614331, 9444904852, 4074947120,
            'aguilmkz', 2994748381, 1314783718, 'rathman', 8592131633,
            'peter', 4743057813, 'tdxy', 2595056894, 1421406103,
            'forcode', 'bobshan', 2859479813, 7694221981, 3966435964,
            'wufaling', 6753271936, 9047587905, 2657407918, 'hbyq',
            2100654541, 1482535759, 1638377010, 'xiaoyaoguhai', 1722979527,
            'wangli', 'Terastar', 'lushanlin', 'fangyongsheng', 'panpan',
            'liyan', 2536207007, 1604871976, 'invescogreatwall', 6928974450,
            1910783512, 'shuailang', 'yangchengdiyiniu', 'mrmarket', 9883838696,
            3881365268, 7146274836, 1940211456, 9761091523, 2164748441,
            7535271733, 2554781328, 'Alwaleed', 5962548939, 'royie',
            4742988362, 2276196460, 'quyueyue', 6195589551, 1597430632,
            7783401784, 'moahmo', 3638360312, 'hikiwa', 1622002697,
            'iamu', 'maotai03', 'wanyeru', 4721867090, 1122569705,
            1091244780, 1448459094, 3940429450, 8059043600, 2944186618,
            'jake', 1921880323, 'yumilicai', 9927088462, 1552517314,
            1641150098, 'orangelin', '17kx', 'njbw1999', 9262059293,
            2431057144, 6677862831, 6474180344, 8058064790, 1948470766,
            1965949492, 'buyi', 1216640586, 'fhsx333', 'takumin',
            5082116371, 7777484873, 'onedot', 'meyspa', 'jinfenghaike',
            'jiangtao', 4043855103, 9203261121, 'junk', 9014255010,
            8138652508, 5048450435, 'hessenberg', 1240915616, 'aoliaking',
            2776244210, 'palebluedot', 7754027870, 8493390925, 'kafeimiao',
            8107994087, 8965749698, 'userfield', 'muzichanggong', 3104472653,
            'TDTTZ', 1545313154, 4300599669, 'windzixun', 'goldbutterfly',
            5395815496, 9842090891, '502deniu', 5498002897, 8082119199,
            'dabaojian', 1447263435, 7730004385, 9526723452, 8600616776,
            'douhun', 5941996397, 5112421699, 'eastStone', 4212721183,
            'rzxct', 9455009211, 'zhichangrongtouzi', 4318577537, 7875173101,
            'frankling', 'boertime', 1766828432, 4671022956, 'ysh999',
            1011339780, 8960894035, 'xiedonghui', 7513286104, 1414968394,
            8295448217, 'jiangkaijian', 2344817898, 5564897980, 1776484023,
            2597413145, 'survivor', 'xchenantai', 4428011814, 'shanhehu',
            5537986930, 'JJQQ', 3714977098, 1392782404, 4047351923,
            6185678262, 'kaycie', 7060402495, 'shiyutang', 8174076853,
            6929804901, 'sherry', 7500022239, 9641724592, 1047509468,
            'bornagainbuffett', 'oneyear', 8714373478, 'xcyk', 1340904670,
            'etfans', 1831827479, 2324897839, 3750902522, 9884766393,
            3915115654, 'whwei', 9868511750, 9904871344, 'threeqian',
            'cwtx', 5680395518, 9651781081, 5344802344, 'yiduomiao77',
            'beiji', 'xiankanhua', 8102984655, 'xgdp', 7937355531,
            4406747817, 2093877750, 'wangfan', 8800638849, 5158708788,
            'cobainhades', 'aliboshi', 5004331787, 'ronglingrui', 5233404610,
            4222486120, 5939653998, 4556118930, 'staghill', 5032728329,
            6529579984, 4136253585, 2403110704, 8628686400, 8142384897,
            'value', 1173786903, 'jiangjian', 'hzb19761', 5703996100,
            6987055001, 6093573275, 1332019576, 'gsrsngdd', 1697559028,
            5564515545, 'hbty', 1608596039, ]

    Name = {5171159182: '玩赚组合', 'assistant': '交易小助手',
            'huodong': '雪球活动', 'fangtan': '雪球访谈', 9485866208: '蛋卷基金', 8152922548: '今日话题', 'xueyingzhengquan': '雪盈证券',
            2709857861: '佰股精', 5828665454: '雪球私募', 3748823499: '雪球保险', 5964068708: '小小辛巴', 9887656769: '梁宏',
            6785033954: 'zangyn', 9528220473: '东博老股民', 8255849716: '跟我走吧14', 3037882447: '云蒙', 'shilaomao': '释老毛',
            'simon': '不明真相的群众', 6424252664: '弱弱的投资者', 'Value_at_Risk': '价值at风险', 'david_freedom': 'DAVID自由之路',
            'TQ1024': '唐史主任司马迁',
            9650668145: '管我财', 'funds': '银行螺丝钉', 2733321298: '瑞鹤仙_5876', 'lord': '金融之王', 8510627167: '进化论一平',
            'nysdy': '那一水的鱼', 1512170192: '西点老A', 'caomaolufei': '草帽路飞', 1175857472: '天南财务健康谈', 'backwasabi': '投星资产',
            2340719306: '流水白菜', 3491303582: '闲来一坐s话投资', 'etfs': 'ETF拯救世界', 9226205191: '处镜如初', 'comy28': '黄建平',
            8780033408: '昆山法律', 'yanbao': '没干货不废话', 2439489334: 'sosme', 9742512811: '丹书铁券', 'gtzhou': 'GT周',
            'dean_li': '丁丁谈股', 1062883669: '青春的泥沼', 6254918995: '小兵oo9', 'laogaowudao': '老高悟道', 4111857140: '山行',
            6146592061: '持有封基', 1102105103: '但斌', 'traveller1985': '一只特立独行的猪', 1127205381: '乔帮主123', 6413254712: '小权',
            'Mario': 'Mario', 'rickyzhong': 'Ricky', 2164183023: '钟华守正出奇', 'chrishine': '我是表好胚', 'zhuankan': '雪球专刊',
            'elephant': '坚信价值', 1538598451: '万法归宗', 'earlzhang': '张翼轸', 'hljj': '红利基金', 1760673340: 'HIS1963',
            'Thecherryking': '樱桃之王', 'tiandaoqiniu': '天道骑牛', 'michael_chen': '诸葛就是不亮', 1272530506: '岁寒知松柏',
            9206125741: '我是任俊杰',
            'laobeiao': '骑行夜幕的统计客', 'xykk': '逍遥狂客', 'xqwy': '电扫洛阳川', 1546206224: '飘仙的个人日记', 4779794911: '老刀101',
            'xingu': '非新不炒', 9640778912: '英科睿资鹰', 8291461932: '房杨凯', 7355827634: '微进化ing', 9905072371: '阿狸',
            'wdx_1984': '秃鹫投资', 8018540373: '国老', 4439117448: 'top_gun888', 'yufu': '渔_夫', 8240989798: '狼用波段',
            'zltz': '厚恩投资张延昆', 9813181917: '方何之子', 1324002892: '盛夏阿凯', 1674117751: '被解放的mogwai', 'wpeak': '西峯',
            'zhongdaqi': '大道平淡平安', 7610708650: '长安大湿人', 'conan': 'Conan的投资笔记', 1662576529: '庚白星君',
            'jingchengjiushao': '京城九少',
            'nick': '梁剑', 4877612337: 'Jacky一路向北', 'congsky': '岗仁波齐', 'lyujz': '吕健中', 6049709616: '朱胜国',
            8780946767: 'HTSC金融研究', 'AaronM': '宁静的冬日M', 1738642461: '老罗话指数投资', 'chenda': '陈达美股投资', 3464131377: '热门概念',
            8064062857: '怪盗KuU', 1373073106: '我是腾腾爸', 'xujiajie': '徐佳杰Pierre', 2915442382: 'Nainital的碎片哥',
            9097259018: '木鱼敬畏',
            3062205427: '小猪爱上牛', 9518372158: 'Stevevai1983', 'cozone': '柯中', 2785562330: '简放', 9586083092: '张可兴',
            7953251915: '百谷王', 'aaatu': '阿土哥a', 4433867848: '空仓屠龙', 2308207656: '虎鼎', 4106327074: 'weike369',
            8029098291: '心中无股HK', 'investor': '余晓光', 8107212038: 'i投资8', 9396837428: '沐阳1', 'olivia': 'O_Livia',
            5190345050: '梦心飞翔2018', 6981947864: '漫步者华越', 7351106301: '等着蚂蚁变大象', 9564664610: '归隐林地',
            'slowisquick': '大道无形我有型',
            5866067799: '安东尼奥188', 4027447937: '巴菲林奇小厄姆', 9603722416: '翰林院大牛1号', 8315885552: '海阳之星',
            1339778771: '风云海的干货店',
            'AAA_3': '疯狂_de_石头', 6867901973: '马马m假装在牛市', 2959851771: 'tkq007', 4248906337: '农民老张', 6160258782: '朱东',
            'Lagom': 'Lagom投资', 6832369826: '微光破晓-刘诚', 'guojingpu': '郭荆璞', 9428236477: '立春', 6510147098: '股海十三年',
            'xuzhihong': '许志宏', 'linjun168': '林隽', 'matias': 'matias', 4017847389: 'MeetDaDevil', 3408310156: '胡涂的森林',
            'tianduo': '天多', 'farfromu': '范小明', 9755618618: '黑暗时代', 2033624326: 'chris_jiang2002',
            1683036638: '童言无忌666666',
            1906328753: '吃跟着大v吃肉肉', 7315353232: '正合奇胜天舒', 7592287001: '风逝_98', 3055849674: '编程浪子',
            6078380931: '上兵伐谋zgz',
            1876614331: '陈绍霞', 9444904852: '北海茶客', 4074947120: '童思侃', 'aguilmkz': '阿贵龙门客栈', 2994748381: '证券市场红周刊',
            1314783718: '饕餮海', 'rathman': 'Rathman', 8592131633: '孥孥的大树', 'peter': '从易', 4743057813: '林奇法则',
            'tdxy': '天地侠影', 2595056894: '中国资本市场', 1421406103: '雨人12369', 'forcode': 'forcode', 'bobshan': 'BobShan',
            2859479813: '听风-春华秋实', 7694221981: '否极泰董宝珍', 3966435964: '慧博', 'wufaling': '自由老木头', 6753271936: '老庐2012',
            9047587905: 'okok74', 2657407918: '何纯在南国', 'hbyq': '华宝油气', 2100654541: '刺猬吃大饼', 1482535759: 'lezi1022',
            1638377010: '大隐无言', 'xiaoyaoguhai': '逍遥股海', 1722979527: '非完全进化体', 'wangli': '电子研究员', 'Terastar': 'Terastar',
            'lushanlin': '卢山林', 'fangyongsheng': '方舟88', 'panpan': '潘潘_策略投资', 'liyan': '李妍', 2536207007: '孙旭东',
            1604871976: '定位理论做投资', 'invescogreatwall': '景顺长城', 6928974450: '紫竹林的一艎', 1910783512: '看好股市的新人',
            'shuailang': '狼啸天',
            'yangchengdiyiniu': '羊城第一牛', 'mrmarket': '香港市場先生', 9883838696: '消失的救赎', 3881365268: '大杨',
            7146274836: '请大家尽量别转发',
            1940211456: 'greatsoup', 9761091523: 'homura', 2164748441: '医药商业', 7535271733: 'Julian-Z',
            2554781328: '学经济家',
            'Alwaleed': 'Alwaleed', 5962548939: '市值风云APP', 'royie': '刘志超', 4742988362: '狂龙十八段', 2276196460: '甲骨文先生',
            'quyueyue': '船长---', 6195589551: '铁公鸡金融', 1597430632: '南方基金', 7783401784: '安久套海通', 'moahmo': '摸啊摸',
            3638360312: '肖志刚', 'hikiwa': 'hikiwa', 1622002697: 'icefighter', 'iamu': 'u兄-万亿之路关善祥', 'maotai03': '茅台03',
            'wanyeru': '万佑希', 4721867090: '跨越巅峰', 1122569705: '小兵突围', 1091244780: '飞泥翱空', 1448459094: '无声',
            3940429450: '分析师徐彪', 8059043600: 'tulip郁金香', 2944186618: 'bztwang', 'jake': '林起', 1921880323: '败家老农民',
            'yumilicai': '优美', 9927088462: '一只花蛤', 1552517314: '闲人老钟', 1641150098: '医药邦', 'orangelin': '橙子lin',
            '17kx': '衣香人影2010', 'njbw1999': '南迦巴瓦1999', 9262059293: '杯酒人生', 2431057144: '老布', 6677862831: '滚一个雪球',
            6474180344: '荔慎投资梁军儒', 8058064790: '老曾阿牛', 1948470766: '关键是心态', 1965949492: '安安静静一个人', 'buyi': '布衣-淡定从容',
            1216640586: '孤鹰广雁', 'fhsx333': '阴阳鱼', 'takumin': 'Takun', 5082116371: '西雨牛仔', 7777484873: 'K线超人',
            'onedot': 'onedot', 'meyspa': 'meyspa', 'jinfenghaike': '金枫海客', 'jiangtao': '江涛', 4043855103: '放眼观美股',
            9203261121: '嘿嘿呀', 'junk': 'Scattergun', 9014255010: '铁臂阿桐木', 8138652508: '尹生', 5048450435: '-花无缺-',
            'hessenberg': '一蓑烟雨V', 1240915616: '舍得', 'aoliaking': '杨饭', 2776244210: '股市大作手', 'palebluedot': '北方的牛',
            7754027870: '海豚音', 8493390925: 'Ten-Bagger', 'kafeimiao': '咖啡喵', 8107994087: '9加加', 8965749698: '医药魔方',
            'userfield': 'userfield', 'muzichanggong': '木子长工', 3104472653: '天山龙江', 'TDTTZ': '土地堂堂主', 1545313154: '静气',
            4300599669: '德国留学炒美股', 'windzixun': 'Wind资讯', 'goldbutterfly': 'Mr-胡', 5395815496: '二元思考',
            9842090891: '量化小王子',
            '502deniu': '502的牛', 5498002897: '月下寒漪', 8082119199: '超级巴飞特', 'dabaojian': '剑胆琴心123', 1447263435: '青城山中鸟',
            7730004385: 'trustno1', 9526723452: 'laoduo', 8600616776: '沈潜', 'douhun': 'douhun', 5941996397: '股市药丸',
            5112421699: '雪鹤', 'eastStone': '东边的小石头', 4212721183: '道氏投资', 'rzxct': 'Tess', 9455009211: 'ruyanliu',
            'zhichangrongtouzi': '知常容', 4318577537: '投资舆情', 7875173101: '量化理财', 'frankling': '富兰克凌', 'boertime': '三宝同学',
            1766828432: '小卫之晓', 4671022956: '稳稳的福利', 'ysh999': '深圳价值投资者', 1011339780: '驱熊人', 8960894035: 'TOPCP',
            'xiedonghui': '炒饭锅锅', 7513286104: 'JJarod', 1414968394: '老肥叔叔', 8295448217: 'benjm-修',
            'jiangkaijian': 'Passion启航',
            2344817898: '联想控股', 5564897980: '江南愤青', 1776484023: '扑扑初心', 2597413145: '楊永清', 'survivor': '唯一幸存者',
            'xchenantai': '陈欣', 4428011814: '方烈', 'shanhehu': '橡谷投资-唐璞', 5537986930: '何田', 'JJQQ': '般若波罗蜜',
            3714977098: '老渔2014', 1392782404: '大只若鱼', 4047351923: '价值信徒', 6185678262: '独行者', 'kaycie': '栀子花开股海丶',
            7060402495: 'dq951163', 'shiyutang': '汤诗语', 8174076853: '仗剑割草', 6929804901: '医药代表只懂医药股', 'sherry': 'sherry',
            7500022239: '王雅媛victoria', 9641724592: 'Dinny_Sachs', 1047509468: '民工君', 'bornagainbuffett': '海不归BaB',
            'oneyear': '投资从入门到精通',
            8714373478: '美国消费', 'xcyk': '雪白血红', 1340904670: '机器喵', 'etfans': 'caskfans', 1831827479: '投资者摩西',
            2324897839: '天涯路', 3750902522: '股海为生869', 9884766393: '后来居上_Dioyan', 3915115654: '点拾投资', 'whwei': '麒睿',
            9868511750: '金鹰基金', 9904871344: '江浙小农', 'threeqian': '钱真理', 'cwtx': '刺猬偷腥', 5680395518: '中欧基金',
            9651781081: '大猪先森', 5344802344: '灰色钻石', 'yiduomiao77': '一朵喵', 'beiji': '北极', 'xiankanhua': '疯投哥',
            8102984655: 'jh786', 'xgdp': '香港大盘_香港本地', 7937355531: '小芥蓝', 4406747817: '聪明投资者', 2093877750: '白白的云',
            'wangfan': '无敌小凡人', 8800638849: '葛剑秋', 5158708788: '西湖-长线是金', 'cobainhades': '邓立君', 'aliboshi': '阿郦博士',
            5004331787: '可可老鼠', 'ronglingrui': '大道至简-荣令睿', 5233404610: '中巴价投研习社', 4222486120: '爱吃海鲜的鲸鱼',
            5939653998: '杨不留行',
            4556118930: '价值发现', 'staghill': '天月剑', 5032728329: '银和投资笔记', 6529579984: '辛无疾', 4136253585: '专诸',
            2403110704: '虾里巴人', 8628686400: '诗安', 8142384897: '白话投资', 'value': '老巴门下走狗', 1173786903: 'RanRan',
            'jiangjian': '姜真人', 'hzb19761': '黄祖斌', 5703996100: '空之轨跡', 6987055001: '小熊投资', 6093573275: 'an小安',
            1332019576: '正奇', 'gsrsngdd': '股市人生牛股多多', 1697559028: '雷动九天', 5564515545: '星星-奶爸', 'hbty': '华宝添益_现金宝',
            1608596039: 'Leo牛'}
    t = 1
    strday = '20180925'
    print(datetime.now().strftime("%Y-%m-%d"))
    e=list()
    for z in User:
        d=Read(t, z,strday,Name)
        try:
            e.extend(d)
            print("e=")
            print(e)
        except:
            pass

    return e

    # for z in User:
    #     Read(t, z,strday,Name)
# scheduler = BlockingScheduler()
# scheduler.add_job(job, 'cron', day_of_week='0-6', hour=15, minute=34)
# scheduler.start()
if __name__=="__main__":
    e=job()
    print(Counter(e))







