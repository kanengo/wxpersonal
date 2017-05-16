import itchat, time, sys

def output_info(msg):
	print('[info] %s' % msg)

def open_QR():
	for get_count in range(10):
		output_info("正在获取 uuid")
		uuid = itchat.get_QRuuid()
		while uuid is None :
			uuid = itchat.get_QRuuid();
			time.sleep(1)
		if itchat.get_QR(uuid, enableCmdQR=True):
			break
		elif get_count >= 9:
			output_info("获取二维码信息失败 请重新运行程序")
			sys.exit()
	output_info("请扫描二维码")
	return uuid

@itchat.msg_register([itchat.content.TEXT])
def get_msg(msg):
	for k, v in msg.items():
		print(k, v)

uuid = open_QR()

while 1:
	status = itchat.check_login(uuid)
	if status == '200':
		break
	elif status == '201':
		output_info("请在手机上确认登陆")
	elif status == '408':
		output_info("二维码已失效 正在重新获取")
		uuid = open_QR()

userInfo = itchat.web_init()
for k, v in userInfo.items():
	print(k, v)
itchat.show_mobile_login()
output_info("获取联系人列表")
contact = itchat.get_contact()
for k in contact:
	print(k)
output_info("登陆成功")
itchat.start_receiving()

itchat.run()
