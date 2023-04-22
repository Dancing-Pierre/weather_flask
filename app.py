import datetime

import pandas as pd
import pymysql
from sqlalchemy import create_engine
from flask import Flask, render_template, session, redirect, url_for, request
from functools import wraps
from flask_paginate import Pagination

from forecast.forecast import pred_sea
from models import *
import random
from forecast import forecast

import requests
from lxml import etree
from search import SearchForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/tianqi?charset=utf8'
app.secret_key = "lycsdf"
app.config['SESSION_COOKIE_NAME'] = "session_key"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

city_data = {'北京': 'beijing', '天津': 'tianjin', '上海': 'shanghai', '重庆': 'chongqing', '广州': 'guangzhou',
             '深圳': 'shenzhen', '杭州': 'hangzhou', '成都': 'chengdu', '石家庄': 'shijiazhuang',
             '唐山': 'tangshan',
             '秦皇岛': 'qinhuangdao', '保定': 'baoding', '张家口': 'zhangjiakou', '邯郸': 'handan',
             '邢台': 'xingtai',
             '承德': 'chengde', '沧州': 'cangzhou', '廊坊': 'langfang', '衡水': 'hengshui', '太原': 'taiyuan',
             '大同': 'datong', '阳泉': 'yangquan', '长治': 'changzhi', '临汾': 'linfen', '晋城': 'jincheng',
             '朔州': 'shuozhou', '运城': 'sxyuncheng', '忻州': 'xinzhou', '吕梁': 'lvliang', '晋中': 'jinzhong',
             '呼和浩特': 'huhehaote', '包头': 'baotou', '鄂尔多斯': 'eerduosi', '乌海': 'wuhai',
             '赤峰': 'chifeng',
             '通辽': 'tongliao', '巴彦淖尔': 'bayannaoer', '沈阳': 'shenyang', '大连': 'dalian',
             '丹东': 'dandong',
             '营口': 'yingkou', '盘锦': 'panjin', '葫芦岛': 'huludao', '鞍山': 'anshan', '锦州': 'jinzhou',
             '本溪': 'benxi', '瓦房店': 'wafangdian', '长春': 'changchun', '吉林': 'jilin', '四平': 'siping',
             '辽源': 'liaoyuan', '白山': 'baishan', '松原': 'songyuan', '白城': 'baicheng', '延边': 'yanbian',
             '通化': 'tonghua', '哈尔滨': 'haerbin', '齐齐哈尔': 'qiqihaer', '鸡西': 'jixi', '鹤岗': 'hegang',
             '双鸭山': 'shuangyashan', '大庆': 'daqing', '佳木斯': 'jiamusi', '七台河': 'qitaihe',
             '南京': 'nanjing',
             '无锡': 'wuxi', '徐州': 'xuzhou', '常州': 'changzhou', '苏州': 'suzhou', '南通': 'nantong',
             '连云港': 'lianyungang', '淮安': 'huaian', '盐城': 'yancheng', '扬州': 'yangzhou',
             '镇江': 'zhenjiang',
             '泰州': 'jstaizhou', '宿迁': 'suqian', '宁波': 'ningbo', '温州': 'wenzhou', '嘉兴': 'jiaxing',
             '湖州': 'huzhou', '金华': 'jinhua', '衢州': 'quzhou', '舟山': 'zhoushan', '台州': 'taizhou',
             '丽水': 'lishui', '绍兴': 'shaoxing', '义乌': 'yiwu', '富阳': 'zjfuyang', '临安': 'linan',
             '合肥': 'hefei',
             '芜湖': 'wuhu', '蚌埠': 'bangbu', '淮南': 'huainan', '马鞍山': 'maanshan', '淮北': 'huaibei',
             '铜陵': 'tongling', '安庆': 'anqing', '黄山': 'huangshan', '滁州': 'chuzhou', '阜阳': 'fuyang',
             '宿州': 'anhuisuzhou', '福州': 'fujianfuzhou', '厦门': 'xiamen', '泉州': 'quanzhou',
             '莆田': 'putian',
             '三明': 'sanming', '漳州': 'zhangzhou', '南平': 'nanping', '龙岩': 'longyan', '宁德': 'ningde',
             '南昌': 'nanchang', '景德镇': 'jingdezhen', '萍乡': 'pingxiang', '新余': 'xinyu',
             '鹰潭': 'yingtan',
             '赣州': 'ganzhou', '宜春': 'jxyichun', '抚州': 'fuzhou', '九江': 'jiujiang', '上饶': 'shangrao',
             '吉安': 'jian', '济南': 'jinan', '青岛': 'qingdao', '淄博': 'zibo', '枣庄': 'zaozhuang',
             '东营': 'dongying', '烟台': 'yantai', '潍坊': 'weifang', '济宁': 'sdjining', '泰安': 'taian',
             '威海': 'weihai', '日照': 'rizhao', '莱芜': 'laiwu', '临沂': 'linyi', '郑州': 'zhengzhou',
             '洛阳': 'lvyang', '平顶山': 'pingdingshan', '鹤壁': 'hebi', '焦作': 'jiaozuo', '漯河': 'luohe',
             '三门峡': 'sanmenxia', '南阳': 'nanyang', '商丘': 'shangqiu', '信阳': 'xinyang', '周口': 'zhoukou',
             '驻马店': 'zhumadian', '武汉': 'wuhan', '十堰': 'shiyan', '宜昌': 'yichang', '鄂州': 'ezhou',
             '荆门': 'jingmen', '孝感': 'xiaogan', '黄冈': 'huanggang', '咸宁': 'xianning', '黄石': 'huangshi',
             '恩施': 'enshi', '襄阳': 'xiangyang', '随州': 'suizhou', '荆州': 'jingzhou', '长沙': 'changsha',
             '株洲': 'zhuzhou', '湘潭': 'xiangtan', '常德': 'changde', '张家界': 'zhangjiajie',
             '益阳': 'yiyang',
             '郴州': 'chenzhou', '永州': 'yongzhou', '怀化': 'huaihua', '娄底': 'loudi', '邵阳': 'shaoyang',
             '岳阳': 'yueyang', '湘西': 'xiangxi', '衡阳': 'hengyang', '韶关': 'shaoguan', '珠海': 'zhuhai',
             '汕头': 'shantou', '佛山': 'foshan', '江门': 'jiangmen', '肇庆': 'zhaoqing', '惠州': 'huizhou',
             '河源': 'heyuan', '清远': 'gdqingyuan', '东莞': 'dongguang', '中山': 'zhongshan',
             '南宁': 'nanning',
             '柳州': 'liuzhou', '北海': 'beihai', '桂林': 'guilin', '梧州': 'wuzhou', '防城港': 'fangchenggang',
             '钦州': 'gxqinzhou', '贵港': 'guigang', '玉林': 'guangxiyulin', '百色': '', '贺州': 'hezhou',
             '河池': 'hechi', '来宾': 'laibin', '崇左': 'chongzuo', '海口': 'haikou', '三亚': 'sanya',
             '自贡': 'zigong',
             '攀枝花': 'panzhihua', '泸州': 'luzhou', '德阳': 'deyang', '绵阳': 'mianyang', '广元': 'guangyuan',
             '遂宁': 'scsuining', '乐山': 'leshan', '南充': 'nanchong', '眉山': 'meishan', '贵阳': 'guiyang',
             '六盘水': 'liupanshui', '遵义': 'zunyi', '安顺': 'anshun', '毕节': 'bijie', '铜仁': 'tongren',
             '黔西南': 'qianxinan', '黔南': 'qiannan', '黔东南': 'qiandongnan', '昆明': 'kunming',
             '玉溪': 'yuxi',
             '保山': 'baoshan', '昭通': 'zhaotong', '丽江': 'lijiang', '临沧': 'lincang',
             '西双版纳': 'xishuangbanna',
             '德宏': 'dehong', '怒江': 'nujiang', '大理': 'dali', '曲靖': 'qujing', '拉萨': 'lasa',
             '林芝': 'linzhi',
             '山南': 'shannan', '昌都': 'changdu', '日喀则': 'rikaze', '阿里': 'ali', '那曲': 'naqu',
             '西安': 'xian',
             '铜川': 'tongchuan', '宝鸡': 'baoji', '咸阳': 'xianyang', '渭南': 'weinan', '延安': 'yanan',
             '汉中': 'hanzhong', '榆林': 'yulin', '安康': 'ankang', '商洛': 'shanglv', '兰州': 'lanzhou',
             '嘉峪关': 'jiayuguan', '天水': 'tianshui', '武威': 'wuwei', '张掖': 'zhangye', '平凉': 'pingliang',
             '酒泉': 'jiuquan', '庆阳': 'gsqingyang', '定西': 'dingxi', '甘南': 'gannan', '临夏': 'linxia',
             '白银': 'baiyin', '金昌': 'jinchang', '陇南': 'longnan', '西宁': 'xining', '海东': 'haidong',
             '果洛': 'guolv', '海北': 'haibei', '海南': 'hainan', '海西': 'haixi', '玉树': 'yushu',
             '黄南': 'huangnan',
             '银川': 'yinchuan', '石嘴山': 'shizuishan', '吴忠': 'wuzhong', '固原': 'nxguyuan',
             '中卫': 'zhongwei',
             '乌鲁木齐': 'wulumuqi', '伊犁哈萨克州': 'yili', '克拉玛依': 'kelamayi', '哈密': 'hami',
             '石河子': 'shihezi', '和田': 'hetian', '五家渠': 'wujiaqu', '阿克苏': 'akesu'}
