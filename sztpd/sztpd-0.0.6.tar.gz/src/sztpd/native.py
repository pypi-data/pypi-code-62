# Copyright (c) 2020 Watsen Networks.  All Rights Reserved.

from __future__ import annotations
_f='should check to see if an alarm can be cleared...'
_e='admin-account'
_d='$0$'
_c='%Y-%m-%dT%H:%M:%SZ'
_b='password-last-modified'
_a='module'
_Z='sztpd.plugins.'
_Y="why wasn't this assertion caught by val? "
_X='operation-failed'
_W='data-exists'
_V='Unable to parse "input" JSON document: '
_U='malformed-message'
_T='method'
_S='\\g<1>'
_R='.*plugins/plugin=([^/]*).*'
_Q='missing-attribute'
_P='function'
_O='need to implement this code'
_N='SZTPD_MODE'
_M='application/yang-data+json'
_L='name'
_K='plugin'
_J='operation-not-supported'
_I='functions'
_H='password'
_G='unknown-element'
_F='sleep'
_E='invalid-value'
_D='application'
_C='protocol'
_B=None
_A='/'
import os,re,sys,json,base64,signal,asyncio,yangson,datetime,basicauth,importlib,pkg_resources
from enum import Enum
from aiohttp import web
from enum import IntFlag
from pyasn1.type import univ
from fifolock import FifoLock
from passlib.hash import sha256_crypt
from .dal import DataAccessLayer
from .val import ValidationLayer
from .rcsvr import RestconfServer
from .handler import RouteHandler
from .  import dal
from .  import val
from .  import utils
class RefAction(IntFlag):ADDED=1;REMOVED=2
class TimeUnit(Enum):Days=2;Hours=1;Minutes=0
class Period:
	def __init__(A,amount,units):A.amount=amount;A.units=units
class PluginNotFound(Exception):0
class PluginSyntaxError(Exception):0
class FunctionNotFound(Exception):0
class FunctionNotCallable(Exception):0
class Read(asyncio.Future):
	@staticmethod
	def is_compatible(holds):return not holds[Write]
class Write(asyncio.Future):
	@staticmethod
	def is_compatible(holds):A=holds;return not A[Read]and not A[Write]
