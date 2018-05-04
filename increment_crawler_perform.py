'''
紧接着increment_crawler_main.py模块，开始把新增的页数解析出ID，并进行去重，接着爬取详情页，入库

'''
from increment_crawler_init import Download_W_R
from bs4 import BeautifulSoup
import requests
import regex as re
from pyquery import PyQuery as pq
import random
import threadpool
import threading
from config import *
from proxies_request import get_ip
import glob
import json
import time
# from lxml import etree
from datetime import datetime
import pymysql
import copy
from cn_to_arab import cn_to_arab
import random

start = datetime.now()


user_agent = random.choice(USER_AGENTS)
headers = {'User-Agent': user_agent}
D = Download_W_R()

#把文件夹中的全部文件名提取出来
def get_files_path():
	zhuzhai_files_path = []
	shangye_files_path = []
	tudi_files_path = []
	gongye_files_path = []
	qita_files_path = []
	#status = ['over','putoff','aborted','withdraw']
	choices = {'zhuzhai':zhuzhai_files_path, 'shangye':shangye_files_path, 'tudi':tudi_files_path, 'gongye':gongye_files_path, 'qita':qita_files_path}
	for key,value in choices.items():
		save_datetime = datetime.now().strftime('%Y-%m-%d')
		#print(save_datetime)
		#save_datetime = '2018-04-29'
		json_filenames = glob.glob(r'over/{}/{}/*.json'.format(key,save_datetime))
		for filename in json_filenames:
			value.append(filename)
		value = list(set(value))
		#print(value)
	a = {'zhuzhai':zhuzhai_files_path,'shangye':shangye_files_path,'tudi':tudi_files_path,'gongye':gongye_files_path,'qita':qita_files_path}
	return a

#读取所有json文件，然后把内容放到缓存列表url_infos中
def get_url_infos(files_path):
	url_infos =[]
	for file in files_path:
		try:
			with open(file,'r',encoding='utf-8') as fp:
				temp = json.loads(fp.read())
			url_infos.append(temp)
		except:
			print('%s出错了'% file)
			pass
	return url_infos


def get_ids(url_infos):
	id_list= []
	for url_info in url_infos:
		ids = re.findall(r"(?<=\'id\': )\d{9}(?=, \'title\')",str(url_info))
		for id in ids:
			id_list.append(id)
		list(set(id_list))
		#print(len(id_list))
	return id_list


def download(url):#下载网页获取html
    try:
        ip = get_ip()
        proxies={"http": "http://{}".format(ip)}
        r = requests.get(url,headers=headers,proxies=proxies)
        #r = requests.get(url,headers=headers)
        r.raise_for_status()
        html = r.content.decode('utf-8')
        if html is None:
            return download
        else:
            r.close
            return html
    except:
        pass

def download_without_ip(url):#不用代理IP
    try:
        r = requests.get(url,headers=headers)
        #r = requests.get(url,headers=headers)
        r.raise_for_status()
        html = r.content.decode('utf-8')
        if html is None:
            return download
        else:
            r.close
            return html
    except:
        pass

def json_loads(data):  # 把字符串转化成json格式
    try:
        json_text = json.loads(data,encoding='utf-8')
        if json_text:
            return json_text
    except:
        return None