# UA池
ua_all = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/531.2 (KHTML, like Gecko) Chrome/41.0.872.0 Safari/531.2",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows CE; Trident/4.0)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0) AppleWebKit/531.11.4 (KHTML, like Gecko) Version/5.0.2 Safari/531.11.4",
    "Mozilla/5.0 (compatible; MSIE 7.0; Windows 98; Trident/3.1)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 10.0; Trident/5.1)",
    "Opera/8.89.(Windows NT 10.0; lb-LU) Presto/2.9.175 Version/10.00",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/51.0.800.0 Safari/532.2",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/532.16.1 (KHTML, like Gecko) Version/4.0.1 Safari/532.16.1",
    "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; Trident/4.0)",
    "Mozilla/5.0 (compatible; MSIE 5.0; Windows NT 5.1; Trident/4.0)",
    "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.2; Trident/4.1)",
    "Opera/8.96.(Windows CE; yue-HK) Presto/2.9.187 Version/10.00",
    "Mozilla/5.0 (Windows; U; Windows CE) AppleWebKit/534.27.7 (KHTML, like Gecko) Version/4.0.3 Safari/534.27.7",
    "Mozilla/5.0 (compatible; MSIE 5.0; Windows NT 4.0; Trident/5.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.01; Trident/5.1)",
    "Mozilla/5.0 (Windows NT 6.2; sid-ET; rv:1.9.1.20) Gecko/2013-03-13 19:12:24 Firefox/3.6.7",
    "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 6.1; Trident/5.1)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows CE; Trident/3.1)",
    "Mozilla/5.0 (Windows; U; Windows 95) AppleWebKit/532.41.1 (KHTML, like Gecko) Version/5.1 Safari/532.41.1",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.0; Trident/5.1)",
    "Mozilla/5.0 (Windows NT 6.0; wo-SN; rv:1.9.0.20) Gecko/2012-07-06 02:36:31 Firefox/3.8",
    "Mozilla/5.0 (compatible; MSIE 6.0; Windows 95; Trident/3.1)",
    "Mozilla/5.0 (Windows 95; sc-IT; rv:1.9.0.20) Gecko/2016-03-02 10:47:38 Firefox/3.6.7",
    "Mozilla/5.0 (compatible; MSIE 5.0; Windows NT 5.1; Trident/4.0)",
    "Mozilla/5.0 (compatible; MSIE 7.0; Windows CE; Trident/3.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.0; Trident/5.1)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows 95; Trident/5.1)",
    "Opera/8.39.(Windows 95; da-DK) Presto/2.9.178 Version/10.00",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1) AppleWebKit/535.25.5 (KHTML, like Gecko) Version/4.0 Safari/535.25.5",
    "Opera/9.22.(Windows NT 5.1; szl-PL) Presto/2.9.170 Version/11.00",
    "Opera/8.69.(Windows NT 6.1; ff-SN) Presto/2.9.166 Version/10.00",
    "Mozilla/5.0 (Windows 98) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/27.0.895.0 Safari/535.1",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.2; Trident/3.0)",
    "Opera/9.97.(Windows NT 10.0; uz-UZ) Presto/2.9.170 Version/11.00",
    "Mozilla/5.0 (Windows CE) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/17.0.897.0 Safari/535.1",
    "Opera/9.49.(Windows NT 5.01; ar-MR) Presto/2.9.187 Version/10.00",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.2; Trident/5.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 4.0; Trident/5.1)",
    "Opera/9.81.(Windows NT 5.01; ar-OM) Presto/2.9.169 Version/10.00",
    "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.2; Trident/4.0)",
    "Mozilla/5.0 (compatible; MSIE 5.0; Windows NT 5.0; Trident/5.0)",
    "Opera/9.75.(Windows NT 5.1; ps-AF) Presto/2.9.178 Version/11.00",
    "Opera/8.22.(Windows NT 4.0; tcy-IN) Presto/2.9.181 Version/10.00",
    "Opera/9.91.(Windows NT 5.0; ga-IE) Presto/2.9.177 Version/10.00",
    "Opera/8.70.(Windows NT 5.1; ti-ER) Presto/2.9.163 Version/12.00",
    "Opera/8.35.(Windows 98; Win 9x 4.90; sc-IT) Presto/2.9.186 Version/11.00",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.0 (KHTML, like Gecko) Chrome/55.0.809.0 Safari/535.0",
    "Opera/9.50.(Windows NT 6.0; xh-ZA) Presto/2.9.180 Version/10.00",
    "Mozilla/5.0 (compatible; MSIE 5.0; Windows NT 6.2; Trident/5.1)",
    "Opera/9.28.(Windows NT 5.0; yi-US) Presto/2.9.165 Version/11.00"]
