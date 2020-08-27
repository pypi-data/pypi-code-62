# Copyright (c) 2020 Watsen Networks.  All Rights Reserved.

_E='content'
_D='certificates'
_C='certificate'
_B='contentType'
_A=None
import re,pem,base64,textwrap
from pyasn1.type import tag,univ
from pyasn1_modules import rfc5652
from pyasn1_modules import rfc5280
from pyasn1.codec.der import decoder as der_decoder
from pyasn1.codec.der import encoder as der_encoder
def gen_rc_errors(error_type,error_tag,error_app_tag=_A,error_path=_A,error_message=_A,error_info=_A):
	E=error_info;D=error_message;C=error_path;B=error_app_tag;A={};A['error-type']=error_type;A['error-tag']=error_tag
	if B is not _A:A['error-app-tag']=B
	if C is not _A:A['error-path']=C
	if D is not _A:A['error-message']=D
	if E is not _A:A['error-info']=E
	return{'ietf-restconf:errors':{'error':[A]}}
def multipart_pem_to_der_dict(multipart_pem):
	A={};E=pem.parse(bytes(multipart_pem,'utf-8'))
	for F in E:
		C=F.as_text().splitlines();D=base64.b64decode(''.join(C[1:-1]));B=re.sub('-----BEGIN (.*)-----','\\g<1>',C[0])
		if B not in A:A[B]=[D]
		else:A[B].append(D)
	return A
def der_dict_to_multipart_pem(der_dict):
	H='-----\n';C=der_dict;A='';D=C.keys()
	for B in D:
		E=C[B]
		for F in E:G=base64.b64encode(F).decode('ASCII');A+='-----BEGIN '+B+H;A+=textwrap.fill(G,64)+'\n';A+='-----END '+B+H
	return A
def ders_to_degenerate_cms_obj(cert_ders):
	B=rfc5652.CertificateSet().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,0))
	for E in cert_ders:F,G=der_decoder.decode(E,asn1Spec=rfc5280.Certificate());assert not G;D=rfc5652.CertificateChoices();D[_C]=F;B[len(B)]=D
	A=rfc5652.SignedData();A['version']=1;A['digestAlgorithms']=rfc5652.DigestAlgorithmIdentifiers().clear();A['encapContentInfo']['eContentType']=rfc5652.id_data;A[_D]=B;C=rfc5652.ContentInfo();C[_B]=rfc5652.id_signedData;C[_E]=der_encoder.encode(A);return C
def degenerate_cms_obj_to_ders(cms_obj):
	A=cms_obj
	if A[_B]!=rfc5652.id_signedData:raise KeyError('unexpected content type: '+str(A[_B]))
	D,H=der_decoder.decode(A[_E],asn1Spec=rfc5652.SignedData());E=D[_D];B=[]
	for F in E:C=F[_C];assert type(C)==rfc5280.Certificate;G=der_encoder.encode(C);B.append(G)
	return B