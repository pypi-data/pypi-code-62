import requests as rq

def login(name, password):
	r=rq.post('http://www.kooft.ml/login', data={'n':name, 'pwd':password})
	if not r.text == 'uncpwd':
		return 'auth:*'+name+'*'+password
	else:
		return False
def login_simple(u):
	r=rq.post('http://www.kooft.ml/login', data={'n':u.split('*')[1], 'pwd':u.split('*')[2]})
	if not r.text == 'uncpwd':
		return True
	else:
		return False

def view(prov):

	r=rq.get('http://www.kooft.ml/type/'+prov+'/')
	return r.text
def add(user, prov, ttl, content, ad):
	if login_simple(user):
		r=rq.post('http://www.kooft.ml/api_content/add/', data={'type':prov,'author':user.split('*')[1],'ttl':ttl,'txt':content,'ad':ad})
		return r.text
	else:
		return False