class NativeViewHandler(RouteHandler):
	len_prefix_running=RestconfServer.len_prefix_running;len_prefix_operational=RestconfServer.len_prefix_operational;len_prefix_operations=RestconfServer.len_prefix_operations
	def __init__(A,_dal,_mode,_loop):
		O=':preferences/system/plugins/plugin/functions/function';N=':preferences/system/plugins/plugin';M=':tenants/tenant/admin-accounts/admin-account/password';L=':admin-accounts/admin-account/password';K=':plugins';A.dal=_dal;A.mode=_mode;A.loop=_loop;A.fifolock=FifoLock();A.create_callbacks={};A.change_callbacks={};A.delete_callbacks={};A.subtree_change_callbacks={};A.somehow_change_callbacks={};A.leafref_callbacks={};A.periodic_callbacks={};A.onetime_callbacks={};A.plugins={};B=A.dal.handle_get_opstate_request('/ietf-yang-library:yang-library');F=A.loop.run_until_complete(B);G=pkg_resources.resource_filename('sztpd','yang/');A.dm=yangson.DataModel(json.dumps(F),[G]);A.val=ValidationLayer(A.dm,A.dal);B=A.dal.handle_get_opstate_request(_A+A.dal.app_ns+':preferences/system/plugins')
		try:D=A.loop.run_until_complete(B)
		except dal.NodeNotFound:pass
		else:
			if _K in D[A.dal.app_ns+K]:
				for C in D[A.dal.app_ns+K][_K]:
					H=C[_L];B=_handle_plugin_created('',{_K:C},'',A,_B);A.loop.run_until_complete(B)
					if _I in C:
						for E in C[_I][_P]:P=E[_L];I='FOO/plugins/plugin='+H+'/BAR';B=_handle_function_created('',{_P:E},I,A,_B);A.loop.run_until_complete(B)
		A.register_create_callback(_A+A.dal.app_ns+L,_handle_admin_passwd_created);A.register_change_callback(_A+A.dal.app_ns+L,_handle_admin_passwd_changed)
		if A.mode=='x':A.register_create_callback(_A+A.dal.app_ns+M,_handle_admin_passwd_created);A.register_change_callback(_A+A.dal.app_ns+M,_handle_admin_passwd_changed)
		A.register_create_callback(_A+A.dal.app_ns+':tenants/tenant',_handle_tenant_created);A.register_create_callback(_A+A.dal.app_ns+N,_handle_plugin_created);A.register_delete_callback(_A+A.dal.app_ns+N,_handle_plugin_deleted);A.register_create_callback(_A+A.dal.app_ns+O,_handle_function_created);A.register_delete_callback(_A+A.dal.app_ns+O,_handle_function_deleted);A.register_change_callback(_A+A.dal.app_ns+':transport/listen',_handle_transport_changed);A.register_delete_callback(_A+A.dal.app_ns+':transport',_handle_transport_delete);A.register_periodic_callback(Period(24,TimeUnit.Hours),datetime.datetime(2000,1,1,0),_check_expirations)
		for J in A.dal.ref_stat_collectors:A.register_create_callback(J.replace('/reference-statistics',''),_handle_ref_stat_parent_created)
	def register_create_callback(A,schema_path,callback):
		C=callback;B=schema_path
		if B not in A.create_callbacks:A.create_callbacks[B]=[C]
		else:A.create_callbacks[B].append(C)
	def register_change_callback(A,schema_path,callback):
		C=callback;B=schema_path
		if B not in A.change_callbacks:A.change_callbacks[B]=[C]
		else:A.change_callbacks[B].append(C)
	def register_subtree_change_callback(A,schema_path,callback):
		C=callback;B=schema_path
		if B not in A.subtree_change_callbacks:A.subtree_change_callbacks[B]=[C]
		else:A.subtree_change_callbacks[B].append(C)
	def register_somehow_change_callback(A,schema_path,callback):
		C=callback;B=schema_path
		if B not in A.somehow_change_callbacks:A.somehow_change_callbacks[B]=[C]
		else:A.somehow_change_callbacks[B].append(C)
	def register_delete_callback(A,schema_path,callback):
		C=callback;B=schema_path
		if B not in A.delete_callbacks:A.delete_callbacks[B]=[C]
		else:A.delete_callbacks[B].append(C)
	def register_onetime_callback(A,timestamp,callback,opaque):
		B=callback
		if schema_path not in A.onetime_callbacks:A.onetime_callbacks[schema_path]=[B]
		else:A.onetime_callbacks[schema_path].append(B)
	def register_periodic_callback(A,period,anchor,callback):0
	def register_leafref_callback(A,schema_path,callback):
		C=callback;B=schema_path
		if B not in A.leafref_callbacks:A.leafref_callbacks[B]=[C]
		else:A.leafref_callbacks[B].append(C)
	async def _insert_audit_log_entry(A,tenant_name,audit_log_entry):
		C=audit_log_entry;B=tenant_name
		if C[_T]in{'GET','HEAD'}:return
		if B==_B:D=_A+A.dal.app_ns+':audit-log'
		else:F=A.dal.opaque();assert F=='x';D=_A+A.dal.app_ns+':tenants/tenant='+B+'/audit-log'
		E={};E[A.dal.app_ns+':log-entry']=C;await A.dal.handle_post_opstate_request(D,E)
	async def _check_auth(B,request,data_path):
		S='No authorization required for fresh installs.';R=':admin-accounts/admin-account';N='access-denied';M='failure';L='success';G='comment';F='outcome';D=request;A={};A['timestamp']=datetime.datetime.utcnow();A['source-ip']=D.remote;A['source-proxies']=list(D.forwarded);A['host']=D.host;A[_T]=D.method;A['path']=D.path;J=D.headers.get('AUTHORIZATION')
		if J is _B:
			H=await B.dal.num_elements_in_list(_A+B.dal.app_ns+R)
			if H==0:A[F]=L;A[G]=S;await B._insert_audit_log_entry(_B,A);return web.Response(status=200)
			A[F]=M;A[G]='No authorization specified in the HTTP header.';await B._insert_audit_log_entry(_B,A);C=web.Response(status=401);E=utils.gen_rc_errors(_C,N);C.text=json.dumps(E);return C
		I,O=basicauth.decode(J);P=_A+B.dal.app_ns+':admin-accounts/admin-account='+I+'/password'
		try:Q=await B.dal.handle_get_config_request(P)
		except dal.NodeNotFound as T:
			H=await B.dal.num_elements_in_list(_A+B.dal.app_ns+R)
			if H==0:A[F]=L;A[G]=S;await B._insert_audit_log_entry(_B,A);return web.Response(status=200)
			A[F]=M;A[G]='Unknown admin: '+I;await B._insert_audit_log_entry(_B,A);C=web.Response(status=401);E=utils.gen_rc_errors(_C,N);C.text=json.dumps(E);return C
		K=Q[B.dal.app_ns+':password'];assert K.startswith('$5$')
		if not sha256_crypt.verify(O,K):A[F]=M;A[G]='Password mismatch for admin '+I;await B._insert_audit_log_entry(_B,A);C=web.Response(status=401);E=utils.gen_rc_errors(_C,N);C.text=json.dumps(E);return C
		A[F]=L;await B._insert_audit_log_entry(_B,A);return web.Response(status=200)
	async def check_headers(F,request):
		E='Accept';D='Content-Type';B=request
		if any((B.method==A for A in('PUT','POST','PATCH'))):
			if B.body_exists:
				if D not in B.headers:A=web.Response(status=400);C=utils.gen_rc_errors(_C,_Q,error_message='"'+B.method+'" request missing the "Content-Type" header (RFC 8040, 5.2).');A.text=json.dumps(C);return A
				if B.headers[D]!=_M:A=web.Response(status=415);C=utils.gen_rc_errors(_C,_J,error_message='Content-Type, when specified, must be "application/yang-data+json".');A.text=json.dumps(C);return A
		if E in B.headers:
			if not any((B.headers[E]==A for A in('*/*','application/*',_M))):A=web.Response(status=406);C=utils.gen_rc_errors(_C,_E,error_message='The "Accept" type, when set, must be "*/*", "application/*", or "application/yang-data+json".');A.text=json.dumps(C);return A
	async def handle_get_opstate_request(C,request):
		D=request;A=D.path[C.len_prefix_operational:]
		if A=='':A=_A
		elif A!=_A and A[-1]==_A:A=A[:-1]
		B=await C._check_auth(D,A)
		if B.status==401:return B
		B=await C.check_headers(D)
		if B!=_B:return B
		B,E=await C.handle_get_opstate_request_lower_half(A,D.query)
		if E!=_B:B.text=json.dumps(E,indent=4)
		return B
	async def handle_get_opstate_request_lower_half(D,data_path,query_dict):
		E=query_dict
		async with D.fifolock(Read):
			if os.environ.get(_N)and _F in E:await asyncio.sleep(int(E[_F]))
			try:F=await D.dal.handle_get_opstate_request(data_path)
			except dal.NodeNotFound as B:A=web.Response(status=404);C=utils.gen_rc_errors(_C,_G,error_message=str(B));A.text=json.dumps(C);return A,_B
			except NotImplementedError as B:A=web.Response(status=501);C=utils.gen_rc_errors(_D,_J,error_message=str(B));A.text=json.dumps(C);return A,_B
			A=web.Response(status=200);A.content_type=_M;return A,F
	async def handle_get_config_request(C,request):
		D=request;A=D.path[C.len_prefix_running:]
		if A=='':A=_A
		elif A!=_A and A[-1]==_A:A=A[:-1]
		B=await C._check_auth(D,A)
		if B.status==401:return B
		B=await C.check_headers(D)
		if B!=_B:return B
		B,E=await C.handle_get_config_request_lower_half(A,D.query)
		if E!=_B:B.text=json.dumps(E,indent=4)
		return B
	async def handle_get_config_request_lower_half(D,data_path,query_dict):
		F=data_path;E=query_dict
		async with D.fifolock(Read):
			try:await D.val.handle_get_config_request(F,E)
			except val.InvalidDataPath as B:A=web.Response(status=400);C=utils.gen_rc_errors(_C,_E,error_message=str(B));A.text=json.dumps(C);return A,_B
			except val.NonexistentSchemaNode as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_E,error_message=str(B));A.text=json.dumps(C);return A,_B
			except val.NodeNotFound as B:A=web.Response(status=404);C=utils.gen_rc_errors(_C,_G,error_message=str(B));A.text=json.dumps(C);return A,_B
			if os.environ.get(_N)and _F in E:await asyncio.sleep(int(E[_F]))
			try:G=await D.dal.handle_get_config_request(F)
			except dal.NodeNotFound as B:A=web.Response(status=404);C=utils.gen_rc_errors(_C,_G,error_message=str(B));A.text=json.dumps(C);return A,_B
			A=web.Response(status=200);A.content_type=_M;return A,G
	async def handle_post_config_request(D,request):
		B=request;A=B.path[D.len_prefix_running:]
		if A=='':A=_A
		elif A!=_A and A[-1]==_A:A=A[:-1]
		C=await D._check_auth(B,A)
		if C.status==401:return C
		C=await D.check_headers(B)
		if C!=_B:return C
		try:F=await B.json()
		except json.decoder.JSONDecodeError as G:E=web.Response(status=400);H=utils.gen_rc_errors(_C,_U,error_message=_V+str(G));E.text=json.dumps(H);return E
		return await D.handle_post_config_request_lower_half(A,B.query,F)
	async def handle_post_config_request_lower_half(D,data_path,query_dict,request_body):
		G=request_body;F=data_path;E=query_dict
		async with D.fifolock(Write):
			try:await D.val.handle_post_config_request(F,E,G)
			except (val.InvalidInputDocument,val.UnrecognizedQueryParameter)as B:A=web.Response(status=400);C=utils.gen_rc_errors(_C,_E,error_message=str(B));A.text=json.dumps(C);return A
			except val.MissingQueryParameter as B:A=web.Response(status=400);C=utils.gen_rc_errors(_C,_Q,error_message=str(B));A.text=json.dumps(C);return A
			except val.NonexistentSchemaNode as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_E,error_message=str(B));A.text=json.dumps(C);return A
			except val.ValidationFailed as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_E,error_message=str(B));A.text=json.dumps(C);return A
			except val.ParentNodeNotFound as B:A=web.Response(status=404);C=utils.gen_rc_errors(_C,_G,error_message=str(B));A.text=json.dumps(C);return A
			except val.UnrecognizedInputNode as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_G,error_message=str(B));A.text=json.dumps(C);return A
			except NotImplementedError as B:A=web.Response(status=501);C=utils.gen_rc_errors(_D,_J,error_message=str(B));A.text=json.dumps(C);return A
			except val.NodeAlreadyExists as B:A=web.Response(status=409);C=utils.gen_rc_errors(_D,_W,error_message=str(B));A.text=json.dumps(C);return A
			if os.environ.get(_N)and _F in E:await asyncio.sleep(int(E[_F]))
			try:await D.dal.handle_post_config_request(F,G,D.create_callbacks,D.change_callbacks,D)
			except dal.CreateCallbackFailed as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_X,error_message=str(B));A.text=json.dumps(C);return A
			except Exception as B:raise Exception(_Y+str(B))
			D.val.inst=D.val.inst2;D.val.inst2=_B;await D.shared_post_commit_logic();return web.Response(status=201)
	async def handle_put_config_request(D,request):
		B=request;A=B.path[D.len_prefix_running:]
		if A=='':A=_A
		elif A!=_A and A[-1]==_A:A=A[:-1]
		C=await D._check_auth(B,A)
		if C.status==401:return C
		C=await D.check_headers(B)
		if C!=_B:return C
		try:F=await B.json()
		except json.decoder.JSONDecodeError as G:E=web.Response(status=400);H=utils.gen_rc_errors(_C,_U,error_message=_V+str(G));E.text=json.dumps(H);return E
		return await D.handle_put_config_request_lower_half(A,B.query,F)
	async def handle_put_config_request_lower_half(D,data_path,query_dict,request_body):
		G=request_body;F=data_path;E=query_dict
		async with D.fifolock(Write):
			try:await D.val.handle_put_config_request(F,E,G)
			except val.InvalidDataPath as B:A=web.Response(status=400);C=utils.gen_rc_errors(_C,_E,error_message=str(B));A.text=json.dumps(C);return A
			except val.ParentNodeNotFound as B:A=web.Response(status=404);C=utils.gen_rc_errors(_C,_G,error_message=str(B));A.text=json.dumps(C);return A
			except val.UnrecognizedInputNode as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_G,error_message=str(B));A.text=json.dumps(C);return A
			except (val.NonexistentSchemaNode,val.ValidationFailed)as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_E,error_message=str(B));A.text=json.dumps(C);return A
			except (val.InvalidInputDocument,val.UnrecognizedQueryParameter)as B:A=web.Response(status=400);C=utils.gen_rc_errors(_C,_E,error_message=str(B));A.text=json.dumps(C);return A
			except val.MissingQueryParameter as B:A=web.Response(status=400);C=utils.gen_rc_errors(_C,_Q,error_message=str(B));A.text=json.dumps(C);return A
			except val.NodeAlreadyExists as B:A=web.Response(status=409);C=utils.gen_rc_errors(_D,_W,error_message=str(B));A.text=json.dumps(C);return A
			except NotImplementedError as B:A=web.Response(status=501);C=utils.gen_rc_errors(_D,_J,error_message=str(B));A.text=json.dumps(C);return A
			if os.environ.get(_N)and _F in E:await asyncio.sleep(int(E[_F]))
			try:await D.dal.handle_put_config_request(F,G,D.create_callbacks,D.change_callbacks,D.delete_callbacks,D)
			except dal.CreateCallbackFailed as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_X,error_message=str(B));A.text=json.dumps(C);return A
			except (PluginNotFound,PluginSyntaxError,FunctionNotFound,FunctionNotCallable)as B:A=web.Response(status=501);C=utils.gen_rc_errors(_D,_J,error_message=str(B));A.text=json.dumps(C);return A
			except Exception as B:raise Exception("why wasn't this assertion caught by val? (assuming it's a YANG validation thing)"+str(B))
			D.val.inst=D.val.inst2;D.val.inst2=_B;await D.shared_post_commit_logic();return web.Response(status=204)
	async def handle_delete_config_request(C,request):
		D=request;A=D.path[C.len_prefix_running:]
		if A=='':A=_A
		elif A!=_A and A[-1]==_A:A=A[:-1]
		B=await C._check_auth(D,A)
		if B.status==401:return B
		B=await C.check_headers(D)
		if B!=_B:return B
		return await C.handle_delete_config_request_lower_half(A)
	async def handle_delete_config_request_lower_half(A,data_path):
		E=data_path
		async with A.fifolock(Write):
			try:await A.val.handle_delete_config_request(E)
			except val.NonexistentSchemaNode as C:B=web.Response(status=400);D=utils.gen_rc_errors(_D,_E,error_message=str(C));B.text=json.dumps(D);return B
			except val.NodeNotFound as C:B=web.Response(status=404);D=utils.gen_rc_errors(_C,_G,error_message=str(C));B.text=json.dumps(D);return B
			except val.ValidationFailed as C:B=web.Response(status=400);D=utils.gen_rc_errors(_D,_E,error_message=str(C));B.text=json.dumps(D);return B
			try:await A.dal.handle_delete_config_request(E,A.delete_callbacks,A.change_callbacks,A)
			except Exception as C:raise Exception(_Y+str(C))
			A.val.inst=A.val.inst2;A.val.inst2=_B;await A.shared_post_commit_logic();return web.Response(status=204)
	async def shared_post_commit_logic(A):0
	async def handle_action_request(A,request):0
	async def handle_rpc_request(A,request):raise NotImplementedError('Native needs an RPC handler?  - client accessible!')
	def _handle_generate_symmetric_key_action(A,data_path,action_input):raise NotImplementedError(_O)
	def _handle_generate_asymmetric_key_action(A,data_path,action_input):raise NotImplementedError(_O)
	def _handle_resend_activation_email_action(A,data_path,action_input):raise NotImplementedError(_O)
	def _handle_generate_certificate_signing_request_action(A,data_path,action_input):raise NotImplementedError(_O)
