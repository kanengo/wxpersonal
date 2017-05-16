import itchat
import requests
import wx_fch
import weather
from itchat.content import *

KEY = '460731ec46e24fe68e4db086abaadade'

AUTOREPLYTAIL = '[[机器人回复]]'
GET_ROBOT_FAIL = '出错了!机器人找不到回复的消息'
AUTO_REPLY = '@自动回复'
NOT_AUTO_REPLY = '@关闭自动回复'
GET_ROBOT = "@机器人"
GET_ROBOT_REPLY = '你好 我是机器人小N[[机器人回复]]'
NOT_ROBOT = '@关闭机器人'
NOT_ROBOT_REPLY = '下次见~[[机器人回复]]'

WEATHER = "@天气"

def get_response(msg):
	apiUrl = 'http://www.tuling123.com/openapi/api'
	data = {
		'key':KEY,
		'info':msg,
		'userid':'wechat-robot',
	}
	try:
		r = requests.post(apiUrl, data = data).json()
		return r.get('text') + AUTOREPLYTAIL
	except:
		return GET_ROBOT_FAIL+ AUTOREPLYTAIL

autoReplyInfo = {}
isAutoReply = False

@itchat.msg_register([TEXT,PICTURE,VIDEO,VOICE])
def handler_receive_msg(msg):
	global isAutoReply
	global autoReplyInfo

	if msg['Type'] == 'Text':
		text = msg['Text']
		if msg['ToUserName'] == 'filehelper':
			if text == AUTO_REPLY:
				isAutoReply = True
			elif text == NOT_AUTO_REPLY:
				isAutoReply = False
		if text == GET_ROBOT and not msg['FromUserName'] in autoReplyInfo:
			autoReplyInfo[msg['FromUserName']] = True
			itchat.send(GET_ROBOT_REPLY, toUserName = msg['FromUserName'])
		elif text == NOT_ROBOT and msg['FromUserName'] in autoReplyInfo:
			del autoReplyInfo[msg['FromUserName']]
			itchat.send(NOT_ROBOT_REPLY, toUserName = msg['FromUserName'])
		elif text[0:3] == WEATHER:
			weatherRet = weather.getRuntimeWeather(text[4:])
			itchat.send(weatherRet, toUserName = msg['FromUserName'])
		elif isAutoReply or msg['FromUserName'] in autoReplyInfo:
			reply = get_response(msg['Text'])
			itchat.send(reply, toUserName = msg['FromUserName'])

	wx_fch.fch_handle(msg)

@itchat.msg_register([NOTE])
def handler_note_msg(msg):
	wx_fch.note_handle(msg)
#	return msg['Text']

if __name__ == '__main__':
	itchat.auto_login(enableCmdQR=True, hotReload=True)
	itchat.run()