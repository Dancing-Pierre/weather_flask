# weather_display_system
基于Python爬虫+flask框架+echarts的天气展示系统

# 1、app.py

## 主功能

```python
@app.route('/view', methods=['GET', 'POST'])
def view():
    from city import find_province
    form = SearchForm()
    if form.validate_on_submit():
        # 接收前端输入框输入的城市和时间
        city = form.city.data
        date = form.date.data
        while True:
            # 判断输入的数据在data.csv是否能查到
            data = read_data_from_csv(city, date)
            if data:
                # 查到直接把数据返回前端
                data_form = {'city': city, 'AQI': data[0], 'PM25': data[1],
                             'PM10': data[2], 'province': find_province(city)}
                print(data_form)
                return render_template('view.html', form=SearchForm(), info=data_form)
            else:
                # 查不到开始爬虫
                city_pinyin = city_data[f'{city}']
                get_data(city, city_pinyin, date)
    else:
        return render_template('view.html', form=form)
```

## 爬虫

```python
# 接收输入的城市，转化为拼音，拼接爬虫请求的链接用
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

# UA池，一定程度上防止反扒
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

# 请求头
header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh-TW;q=0.9,zh;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "tianqihoubao.com",
    "User-Agent": random.choice(ua_all),
}

# 爬虫函数
def get_data(city, city_pinyin, date):
    date = date[0:6]
    url = f'http://tianqihoubao.com/aqi/{city_pinyin}-{date}.html'
    a = requests.get(url=url, headers=header)
    # 返回数据转化为树结构
    data = etree.HTML(a.text)
    print(data)
    # 取祖宗节点
    data = data.xpath('//table//tr[position()>1]')
    for i in data:
        # xpath获取数据
        date = ''.join(i.xpath('./td[1]//text()')).replace("-", "").replace(" ", "").replace("\n", "").replace(
            "\r", "")
        aqi = ''.join(i.xpath('./td[3]//text()')).replace(" ", "").replace("\n", "").replace("\r", "")
        pm25 = ''.join(i.xpath('./td[5]//text()')).replace(" ", "").replace("\n", "").replace("\r", "")
        pm10 = ''.join(i.xpath('./td[6]//text()')).replace(" ", "").replace("\n", "").replace("\r", "")
        # 写入cav
        write_data_to_csv(city, date, aqi, pm25, pm10)
```

## 其他

```python
# 从csv读取数据方法
def read_data_from_csv(city, date):
    with open('data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == city and row[1] == date:
                return row[2], row[3], row[4]
        return None
 
# 爬虫csv方法
def write_data_to_csv(city, date, aqi, pm25, pm10):
    with open('data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([city, date, aqi, pm25, pm10])


#  如果存储数据的CSV文件不存在，则创建文件，并写入表头
if not os.path.isfile('data.csv'):
    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['城市', '日期', 'aqi', 'pm2.5', 'pm10'])
```

# 2、view.html