async def _handle_tenant_created(watched_node_path,jsob,jsob_data_path,obj,conn):jsob['tenant']['audit-log']={}
async def _handle_transport_changed(watched_node_path,jsob,jsob_data_path,obj):os.kill(os.getpid(),signal.SIGHUP)
async def _handle_transport_delete(watched_node_path,opaque):raise NotImplementedError('Deleting the /transport node itself cannot be constrained by YANG.')
async def _handle_plugin_created(watched_node_path,jsob,jsob_data_path,opaque,conn):
	B=opaque;A=jsob[_K][_L];C=_Z+A
	if A in B.plugins:E=sys.modules[C];del sys.modules[C];del E;del B.plugins[A]
	try:F=importlib.import_module(C)
	except ModuleNotFoundError as D:raise PluginNotFound(str(D))
	except SyntaxError as D:raise PluginSyntaxError('SyntaxError: '+str(D))
	B.plugins[A]={_a:F,_I:{}}
async def _handle_plugin_deleted(watched_node_path,opaque):C=opaque;A=re.sub(_R,_S,watched_node_path);B=_Z+A;D=sys.modules[B];del sys.modules[B];del D;del C.plugins[A]
async def _handle_function_created(watched_node_path,jsob,jsob_data_path,opaque,conn):
	B=opaque;C=re.sub(_R,_S,jsob_data_path);A=jsob[_P][_L]
	try:D=getattr(B.plugins[C][_a],A)
	except AttributeError as E:raise FunctionNotFound(str(E))
	if not callable(D):raise FunctionNotCallable("The plugin function name '"+A+"' is not callable.")
	B.plugins[C][_I][A]=D
