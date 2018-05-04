import requests
import time
import regex as re
# 代理服务器
def prequest(url= "http://ip.chinaz.com/getip.aspx", headers=None, cookies=None, use_proxies=True):

    time.sleep(2)

    proxyHost = "http-pro.abuyun.com"
    proxyPort = "9010"

    # 代理隧道验证信息
    proxyUser = "H39A0HL50PCCB02P"
    proxyPass = "29148984E07D9E97"


    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }


    if use_proxies == True:
        proxy_handler = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
        resp = requests.get(url, headers=headers, cookies=cookies, proxies=proxy_handler)
    else:
        resp = requests.get(url, headers=headers, cookies=cookies)
    return resp


def get_ip():
    string_ip = prequest().text
    # print(string_ip)
    # print(prequest())
    try:
    #if re.findall(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", string_ip)
        ip = re.findall(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", string_ip)[0]
        return ip
    except:
        #print('aaaa')
        return get_ip()

        
# for i in range(10):
#     ip = get_ip()
#     time.sleep(10)
#     print(ip)



#return ip
#print(ip)
# from selenium import webdriver
# chromeOptions = webdriver.ChromeOptions()
#
# # 设置代理
# chromeOptions.add_argument("--proxy-server=http://%s:9010" % ip)
# # 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
# browser = webdriver.Chrome(chrome_options = chromeOptions)
#
# # 查看本机ip，查看代理是否起作用
# browser.get('https://auction.jd.com/sifa.html')
# print(browser.page_source)
#
# # 退出，清除浏览器缓存
# browser.quit()