def extract(ids):
    #print("IDS")
    id = ids.pop()
    full_url = 'https://paimai.jd.com/{}'.format(id)#网页源码URL
    main_html = download(full_url)
    soup = BeautifulSoup(main_html,'lxml')

    try:
        input1 = soup.select('div.pm-support > input#ensurePrice')[0]                   #保证金（单位分）
        cash_deposit = float(input1.get('value'))*100
    except:
        cash_deposit = None

    try:
        input2 = soup.select('div.pm-support > input#skuId')[0]
        skuId = input2.get('value')
    except:
        skuId = None

    try:
        input7 = soup.select('div.pm-support > input#priceLowerOffset')[0]                         #最小加价幅度(单位分)
        min_raise_price = float(input7.get('value'))*100
    except:
        min_raise_price = None

    albumID_url = 'https://paimai.jd.com/json/current/initBreadCrumb.html?paimaiId={}'.format(id)#包含albumID的URL，albumID是竞买公告的URL包含的ID信息
    album_html = download(albumID_url)
    albumID = json_loads(album_html)['albumId']

    notice_url = 'https://paimai.jd.com/json/current/queryAlbumAnnouncement?albumId={}'.format(albumID)  #竞买公告
    announcement_url = 'https://paimai.jd.com/json/current/getAuctionNotice.html?paimaiId={}'.format(id)#竞买须知
    if skuId is not None:
        currentprice_url = 'https://paimai.jd.com/json/current/englishquery.html?paimaiId={}&skuId={}&start=0&end=9'.format(id,skuId)#包含成交价等信息,还可以根据里面是否有username来判断流拍还是成交
    else:
        currentprice_url = 'https://paimai.jd.com/json/current/englishquery.html?paimaiId={}&start=0&end=9'.format(id)

    try:
        productId = currentprice_data['bidList'][0]['productId']            #productId
    except:
        productId = skuId

    product_url = 'https://paimai.jd.com/json/paimaiProduct/productDesciption?productId={}'.format(productId)           #标的物介绍

    notice_html = download(notice_url)
    announcement_html = download(announcement_url)
    product_html = download(product_url)
    notice_text = pq(notice_html).text()
    notice_text = notice_text.replace(' ', '').replace('：', '').replace('\n', '').replace('￥', '')
    announcement_text = pq(announcement_html).text()
    product_text = pq(product_html).text()

    currentprice_html = download(currentprice_url)

    currentprice_data = json_loads(currentprice_html)

    try:
        transaction_price = currentprice_data['bidList'][0]['price']            #成交价
        transaction_price = float(transaction_price)*100
    except:
        transaction_price = None

    pm = soup.select('div.pm-support')#里面包含很多信息
    resource_id = int(id)                                            #来源网站的ID
    resource_type = 6                                  #来源网站
    try:
        name =  str(soup.title.string.replace('－京东司法拍卖',''))                               #资产名称
    except:
        name = None

    try:
        address = str(soup.find(id='paimaiAddress').string)
        if address is None:                 #资产地址
            address = name
    except:
        address = None

    try:
        addr = address.replace(' ','')
        location_url = 'http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=wPh1zq1a818gaVKpOsGQEhrCBevNuVyy&callback=showLocation' % addr
        bd = download_without_ip(location_url)
        s = re.findall(r"(?<=showLocation&&showLocation\()[\w\W]*?(?<=}})",bd)[0]
        json_bd = json_loads(s)['result']['location']
        location = str(json_bd['lng'])+ ',' + str(json_bd['lat'])
    except:
        location = None

    try:
        province = str(address.split(' ')[0])                             #省份
    except:
        province = None
    try:
        city = str(address.split(' ')[1])                                 #城市
    except:
        city = None
    try:
        district = str(address.split(' ')[2])                         #区县
    except:
        district = None

    longitude =  None           #经度
    latitude = None         #维度
    price = None                #单价
    try:
        land_use = 0
        if id in qita_id_list:                            #规划用途：0、未知；1、住宅用地；2、商业/办公用地；3、工业用地；4、其他用地
            land_use = 4
        elif id in zhuzhai_id_list:
            land_use = 1
        elif id in shangye_id_list:
            land_use = 2
        elif id in gongye_id_list:
            land_use = 3
        elif id in tudi_id_list:
            land_use = 0
    except:
        land_use = 0

    sell_type = 2                               #出让形式：0、未知;1、招标;2、拍卖;3、挂牌

    try:
        land_type = 0
        if re.search(r'机器|工业|厂房|库房|厂',notice_text):
            land_type = 1                                             #建筑性质：0、未知；1、厂房；2、商铺；3、住宅；4、商业；5、仓库；6、办公；7、商住房；8、别墅
        elif re.search(r'商铺|营业|商铺|门面房',notice_text):
            land_type = 2
        elif re.search(r'住宅', notice_text):
            land_type = 3
        elif re.search(r'商用',notice_text):
            land_type = 4
        elif re.search(r'仓库',notice_text):
            land_type = 5
        elif re.search(r'办公',notice_text):
            land_type = 6
        elif re.search(r'商住房|商品房|商服用房',notice_text):
            land_type = 7
        elif re.search(r'别墅',notice_text):
            land_type = 8
        else:
            lan_type = 0
    except:
        lan_type = 0                                               #建筑性质：0、未知；1、厂房；2、商铺；3、住宅；4、商业；5、仓库；6、办公；7、商住房；8、别墅

    try:
        if currentprice_data['bidList'] != []:                  #成交状态：0、未知；1、未成交；2、已成交；3、流拍
            deal_status = 2
        elif currentprice_data['bidList'] == []:
            deal_status = 3
        else:
            deal_status = 0
    except:
        deal_status = 0

    source_url = str(full_url)                                           #来源网站
    land_scope = None                                               #四至（土地范围涵盖区域，eg：东至XXX，西至XXX...）

    total_area = None                                       #总用地面积,单位平方米,未找到
    confiscated_area = None                                 #代征面积,单位平方米,未找到
    plan_construction_area = None                           #规划建筑面积,单位平方米,未找到
    construction_area =  None                               #建筑用地面积,单位平方米，未找到

    try:
        plot_rate = str(format(housing_area/land_area,'.3f'))     #容积率,总建筑面积/用地面积
    except:
        plot_rate = None

    green_rate = None                                       #绿化率，未知
    build_density =  None                                   #建筑密度，因建筑物基地总面积与规划建筑面积均未知，所以建筑密度未知
    limit_height =  None                                    #限制高度，未知
    business_rate = None                                    #商业比例,未知
    sell_age_limit =  None                                  #出让年限，未知

    try:
        results = re.findall(r'(?=二|2)(.*?)(?<=日)',notice_text[-20:])        #公告日期,先在竞买公告里找，找不到再在竞买须知里找
        if results != []:
            declaration_time_l = cn_to_arab(results[0].replace(' ',''))
            if re.search(r'(\A\d{4}\-\d{2}\-\d{2}\Z)',declaration_time_l):
                declaration_time = declaration_time_l+' 00:00:00'
            else:
                declaration_time = None
        else:
            results = re.findall(r'(?=二|2)(.*?)(?<=日)',announcement_text[-20:])
            if results != []:
                declaration_time_l = cn_to_arab(results[0].replace(' ',''))
                if re.search(r'(\A\d{4}\-\d{2}\-\d{2}\Z)',declaration_time_l):
                    declaration_time = declaration_time_l +' 00:00:00'
                else:
                    declaration_time = None
            else:
                declaration_time = None
    except:
        declaration_time = None

    try:
        results1 = re.findall(r'(201\d年\d{1,2}月\d{1,2}日)',notice_text[:180])                  #开始日期    
        if results1 != []:
            start_time_l = cn_to_arab(results1[0].replace(' ',''))
            if re.search(r'(\A\d{4}\-\d{2}\-\d{2}\Z)',start_time_l):
                start_time = start_time_l+' 10:00:00'
            else:
                start_time = None
        else:
            start_time = None
    except:
        start_time = None

    try:
        results2 = re.findall(r'(?<=至)(.*?)(?<=日)',notice_text[:180])                 #截止日期
        if results2 != []:
            expiration_time_l = cn_to_arab(results2[0].replace(' ',''))
            if re.search(r'(\A\d{4}\-\d{2}\-\d{2}\Z)',expiration_time_l):
                expiration_time = expiration_time_l+' 10:00:00'
            else:
                expiration_time = None
        else:
            expiration_time = None
    except:
        expiration_time = None

    try:
        start_price = re.findall(r'(?<=起拍价：|起拍价)(.*?)(?<=万元|元)',notice_text)               #起始价(单位分)',起拍价
        if start_price != []:
            start_price = start_price[0]
            if '万' in start_price:
                start_price = (float(start_price[:-2]))*1000000
            else:
                start_price = (float(start_price[:-1]))*100
        else:
            start_price = None
    except:
        start_price = None

    premium_rate = None                                                                          #溢价率
    start_accommodation_value = None                                                             #推出楼面价(单位分)
    transaction_accommodation_value = None                                                       #成交楼面价(单位分)
    trading_place = address                                                                         #交易地点

    try:
        assignee = str(currentprice_data['bidList'][0]['username'])                                 #竞得方
    except:
        assignee = None

    try:
        fixture_time_l = str(currentprice_data['bidList'][0]['bidTimeStr1'].replace('  ',' '))
        if re.search(r'(\A\d{4}\-\d{2}\-\d{2} \d{2}\:\d{2}\:\d{2}\Z)',fixture_time_l):
                fixture_time = fixture_time_l
        else:
                fixture_time = None                                      #成交日期
    except:
        fixture_time = None

    consult_tel = fixture_time                                                                      #和fixture_time相同

    announce_num = None                                                                         #公告编号

    try:
        subject_type = 0
        if id in qita_id_list or id in zhuzhai_id_list or id in shangye_id_list or id in gongye_id_list:                #根据拍卖ID来源区分    #标的物类型：0、未知；1、房产；2、土地；标的物类型；淘宝拍卖和上海公拍为房产，房天下和土地交易市场网为土地
            subject_type = 1
        elif id in tudi_id_list:
            subject_type = 2
    except:
        subject_type = 0


    # try:                                                                             #(房产)建筑面积,示例：123.5平方米
    #     _area = re.compile(r'((?<=总建筑面积：)|(?<=房屋面积：)|(?<=建筑物)|(?<=建筑面积约)|(?<=建筑面积共)|(?<=建筑面积)|(?<=建面)|(?<=建筑面积为)|(?<=建筑面积是)|(?<=建筑面积共计)|(?<=建筑面积：)|(?<=建筑面积合计))(?<=共:)(.*?)(平方米|㎡|公顷|M2|m2)')
    #     ha = _area.findall(notice_text)
    #     housing_area = []
    #     if len(ha) != 0:
    #         for i in ha:
    #             a = i[1] + i[2]
    #             a = a.replace('约', '').replace('为', '').replace('是', '').replace('共计', '')
    #             if a not in housing_area:
    #                 housing_area.append(a)
    #                 housing_area = housing_area[0]
    #     else:
    #         housing_area = ''
    #     # elif ha == []:
    #     #     ha = re.findall(r'(?<=建筑物|建筑面积约|建筑面积|建面|建筑面积为|建筑面积是|建筑面积共计|建筑面积:|共:|建筑面积合计)(.*?)(?=平方米|㎡|公顷|M2|m2)',product_text)
    #     #     housing_area = ha[0]+'平方米'
    # except:
    #     housing_area = None


    land_areas= []                          #土地
    areas_l = []
    a = re.findall(r'(\d{1,5}\.\d{1,2}平方米)',notice_text)
    b = re.findall(r'(\d{1,5}\.\d{1,2}㎡)',notice_text)
    c = re.findall(r'(\d{1,5}\.\d{1,2}亩)', notice_text)
    d = re.findall(r'(\d{1,5}\.\d{1,2}平米)', notice_text)
    if a == [] and b == [] and c == [] and d ==[]:
        land_area = None
    elif a != [] or b != [] or c != [] or d != []:
        land_areas = [i for i in a]
        for j in b:
            land_areas.append(j)
        for k in c:
            land_areas.append(k)
        for l in d:
            land_areas.append(l)
        index = []
        temp = {}
        for item in land_areas:
            index.append(notice_text.find(item))
        temp = dict(zip(land_areas,index))
        for k,v in temp.items():
            if v:
                related_ss = notice_text[v-10:v+10]
                if '土地使用权' in related_ss or '使用权面积为' in related_ss or '用地' in related_ss or '使用权面积' in related_ss or '土地面积约' in related_ss\
                    or '土地证载面积' in related_ss or '土地面积' in related_ss or '土地面积为' in related_ss or '土地面积是' in related_ss\
                    or '土地面积共计' in related_ss or '用地面积' in related_ss or '工业用地' in related_ss or '林地面积' in related_ss or '土地' in related_ss:
                    if '亩' in k:
                        k = float(k.replace('亩', ''))
                        k = k * 666.6666667
                    kk_figure = float(str(k).replace('平方米', '').replace('平米', '').replace('㎡', ''))
                    areas_l.append(kk_figure)
                else:
                    land_area = None
        land_area = get_area(areas_l)

    housing_areas = []                      #房产面积
    areas = []
    housing_area = 0
    a = re.findall(r'(\d{1,5}\.\d{1,2}平方米)', notice_text)
    b = re.findall(r'(\d{1,5}\.\d{1,2}㎡)', notice_text)
    c = re.findall(r'(\d{1,5}\.\d{1,2}平米)', notice_text)
    if a == [] and b == []:
        housing_area = None
    elif a != [] or b != []:
        housing_areas = [i for i in a]
        for j in b:
            housing_areas.append(j)
        for k in c:
            housing_areas.append(k)
        index = []
        temp = {}
        for item in housing_areas:
            index.append(notice_text.find(item))
        temp = dict(zip(housing_areas, index))
        for k, v in temp.items():
            if v:#(?<=总建筑面积：)|(?<=房屋面积：)|(?<=建筑物)|(?<=建筑面积约)|(?<=建筑面积共)|(?<=建筑面积)|(?<=建面)|(?<=建筑面积为)|(?<=建筑面积是)|(?<=建筑面积共计)|(?<=建筑面积：)|(?<=建筑面积合计
                related_s = notice_text[v-10:v+10]
                #print(related_s)
                # if '总建筑面积' in related_s or '建筑物' in related_s or '建筑面积为' in related_s or '建筑面积共' in related_s or '建筑面积共计' in related_s \
                #         or '建筑面积' in related_s or '建筑面积合计' in related_s or '建筑面积约' in related_s or '房产' in related_s \
                #         or '房屋建筑物' in related_s:
                if '建筑' in related_s or '房产' in related_s or '房屋' in related_s or '房产' in related_s or '住宅' in related_s:
                    k_figure = float(k.replace('平方米','').replace('平米','').replace('㎡',''))
                    areas.append(k_figure)
                    #housing_area = areas[-1]+'平方米'
                    # if '㎡' in housing_area:
                    #     housing_area = housing_area.replace('㎡', '平方米')
                else:
                    housing_area = None
        housing_area = get_area(areas)

    # try:                                                                              #(房产)土地面积,示例：123.5平方米
    #     area = re.compile(r'((?<=使用权面积为)|(?<=用地)|(?<=使用权面积)|(?<=土地面积约)|(?<=土地证载面积)|(?<=土地面积)|(?<=土地证载面积)|(?<=土地面积为)|(?<=土地面积是)|(?<=土地面积共计))(.*?)(平方米|㎡|公顷|M2|m2)')
    #     la = area.findall(notice_text)
    #     land_area = []
    #     if len(la) != 0:
    #         for i in la:
    #             a = i[1] + i[2]
    #             a = a.replace('约', '').replace('为', '').replace('是', '').replace('共计', '')
    #             if a not in land_area:
    #                 land_area.append(a)
    #                 land_area = land_area[0]
    #     else:
    #         land_area =''
    #     # elif la == []:
    #     #     la = re.findall(r'(?<=使用权|使用权面积|土地面积约|土地面积|土地证载面积|土地面积为|土地面积是|土地面积共计)(.*?)(?=平方米|㎡|公顷|M2|m2)',product_text)
    #     #     land_area = la[0]+'平米'
    # except:
    #     land_area = None

    try:
        plot_rate = format(float(housing_area[:-3])/float(land_area[:-3]),'.3f')     #容积率,总建筑面积/用地面积
    except:
        plot_rate = None

    try:
        ep = soup.select('div.pm-attachment > ul.fn-clear > li.fore3 > em.fn-rmb')[0]             #(房产)评估价,单位分
        evaluate_price = ep.string[1:].replace(',','')
        evaluate_price = (float(evaluate_price))*100
    except:
        evaluate_price= None

    try:
        auction_stage = 0
        status = currentprice_data['auctionStatus']                                                   #(房产)拍卖阶段：0、未知；1、第一次拍卖；2、第二次拍卖；3、第三次拍卖；4、变卖
        if status == 0:
            auction_stage = 0
        elif status == 1:
            auction_stage = 1
        elif status == 2:
            auction_stage = 2
        elif status == 3:
            auction_stage = 3
        elif status == 4:
            auction_stage = 4
    except:
        auction_stage = 0
    memo = None
    if declaration_time == None or start_time == None or expiration_time == None or fixture_time == None:
        memo = "公告日期或起始日期或截止日期或成交日期是错误的"                                                                         #备注
    is_deleted = 0                                                                      #删除状态：1删除，0未删除
    gmt_created = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')                                      #添加日期
    gmt_modified = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')                                    #修改日期
    is_bid = 0

    #return ([resource_id,resource_type,name,area,address,location,longitude,latitude,price,
    #          land_use,sell_type,land_type,deal_status,source_url,land_scope,total_area,
    #          confiscated_area,plan_construction_area,construction_area,plot_rate,green_rate,
    #          build_density,limit_height,business_rate,sell_age_limit,declaration_time,
    #          start_time,expiration_time,start_price,transaction_price,premium_rate,
    #          min_raise_price,cash_deposit,start_accommodation_value,transaction_accommodation_value,
    #          trading_place,assignee,fixture_time,consult_tel,announce_num,subject_type,housing_area,
    #          land_area,evaluate_price,auction_stage,memo,is_deleted,gmt_created,gmt_modified])
    #print([land_area,housing_area])
    #print(address)
    #return land_area,housing_area
    #return notice_text
    #return housing_area
    data = {}
    data['resource_id'] = resource_id  #网页ID %d
    data['resource_type'] = resource_type   #来源网站，固定为6  %d
    data['name'] = name      #资产名称  %s
    data['address'] = address   #资产地址  %s
    data['location'] = location  #百度地图坐标   %s
    data['land_use'] = land_use  #规划用途   %d
    data['sell_type'] = sell_type  #出让形式  %d
    data['land_type'] = land_type   #建筑性质：0、未知；1、厂房；2、商铺；3、住宅；4、商业；5、仓库；6、办公；7、商住房；8、别墅  %d
    data['is_bid'] = is_bid                                     #%d      
    data['deal_status'] = deal_status     #成交状态：0、未知；1、未成交；2、已成交；3、流拍   %d
    data['source_url'] = source_url   #来源网站  %s
    data['province'] = province     #省份  %s
    data['city'] = city             #城市     %s
    data['district'] = district     #区县  %s
    data['plot_rate'] = plot_rate     #容积率  %s
    data['declaration_time'] = declaration_time    #公告日期  %s
    data['start_time'] = start_time      #起始日期   %s
    data['expiration_time'] = expiration_time    #截止日期  %s
    data['start_price'] = start_price      #起拍价     %s  
    data['transaction_price'] = transaction_price    #成交价(单位分)    %s
    data['min_raise_price'] = min_raise_price   #最小加价幅度(单位分)   %s
    data['cash_deposit'] = cash_deposit    #保证金(单位分)   %s
    data['trading_place'] = trading_place   #交易地点 %s
    data['assignee'] = assignee             #竞得方 %s
    data['fixture_time'] = fixture_time    #成交日期 %s
    data['consult_tel'] = consult_tel     #成交日期 %s
    data['subject_type'] = subject_type    #%d 标的物类型：0、未知；1、房产；2、土地；标的物类型；淘宝拍卖和上海公拍为房产，房天下和土地交易市场网为土地
    data['housing_area'] = housing_area    #(房产)建筑面积,示例：123.5平方米 %s
    data['land_area'] = land_area           #(房产)土地面积,示例：123.5平方米  %s
    data['evaluate_price'] = evaluate_price   #(房产)评估价,单位分  %s
    data['auction_stage'] = auction_stage  #(房产)拍卖阶段：0、未知；1、第一次拍卖；2、第二次拍卖；3、第三次拍卖；4、变卖  %d
    data['is_deleted'] = 0          #删除状态：1删除，0未删除  %d
    t = datetime.now()
    t = str(t).split('.')[0]
    data['gmt_created'] = t
    data['gmt_modified'] = t
    #print(location)
    print('***********************************')
    print(data)
    sql = get_sql(data)
    print(sql)
    #print(notice_text[:180])
    #print([declaration_time,start_time,expiration_time])
    #print(fixture_time)
    #if not search_info(resource_id):
    write_into_db(data)
 
