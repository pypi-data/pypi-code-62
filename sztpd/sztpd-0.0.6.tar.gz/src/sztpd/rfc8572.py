# Copyright (c) 2020 Watsen Networks.  All Rights Reserved.

from __future__ import annotations
_A2='RPC "input" node fails YANG validation here: '
_A1='ietf-sztp-bootstrap-server'
_A0='urn:ietf:params:xml:ns:yang:ietf-sztp-bootstrap-server'
_z='Unable to parse "input" JSON document: '
_y='"Accept, when specified, must be "*/*", "application/*", or "application/yang-data+json".'
_x='application/*'
_w='*/*'
_v='Content-Type must be specified when request bodies are passed (RFC 8040, 5.2).'
_u='ssl_object'
_t='Resource does not exist.'
_s='Requested resource does not exist.'
_r=':log-entry'
_q='/devices/device='
_p=':devices/device='
_o='webhooks'
_n='RPC "input" node missing.'
_m='ietf-sztp-bootstrap-server:input'
_l='malformed-message'
_k='bad-attribute'
_j='missing-attribute'
_i='Unhandled exception: '
_h='Parent node does not exist.'
_g='Resource can not be modified.'
_f='webhook'
_e=True
_d='callback'
_c='passed-input'
_b='application/yang-data+xml'
_a=':device'
_Z='operation-not-supported'
_Y='1'
_X=':tenants/tenant='
_W='x'
_V='reference'
_U='name'
_T='Accept'
_S='return-code'
_R='unknown-element'
_Q='path'
_P='method'
_O='source-ip'
_N='timestamp'
_M='access-denied'
_L='application/yang-data+json'
_K='0'
_J='Content-Type'
_I=':dynamic-callout'
_H='application'
_G='invalid-value'
_F='dynamic-callout'
_E='error-returned'
_D='/'
_C='protocol'
_B='event-details'
_A=None
import os,json,base64,pprint,asyncio,aiohttp,yangson,datetime,basicauth,urllib.parse,pkg_resources
from .  import yl
from .  import dal
from .  import utils
from aiohttp import web
from pyasn1.type import univ
from .dal import DataAccessLayer
from .rcsvr import RestconfServer
from .handler import RouteHandler
from .native import Read
from pyasn1_modules import rfc5652
from passlib.hash import sha256_crypt
from pyasn1.codec.der.encoder import encode as encode_der
from pyasn1.codec.der.decoder import decode as der_decoder
from certvalidator import CertificateValidator,ValidationContext,PathBuildingError
from cryptography.hazmat.backends import default_backend
from cryptography import x509
class RFC8572ViewHandler(RouteHandler):
	len_prefix_running=len(RestconfServer.root+'/ds/ietf-datastores:running');len_prefix_operational=len(RestconfServer.root+'/ds/ietf-datastores:operational');len_prefix_operations=len(RestconfServer.root+'/operations');id_ct_sztpConveyedInfoXML=rfc5652._buildOid(1,2,840,113549,1,9,16,1,42);id_ct_sztpConveyedInfoJSON=rfc5652._buildOid(1,2,840,113549,1,9,16,1,43)
	def __init__(A,dal,mode,yl,nvh):A.dal=dal;A.mode=mode;A.nvh=nvh;B=pkg_resources.resource_filename('sztpd','yang/');A.dm=yangson.DataModel(json.dumps(yl),[B])
	async def _insert_bootstrapping_log_entry(A,device_id,bootstrapping_log_entry):
		E='/bootstrapping-log';B=device_id
		if A.mode==_K:C=_D+A.dal.app_ns+':device/bootstrapping-log'
		elif A.mode==_Y:C=_D+A.dal.app_ns+_p+B[0]+E
		elif A.mode==_W:C=_D+A.dal.app_ns+_X+B[1]+_q+B[0]+E
		D={};D[A.dal.app_ns+_r]=bootstrapping_log_entry;await A.dal.handle_post_opstate_request(C,D)
	async def _insert_audit_log_entry(A,tenant_name,audit_log_entry):
		B=tenant_name
		if A.mode==_K or A.mode==_Y or B==_A:C=_D+A.dal.app_ns+':audit-log'
		elif A.mode==_W:C=_D+A.dal.app_ns+_X+B+'/audit-log'
		D={};D[A.dal.app_ns+_r]=audit_log_entry;await A.dal.handle_post_opstate_request(C,D)
	async def handle_get_opstate_request(F,request):
		C=request;D=C.path[F.len_prefix_operational:];G=await F._check_auth(C,D)
		if G is _A:A=web.Response(status=401);E=utils.gen_rc_errors(_C,_M);A.text=json.dumps(E);return A
		B={};B[_N]=datetime.datetime.utcnow();B[_O]=C.remote;B[_P]=C.method;B[_Q]=C.path
		if D=='/ietf-yang-library:yang-library'or D==_D or D=='':A=web.Response(status=200);A.content_type=_L;A.text=getattr(yl,'sbi_rfc8572')()
		else:A=web.Response(status=404);E=utils.gen_rc_errors(_C,_R,error_message=_s);A.text=json.dumps(E);B[_E]=E
		B[_S]=A.status;await F._insert_bootstrapping_log_entry(G,B);return A
	async def handle_get_config_request(E,request):
		C=request;F=C.path[E.len_prefix_running:];G=await E._check_auth(C,F)
		if G is _A:A=web.Response(status=401);D=utils.gen_rc_errors(_C,_M);A.text=json.dumps(D);return A
		B={};B[_N]=datetime.datetime.utcnow();B[_O]=C.remote;B[_P]=C.method;B[_Q]=C.path
		if F==_D or F=='':A=web.Response(status=204)
		else:A=web.Response(status=404);D=utils.gen_rc_errors(_C,_R,error_message=_s);A.text=json.dumps(D);B[_E]=D
		B[_S]=A.status;await E._insert_bootstrapping_log_entry(G,B);return A
	async def handle_post_config_request(E,request):
		D=request;F=D.path[E.len_prefix_running:];G=await E._check_auth(D,F)
		if G is _A:A=web.Response(status=401);C=utils.gen_rc_errors(_C,_M);A.text=json.dumps(C);return A
		B={};B[_N]=datetime.datetime.utcnow();B[_O]=D.remote;B[_P]=D.method;B[_Q]=D.path
		if F==_D or F=='':A=web.Response(status=400);C=utils.gen_rc_errors(_H,_G,error_message=_g);A.text=json.dumps(C)
		else:A=web.Response(status=404);C=utils.gen_rc_errors(_C,_R,error_message=_h);A.text=json.dumps(C)
		B[_S]=A.status;B[_E]=C;await E._insert_bootstrapping_log_entry(G,B);return A
	async def handle_put_config_request(E,request):
		D=request;F=D.path[E.len_prefix_running:];G=await E._check_auth(D,F)
		if G is _A:A=web.Response(status=401);C=utils.gen_rc_errors(_C,_M);A.text=json.dumps(C);return A
		B={};B[_N]=datetime.datetime.utcnow();B[_O]=D.remote;B[_P]=D.method;B[_Q]=D.path
		if F==_D or F=='':A=web.Response(status=400);C=utils.gen_rc_errors(_H,_G,error_message=_g);A.text=json.dumps(C)
		else:A=web.Response(status=404);C=utils.gen_rc_errors(_C,_R,error_message=_h);A.text=json.dumps(C)
		B[_S]=A.status;B[_E]=C;await E._insert_bootstrapping_log_entry(G,B);return A
	async def handle_delete_config_request(E,request):
		D=request;F=D.path[E.len_prefix_running:];G=await E._check_auth(D,F)
		if G is _A:A=web.Response(status=401);C=utils.gen_rc_errors(_C,_M);A.text=json.dumps(C);return A
		B={};B[_N]=datetime.datetime.utcnow();B[_O]=D.remote;B[_P]=D.method;B[_Q]=D.path
		if F==_D or F=='':A=web.Response(status=400);C=utils.gen_rc_errors(_H,_G,error_message=_g);A.text=json.dumps(C)
		else:A=web.Response(status=404);C=utils.gen_rc_errors(_C,_R,error_message=_h);A.text=json.dumps(C)
		B[_S]=A.status;B[_E]=C;await E._insert_bootstrapping_log_entry(G,B);return A
	async def handle_action_request(E,request):
		D=request;F=D.path[E.len_prefix_operational:];G=await E._check_auth(D,F)
		if G is _A:A=web.Response(status=401);C=utils.gen_rc_errors(_C,_M);A.text=json.dumps(C);return A
		B={};B[_N]=datetime.datetime.utcnow();B[_O]=D.remote;B[_P]=D.method;B[_Q]=D.path
		if F==_D or F=='':A=web.Response(status=400);C=utils.gen_rc_errors(_H,_G,error_message='Resource does not support action.');A.text=json.dumps(C)
		else:A=web.Response(status=404);C=utils.gen_rc_errors(_C,_R,error_message=_t);A.text=json.dumps(C)
		B[_S]=A.status;B[_E]=C;await E._insert_bootstrapping_log_entry(G,B);return A
	async def handle_rpc_request(E,request):
		J='is this ever called?';I='sleep';D=request;F=D.path[E.len_prefix_operations:];G=await E._check_auth(D,F)
		if G is _A:A=web.Response(status=401);B=utils.gen_rc_errors(_C,_M);A.text=json.dumps(B);return A
		C={};C[_N]=datetime.datetime.utcnow();C[_O]=D.remote;C[_P]=D.method;C[_Q]=D.path
		if F=='/ietf-sztp-bootstrap-server:get-bootstrapping-data':
			async with E.nvh.fifolock(Read):
				if os.environ.get('SZTPD_MODE')and I in D.query:await asyncio.sleep(int(D.query[I]))
				try:A=await E._handle_get_bootstrapping_data_rpc(G,D,C)
				except NotImplementedError as H:raise NotImplementedError(J);A=web.Response(status=501);B=utils.gen_rc_errors(_H,_Z,error_message=_i+str(H));A.text=json.dumps(B);C[_E]=B
		elif F=='/ietf-sztp-bootstrap-server:report-progress':
			try:A=await E._handle_report_progress_rpc(G,D,C)
			except NotImplementedError as H:raise NotImplementedError(J);A=web.Response(status=501);B=utils.gen_rc_errors(_H,_Z,error_message=_i+str(H));A.text=json.dumps(B);C[_E]=B
		elif F==_D or F=='':A=web.Response(status=400);B=utils.gen_rc_errors(_H,_G,error_message=_t);A.text=json.dumps(B);C[_E]=B
		else:A=web.Response(status=404);B=utils.gen_rc_errors(_C,_R,error_message='Unrecognized RPC.');A.text=json.dumps(B);C[_E]=B
		C[_S]=A.status;await E._insert_bootstrapping_log_entry(G,C);return A
	async def _check_auth(B,request,data_path):
		t='local-truststore-reference';s=':device-type';r='identity-certificates';q='activation-code';p='" not found for any tenant.';o='Device "';n='X-Client-Cert';a='verification';Z='device-type';I='comment';H='failure';G='outcome';D=request;A={};A[_N]=datetime.datetime.utcnow();A[_O]=D.remote;A['source-proxies']=list(D.forwarded);A['host']=D.host;A[_P]=D.method;A[_Q]=D.path;J=set();K=_A;L=D.transport.get_extra_info('peercert')
		if L is not _A:M=L['subject'][-1][0][1];J.add(M)
		elif D.headers.get(n)!=_A:b=D.headers.get(n);R=bytes(urllib.parse.unquote(b),'utf-8');K=x509.load_pem_x509_certificate(R,default_backend());c=K.subject;M=c.get_attributes_for_oid(x509.ObjectIdentifier('2.5.4.5'))[0].value;J.add(M)
		O=_A;S=_A;P=D.headers.get('AUTHORIZATION')
		if P!=_A:O,S=basicauth.decode(P);J.add(O)
		if len(J)==0:A[G]=H;A[I]='Device provided no identification credentials.';await B._insert_audit_log_entry(_A,A);return _A
		if len(J)!=1:A[G]=H;A[I]='Device provided mismatched authentication credentials ('+M+' != '+O+').';await B._insert_audit_log_entry(_A,A);return _A
		E=J.pop();C=_A
		if B.mode==_K:N=_D+B.dal.app_ns+_a
		elif B.mode==_Y:N=_D+B.dal.app_ns+_p+E
		if B.mode!=_W:
			try:C=await B.dal.handle_get_config_request(N)
			except dal.NodeNotFound as T:A[G]=H;A[I]=o+E+p;await B._insert_audit_log_entry(_A,A);return _A
			F=_A
		else:
			try:F=await B.dal.get_tenant_name_for_global_key(_D+B.dal.app_ns+':tenants/tenant/devices/device',E)
			except dal.NodeNotFound as T:A[G]=H;A[I]=o+E+p;await B._insert_audit_log_entry(_A,A);return _A
			N=_D+B.dal.app_ns+_X+F+_q+E;C=await B.dal.handle_get_config_request(N)
		assert C!=_A;assert B.dal.app_ns+_a in C;C=C[B.dal.app_ns+_a]
		if B.mode!=_K:C=C[0]
		if q in C:
			if P==_A:A[G]=H;A[I]='Activation code required but none passed for serial number '+E;await B._insert_audit_log_entry(F,A);return _A
			U=C[q];assert U.startswith('$5$')
			if not sha256_crypt.verify(S,U):A[G]=H;A[I]='Activation code mismatch for serial number '+E;await B._insert_audit_log_entry(F,A);return _A
		else:0
		assert Z in C;d=_D+B.dal.app_ns+':device-types/device-type='+C[Z];V=await B.dal.handle_get_config_request(d)
		if r in V[B.dal.app_ns+s][0]:
			if L is _A and K is _A:A[G]=H;A[I]='Client cert required but none passed for serial number '+E;await B._insert_audit_log_entry(F,A);return _A
			if L:W=D.transport.get_extra_info(_u);assert W is not _A;X=W.getpeercert(_e)
			else:assert K is not _A;X=R
			Q=V[B.dal.app_ns+s][0][r];assert a in Q;assert t in Q[a];Y=Q[a][t];e=_D+B.dal.app_ns+':truststore/certificate-bags/certificate-bag='+Y['certificate-bag']+'/certificate='+Y['certificate'];f=await B.dal.handle_get_config_request(e);g=f[B.dal.app_ns+':certificate'][0]['cert-data'];h=base64.b64decode(g);i,j=der_decoder(h,asn1Spec=rfc5652.ContentInfo());assert not j;k=utils.degenerate_cms_obj_to_ders(i);l=ValidationContext(trust_roots=k);m=CertificateValidator(X,validation_context=l)
			try:m._validate_path()
			except PathBuildingError as T:A[G]=H;A[I]="Client cert for serial number '"+E+"' does not validate using trust anchors specified by device-type '"+C[Z]+"'";await B._insert_audit_log_entry(F,A);return _A
		A[G]='success';await B._insert_audit_log_entry(F,A);return[E,F]
	async def _handle_get_bootstrapping_data_rpc(B,device_id,request,bootstrapping_log_entry):
		Ao='ietf-sztp-bootstrap-server:output';An='ASCII';Am='contentType';Al=':configuration';Ak='configuration-handling';Aj='script';Ai='hash-value';Ah='hash-algorithm';Ag='address';Af='referenced-definition';Ae='exited-normally';Ad='function';Ac='plugin';Ab='callout-type';Aa='serial-number';AZ='rpc-supported';AY='not';AX='match-criteria';AW='matched-response';AV='input';AF='post-configuration-script';AE='configuration';AD='pre-configuration-script';AC='os-version';AB='os-name';AA='trust-anchor';A9='port';A8='bootstrap-server';A7='ietf-sztp-conveyed-info:redirect-information';A6='data-missing';A5='response-manager';w='image-verification';v='download-uri';u='boot-image';t='callback-results';s='selected-response';r='value';l=device_id;k='onboarding-information';g='error-tag';f='key';d='ietf-sztp-conveyed-info:onboarding-information';c='redirect-information';b='error';X='ietf-restconf:errors';L='response';J='managed-response';I='response-details';H=request;E='get-bootstrapping-data-event';D='conveyed-information';C=bootstrapping_log_entry
		if H.body_exists:
			if not _J in H.headers:A=web.Response(status=400);F=utils.gen_rc_errors(_C,_j,error_message=_v);A.text=json.dumps(F);return A
			if H.headers[_J]!=_L:A=web.Response(status=415);F=utils.gen_rc_errors(_C,_k,error_message='Content-Type must be "application/yang-data+json". Got: '+H.headers[_J]);A.text=json.dumps(F);return A
		if _T in H.headers:
			if not any((H.headers[_T]==A for A in(_w,_x,_L))):A=web.Response(status=406);F=utils.gen_rc_errors(_C,_G,error_message=_y);A.text=json.dumps(F);return A
		Y=_A
		if H.body_exists:
			if H.headers[_J]==_L:
				try:Y=await H.json()
				except json.decoder.JSONDecodeError as T:A=web.Response(status=400);F=utils.gen_rc_errors(_C,_l,error_message=_z+str(T));A.text=json.dumps(F);return A
			else:raise NotImplementedError("XML is not supported yet. THIS LINE SHOULDN'T BE REACHED.");assert H.headers[_J]==_b;AG=await H.text();AH={_A0:_A1};Y=xmltodict.parse(AG,process_namespaces=_e,namespaces=AH)
		M=_A
		if Y:
			try:M=Y[_m]
			except KeyError:A=web.Response(status=400);F=utils.gen_rc_errors(_C,_G,error_message=_n);A.text=json.dumps(F);return A
			AI=B.dm.get_schema_node('/ietf-sztp-bootstrap-server:get-bootstrapping-data/input')
			try:AI.from_raw(M)
			except yangson.exceptions.RawMemberError as T:A=web.Response(status=400);F=utils.gen_rc_errors(_C,_G,error_message=_A2+str(T));A.text=json.dumps(F);return A
		if B.mode!=_W:O=_D+B.dal.app_ns+':'
		else:O=_D+B.dal.app_ns+_X+l[1]+_D
		if B.mode==_K:x=O+'device'
		else:x=O+'devices/device='+l[0]
		try:Q=await B.dal.handle_get_config_request(x)
		except Exception as T:A=web.Response(status=501);F=utils.gen_rc_errors(_H,_Z,error_message=_i+str(T));A.text=json.dumps(F);return A
		assert Q!=_A;assert B.dal.app_ns+_a in Q;Q=Q[B.dal.app_ns+_a]
		if B.mode!=_K:Q=Q[0]
		C[_B]={};C[_B][E]={};C[_B][E][_c]={}
		if Y is _A or M is _A:C[_B][E][_c]['no-input-passed']=[_A]
		else:
			C[_B][E][_c][AV]=[]
			for y in M.keys():input={};input[f]=y;input[r]=M[y];C[_B][E][_c][AV].append(input)
		if A5 not in Q or AW not in Q[A5]:A=web.Response(status=404);F=utils.gen_rc_errors(_H,A6,error_message='No responses configured.');A.text=json.dumps(F);C[_E]=F;C[_B][E][s]='no-responses-configured';return A
		G=_A
		for h in Q[A5][AW]:
			if not AX in h:G=h;break
			if Y is _A:continue
			for P in h[AX]['match']:
				if P[f]not in M:break
				if'present'in P:
					if AY in P:
						if P[f]in M:break
					elif P[f]not in M:break
				elif r in P:
					if AY in P:
						if P[r]==M[P[f]]:break
					elif P[r]!=M[P[f]]:break
				else:raise NotImplementedError("Unrecognized 'match' expression.")
			else:G=h;break
		if G is _A or'none'in G[L]:
			if G is _A:C[_B][E][s]='no-match-found'
			else:C[_B][E][s]=G[_U]+" (explicit 'none')"
			A=web.Response(status=404);F=utils.gen_rc_errors(_H,A6,error_message='No matching responses configured.');A.text=json.dumps(F);C[_E]=F;return A
		C[_B][E][s]=G[_U];C[_B][E][I]={J:{}}
		if D in G[L]:
			C[_B][E][I][J]={D:{}};N={}
			if _F in G[L][D]:
				C[_B][E][I][J][D]={_F:{}};assert _V in G[L][D][_F];m=G[L][D][_F][_V];C[_B][E][I][J][D][_F][_U]=m;U=await B.dal.handle_get_config_request(O+'dynamic-callouts/dynamic-callout='+m);assert m==U[B.dal.app_ns+_I][0][_U];C[_B][E][I][J][D][_F][AZ]=U[B.dal.app_ns+_I][0][AZ];Z={}
				if B.mode!=_K:Z[Aa]=l[0]
				else:Z[Aa]='mode-0 == no-sn'
				Z['source-ip-address']=H.remote
				if M:Z['from-device']=M
				z=H.transport.get_extra_info(_u)
				if z:
					A0=z.getpeercert(_e)
					if A0:Z['identity-certificate']=A0
				if _d in U[B.dal.app_ns+_I][0]:
					C[_B][E][I][J][D][_F][Ab]=_d;A1=U[B.dal.app_ns+_I][0][_d][Ac];A2=U[B.dal.app_ns+_I][0][_d][Ad];C[_B][E][I][J][D][_F]['callback-details']={Ac:A1,Ad:A2};C[_B][E][I][J][D][_F][t]={};K=_A
					try:K=B.nvh.plugins[A1]['functions'][A2](Z)
					except Exception as T:C[_B][E][I][J][D][_F][t]['exception-thrown']=str(T);A=web.Response(status=500);F=utils.gen_rc_errors(_H,_Z,error_message='Server encountered an error while trying to generate a response.');A.text=json.dumps(F);C[_E]=F;return A
					assert K and type(K)==dict
					if X in K:
						assert len(K[X][b])==1
						if any((A==K[X][b][0][g]for A in(_G,'too-big',_j,_k,'unknown-attribute','bad-element',_R,'unknown-namespace',_l))):A=web.Response(status=400)
						elif any((A==K[X][b][0][g]for A in _M)):A=web.Response(status=403)
						elif any((A==K[X][b][0][g]for A in('in-use','lock-denied','resource-denied','data-exists',A6))):A=web.Response(status=409)
						elif any((A==K[X][b][0][g]for A in('rollback-failed','operation-failed','partial-operation'))):A=web.Response(status=500)
						elif any((A==K[X][b][0][g]for A in _Z)):A=web.Response(status=501)
						else:raise NotImplementedError('Unrecognized error-tag: '+K[X][b][0][g])
						A.text=json.dumps(K);C[_E]=K;C[_B][E][I][J][D][_F][t][Ae]='Returning an RPC-error provided by callback (NOTE: RPC-error != exception, hence a normal exit).';return A
					else:C[_B][E][I][J][D][_F][t][Ae]='Returning conveyed information provided by callback.'
				elif _o in U[B.dal.app_ns+_I][0]:C[_B][E][I][J][D][_F][Ab]=_f;raise NotImplementedError('webhooks callout support pending!')
				else:raise NotImplementedError('unhandled dynamic callout type: '+str(U[B.dal.app_ns+_I][0]))
				N=K
			elif c in G[L][D]:
				C[_B][E][I][J][D]={c:{}};N[A7]={};N[A7][A8]=[]
				if _V in G[L][D][c]:
					e=G[L][D][c][_V];C[_B][E][I][J][D][c]={Af:e};n=await B.dal.handle_get_config_request(O+'conveyed-information-responses/redirect-information-response='+e)
					for AJ in n[B.dal.app_ns+':redirect-information-response'][0][c][A8]:
						V=await B.dal.handle_get_config_request(O+'bootstrap-servers/bootstrap-server='+AJ);V=V[B.dal.app_ns+':bootstrap-server'][0];i={};i[Ag]=V[Ag]
						if A9 in V:i[A9]=V[A9]
						if AA in V:i[AA]=V[AA]
						N[A7][A8].append(i)
				else:raise NotImplementedError('unhandled redirect-information config type: '+str(G[L][D][c]))
			elif k in G[L][D]:
				C[_B][E][I][J][D]={};N[d]={}
				if _V in G[L][D][k]:
					e=G[L][D][k][_V];C[_B][E][I][J][D][k]={Af:e};n=await B.dal.handle_get_config_request(O+'conveyed-information-responses/onboarding-information-response='+e);R=n[B.dal.app_ns+':onboarding-information-response'][0][k]
					if u in R:
						AK=R[u];AL=await B.dal.handle_get_config_request(O+'boot-images/boot-image='+AK);S=AL[B.dal.app_ns+':boot-image'][0];N[d][u]={};a=N[d][u]
						if AB in S:a[AB]=S[AB]
						if AC in S:a[AC]=S[AC]
						if v in S:
							a[v]=list()
							for AM in S[v]:a[v].append(AM)
						if w in S:
							a[w]=list()
							for A3 in S[w]:o={};o[Ah]=A3[Ah];o[Ai]=A3[Ai];a[w].append(o)
					if AD in R:AN=R[AD];AO=await B.dal.handle_get_config_request(O+'scripts/pre-configuration-script='+AN);N[d][AD]=AO[B.dal.app_ns+':pre-configuration-script'][0][Aj]
					if AE in R:AP=R[AE];A4=await B.dal.handle_get_config_request(O+'configurations/configuration='+AP);N[d][Ak]=A4[B.dal.app_ns+Al][0][Ak];N[d][AE]=A4[B.dal.app_ns+Al][0]['config']
					if AF in R:AQ=R[AF];AR=await B.dal.handle_get_config_request(O+'scripts/post-configuration-script='+AQ);N[d][AF]=AR[B.dal.app_ns+':post-configuration-script'][0][Aj]
			else:raise NotImplementedError('unhandled conveyed-information type: '+str(G[L][D]))
		else:raise NotImplementedError('unhandled response type: '+str(G[L]))
		W=_A
		if _T in H.headers:
			if any((H.headers[_T]==A for A in(_L,_b))):W=H.headers[_T]
		if W is _A:W=H.headers[_J]
		if W==_b:raise NotImplementedError('XML-based response not implemented yet...')
		j=rfc5652.ContentInfo()
		if W==_L:j[Am]=B.id_ct_sztpConveyedInfoJSON;j['content']=encode_der(json.dumps(N,indent=4),asn1Spec=univ.OctetString())
		else:assert W==_b;j[Am]=B.id_ct_sztpConveyedInfoXML;raise NotImplementedError('XML based responses not supported.')
		AS=encode_der(j,rfc5652.ContentInfo());p=base64.b64encode(AS).decode(An);AT=base64.b64decode(p);AU=base64.b64encode(AT).decode(An);assert p==AU;q={};q[Ao]={};q[Ao][D]=p;A=web.Response(status=200);A.content_type=W;A.text=json.dumps(q,indent=4);return A
	async def _handle_report_progress_rpc(B,device_id,request,bootstrapping_log_entry):
		f='remote-port';e='wn-sztpd-rpcs:input';d='webhook-results';U='tcp-client-parameters';T='encoding';R=device_id;Q='http';N='dynamic-callout-result';I='report-progress-event';F=bootstrapping_log_entry;D=request
		if _J not in D.headers:A=web.Response(status=400);C=utils.gen_rc_errors(_C,_j,error_message=_v);A.text=json.dumps(C);return A
		if D.headers[_J]!=_L:A=web.Response(status=415);C=utils.gen_rc_errors(_C,_k,error_message='Content-Type must be "application/yang-data+json".');A.text=json.dumps(C);return A
		if _T in D.headers:
			if not any((D.headers[_T]==A for A in(_w,_x,_L))):A=web.Response(status=406);C=utils.gen_rc_errors(_C,_G,error_message=_y);A.text=json.dumps(C);return A
		G=_A
		if not D.body_exists:A=web.Response(status=400);C=utils.gen_rc_errors(_C,_G,error_message=_n);A.text=json.dumps(C);return A
		if D.headers[_J]==_L:
			try:G=await D.json()
			except json.decoder.JSONDecodeError as H:A=web.Response(status=400);C=utils.gen_rc_errors(_C,_l,error_message=_z+str(H));A.text=json.dumps(C);return A
		else:assert D.headers[_J]==_b;V=await D.text();W={_A0:_A1};G=xmltodict.parse(V,process_namespaces=_e,namespaces=W)
		assert not G is _A
		try:X=G[_m]
		except KeyError:A=web.Response(status=400);C=utils.gen_rc_errors(_C,_G,error_message=_n);A.text=json.dumps(C);return A
		Y=B.dm.get_schema_node('/ietf-sztp-bootstrap-server:report-progress/input')
		try:Y.from_raw(X)
		except (yangson.exceptions.RawMemberError,yangson.exceptions.RawTypeError)as H:A=web.Response(status=400);C=utils.gen_rc_errors(_C,_G,error_message=_A2+str(H));A.text=json.dumps(C);return A
		F[_B]={};F[_B][I]={};F[_B][I][_c]=G[_m];F[_B][I][N]={}
		if B.mode==_K or B.mode==_Y:J=_D+B.dal.app_ns+':preferences/notification-delivery'
		elif B.mode==_W:J=_D+B.dal.app_ns+_X+R[1]+'/preferences/notification-delivery'
		try:Z=await B.dal.handle_get_config_request(J)
		except Exception as H:F[_B][I][N]['no-webhooks-configured']=[_A]
		else:
			O=Z[B.dal.app_ns+':notification-delivery'][_F][_V];F[_B][I][N][_U]=O
			if B.mode==_K or B.mode==_Y:J=_D+B.dal.app_ns+':dynamic-callouts/dynamic-callout='+O
			elif B.mode==_W:J=_D+B.dal.app_ns+_X+R[1]+'/dynamic-callouts/dynamic-callout='+O
			L=await B.dal.handle_get_config_request(J);F[_B][I][N][d]={_f:[]};P={};P[e]={};P[e]['notification']=G;a=json.dumps(P);b='FIXME: xml output'
			if _d in L[B.dal.app_ns+_I][0]:raise NotImplementedError('callback support not implemented yet')
			elif _o in L[B.dal.app_ns+_I][0]:
				for E in L[B.dal.app_ns+_I][0][_o][_f]:
					K={};K[_U]=E[_U]
					if T not in E or E[T]=='json':S=a
					elif E[T]=='xml':S=b
					if Q in E:
						M='http://'+E[Q][U]['remote-address']
						if f in E[Q][U]:M+=':'+str(E[Q][U][f])
						M+='/relay-notification';K['uri']=M
						try:
							async with aiohttp.ClientSession()as c:A=await c.post(M,data=S)
						except aiohttp.client_exceptions.ClientConnectorError as H:K['connection-error']=str(H)
						else:
							K['http-status-code']=A.status
							if A.status==200:break
					else:assert'https'in E;raise NotImplementedError('https-based webhook is not supported yet.')
					F[_B][I][N][d][_f].append(K)
			else:raise NotImplementedError('unrecognized callout type '+str(L[B.dal.app_ns+_I][0]))
		A=web.Response(status=204);return A