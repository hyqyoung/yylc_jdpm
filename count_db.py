from bs4 import BeautifulSoup
import requests
import regex as re
from pyquery import PyQuery as pq
import random
import threadpool
import threading
from config import *
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



# user_agent = random.choice(USER_AGENTS)
# headers = {'User-Agent': user_agent}
# proxies={"http": "http://{}".format(ip)}

# #把文件夹中的全部文件名提取出来
# def get_files_path():
#     zhuzhai_files_path = []
#     shangye_files_path = []
#     tudi_files_path = []
#     gongye_files_path = []
#     qita_files_path = []
#     #status = ['over','putoff','aborted','withdraw']
#     status = ['over']
#     choices = {'zhuzhai':zhuzhai_files_path, 'shangye':shangye_files_path, 'tudi':tudi_files_path, 'gongye':gongye_files_path, 'qita':qita_files_path}
#     for statu in status:
#         for key,value in choices.items():
#             json_filenames = glob.glob(r'D:/Postgraduate/盈盈/Hyq/Hyq/{}/{}/*.json'.format(statu,key))
#             for filename in json_filenames:
#                 value.append(filename)
#         value = list(set(value))
#     return {'zhuzhai':zhuzhai_files_path,'shangye':shangye_files_path,'tudi':tudi_files_path,'gongye':gongye_files_path,'qita':qita_files_path}
# a = get_files_path()

# #读取所有json文件，然后把内容放到缓存列表url_infos中
# def get_url_infos(files_path):
#     url_infos =[]
#     for file in files_path:
#         try:
#             with open(file,'r',encoding='utf-8') as fp:
#                 temp = json.loads(fp.read())
#             url_infos.append(temp)
#         except:
#             print('%s出错了'% file)
#             pass
#     return url_infos

# zhuzhai_url_infos = get_url_infos(a['zhuzhai'])
# shangye_url_infos = get_url_infos(a['shangye'])
# tudi_url_infos = get_url_infos(a['tudi'])
# gongye_url_infos = get_url_infos(a['gongye'])
# qita_url_infos = get_url_infos(a['qita'])


# def get_ids(url_infos):
#     id_list= []
#     for url_info in url_infos:
#         ids = re.findall(r"(?<=\'id\': )\d{9}(?=, \'title\')",str(url_info))
#         for id in ids:
#             id_list.append(id)
#         list(set(id_list))
#         #print(len(id_list))
#     return id_list

# zhuzhai_id_list = get_ids(zhuzhai_url_infos)
# shangye_id_list = get_ids(shangye_url_infos)
# tudi_id_list = get_ids(tudi_url_infos)
# gongye_id_list = get_ids(gongye_url_infos)
# qita_id_list = get_ids(qita_url_infos)

# ids = copy.deepcopy(zhuzhai_id_list)
# ids.extend(shangye_id_list)               #详情页ID来源
# ids.extend(tudi_id_list)
# ids.extend(gongye_id_list)
# ids.extend(qita_id_list)


db = pymysql.connect(host=db_host, user=db_user, password=db_password, port=db_port, db=db_name, charset='utf8')
cursor = db.cursor()


def search_info():
    print('in search_info')
    #sql = 'SELECT * FROM  fixed_asset_new WHERE resource_type=6 and resource_id = %d' %(id)
    sql = 'SELECT * FROM  fixed_asset_new WHERE resource_type=6'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        #print(len(results))
    except:
        print('000000000000')
        return 0
    #print(len(results))
    return len(results)
# num = 0
# for id in ids:
# 	a = search_info(int(id))
# 	if a == 1:
# 		num += 1
# a = search_info(2332233)
# print(a)

for i in range(10000):
	a = search_info()
	print(a)
	time.sleep(1)