def get_sql(data):
    sql_1 = 'INSERT INTO fixed_asset_new ('
    sql_2 = ') VALUES ('
    for key, value in data.items():
        if data[key] != None:
            sql_1 = sql_1 + key
            # keys.append(key)
            # values.append("'"+str(data[key])+"'")
            if type(data[key]) == str:
                sql_2 = sql_2 + "'" + data[key] + "'"
            else:
                sql_2 = sql_2 + str(data[key])
            sql_1 = sql_1 + ','
            sql_2 = sql_2 + ','
    sql_1 = sql_1[:-1]
    sql_2 = sql_2[:-1]
    sql = sql_1 + sql_2 +')'
    return sql

def write_into_db(data):
    db = pymysql.connect(host=db_host, user=db_user, password=db_password, port=db_port, db=db_name, charset='utf8')
    cursor = db.cursor()
    print('start inserting into db')
    print(data)
    t = datetime.now()
    t = str(t).split('.')[0]
    sql = get_sql(data)
    #sql = "INSERT INTO fixed_asset_new (resource_id,resource_type,name,address,location,land_use,sell_type,land_type,is_bid,deal_status,source_url,province,city,district,plot_rate,declaration_time,start_time,expiration_time,start_price,transaction_price,min_raise_price,cash_deposit,trading_place,assignee,fixture_time,consult_tel,subject_type,housing_area,land_area,evaluate_price,auction_stage,is_deleted,gmt_created,gmt_modified) VALUES (%d,%d,'%s','%s','%s',%d,%d,%d,%d,%d,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%d ,'%s','%s',%s,%d,%d,'%s','%s')" % (data['resource_id'],data['resource_type'],data['name'],data['address'],data['location'],data['land_use'],data['sell_type'],data['land_type'],0,data['deal_status'],data['source_url'],data['province'],data['city'],data['district'],data['plot_rate'],data['declaration_time'],data['start_time'],data['expiration_time'],data['start_price'],data['transaction_price'],data['min_raise_price'],data['cash_deposit'],data['trading_place'],data['assignee'],data['fixture_time'],data['consult_tel'],data['subject_type'],data['housing_area'],data['land_area'],data['evaluate_price'],data['auction_stage'],data['is_deleted'],t,t)
    try:
        cursor.execute(sql)
        db.commit()
        print('successful')
    except Exception as e:
        print(e)
        db.rollback()