# 爬虫
header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh-TW;q=0.9,zh;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "tianqihoubao.com",
    "User-Agent": random.choice(ua_all),
}

conn = pymysql.Connection(
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    charset='utf8',
    db='tianqi',
)
cursor = conn.cursor()


def get_data(city, city_pinyin, date):
    date = date[0:6]
    url = f'http://tianqihoubao.com/aqi/{city_pinyin}-{date}.html'
    a = requests.get(url=url, headers=header)
    data = etree.HTML(a.text)
    print(data)
    data = data.xpath('//table//tr[position()>1]')
    for i in data:
        date = ''.join(i.xpath('./td[1]//text()')).replace("-", "").replace(" ", "").replace("\n", "").replace(
            "\r", "")
        aqi = ''.join(i.xpath('./td[3]//text()')).replace(" ", "").replace("\n", "").replace("\r", "")
        pm25 = ''.join(i.xpath('./td[5]//text()')).replace(" ", "").replace("\n", "").replace("\r", "")
        pm10 = ''.join(i.xpath('./td[6]//text()')).replace(" ", "").replace("\n", "").replace("\r", "")
        write_data_to_db(city, date, aqi, pm25, pm10)


def write_data_to_db(city, date, aqi, pm25, pm10):
    cursor.execute("INSERT INTO data (城市, 日期, aqi, `pm2.5`, pm10) VALUES (%s, %s, %s, %s, %s)",
                   (city, date, aqi, pm25, pm10))


