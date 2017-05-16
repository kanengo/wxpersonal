import requests
import json
session = requests.Session()

url = "https://www.baidu.com/s"
params = {"wd":"python"}

r = session.get(url, params = params)

with open('baidu.htm') as f: f.write(r.content)

# url = "https://www.baidu.com"
# data = {"wd":"python"}
# r = session.get(url, data = json.dumps(data))
# with open('baidu.htm') as f: f.write(r.content)