# def delete_info():
#     table = 'fixed_asset_new'
#     condition = 'resource_type= 6'
#     db = pymysql.connect(host=db_host, user=db_user, password=db_password, port=db_port, db=db_name, charset='utf8')
#     cursor = db.cursor()
#     sql = 'DELETE FROM {table} WHERE {condition}'.format(table=table,condition=condition)
#     try:
#         cursor.execute(sql)
#         db.commit()
#         print('删除成功')
#     except:
#         db.rollback()
#     db.close()

# def search_info(resource_id):
#     print('in search_info')
#     db = pymysql.connect(host=db_host, user=db_user, password=db_password, port=db_port, db=db_name, charset='utf8')
#     cursor = db.cursor()
#     sql = 'SELECT * FROM  fixed_asset_new WHERE resource_type=6 and resource_id = %d' %(resource_id)
#     try:
#         cursor.execute(sql)
#         results = cursor.fetchall()
#     except Exception as e:
#         print('000000000000')
#         print(e)
#         return 0
#     print(len(results))
#     return len(results)

# def insert_update():
#     table = 'fixed_asset_new'
#     #condition = 'resource_type= 6'
#     db = pymysql.connect(host=db_host, user=db_user, password=db_password, port=db_port, db=db_name, charset='utf8')
#     cursor = db.cursor()
#     data = {
#         'resource_id':105446381,
#         'plot_rate':'null',
#         'resource_type':6
#     }
#     keys = ','.join(data.keys())
#     values = '%d,%s,%d'
#     sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table,keys=keys,values=values)
#     update = 'resource_id = %d,plot_rate = %s,resource_type = %d'
#     sql = sql+' '+ update
#     try:
#         if cursor.execute(sql,tuple(data.values())*2):
#             print('Successful')
#             db.commit()
#     except Exception as e:
#         print(e)
#         db.rollback
#     db.close()

