# # constants for chinese_to_arabic
# CN_NUM = {
#     '〇' : 0, '一' : 1, '二' : 2, '三' : 3, '四' : 4, '五' : 5, '六' : 6, '七' : 7, '八' : 8, '九' : 9, '零' : 0,
#     '壹' : 1, '贰' : 2, '叁' : 3, '肆' : 4, '伍' : 5, '陆' : 6, '柒' : 7, '捌' : 8, '玖' : 9, '貮' : 2, '两' : 2,
# }

# CN_UNIT = {
#     '十' : 10,
#     '拾' : 10,
#     '百' : 100,
#     '佰' : 100,
#     '千' : 1000,
#     '仟' : 1000,
#     '万' : 10000,
#     '萬' : 10000,
#     '亿' : 100000000,
#     '億' : 100000000,
#     '兆' : 1000000000000,
# }

# def chinese_to_arabic(cn:str) -> int:
#     unit = 0   # current
#     ldig = []  # digest
#     for cndig in reversed(cn):
#         if cndig in CN_UNIT:
#             unit = CN_UNIT.get(cndig)
#             if unit == 10000 or unit == 100000000:
#                 ldig.append(unit)
#                 unit = 1
#         else:
#             dig = CN_NUM.get(cndig)
#             if unit:
#                 dig *= unit
#                 unit = 0
#             ldig.append(dig)
#     if unit == 10:
#         ldig.append(10)
#     val, tmp = 0, 0
#     for x in reversed(ldig):
#         if x == 10000 or x == 100000000:
#             val += tmp * x
#             tmp = 0
#         else:
#             tmp += x
#     val += tmp
#     return val


# # TODO: make a full unittest
# def test():
#     test_dig = ['八',
#                 '十一',
#                 '一百二十三',
#                 '一千二百零三',
#                 '一万一千一百零一',
#                 '十万零三千六百零九',
#                 '一百二十三万四千五百六十七',
#                 '一千一百二十三万四千五百六十七',
#                 '一亿一千一百二十三万四千五百六十七',
#                 '一月零二亿五千零一万零一千零三十八',
#                 '二']
#     for cn in test_dig:
#         x = chinese_to_arabic(cn)
#         print(cn, x)
#     assert x == 10250011038

# if __name__ == '__main__':
#     test()

