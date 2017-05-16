import requests

KEY = '57fa6a316c9d46dc8a225f2870b07e9e'  # API key
UID = "U919A7B33E"  # 用户ID
#https://api.seniverse.com/v3/weather/now.json'
LOCATION = 'guangzhou'  # 所查询的位置，可以使用城市拼音、v3 ID、经纬度等
nowUrl = 'https://free-api.heweather.com/v5/now' # API URL，可替换为其他 URL
UNIT = 'c'  # 单位
LANGUAGE = 'zh-Hans'  # 查询结果的返回语言

GET_RUNTIME_WEATERH_ERROR = "获取实时天气出错"

RUNTIME_WEATERH_FORMAT  = """实时天气情况
国家:{cnty}
城市:{city}
天气状况:{cond}
体感温度:{fl}℃
相对湿度:{hum}%
降水量:{pcpn}mm
气压:{pres}hpa
温度:{tmp}℃
能见度:{vis}km
风向:{dir}
风力:{sc}
风速:{spd}kmph
更新时间:{updatetime}"""
#"https://free-api.heweather.com/v5/"

def pasreRuntimeWeatherInfo(weatherInfo):
	return RUNTIME_WEATERH_FORMAT.format(
		cnty = weatherInfo['basic']['cnty'], 
		city = weatherInfo['basic']['city'],
		updatetime = weatherInfo['basic']['update']['loc'],
		cond = weatherInfo['now']['cond']['txt'],
		fl = weatherInfo['now']['fl'],
		hum = weatherInfo['now']['hum'],
		pcpn = weatherInfo['now']['pcpn'],
		pres = weatherInfo['now']['pres'],
		tmp = weatherInfo['now']['tmp'],
		vis = weatherInfo['now']['vis'],
		dir = weatherInfo['now']['wind']['dir'],
		sc = weatherInfo['now']['wind']['sc'],
		spd = weatherInfo['now']['wind']['spd'],
		)


def getRuntimeWeather(city = LOCATION):
	if city == '':
		city = LOCATION
	ret = requests.get(nowUrl, params = {
		'key':KEY,
		'city' : city,
		}).json()

	weatherInfo = ret['HeWeather5'][0]
	if weatherInfo['status'] != 'ok':
		return GET_RUNTIME_WEATERH_ERROR + ":" + weatherInfo['status']

	return pasreRuntimeWeatherInfo(weatherInfo)

if __name__ == '__main__':
	print(getRuntimeWeather("广州"))
	

	