# def update():
#     table = 'fixed_asset_new'
#     #condition = 'resource_type= 6'
#     db = pymysql.connect(host=db_host, user=db_user, password=db_password, port=db_port, db=db_name, charset='utf8')
#     cursor = db.cursor()
#     # data = {
#     #     'resource_id':105446381,
#     #     'plot_rate':'null',
#     #     'resource_type':6
#     # }
#     # keys = ','.join(data.keys())
#     # values = '%d,%s,%d'
#     sql = 'UPDATE {table} SET plot_rate = {plot_rate} WHERE resource_id = {resource_id}'.format(table=table,plot_rate='null',resource_id=105446381)
#     try:
#         cursor.execute(sql)
#         print('Successful')
#         db.commit()
#     except Exception as e:
#         print(e)
#         db.rollback
#     db.close()
# #update()

#得到一篇文档中的一串areas中的area，策略：如果一串areas中的最大项等于其余项之和，就把这项设为面积，否则的话就把所有项相加得到面积
def get_area(areas): 
    area = None
    areas.sort()
    areass = areas.copy()
    if len(areas) > 1:
        areass.pop()
        if max(areas) == sum(areass):
            area = max(areas)
        else:
            area = str(sum(areas)) + '平方米'
    elif len(areas) == 1:
        area = str(areas[0]) + '平方米'
    return area




