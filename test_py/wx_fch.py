# -*-encoding:utf-8-*-
import itchat
import time
import os
import re
import imp
from itchat.content import *


msg_dict = {}
fileMap = {
	"Picture":"img",
	"Video":"vid",
	"Recording":"fil",	
}

rec_tmp_dir = "/root/py/wxTmpRec/"
if not os.path.exists(rec_tmp_dir):
	os.mkdir(rec_tmp_dir)

def clearTimeOutMsg():
	if len(msg_dict) > 0:
		for msgId in list(msg_dict.keys()):
			if time.time() - msg_dict.get(msgId, None)['msg_time'] > 130.0:
				msgInfo = msg_dict.pop(msgId)
				if msgInfo['msg_type'] == 'Picture' \
				or msgInfo['msg_type'] == 'Video' \
				or msgInfo['msg_type'] == 'Recording':
					os.remove(rec_tmp_dir + msgInfo["msg_content"])


def fch_handle(msg):
	msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	msg_id = msg['MsgId']
	msg_time = msg['CreateTime']
	msg_from = itchat.search_friends(userName = msg['FromUserName'])['NickName']
	msg_type = msg['Type']
	msg_content = None
	if msg['Type'] == 'Text':
		msg_content = msg['Text']
	elif msg['Type'] == 'Picture' \
		or msg['Type'] == 'Video' \
		or msg['Type'] == "Recording":
		msg_content = r"" + msg['FileName']
		msg['Text'](rec_tmp_dir + msg['FileName'])

	msg_dict[msg_id] = {
				"msg_time_rec":msg_time_rec,
				"msg_time":msg_time,
				"msg_from":msg_from,
				"msg_type":msg_type, 
				"msg_content":msg_content,
			}
	clearTimeOutMsg()


# @itchat.msg_register([TEXT,PICTURE,VIDEO,VOICE])
# def handler_receive_msg(msg):
# 	fch_handle(msg)


def note_handle(msg):
	if re.search(r"\<\!\[CDATA\[.*撤回了一条消息\]\]\>", msg['Content']) is not None:
		oldMsgId = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
		oldMsgInfo = msg_dict.get(oldMsgId, None)
		if oldMsgInfo is not None:
			msg_body = oldMsgInfo["msg_from"] + "在" + oldMsgInfo["msg_time_rec"] + "撤回了一条消息:" + oldMsgInfo["msg_content"]
			itchat.send(msg_body, "filehelper")
			if oldMsgInfo["msg_type"] == "Picture" \
				or oldMsgInfo["msg_type"] == "Video" \
				or oldMsgInfo["msg_type"] == "Recording":
				sendMsg = "@%s@%s" % (fileMap.get(oldMsgInfo["msg_type"]), (rec_tmp_dir + oldMsgInfo["msg_content"]))
				print(sendMsg)
				itchat.send(sendMsg, "filehelper")
				os.remove(rec_tmp_dir + oldMsgInfo["msg_content"])
			msg_dict.pop(oldMsgId)

# @itchat.msg_register([NOTE])
# def handler_note_msg(msg):
# 	note_handle(msg)

if __name__ == '__main__':
	itchat.auto_login(enableCmdQR=True, hotReload=True)
	itchat.run()