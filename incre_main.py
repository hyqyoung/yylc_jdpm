#主运行文件
from increment_crawler_init import main_init
from increment_crawler_perform import main_perform
from datetime import datetime
import time

def main():
	while True:
		#clock = datetime.now()
		clock_time = datetime.now().strftime('%H-%M')
		#print(clock_time)
		if clock_time == '16-00':
			#start = time.time()
			main_init()
			#print('hhhhhh')
			main_perform()
			#print('ewdded')
			
			#print('aaa')
			time.sleep(60)
			# end = time.time()
			# run_time = end-start
		else:
			time.sleep(1)

if __name__ == '__main__':
	main()





# keys = []
# values = []
# for key, value in params1.items():
#     if params1[key] != None:
#         keys.append(key)
#         values.append("'" + str(params1[key]) + "'")
# keys_str = ','.join(keys)
# values_str = ','.join(values)
# sql = '''insert into fixed_asset_new(%s) values(%s)''' % (keys_str, values_str)
# print(sql)

keys = []
values =[]
for key,value in data.items():
	if data[key] != None and data[key]:
		keys.append(key)
		values.append(data[key])

values = ',',join(['%s']*len(data))