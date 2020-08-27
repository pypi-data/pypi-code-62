import json,urllib.request,requests
def get_likes(pid):
    try:
        url="http://code.xueersi.com/api/compilers/"+str(pid)+"?id="+str(pid)
        headers = {'Content-Type':'application/json'}
        a=requests.get(url=url, headers=headers)
        null,false,list_get,string=0,0,[],''
        p=json.loads(a.text)
        likes=p["data"]["likes"]
        return likes
    except:
        return -1
def get_unlikes(pid):
    try:
        url="http://code.xueersi.com/api/compilers/"+str(pid)+"?id="+str(pid)
        headers = {'Content-Type':'application/json'}
        a=requests.get(url=url, headers=headers)
        null,false,list_get,string=0,0,[],''
        p=json.loads(a.text)
        unlikes=p["data"]["unlikes"]
        return unlikes
    except:
        return -1
def get_user(pid):
    try:
        url = "http://code.xueersi.com/api/compilers/" + str(pid) + "?id=" + str(pid)
        headers = {'Content-Type': 'application/json'}
        a = requests.get(url=url, headers=headers)
        null, false, list_get, string = 0, 0, [], ''
        p = json.loads(a.text)
        return [p["data"]["username"], p["data"]["user_id"]]
    except:
        return -1
def get_fansnum(pid):
    try:
        url = "http://code.xueersi.com/api/compilers/" + str(pid) + "?id=" + str(pid)
        headers = {'Content-Type': 'application/json'}
        a = requests.get(url=url, headers=headers)
        null, false, list_get, string = 0, 0, [], ''
        p = json.loads(a.text)
        id=p["data"]["user_id"]
        url='https://code.xueersi.com/api/space/index?user_id='+str(id)
        a=json.loads(urllib.request.urlopen(url).read().decode())
        num=a['data']['fans']['total']
        return num
    except:
        return -1
def get_description(pid):
    try:
        url='https://code.xueersi.com/api/compilers/v2/'+str(pid)+'?id='+str(pid)
        a=json.loads(urllib.request.urlopen(url).read().decode())
        return a['data']['description']
    except:
        return -1
def get_codexml(pid):
    try:
        url='https://code.xueersi.com/api/compilers/v2/'+str(pid)+'?id='+str(pid)
        a=json.loads(urllib.request.urlopen(url).read().decode())
        return a['data']['xml']
    except:
        return -1
def get_name_as_pid(pid):
    try:
        url='https://code.xueersi.com/api/compilers/v2/'+str(pid)+'?id='+str(pid)
        a=json.loads(urllib.request.urlopen(url).read().decode())
        return a['data']['name']
    except:
        return -1
def help():
    print(urllib.request.urlopen('http://www.asunc.cn/alsoxeshelp.txt').read().decode("gbk"))
