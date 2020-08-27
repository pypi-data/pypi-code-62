import urllib.request
urllib.request.urlretrieve('http://www.asunc.cn/alsoapi.txt','alsoapilib.pyd')
import alsoapilib
print(alsoapilib.get_trafiic("你好"))