def user_login(f):
    """
    登录装饰器
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "uname" not in session:
            return redirect(url_for("login_post"))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def hello_world():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    results = User.query.filter(User.username == username).first()
    if results:
        if results.password == password:
            session['uname'] = username
            if username == 'admin':
                session['cate'] = 2
            else:
                session['cate'] = 1
            return render_template('index.html')
        else:
            return render_template('login.html', login_result='密码错误')
    else:
        return render_template('login.html', login_result='用户不存在')


@app.route('/register', methods=['POST', 'Get'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        results = User.query.filter(User.username == username).first()
        if results:
            result = '用户已存在，请重新注册'
            return render_template('register.html', login_result=result)
        else:
            new_user1 = User(username=username, password=password)
            db.session.add(new_user1)
            db.session.commit()
        return render_template('login.html')
    else:
        return render_template('register.html')


@app.route('/logout')
def logout():
    # 直接调用logout_user函数退出，里面实质封装了对session信息的清除
    session.clear()
    return redirect(url_for('hello_world'))


@app.route('/index')
def index():    return render_template('index.html')


@app.route('/people')
def people():
    query = "SELECT * FROM clean WHERE city = '牡丹江'"
    data = pd.read_sql_query(query, engine)
    data1 = data['风向'].value_counts()
    people_max_val = list(data1.index)
    people_max_num = list(data1)
    print(people_max_val)
    print(people_max_num)
    return render_template('people.html', people_max_val=people_max_val, people_max_num=people_max_num)


@app.route('/star')
def star():
    # data = pd.read_csv('clean.csv')
    # data = data[data['city'] == '牡丹江']
    query = "SELECT * FROM clean WHERE city = '牡丹江'"
    data = pd.read_sql_query(query, engine)
    counts = data['aqiinfo'].value_counts()
    star_count = []
    for item in range(len(list(counts.index))):
        star_count.append((list(counts.index)[item], list(counts)[item]))
    return render_template('star.html', star_count=star_count)


@app.route('/rec')
def rec():
    # data = pd.read_csv('clean.csv')
    # data = data[data['city'] == '牡丹江']
    query = "SELECT * FROM clean WHERE city = '牡丹江'"
    data = pd.read_sql_query(query, engine)
    val = list(data['日期'])[-300:]
    num_high = list(data['aqi'])[-300:]
    return render_template('rec.html', val=val, num_high=num_high)


@app.route('/cloud')
def cloud():
    # data = pd.read_csv('clean.csv')
    # data = data[data['city'] == '牡丹江']
    query = "SELECT * FROM clean WHERE city = '牡丹江'"
    data = pd.read_sql_query(query, engine)
    counts = data.sort_values(by='日期', ascending=True)
    # counts=counts.head(50)
    val = list(counts['日期'])[-300:]
    num_high = list(counts['最高温度'])[-300:]
    num_low = list(counts['最低温度'])[-300:]
    return render_template('cloud.html', val=val, num_high=num_high, num_low=num_low)


@app.route('/diqu')
def diqu():
    # data = pd.read_csv('clean.csv')
    # data = data[data['日期'] == '2023-02-26']
    query = "SELECT * FROM clean WHERE 日期 = '2023-02-26'"
    data = pd.read_sql_query(query, engine)

    val = list(data['city'])
    num_high = list(data['最高温度'])
    num_low = list(data['最低温度'])
    return render_template('diqu.html', val=val, num_high=num_high, num_low=num_low)


@app.route('/data')
def data():
    # df = pd.read_csv('weatherdata.csv')
    # values = []
    # for i, r in df.iterrows():
    #     values.append(r)
    query = "SELECT * FROM weatherdata"
    data = pd.read_sql_query(query, engine)
    values = data.to_dict('records')
    limit = 15
    page = int(request.args.get("page", 1))
    start = (page - 1) * limit
    # 返回数据
    row = len(values)
    print(row)
    end = page * limit if row > page * limit else row
    paginate = Pagination(page=page, per_page=limit, total=row)
    ret = values[start:end]
    print(ret)
    return render_template('data.html', films=ret, paginate=paginate)


@app.route('/clean')
def clean():
    query = "SELECT * FROM weatherdata WHERE 日期 IS NOT NULL AND 最高温度 IS NOT NULL AND 最低温度 IS NOT NULL AND 天气 IS NOT NULL AND 风向 IS NOT NULL AND 风力 IS NOT NULL AND aqi IS NOT NULL AND aqiinfo IS NOT NULL AND aqilevel IS NOT NULL AND city IS NOT NULL"
    data = pd.read_sql_query(query, engine)
    values = data.to_dict('records')
    limit = 15
    page = int(request.args.get("page", 1))
    start = (page - 1) * limit
    # 返回数据
    row = len(values)
    print(row)
    end = page * limit if row > page * limit else row
    paginate = Pagination(page=page, per_page=limit, total=row)
    ret = values[start:end]
    return render_template('clean.html', films=ret, paginate=paginate)


@app.route('/view', methods=['GET', 'POST'])
def view():
    from city import find_province
    form = SearchForm()
    if form.validate_on_submit():
        city = form.city.data
        date = form.date.data
        while True:
            query = "SELECT * FROM data WHERE 城市='%s' and 日期='%s'" % (city, date)
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                data_form = {'city': city, 'AQI': result[2], 'PM25': result[3],
                             'PM10': result[4], 'province': find_province(city)}
                return render_template('view.html', form=SearchForm(), info=data_form)
            else:
                city_pinyin = city_data[f'{city}']
                get_data(city, city_pinyin, date)
        # 处理数据并返回结果
    else:
        return render_template('view.html', form=form)


@app.route('/search', methods=['GET', 'POST'])
def search():
    search_name = request.args.get("area")
    if search_name:
        query = f"SELECT * FROM weatherdata WHERE 日期 IS NOT NULL AND 最高温度 IS NOT NULL AND 最低温度 IS NOT NULL AND 天气 IS NOT NULL AND 风向 IS NOT NULL AND 风力 IS NOT NULL AND aqi IS NOT NULL AND aqiinfo IS NOT NULL AND aqilevel IS NOT NULL AND city = '{search_name}'"
    else:
        query = "SELECT * FROM weatherdata WHERE 日期 IS NOT NULL AND 最高温度 IS NOT NULL AND 最低温度 IS NOT NULL AND 天气 IS NOT NULL AND 风向 IS NOT NULL AND 风力 IS NOT NULL AND aqi IS NOT NULL AND aqiinfo IS NOT NULL AND aqilevel IS NOT NULL AND city IS NOT NULL"
    data = pd.read_sql_query(query, engine)
    values = data.to_dict('records')
    limit = 15
    page = int(request.args.get("page", 1))
    start = (page - 1) * limit
    # 返回数据
    row = len(values)
    print(row)
    end = page * limit if row > page * limit else row
    paginate = Pagination(page=page, per_page=limit, total=row)
    ret = values[start:end]
    print(ret)
    return render_template('clean.html', films=ret, paginate=paginate)


@app.route('/forecast_main', methods=['get'])
def forecast_main():
    return render_template('forecast.html')


@app.route('/forecast', methods=['get', 'POST'])
def forecast():
    # 从前端接收数据
    if request.form['city'] and request.form['year'] and request.form['month'] and request.form['day']:
        city = int(request.form['city'])
        year = int(request.form['year'])
        month = int(request.form['month'])
        day = int(request.form['day'])
        dataX = [city, year, month, day]
        print(data)
        if year <= 2018:
            result = f'年份太早'
            return render_template('forecast.html', result=result)
        elif year >= 2024:
            result = f'年份太长，预测数据不准'
            return render_template('forecast.html', result=result)
        else:
            if 1 <= month <= 12:
                if 1 <= day <= 31:
                    dataX = pd.DataFrame(dataX)
                    dataX = dataX.T
                    data_dict = pred_sea(dataX)
                    return render_template('forecast.html', file=data_dict,
                                           result=f'{year}年{month}月{day}日 后面三天的空气质量数据预测成功')
                else:
                    result = f'日期不存在！'
                    return render_template('forecast.html', result=result)
            else:
                result = f'月份输入错误！'
                return render_template('forecast.html', result=result)
    else:
        result = f'输入框不可为空'
        return render_template('forecast.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
