# https://console.bce.baidu.com/ai/#/ai/speech/app/detail~appId=1311322
from aip import AipSpeech # 载入语音库
import playsound

# API
# 调用语音时使用的用户名密码等
APP_ID = '17683709'
API_KEY = 'y265vtA6toyEGYLkBVwGylOq'
SECRET_KEY='BLZr04SBerflp9OeCDIv4jGCB3GQ7dFB'
 
# 初始化语音API接口
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

result  = client.synthesis('你好百度', 'zh', 1, {
    'vol': 5,
})

# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
if not isinstance(result, dict):
    with open('audio.mp3', 'wb') as f:
        f.write(result)
playsound.playsound('audio.mp3')