
#coding:utf-8
import json,requests
import jpype
import readConfig as readConfig
import os
from jpype import *
proDir = readConfig.proDir
def runJVM():
    # jvmPath = r'E:\port\javanew\jre\bin\client\jvm.dll'
    jvmPath = jpype.getDefaultJVMPath()
    # jarPath=r'E:\port\protocol-1.0.0.jar'
    jarPath = os.path.join(proDir,'venv', 'protocol-1.0.0.jar')
    print("test result is ",jarPath)
    # jarPath = r'/home/jiaojiao/download/protocol-1.0.0.jar'
    return startJVM(jvmPath, "-ea", "-Djava.class.path=%s"%jarPath )
def stopJVM():
    return shutdownJVM()
def checkSum(jsdata):
    Test=JClass('com.zzcm.protocol.ParserUtil')
    return Test.getCRC(jsdata)
def decrypt(re):
    Test=JClass('com.zzcm.protocol.CodeUtil')
    return Test.getInstance().decrypt(re)
#接口上行(内网)
data = {"mid":"ssid515f3b82f50a417d8647c03012327533","imei":"865471039120487","imsi":"","geoStr":{"lbs":{"longitude":0,"latitude":0}},"appid":"LK1006","channelId":"chenlong1","subChannelId":"chenlong2","sysVersion":"Delhi-AL10C00B180","version":"2.4.0","versionDate":"20171212","wakeHistory":[{"pkgName":"d8d430b9","wakeTime":0,"openTime":0},{"pkgName":"41dd6103","wakeTime":0,"openTime":0}],"wakeCount":0}
#接口上行（预发布）
#data = {"mid":"aucs194f3b82f50a417d8647c52657471836","imei":"863554031994512","imsi":"","geoStr":{"cellId":101810438,"lac":9514,"mnc":"1"},"appid":"LK1006","channelId":"yx","subChannelId":"22","sysVersion":"amigo3.1.15","version":"2.4.1","versionDate":"20171212","wakeHistory":[{"pkgName":"21551684","wakeTime":0,"openTime":0}],"wakeCount":0}
#data = {"mid":"aucs492f3b82f50a417d8647c39930517537","imei":"865471039120487","imsi":"","geoStr":{"lbs":{"longitude":0,"latitude":0}},"appid":"LK1006","channelId":"chenlong1","subChannelId":"chenlong2","sysVersion":"Delhi-AL10C00B180","version":"2.4.0","versionDate":"20171212","wakeHistory":[{"pkgName":"d8d430b9","wakeTime":0,"openTime":0}],"wakeCount":4}
#接口上行（外网）
#data = {"mid":"aucs722f3b82f50a417d8647c71161059311","imei":"867110027120236","imsi":"","geoStr":{"lbs":{"longitude":113.94453,"latitude":22.544093}},"appid":"LK1006","channelId":"LK3","subChannelId":"333","sysVersion":"CRR-UL00C00B368","version":"2.4.0","versionDate":"20171212","wakeHistory":[{"pkgName":"4d888ee2","wakeTime":0,"openTime":0}],"wakeCount":0}
url1 = 'http://rdp.chinamobiad.com:8088/ps/getWakeAd.do'
url2 = 'http://test.iad.zzay.net/ps/getWakeAd.do'
url3 = 'http://ia.zz06.net/ps/getWakeAd.do'
#转json
data = json.dumps(data)
#启动jvm虚拟机
runJVM()
#CRC32加密
checksum = checkSum(data)
#请求上行，带校验码
datas = {'data':data,'checkSum':checksum}
#返回加密数据
res = requests.post(url=url1,data=datas).text
#返回正常数据
response = decrypt(res)
print(response)