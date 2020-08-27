# Copyright (c) 2020 Watsen Networks.  All Rights Reserved.

_G='tested?'
_F='$0$'
_E='wn-sztpd-0:device'
_D='device'
_C='activation-code'
_B='/'
_A=None
import gc,tracemalloc,os,re,json,signal,asyncio,datetime,functools,pkg_resources
from .  import yl
from .dal import DataAccessLayer,CreateCallbackFailed
from .rcsvr import RestconfServer
from passlib.hash import sha256_crypt
from .tenant import TenantViewHandler
from .rfc8572 import RFC8572ViewHandler
from .native import NativeViewHandler,Period,TimeUnit
loop=_A
sig=_A
def signal_handler(name):global loop;global sig;sig=name;loop.stop()
def run(db_url,cacert_param=_A,cert_param=_A,key_param=_A):
	d=':transport';c='SIGHUP';b=True;V='use-for';U='x';T='1';N=db_url;J=key_param;I=cert_param;H=cacert_param;global loop;global sig;A=_A;B=_A;Q=False
	if H is not _A and N.startswith('sqlite:'):print('The "sqlite" dialect does not support the "cacert" parameter.');return 1
	if(I or J)and not H:print('The "cacert" parameter must be specified whenever the "key" and "cert" parameters are specified.');return 1
	if(I is _A)!=(J is _A):print('The "key" and "cert" parameters must be specified together.');return 1
	try:A=DataAccessLayer(N,H,I,J)
	except (SyntaxError,AssertionError)as K:print(str(K));return 1
	except NotImplementedError as K:Q=b
	else:B=A.opaque()
	if Q==b:
		L=os.environ.get('SZTPD_MODE')
		if L!=_A:
			assert type(L)==str
			if L not in[T,U]:print("Unknown SZTPD_MODE value.  Must be '1' or 'x'.");return 1
			B=L
		else:
			print('');W=pkg_resources.resource_filename('sztpd','LICENSE.txt');R=open(W,'r');print(R.read());R.close();print('First time initialization.  Please accept the license terms.');print('');print('By entering "Yes" below, you agree to be bound to the terms and conditions contained on this screen with Watsen Networks.');print('');X=input('Please enter "Yes" or "No": ')
			if X!='Yes':print('');print('Thank you for your consideration.');print('');return 1
			print('');print('Modes:');print('  1 - single-tenant');print('  x - multi-tenant');print('');B=input('Please select mode: ')
			if B not in[T,U]:print('Unknown mode selection.  Please try again.');return 1
			print('');print("Running SZTPD in mode '"+B+"'. (No more output expected)");print('')
		try:A=DataAccessLayer(N,H,I,J,json.loads(getattr(yl,'nbi_'+B)()),'wn-sztpd-'+B,B)
		except Exception as K:raise K;return 1
	assert B!=_A;assert A!=_A;tracemalloc.start(25);loop=asyncio.get_event_loop();loop.add_signal_handler(signal.SIGHUP,functools.partial(signal_handler,name=c));loop.add_signal_handler(signal.SIGTERM,functools.partial(signal_handler,name='SIGTERM'));loop.add_signal_handler(signal.SIGINT,functools.partial(signal_handler,name='SIGINT'));loop.add_signal_handler(signal.SIGQUIT,functools.partial(signal_handler,name='SIGQUIT'))
	while sig is _A:
		M=[];E=A.handle_get_config_request(_B+A.app_ns+d);O=loop.run_until_complete(E)
		for D in O[A.app_ns+d]['listen']['endpoint']:
			if D[V][0]=='native-interface':
				C=NativeViewHandler(A,B,loop)
				if B=='0':F=_B+A.app_ns+':device'
				elif B==T:F=_B+A.app_ns+':devices/device'
				elif B==U:F=_B+A.app_ns+':tenants/tenant/devices/device'
				C.register_create_callback(F,_handle_device_created);Y=F+'/activation-code';C.register_change_callback(Y,_handle_device_act_code_changed);C.register_subtree_change_callback(F,_handle_device_subtree_changed);C.register_somehow_change_callback(F,_handle_device_somehow_changed);C.register_delete_callback(F,_handle_device_deleted);C.register_periodic_callback(Period(24,TimeUnit.Hours),datetime.datetime(2000,1,1,0),_check_expirations);P=RestconfServer(loop,A,D,C)
			elif D[V][0]=='tenant-interface':Z=TenantViewHandler(C);P=RestconfServer(loop,A,D,Z)
			else:assert D[V][0]=='rfc8572-interface';S=json.loads(getattr(yl,'sbi_rfc8572')());a=RFC8572ViewHandler(A,B,S,C);P=RestconfServer(loop,A,D,a,S)
			M.append(P);del D;D=_A
		del O;O=_A;loop.run_forever()
		for G in M:E=G.app.shutdown();loop.run_until_complete(E);E=G.runner.cleanup();loop.run_until_complete(E);E=G.app.cleanup();loop.run_until_complete(E);del G;G=_A
		del M;M=_A
		if sig==c:sig=_A
	loop.close();del A;return 0