```html
{% extends 'base.html' %}
{% block content %}

    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=EDGE">

	// css定义前端样式
    <style>
        #china-map {
            width: 1000px;
            height: 1000px;
            margin: auto;
        }

        #box {
            display: none;
            background-color: goldenrod;
            width: 180px;
            height: 90px;
            text-align: center;
        }

        #box-title {
            display: block;
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 5px;
        }

        #aqi, #pm2_5, #pm10 {
            display: block;
            font-size: 14px;
            margin-top: 5px;
        }

        form {
            display: flex;
            justify-content: center;
        }

        label {
            display: inline-block;
            width: 60px;
            text-align: right;
        }

        input {
            width: 200px;
            margin-right: 20px;
        }

        button {
            width: 80px;
            margin-left: 30px;
            border: none;
        }

        #map {
            margin-top: 20px;
        }

        .map-info {
            background-color: #6F6F6F;
            color: #fff;
            width: 7vw;
            padding: 0.5vw;
            border-radius: 10% 10%;
            position: absolute;
            right: 8vw;
            bottom: 0.5vh;
        }

        /* Updated CSS styles for legend */
        .legend {
            position: absolute;
            bottom: 5px;
            right: 25px;
            background-color: #fff;
            border: none;
            padding: 5px;
            font-size: 14px;
            top: 700px;
            left: 50px;
        }

        .legend td, .legend th {
            text-align: center;
            padding: 5px;
            border: 1px solid black;
        }

        .good {
            background-color: #00E400;
        }

        .moderate {
            background-color: #FFFF00;
        }

        .unhealthy-sensitive {
            background-color: #FF7E00;
        }

        .unhealthy {
            background-color: #FF0000;
        }

        .very-unhealthy {
            background-color: #8F3F97;
        }

        .hazardous {
            background-color: #7E0023;
            color: #FFF;
        }

    </style>

    <script type="text/javascript" src="../static/js/jquery.min.js"></script>
    <script type="text/javascript" src="../static/js/echarts.min.js"></script>
    <script type="text/javascript" src="../static/js/map/china.js"></script>

	// 城市日期输入框和按钮
    <form id="map" method="POST" action="{{ url_for('view') }}">
        {{ form.csrf_token }}
        <label for="city-input">城市：</label>
        {{ form.city(size=20) }}
        <label for="date-input">日期：</label>
        {{ form.date(size=20) }}
        <button id="search-button" type="submit">搜索</button>
    </form>

	// 返回数据的弹窗
    {% if info %}
        <div class="map-info">
            <div class="info-item">城市：{{ info.city }}</div>
            <div class="info-item">AQI：{{ info.AQI }}</div>
            <div class="info-item">PM25：{{ info.PM25 }}</div>
            <div class="info-item">PM10：{{ info.PM10 }}</div>
        </div>
    {% endif %}

    <div style="text-align:center;clear:both;">
        <script src="/gg_bd_ad_720x90.js" type="text/javascript"></script>
        <script src="/follow.js" type="text/javascript"></script>
    </div>

	// 用echarts的中国地图
    <button id="back"></button>
    <div id="china-map"></div>

	// 左下角图例
    <div>
        <table class="legend">
            <tr>
                <th>AQI范围</th>
                <th>空气质量指数级别</th>
            </tr>
            <tr class="good">
                <td>0-50</td>
                <td>优</td>
            </tr>
            <tr class="moderate">
                <td>51-100</td>
                <td>良</td>
            </tr>
            <tr class="unhealthy-sensitive">
                <td>101-150</td>
                <td>轻度污染</td>
            </tr>
            <tr class="unhealthy">
                <td>151-200</td>
                <td>中度污染</td>
            </tr>
            <tr class="very-unhealthy">
                <td>201-300</td>
                <td>重度污染</td>
            </tr>
            <tr class="hazardous">
                <td>301-500</td>
                <td>严重污染</td>
            </tr>
        </table>
    </div>

	// 中国地图的js文件
    <script>
        var myChart = echarts.init(document.getElementById('china-map'));
        var oBack = document.getElementById("back");
        var oPopup = document.getElementById("popup");
        var oBox = document.getElementById("box");
        var oBoxTitle = document.getElementById("box-title");
        var oAqi = document.getElementById("aqi");
        var oPm2_5 = document.getElementById("pm2_5");
        var oPm10 = document.getElementById("pm10");

        var provinces = ['shanghai', 'hebei', 'shanxi', 'neimenggu', 'liaoning', 'jilin', 'heilongjiang', 'jiangsu', 'zhejiang', 'anhui', 'fujian', 'jiangxi', 'shandong', 'henan', 'hubei', 'hunan', 'guangdong', 'guangxi', 'hainan', 'sichuan', 'guizhou', 'yunnan', 'xizang', 'shanxi1', 'gansu', 'qinghai', 'ningxia', 'xinjiang', 'beijing', 'tianjin', 'chongqing', 'xianggang', 'aomen'];

        var provincesText = ['上海', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '广西', '海南', '四川', '贵州', '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆', '北京', '天津', '重庆', '香港', '澳门'];

        var seriesData = [
            {
                name: '北京',
                value: 100
            }, {
                name: '天津',
                value: 0
            }, {
                name: '上海',
                value: 60
            }, {
                name: '重庆',
                value: 0
            }, {
                name: '河北',
                value: 60
            }, {
                name: '河南',
                value: 60
            }, {
                name: '云南',
                value: 0
            }, {
                name: '辽宁',
                value: 0
            }, {
                name: '黑龙江',
                value: 0
            }, {
                name: '湖南',
                value: 60
            }, {
                name: '安徽',
                value: 0
            }, {
                name: '山东',
                value: 60
            }, {
                name: '新疆',
                value: 0
            }, {
                name: '江苏',
                value: 0
            }, {
                name: '浙江',
                value: 0
            }, {
                name: '江西',
                value: 0
            }, {
                name: '湖北',
                value: 60
            }, {
                name: '广西',
                value: 60
            }, {
                name: '甘肃',
                value: 0
            }, {
                name: '山西',
                value: 60
            }, {
                name: '内蒙古',
                value: 0
            }, {
                name: '陕西',
                value: 0
            }, {
                name: '吉林',
                value: 0
            }, {
                name: '福建',
                value: 0
            }, {
                name: '贵州',
                value: 0
            }, {
                name: '广东',
                value: 597
            }, {
                name: '青海',
                value: 0
            }, {
                name: '西藏',
                value: 0
            }, {
                name: '四川',
                value: 60
            }, {
                name: '宁夏',
                value: 0
            }, {
                name: '海南',
                value: 60
            }, {
                name: '台湾',
                value: 0
            }, {
                name: '香港',
                value: 0
            }, {
                name: '澳门',
                value: 0
            }];

        oBack.onclick = function () {
            initEcharts("china", "中国");
        };

        initEcharts("china", "中国");

        // 初始化echarts
        function initEcharts(pName, Chinese_) {
            var tmpSeriesData = pName === "china" ? seriesData : [];

            var option = {
                title: {
                    text: Chinese_ || pName,
                    left: 'center'
                },
                tooltip: {
                    show: true,
                    trigger: 'item',
                    alwaysShowContent: false,
                    showContent: false,
                },
                series: [
                    {
                        name: Chinese_ || pName,
                        type: 'map',
                        mapType: pName,
                        roam: false,//是否开启鼠标缩放和平移漫游
                        data: tmpSeriesData,
                        top: "3%",//组件距离容器的距离
                        zoom: 1.1,
                        //selectedMode: 'single',
                        selectedMode: false, // 禁止点击选中
                        silent: true, // 禁止地图上的省份响应鼠标事件

                        label: {
                            normal: {
                                show: true,//显示省份标签
                                textStyle: {color: "#fbfdfe"}//省份标签字体颜色
                            },
                            emphasis: {//对应的鼠标悬浮效果
                                show: true,
                                textStyle: {color: "#323232"}
                            }
                        },
                        itemStyle: {
                            normal: {
                                borderWidth: .5,//区域边框宽度
                                borderColor: '#0550c3',//区域边框颜色
                                areaColor: "#4ea397",//区域颜色

                            },

                            emphasis: {
                                borderWidth: .5,
                                borderColor: '#4b0082',
                                areaColor: "#ece39e",
                            }
                        },
                    }
                ]

            };

            myChart.setOption(option);

            myChart.off("click");

            if (pName === "china") { // 全国时，添加click 进入省级
                {% if info %}
                    let dataIndex = 0;
                    for (let i = 0; i < seriesData.length; i++) {
                        if (seriesData[i]['name'] == '{{ info.province }}') {
                            dataIndex = i;
                            break;
                        }
                    }
                    // 移动鼠标禁止高亮
                    myChart.on('mouseover', function (param) {
                        for (let i = 0; i < seriesData.length; i++) {
                            if (i != dataIndex) {
                                myChart.dispatchAction({
                                    type: 'downplay',
                                    dataIndex: i
                                });
                            }
                        }
                    });
                {% endif %}
            }
        }


        {% if info %}

            let dataIndex = 0;
            for (let i = 0; i < seriesData.length; i++) {
                if (seriesData[i]['name'] == '{{ info.province }}') {
                    dataIndex = i;
                    break;
                }
            }

            myChart.dispatchAction({
                type: 'highlight',
                dataIndex,
            });

        {% endif %}
    </script>
{% endblock %}
```