#把日期转换成数据库日期标准格式
def cn_to_arab(strs):
    str1 = str2 =  str3 = ''
    try:
        if '二0一八年' in strs or '二〇一八年' in strs or '2018年' in strs:
            str1 = strs.replace('二0一八年','2018-').replace('二〇一八年','2018-').replace('2018年','2018-')
        elif '二0一七' in strs or '二〇一七年' in strs or '2017年' in strs:
            str1 = strs.replace('二0一七年','2017-').replace('二〇一七年','2017-').replace('2017年','2017-')

        if '-一月' in str1:
            str2 = str1.replace('-一月','-01-')
        elif '-二月' in str1:
            str2 = str1.replace('-二月','-02-')
        elif '-三月' in str1:
            str2 = str1.replace('-三月','-03-')
        elif '-四月' in str1:
            str2 = str1.replace('-四月','-04-')
        elif '-五月' in str1:
            str2 = str1.replace('-五月','-05-')
        elif '-六月' in str1:
            str2 = str1.replace('-六月','-06-')
        elif '-七月' in str1:
            str2 = str1.replace('-七月','-07-')
        elif '-八月' in str1:
            str2 = str1.replace('-八月','-08-')
        elif '-九月' in str1:
            str2 = str1.replace('-九月','-09-')
        elif '-十月' in str1:
            str2 = str1.replace('-十月','-10-')
        elif '-十一月' in str1:
            str2 = str1.replace('-十一月','-11-')
        elif '-十二月' in str1:
            str2 = str1.replace('-十二月','-12-')

        if '-1月' in str1:
            str2 = str1.replace('-1月','-01-')
        elif '-2月' in str1:
            str2 = str1.replace('-2月','-02-')
        elif '-3月' in str1:
            str2 = str1.replace('-3月','-03-')
        elif '-4月' in str1:
            str2 = str1.replace('-4月','-04-')
        elif '-5月' in str1:
            str2 = str1.replace('-5月','-05-')
        elif '-6月' in str1:
            str2 = str1.replace('-6月','-06-')
        elif '-7月' in str1:
            str2 = str1.replace('-7月','-07-')
        elif '-8月' in str1:
            str2 = str1.replace('-8月','-08-')
        elif '-9月' in str1:
            str2 = str1.replace('-9月','-09-')
        elif '-10月' in str1:
            str2 = str1.replace('-10月','-10-')
        elif '-11月' in str1:
            str2 = str1.replace('-11月','-11-')
        elif '-12月' in str1:
            str2 = str1.replace('-12月','-12-')

        if '-01月' in str1:
            str2 = str1.replace('-01月','-01-')
        elif '-02月' in str1:
            str2 = str1.replace('-02月','-02-')
        elif '-03月' in str1:
            str2 = str1.replace('-03月','-03-')
        elif '-04月' in str1:
            str2 = str1.replace('-04月','-04-')
        elif '-05月' in str1:
            str2 = str1.replace('-05月','-05-')
        elif '-06月' in str1:
            str2 = str1.replace('-06月','-06-')
        elif '-07月' in str1:
            str2 = str1.replace('-07月','-07-')
        elif '-08月' in str1:
            str2 = str1.replace('-08月','-08-')
        elif '-09月' in str1:
            str2 = str1.replace('-09月','-09-')
    

        if '-一日' in str2:
            str3 = str2.replace('-一日','-01')
        elif '-二日' in str2:
            str3 = str2.replace('-二日','-02')
        elif '-三日' in str2:
            str3 = str2.replace('-三日','-03')
        elif '-四日' in str2:
            str3 = str2.replace('-四日','-04')
        elif '-五日' in str2:
            str3 = str2.replace('-五日','-05')
        elif '-六日' in str2:
            str3 = str2.replace('-六日','-06')
        elif '-七日' in str2:
            str3 = str2.replace('-七日','-07')
        elif '-八日' in str2:
            str3 = str2.replace('-八日','-08')
        elif '-九日' in str2:
            str3 = str2.replace('-九日','-09')
        elif '-十日' in str2:
            str3 = str2.replace('-十日','-10')
        elif '-十一日' in str2:
            str3 = str2.replace('-十一日','-11')
        elif '-十二日' in str2:
            str3 = str2.replace('-十二日','-12')
        elif '-十三日' in str2:
            str3 = str2.replace('-十三日','-13')
        elif '-十四日' in str2:
            str3 = str2.replace('-十四日','-14')
        elif '-十五日' in str2:
            str3 = str2.replace('-十五日','-15')
        elif '-十六日' in str2:
            str3 = str2.replace('-十六日','-16')
        elif '-十七日' in str2:
            str3 = str2.replace('-十七日','-17')
        elif '-十八日' in str2:
            str3 = str2.replace('-十八日','-18')
        elif '-十九日' in str2:
            str3 = str2.replace('-十九日','-19')
        elif '-二十日' in str2:
            str3 = str2.replace('-二十日','-20')
        elif '-二十一日' in str2:
            str3 = str2.replace('-二十一日','-21')
        elif '-二十二日' in str2:
            str3 = str2.replace('-二十二日','-22')
        elif '-二十三日' in str2:
            str3 = str2.replace('-二十三日','-23')
        elif '-二十四日' in str2:
            str3 = str2.replace('-二十四日','-24')
        elif '-二十五日' in str2:
            str3 = str2.replace('-二十五日','-25')
        elif '-二十六日' in str2:
            str3 = str2.replace('-二十六日','-26')
        elif '-二十七日' in str2:
            str3 = str2.replace('-二十七日','-27')
        elif '-二十八日' in str2:
            str3 = str2.replace('-二十八日','-28')
        elif '-二十九日' in str2:
            str3 = str2.replace('-二十九日','-29')
        elif '-三十日' in str2:
            str3 = str2.replace('-三十日','-30')
        elif '-三十一日' in str2:
            str3 = str2.replace('-三十一日','-31')


        if '-1日' in str2:
            str3 = str2.replace('-1日','-01')
        elif '-01日' in str2:
            str3 = str2.replace('-01日','-01')
        elif '-2日' in str2:
            str3 = str2.replace('-2日','-02')
        elif '-02日' in str2:
            str3 = str2.replace('-02日','-02')
        elif '-3日' in str2:
            str3 = str2.replace('-3日','-03')
        elif '-03日' in str2:
            str3 = str2.replace('-03日','-03')
        elif '-4日' in str2:
            str3 = str2.replace('-4日','-04')
        elif '-04日' in str2:
            str3 = str2.replace('-04日','-04')
        elif '-5日' in str2:
            str3 = str2.replace('-5日','-05')
        elif '-05日' in str2:
            str3 = str2.replace('-05日','-05')
        elif '-6日' in str2:
            str3 = str2.replace('-6日','-06')
        elif '-06日' in str2:
            str3 = str2.replace('-06日','-06')
        elif '-7日' in str2:
            str3 = str2.replace('-7日','-07')
        elif '-07日' in str2:
            str3 = str2.replace('-07日','-07')
        elif '-8日' in str2:
            str3 = str2.replace('-8日','-08')
        elif '-08日' in str2:
            str3 = str2.replace('-08日','-08')
        elif '-9日' in str2:
            str3 = str2.replace('-9日','-09')
        elif '-09日' in str2:
            str3 = str2.replace('-09日','-09')
        elif '-10日' in str2:
            str3 = str2.replace('-10日','-10')
        elif '-11日' in str2:
            str3 = str2.replace('-11日','-11')
        elif '-12日' in str2:
            str3 = str2.replace('-12日','-12')
        elif '-13日' in str2:
            str3 = str2.replace('-13日','-13')
        elif '-14日' in str2:
            str3 = str2.replace('-14日','-14')
        elif '-15日' in str2:
            str3 = str2.replace('-15日','-15')
        elif '-16日' in str2:
            str3 = str2.replace('-16日','-16')
        elif '-17日' in str2:
            str3 = str2.replace('-17日','-17')
        elif '-18日' in str2:
            str3 = str2.replace('-18日','-18')
        elif '-19日' in str2:
            str3 = str2.replace('-19日','-19')
        elif '-20日' in str2:
            str3 = str2.replace('-20日','-20')
        elif '-21日' in str2:
            str3 = str2.replace('-21日','-21')
        elif '-22日' in str2:
            str3 = str2.replace('-22日','-22')
        elif '-23日' in str2:
            str3 = str2.replace('-23日','-23')
        elif '-24日' in str2:
            str3 = str2.replace('-24日','-24')
        elif '-25日' in str2:
            str3 = str2.replace('-25日','-25')
        elif '-26日' in str2:
            str3 = str2.replace('-26日','-26')
        elif '-27日' in str2:
            str3 = str2.replace('-27日','-27')
        elif '-28日' in str2:
            str3 = str2.replace('-28日','-28')
        elif '-29日' in str2:
            str3 = str2.replace('-29日','-29')
        elif '-30日' in str2:
            str3 = str2.replace('-30日','-30')
        elif '-31日' in str2:
            str3 = str2.replace('-31日','-31')
    except:
        str3 = '1995-03-03 00:00:00'

    return str3
   
