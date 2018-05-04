''''
每天增量爬取，按结束时间从第一页开始，到某一页存在id_lists中的ID时，则停止解析下一页，
并记录此时的页数，按照页数爬取对应的列表页.存放到按日期名创建的目录下
'''
from config import *
import requests
import re
import json
from proxies_request import get_ip
import random
import time
from datetime import datetime
import os 

over_urls ={
			'zhuzhai':
			 'https://auction.jd.com/getJudicatureList.html?callback=jQuery4392669&page=1&limit=40&childrenCateId=12728&sortField=9&paimaiStatus=2&_=1524136833906',
		 	'shangye':
			'https://auction.jd.com/getJudicatureList.html?callback=jQuery6982580&page=1&limit=40&childrenCateId=13809&sortField=9&paimaiStatus=2&_=1524187441176',
		 	'gongye':
			 'https://auction.jd.com/getJudicatureList.html?callback=jQuery3769558&page=1&limit=40&paimaiStatus=2&childrenCateId=13817&sortField=9&_=1524187543068',
		 	'qita':
			 'https://auction.jd.com/getJudicatureList.html?callback=jQuery4296846&page=1&limit=40&paimaiStatus=2&childrenCateId=13810&sortField=9&_=1524187650295',
			'tudi':
			'https://auction.jd.com/getJudicatureList.html?callback=jQuery9395886&page=1&limit=40&paimaiStatus=2&childrenCateId=12730&sortField=9&_=1524187793066'
				}

class Download_W_R(object):

	def __init__(self):
		self.user_agent = random.choice(USER_AGENTS)
		self.headers = {'User-Agent': self.user_agent}
		self.ip = get_ip()
		self.proxies={"http": "http://{}".format(self.ip)}
	def download(self,url):#下载网页获取html
		try:
			r = requests.get(url,headers=self.headers,proxies=self.proxies)
			r.raise_for_status()
			r.encoding = r.apparent_encoding
			html = r.content.decode('utf-8')
			r.close
			return html
		except:
			pass
	def write_in_txt(self,ids_new):
		s = ''
		for id in ids_new:
			s = s+str(id) + ' '
		with open('id_list.txt','a') as fp:
			fp.write(s)
			
	def read_from_txt(self):
		with open('id_list.txt','r') as fp:
			content = fp.read()
		#idlist = content.split(' ')
		return content

D = Download_W_R()

def save_json(html,choice,save_datetime,save_time):#把html转成json格式并保存到本地，文件名是页码
	file_args = [choice,save_datetime,save_time]
	#file_path = r'/urls_files/{0[0]}/{0[1]}/{0[2]}.json'.format(file_args)
	dir_path = r'over/{0[0]}/{0[1]}'.format(file_args)
	#print(dir_path)
	isExists=os.path.exists(dir_path)
	if not isExists:
		os.makedirs(dir_path)
	file_path = dir_path+'/{0[2]}.json'.format(file_args)
	try:
	    json_file = re.findall(r"(?<=\"ls\"\:)[\w\W]*?(?=\,\"total\")",html)[0]
	    #print('哈哈哈哈')
	    json_data = json.loads(json_file,encoding='utf-8')
	    #print(json_data)
	    with open(file_path,'w',encoding='utf-8') as fp:
	        json.dump(json_data, fp=fp, ensure_ascii=False, indent=4)
	    print('saved_success————————————————————————————————')
	except:
		pass


def crawler(initial_url,choice):#主函数
    try:
        html = D.download(initial_url)
        #page_number = getPage_number(initial_url)
        save_datetime = datetime.now().strftime('%Y-%m-%d')
        save_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        save_json(html,choice,save_datetime,save_time)
        print(html)
        #print(page_number)
        # print('成功%d次'%i)
        # i += 1
        time.sleep(1)
    except Exception as e:
        print(e)
    print('over')

def get_newpagenum(idlist_str):#获取每种类型每天增量爬取的页数
	klist =[]
	num_list = []
	for k,v in over_urls.items():
		page_number = 1
		Value = True
		while Value:
			update_url = re.findall(r'(?=https)(.*?)(?<=page\=)',v)[0]+str(page_number)+re.findall(r'(?=&limit)(.*?)(?<=\d{13})',v)[0]
			html = D.download(update_url)
			json_file = re.findall(r"(?<=\"ls\"\:)[\w\W]*?(?=\,\"total\")",html)[0]
			json_data = json.loads(json_file,encoding='utf-8')
			for data in json_data:
				if str(data["id"]) in idlist_str:
					Value = False
					break
			page_number += 1
		klist.append(k)
		num_list.append(page_number-1)
	choice_num = dict(zip(klist,num_list))
	return choice_num


def getInitial_urls(initial_url,page_number):
    initial_urls = []
    if int(page_number) == 1:
        initial_urls.append(initial_url)
    elif int(page_number) > 1:
        for i in range(1,int(page_number)+1):
            url = initial_url.replace("page=1","page=%d"%i)
            initial_urls.append(url)
    return initial_urls


def main_init():
	idlist_str = D.read_from_txt()#把存放的ID读为一个字符串
	choice_num = get_newpagenum(idlist_str)
	print(choice_num)
	for k,v in choice_num.items():
		choice = k
		initial_urls = getInitial_urls(over_urls[k],v)
		for initial_url in initial_urls:
			crawler(initial_url,choice)

# if __name__ == '__main__':
# 	main_init()

