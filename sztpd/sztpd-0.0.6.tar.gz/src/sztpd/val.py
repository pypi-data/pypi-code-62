# Copyright (c) 2020 Watsen Networks.  All Rights Reserved.

from __future__ import annotations
_M='Unrecognized member: '
_L='The top-level node-identifier must be prefixed by a namespace followed by a colon.'
_K='Parent data node ('
_J='Input document must contain at least one top-level node.'
_I='Data node ('
_H='Unrecognized schema path: '
_G='Invalid data path: '
_F=":admin-accounts'"
_E='[/] missing-data: expected'
_D='Validation failed: '
_C=') does not exist.'
_B=True
_A='/'
import yangson,asyncio
class NodeAlreadyExists(Exception):0
class NodeNotFound(Exception):0
class ParentNodeNotFound(Exception):0
class InvalidDataPath(Exception):0
class InvalidInputDocument(Exception):0
class UnrecognizedInputNode(Exception):0
class UnrecognizedQueryParameter(Exception):0
class MissingQueryParameter(Exception):0
class NonexistentSchemaNode(Exception):0
class ValidationFailed(Exception):0
class ValidationLayer:
	def __init__(A,dm,dal):
		A.dm=dm;A.dal=dal;C=asyncio.get_event_loop();D=A.dal.handle_get_config_request(_A);E=C.run_until_complete(D);A.inst=A.dm.from_raw(E)
		try:A.inst.validate()
		except yangson.exceptions.SchemaError as B:assert str(B).startswith(_E);assert str(B).endswith(_F)
	async def reload(A):
		C=await A.dal.handle_get_config_request(_A);A.inst=A.dm.from_raw(C)
		try:A.inst.validate()
		except yangson.exceptions.SchemaError as B:assert str(B).startswith(_E);assert str(B).endswith(_F)
	async def handle_get_config_request(C,data_path,query_dict):
		A=data_path;assert A!='';assert not(A!=_A and A[-1]==_A)
		try:D=C.dm.parse_resource_id(A)
		except yangson.exceptions.UnexpectedInput as B:raise InvalidDataPath(_G+str(B))
		except yangson.exceptions.NonexistentSchemaNode as B:raise NonexistentSchemaNode(_H+A)
		try:E=C.inst.goto(D)
		except yangson.exceptions.NonexistentInstance as B:raise NodeNotFound(_I+A+_C)
	async def handle_post_config_request(I,data_path,query_dict,request_body):
		Y='=';Q=None;E=request_body;B=data_path;assert B!='';assert not(B!=_A and B[-1]==_A)
		if len(E)<1:raise InvalidInputDocument(_J)
		if len(E)>1:raise InvalidInputDocument('Input document must not have more than one top-level node.')
		try:R=I.dm.parse_resource_id(B)
		except yangson.exceptions.NonexistentSchemaNode as C:raise NonexistentSchemaNode('Unrecognized schema path for parent node: '+B)
		try:F=I.inst.goto(R)
		except yangson.exceptions.NonexistentInstance as C:raise ParentNodeNotFound(_K+B+_C)
		A=next(iter(E))
		if':'not in A:raise InvalidInputDocument(_L)
		S,G=A.split(':');K=F.schema_node;H=K.get_child(G,S)
		if H is Q:raise UnrecognizedInputNode('Input document contains unrecognized top-level node.')
		if not K.ns is Q:assert K.ns==H.ns
		if isinstance(H,yangson.schemanode.SequenceNode):
			if type(H)==yangson.schemanode.ListNode:
				T=H.keys[0];U=T[0]
				if type(E[A])!=list:raise InvalidInputDocument("Input node '"+G+"' not a 'list' node.")
				if len(E[A])!=1:raise InvalidInputDocument("Input 'list' node '"+G+"' must contain one element.")
				N=E[A][0];O=N[U]
			elif type(H)==yangson.schemanode.LeafListNode:raise NotImplementedError('Inserting into LeafListNode not implemented yet.')
			else:raise AssertionError('Logic cannot reach this point')
			if B==_A:D=A;L=_A+D+Y+O
			else:D=G;L=B+_A+D+Y+O
			try:V=I.dm.parse_resource_id(L)
			except yangson.exceptions.NonexistentSchemaNode as C:raise NonexistentSchemaNode('Unrecognized schema path for insertion node: '+L)
			try:I.inst.goto(V)
			except yangson.exceptions.NonexistentInstance as C:pass
			else:raise NodeAlreadyExists('Child data node ('+L+') already exists.')
			try:J=F[D]
			except yangson.exceptions.NonexistentInstance:J=F.put_member(D,yangson.instvalue.ArrayValue([]))
			assert isinstance(J.schema_node,yangson.schemanode.SequenceNode)
			if len(J.value)==0:
				try:W=J.update([N],raw=_B)
				except yangson.exceptions.RawMemberError as C:raise UnrecognizedInputNode('Incompatable node data. '+str(C))
				M=W.up()
			else:X=J[-1];M=X.insert_after(N,raw=_B).up()
		else:
			if B==_A:D=A
			else:D=G
			if D in F:raise NodeAlreadyExists('Node "'+D+'" already exists.')
			try:
				if K.ns==Q:M=F.put_member(A,E[A],raw=_B).up()
				else:M=F.put_member(G,E[A],raw=_B).up()
			except yangson.exceptions.RawMemberError as C:raise UnrecognizedInputNode(_M+str(C))
		P=M.top()
		try:P.validate()
		except Exception as C:raise ValidationFailed(_D+str(C))
		I.inst2=P
	async def handle_put_config_request(C,data_path,query_dict,request_body):
		D=request_body;B=data_path;assert B!='';assert not(B!=_A and B[-1]==_A)
		if len(D)<1:raise InvalidInputDocument(_J)
		G=next(iter(D))
		if':'not in G:raise InvalidInputDocument(_L)
		try:H=C.dm.parse_resource_id(B)
		except yangson.exceptions.UnexpectedInput as A:raise InvalidDataPath(_G+str(A))
		except yangson.exceptions.NonexistentSchemaNode as A:raise NonexistentSchemaNode(_H+B)
		try:E=C.inst.goto(H)
		except yangson.exceptions.NonexistentInstance as A:
			F=B.rsplit(_A,1)[0]
			if F=='':F=_A
			H=C.dm.parse_resource_id(F)
			try:E=C.inst.goto(H)
			except yangson.exceptions.NonexistentInstance as A:raise ParentNodeNotFound(_K+F+') does not exist. '+str(A))
			await C.handle_post_config_request(F,query_dict,D);return
		try:
			if B==_A:I=E.update(D,raw=_B)
			elif isinstance(E.schema_node,yangson.schemanode.SequenceNode):I=E.update(D[G][0],raw=_B)
			else:I=E.update(D[G],raw=_B)
		except yangson.exceptions.RawMemberError as A:raise UnrecognizedInputNode(_M+str(A))
		except Exception as A:raise NotImplementedError(str(type(A))+' = '+str(A))
		J=I.top()
		try:J.validate()
		except Exception as A:raise ValidationFailed(_D+str(A))
		C.inst2=J
	async def handle_delete_config_request(C,data_path):
		A=data_path;assert A!=''
		if A==_A:E=RootNode(ObjectValue({}),C.inst.schema_node,datetime.now())
		else:
			assert A[0]==_A;assert A[-1]!=_A
			try:J=C.dm.parse_resource_id(A)
			except yangson.exceptions.NonexistentSchemaNode as F:raise NonexistentSchemaNode('Unrecognized schema path for data node: '+A)
			try:D=C.inst.goto(J)
			except yangson.exceptions.NonexistentInstance as F:raise NodeNotFound(_I+A+_C)
			H=D.up()
			if type(D)==yangson.instance.ArrayEntry:
				B=H.delete_item(D.index)
				if len(B.value)==0:
					G=B.up()
					if isinstance(G.schema_node,yangson.schemanode.SequenceNode):I=G.delete_item(B.index);raise NotImplementedError('tested? list inside a list...')
					else:I=G.delete_item(B.name)
					B=I
			else:B=H.delete_item(D.name)
			E=B.top()
		try:E.validate()
		except Exception as F:raise ValidationFailed(_D+str(F))
		C.inst2=E