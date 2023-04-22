import requests
import pandas as pd
import re
import urllib.request

months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
years = [2018, 2019, 2020, 2021, 2022, 2023]
city = {
    '大兴安岭': 50442,
    '黑河': 50468,
    '齐齐哈尔': 50745,
    '伊春': 50774,
    '鹤岗': 50775,
    '大庆': 50842,
    '绥化': 50853,
    '佳木斯': 50873,
    '双鸭山': 50884,
    '哈尔滨': 50953,
    '七台河': 50973,
    '鸡西': 50978,
    '牡丹江': 54094,

}  # 北京代码54511，也可以设置其他城市
index_ = ['日期', '最高温度', '最低温度', '天气', '风向', '风力', 'aqi', 'aqiinfo', 'aqilevel', 'city']  # 选取的气象要素
data = pd.DataFrame(columns=index_)  # 建立一个空dataframe
for y in years:
    for m in months:
        try:
            for k, v in city.items():
                # 找到json格式数据的url
                url = "http://tianqi.2345.com/t/wea_history/js/" + str(y) + str(m) + '/' + str(v) + "_" + str(y) + str(
                    m) + ".js"
                print(url)
                # response = requests.get(url=url)
                head = {  # 模拟头部信息
                    "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 91.0.4472.164Safari / 537.36"
                }
                request = urllib.request.Request(url, headers=head)
                response = urllib.request.urlopen(request)
                html = response.read().decode("gbk")
                print(html)
                response2 = html.replace('/', '')
                #  利用正则表达式获取5个气象要素（方法不唯一）
                date = re.findall("[0-9]{4}-[0-9]{2}-[0-9]{2}", response2)  # 去除最后两个无关的数据
                mintemp = re.findall("yWendu:'(.*?)'", response2)
                maxtemp = re.findall("bWendu:'(.*?)'", response2)
                tianqi = re.findall("tianqi:'(.*?)',", response2)
                winddir = re.findall("fengxiang:'([\u4E00-\u9FA5]+)", response2)
                wind = re.findall("fengli:'(.*?)'", response2)
                aqi = re.findall("aqi:'(.*?)',", response2)
                aqiinfo = re.findall("aqiInfo:'(.*?)',", response2)
                aqilevel = re.findall("aqiLevel:'(.*?)'},", response2)
                cit = []
                for item in aqi:
                    cit.append(k)
                data_spider = pd.DataFrame(
                    [date, maxtemp, mintemp, tianqi, winddir, wind, aqi, aqiinfo, aqilevel, cit]).T
                data_spider.columns = index_  # 修改列名
                data_spider.index = date  # 修改索引
                data = pd.concat((data, data_spider), axis=0)  # 数据拼接
                print('%s年%s月的数据抓取成功' % (y, m))
        except:
            continue

data.to_csv('weatherdata.csv')
print('爬取数据展示：\n', data)