async def _handle_function_deleted(watched_node_path,opaque):A=watched_node_path;B=opaque;C=re.sub(_R,_S,A);D=A.rsplit('=',1)[1];del B.plugins[C][_I][D]
async def _handle_admin_passwd_created(watched_node_path,jsob,jsob_data_path,obj,conn):
	A=jsob
	def B(item):
		A=item;A[_b]=datetime.datetime.utcnow().strftime(_c)
		if _H in A and A[_H].startswith(_d):A[_H]=sha256_crypt.using(rounds=1000).hash(A[_H][3:])
	if type(A)==dict:B(A[_e])
	else:
		assert False;assert type(A)==list
		for C in A:assert type(C)==dict;B(C)
async def _handle_admin_passwd_changed(watched_node_path,json,jsob_data_path,obj):
	def A(item):
		A=item;A[_b]=datetime.datetime.utcnow().strftime(_c)
		if _H in A and A[_H].startswith(_d):A[_H]=sha256_crypt.using(rounds=1000).hash(A[_H][3:])
		else:0
	assert json!=_B;assert jsob_data_path!=_B;A(json[_e])
async def _handle_ref_stat_parent_created(watched_node_path,jsob,jsob_data_path,obj,conn):
	A=jsob;assert watched_node_path==jsob_data_path
	def B(item):item['reference-statistics']={'reference-count':0,'last-referenced':'never'}
	if type(A)==dict:D=next(iter(A));B(A[D])
	else:
		raise NotImplementedError('dead code?');assert type(A)==list
		for C in A:assert type(C)==dict;B(C)
def _handle_ref_stats_changed(leafrefed_node_data_path,obj):raise NotImplementedError('_handle_ref_stats_changed tested?')
def _handle_lingering_unreferenced_node_change(watched_node_path,obj):raise NotImplementedError(_f)
def _handle_expiring_certificate_change(watched_node_path,obj):raise NotImplementedError(_f)
async def _check_expirations(nvh):0