async def _handle_device_created_post_sweep(watched_node_path,conn,opaque):
	k=':dynamic-callout';j='webhooks';i='verification-result';h='failure';g='=';f='tenant';e='function';d='functions';c='plugin';b='callback';a='ownership-authorization';W='verification-results';V='dynamic-callout';U='device-type';T='row_id';S='=[^/]*';J='wn-sztpd-rpcs:output';H=watched_node_path;B=conn;A=opaque;C=A.dal._get_row_data_for_list_path(H,B);D=re.sub(S,'',H);X=A.dal._get_jsob_for_row_id_in_table(D,C[T],B);K=_B+A.dal.app_ns+':device-types/device-type='+X[_D][U];C=A.dal._get_row_data_for_list_path(K,B);D=re.sub(S,'',K);L=A.dal._get_jsob_for_row_id_in_table(D,C[T],B)
	if a in L[U]:
		M=_B+A.dal.app_ns+':dynamic-callouts/dynamic-callout='+L[U][a][V]['reference'];C=A.dal._get_row_data_for_list_path(M,B);D=re.sub(S,'',M);E=A.dal._get_jsob_for_row_id_in_table(D,C[T],B)
		if b in E[V]:
			F=E[V][b];assert F[c]in A.plugins;N=A.plugins[F[c]];assert d in N;O=N[d];assert F[e]in O;Y=O[F[e]];I=H.split(_B)
			if I[2]==f:P=I[1].split(g)[1]
			else:P='not-applicable'
			Q=I[-1].split(g)[1];Z={'wn-sztpd-rpcs:input':{f:P,'serial-number':[Q]}};G=Y(Z);R=h
			if J in G:
				if W in G[J]:
					if i in G[J][W]:R=G[J][W][i][0]['result']
			if R==h:raise CreateCallbackFailed('Unable to verify ownership for device: '+Q)
		else:assert j in E[A.dal.app_ns+k][0];l=E[A.dal.app_ns+k][0][j];raise NotImplementedError('webhooks for ownership verification not implemented yet')
async def _handle_device_created(watched_node_path,jsob,jsob_data_path,nvh,conn):
	C=nvh;B=jsob;assert type(B)==dict
	if jsob_data_path==_B:assert _E in B;A=B[_E]
	else:assert _D in B;A=B[_D]
	if C.dal.post_dal_callbacks is _A:C.dal.post_dal_callbacks=[]
	C.dal.post_dal_callbacks.append((_handle_device_created_post_sweep,watched_node_path,C));A['lifecycle-statistics']={'nbi-access-stats':{'created':datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),'num-times-modified':0},'sbi-access-stats':{'num-times-accessed':0}};A['bootstrapping-log']={'log-entry':[]}
	if _C in A and A[_C].startswith(_F):A[_C]=sha256_crypt.using(rounds=1000).hash(A[_C][3:])
async def _handle_device_act_code_changed(watched_node_path,jsob,jsob_data_path,nvh):
	A=jsob;assert type(A)==dict
	if jsob_data_path==_B:assert _E in A;B=A[_E]
	else:assert _D in A;B=A[_D]
	if _C in B and B[_C].startswith(_F):B[_C]=sha256_crypt.using(rounds=1000).hash(B[_C][3:])
async def _handle_device_subtree_changed(watched_node_path,jsob,jsob_data_path,nvh):raise NotImplementedError(_G)
async def _handle_device_somehow_changed(watched_node_path,jsob,jsob_data_path,nvh):raise NotImplementedError(_G)
async def _handle_device_deleted(data_path,nvh):0
def _check_expirations(nvh):0