#线程池
# def main():
# 	pool = threadpool.ThreadPool(8)
# 	tasks = threadpool.makeRequests(extract, ids)
# 	[pool.putRequest(task) for task in tasks]
# 	pool.wait()
def threads(ids_):
    ids = ids_
    threads = []
    while ids or threads:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < 10 and ids:
            thread = threading.Thread(target=extract,args=(ids_,))
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)
        # TIME = random.uniform(0.2,0.6)  #随机产生一个1到3之间的小数
        # time.sleep(TIME)

def main_perform():
    a = get_files_path()
    zhuzhai_url_infos = get_url_infos(a['zhuzhai'])
    shangye_url_infos = get_url_infos(a['shangye'])
    tudi_url_infos = get_url_infos(a['tudi'])
    gongye_url_infos = get_url_infos(a['gongye'])
    qita_url_infos = get_url_infos(a['qita'])

    zhuzhai_id_list = get_ids(zhuzhai_url_infos)
    shangye_id_list = get_ids(shangye_url_infos)
    tudi_id_list = get_ids(tudi_url_infos)
    gongye_id_list = get_ids(gongye_url_infos)
    qita_id_list = get_ids(qita_url_infos)

    ids = copy.deepcopy(zhuzhai_id_list)
    ids.extend(shangye_id_list)                 #详情页ID来源
    ids.extend(tudi_id_list)
    ids.extend(gongye_id_list)
    ids.extend(qita_id_list)
    ids_update = ids                            #存放每天增量爬取的ID，但未去重
    ids_uniq = []                               #初始空列表,不断添加去重后新的ID
    idlist_str = D.read_from_txt()
    for id in ids_update:
        if id not in idlist_str:
            ids_uniq.append(id)
    ids = ids_uniq
    threads(ids)
    D.write_in_txt(ids_uniq)
    #extract()

# if __name__ == "__main__":
    
#     print('开始的时候所有详情页共有%d个:'%len(ids))
#     main_perform()
#     #D.write_in_txt(ids_uniq)					#爬取结束之后再执行
#     # #search_info()
#     #delete_info()
#     print('结束之后所有详情页共有%d个:'%len(ids))
#     end = datetime.now()
#     print('程序运行时间：',end-start)