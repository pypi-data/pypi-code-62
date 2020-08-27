# Copyright (c) 2020 Watsen Networks.  All Rights Reserved.

from __future__ import annotations
_U='wn-sztpd-x:'
_T='Unable to parse "input" JSON document: '
_S='malformed-message'
_R='wn-sztpd-x'
_Q='/wn-sztpd-x:tenants/tenant=[^ ]*'
_P='/wn-sztpd-x:tenants/tenant=[^/]*/'
_O='Top node names must begin with the "wn-sztpd-1" prefix.'
_N='application'
_M='wn-sztpd-1'
_L='name'
_K='wn-sztpd-1:'
_J='/wn-sztpd-x:tenants/tenant/0/'
_I='Non-root data_paths must begin with "/wn-sztpd-1:".'
_H='wn-sztpd-x:tenant'
_G='invalid-value'
_F='protocol'
_E='/wn-sztpd-x:tenants/tenant='
_D=':'
_C='/wn-sztpd-1:'
_B=None
_A='/'
import re,json,datetime,basicauth
from aiohttp import web
from passlib.hash import sha256_crypt
from .  import yl
from .  import dal
from .  import utils
from .rcsvr import RestconfServer
from .handler import RouteHandler
class TenantViewHandler(RouteHandler):
	def __init__(A,native):A.native=native
	async def _check_auth(C,request):
		K='access-denied';J='comment';I='failure';H='outcome';E=request;A={};A['timestamp']=datetime.datetime.utcnow();A['source-ip']=E.remote;A['source-proxies']=list(E.forwarded);A['host']=E.host;A['method']=E.method;A['path']=E.path;L=E.headers.get('AUTHORIZATION')
		if L is _B:A[H]=I;A[J]='No authorization specified in the HTTP header.';await C.native._insert_audit_log_entry(_B,A);B=web.Response(status=401);D=utils.gen_rc_errors(_F,K);B.text=json.dumps(D);return B
		F,O=basicauth.decode(L);R=_B
		try:G=await C.native.dal.get_tenant_name_for_admin(F)
		except dal.NodeNotFound as S:A[H]=I;A[J]='Unknown admin: '+F;await C.native._insert_audit_log_entry(_B,A);B=web.Response(status=401);D=utils.gen_rc_errors(_F,K);B.text=json.dumps(D);return B
		if G==_B:A[H]=I;A[J]='Host-level admins cannot use tenant interface ('+F+').';await C.native._insert_audit_log_entry(_B,A);B=web.Response(status=401);D=utils.gen_rc_errors(_F,K);B.text=json.dumps(D);return B
		P=_A+C.native.dal.app_ns+':tenants/tenant='+G+'/admin-accounts/admin-account='+F+'/password';Q=await C.native.dal.handle_get_config_request(P);M=Q[C.native.dal.app_ns+':password'];assert M.startswith('$5$')
		if not sha256_crypt.verify(O,M):A[H]=I;A[J]='Password mismatch for admin '+F;await C.native._insert_audit_log_entry(G,A);B=web.Response(status=401);D=utils.gen_rc_errors(_F,K);B.text=json.dumps(D);return B
		A[H]='success';await C.native._insert_audit_log_entry(G,A);N=web.Response(status=200);N.text=G;return N
	async def handle_get_opstate_request(F,request):
		E=request;M=E.path;A=M[RestconfServer.len_prefix_operational:]
		if A=='':A=_A
		elif A!=_A and A[-1]==_A:A=A[:-1]
		B=await F._check_auth(E)
		if B.status==401:return B
		J=B.text;B=await F.native.check_headers(E)
		if B!=_B:return B
		if A=='/ietf-yang-library:yang-library':D=web.Response(status=200);D.content_type='application/yang-data+json';D.text=getattr(yl,'nbi_x_tenant')();return D
		assert A==_A or A.startswith(_C)
		if A==_A:K=_E+J
		else:
			if not A.startswith(_C):D=web.Response(status=400);N=utils.gen_rc_errors(_F,_G,error_message=_I);D.text=json.dumps(N);return D
			Q,L=A.split(_D,1);assert L!=_B;K=_E+J+_A+L
		B,C=await F.native.handle_get_opstate_request_lower_half(K,E.query)
		if C!=_B:
			assert B.status==200;G={}
			if A==_A:
				for H in C[_H][0].keys():
					if H==_L:continue
					G[_K+H]=C[_H][0][H]
			else:I=next(iter(C));assert I.count(_D)==1;O,P=I.split(_D);assert O==_R;assert type(C)==dict;assert len(C)==1;G[_K+P]=C[I]
			B.text=json.dumps(G,indent=2)
		return B
	async def handle_get_config_request(E,request):
		D=request;M=D.path;A=M[RestconfServer.len_prefix_running:]
		if A=='':A=_A
		elif A!=_A and A[-1]==_A:A=A[:-1]
		B=await E._check_auth(D)
		if B.status==401:return B
		I=B.text;B=await E.native.check_headers(D)
		if B!=_B:return B
		assert A==_A or A.startswith(_C)
		if A==_A:J=_E+I
		else:
			if not A.startswith(_C):K=web.Response(status=400);N=utils.gen_rc_errors(_F,_G,error_message=_I);K.text=json.dumps(N);return K
			Q,L=A.split(_D,1);assert L!=_B;J=_E+I+_A+L
		B,C=await E.native.handle_get_config_request_lower_half(J,D.query)
		if C!=_B:
			assert B.status==200;F={}
			if A==_A:
				for G in C[_H][0].keys():
					if G==_L:continue
					F[_K+G]=C[_H][0][G]
			else:H=next(iter(C));assert H.count(_D)==1;O,P=H.split(_D);assert O==_R;assert type(C)==dict;assert len(C)==1;F[_K+P]=C[H]
			B.text=json.dumps(F,indent=2)
		return B
	async def handle_post_config_request(G,request):
		D=request;L=D.path;B=L[RestconfServer.len_prefix_running:]
		if B=='':B=_A
		elif B!=_A and B[-1]==_A:B=B[:-1]
		C=await G._check_auth(D)
		if C.status==401:return C
		I=C.text;C=await G.native.check_headers(D)
		if C!=_B:return C
		if B==_A:J=_E+I
		else:
			if not B.startswith(_C):A=web.Response(status=400);E=utils.gen_rc_errors(_F,_G,error_message=_I);A.text=json.dumps(E);return A
			Q,K=B.split(_D,1);assert K!=_B;J=_E+I+_A+K
		try:F=await D.json()
		except json.decoder.JSONDecodeError as M:A=web.Response(status=400);E=utils.gen_rc_errors(_F,_S,error_message=_T+str(M));A.text=json.dumps(E);return A
		assert type(F)==dict;assert len(F)==1;H=next(iter(F));assert H.count(_D)==1;N,O=H.split(_D)
		if N!=_M:A=web.Response(status=400);E=utils.gen_rc_errors(_N,_G,error_message=_O);A.text=json.dumps(E);return A
		P={_U+O:F[H]};A=await G.native.handle_post_config_request_lower_half(J,D.query,P)
		if A.status!=201:
			if'/wn-sztpdex:tenants/tenant/0/'in A.text:A.text=A.text.replace(_J,_C)
			elif _E in A.text:A.text=re.sub(_P,_C,A.text);A.text=re.sub(_Q,_C,A.text)
		return A
	async def handle_put_config_request(G,request):
		F=request;N=F.path;B=N[RestconfServer.len_prefix_running:]
		if B=='':B=_A
		elif B!=_A and B[-1]==_A:B=B[:-1]
		D=await G._check_auth(F)
		if D.status==401:return D
		H=D.text;D=await G.native.check_headers(F)
		if D!=_B:return D
		if B==_A:L=_E+H
		else:
			if not B.startswith(_C):A=web.Response(status=400);C=utils.gen_rc_errors(_F,_G,error_message=_I);A.text=json.dumps(C);return A
			T,M=B.split(_D,1);assert M!=_B;L=_E+H+_A+M
		try:E=await F.json()
		except json.decoder.JSONDecodeError as O:A=web.Response(status=400);C=utils.gen_rc_errors(_F,_S,error_message=_T+str(O));A.text=json.dumps(C);return A
		if B==_A:
			I={_H:[{_L:H}]}
			for J in E.keys():
				assert J.count(_D)==1;P,Q=J.split(_D)
				if P!=_M:A=web.Response(status=400);C=utils.gen_rc_errors(_N,_G,error_message=_O);A.text=json.dumps(C);return A
				I[_H][0][Q]=E[J]
		else:
			assert type(E)==dict;assert len(E)==1;K=next(iter(E));assert K.count(_D)==1;R,S=K.split(_D)
			if R!=_M:A=web.Response(status=400);C=utils.gen_rc_errors(_N,_G,error_message=_O);A.text=json.dumps(C);return A
			I={_U+S:E[K]}
		A=await G.native.handle_put_config_request_lower_half(L,F.query,I)
		if A.status!=204:
			if _J in A.text:A.text=A.text.replace(_J,_C)
			elif _E in A.text:A.text=re.sub(_P,_C,A.text);A.text=re.sub(_Q,_C,A.text)
		return A
	async def handle_delete_config_request(D,request):
		E=request;I=E.path;B=I[RestconfServer.len_prefix_running:]
		if B=='':B=_A
		elif B!=_A and B[-1]==_A:B=B[:-1]
		C=await D._check_auth(E)
		if C.status==401:return C
		F=C.text;C=await D.native.check_headers(E)
		if C!=_B:return C
		if B==_A:G=_E+F
		else:
			if not B.startswith(_C):A=web.Response(status=400);J=utils.gen_rc_errors(_F,_G,error_message=_I);A.text=json.dumps(J);return A
			K,H=B.split(_D,1);assert H!=_B;G=_E+F+_A+H
		A=await D.native.handle_delete_config_request_lower_half(G)
		if A.status!=204:
			if _J in A.text:A.text=A.text.replace(_J,_C)
			elif _E in A.text:A.text=re.sub(_P,_C,A.text);A.text=re.sub(_Q,_C,A.text)
		return A
	async def handle_action_request(A,request):0
	async def handle_rpc_request(A,request):0