from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from IPython.core.getipython import get_ipython
from iconsdk.exception import JSONRPCException
from iconsdk.builder.transaction_builder import CallTransactionBuilder, TransactionBuilder, DeployTransactionBuilder
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.signed_transaction import SignedTransaction
from repeater import retry
import requests
import json

shell = get_ipython()
icon_service = IconService(HTTPProvider("https://bicon.net.solidwallet.io",3))
RANDOM_ADDRESS = 'hx8b94a3792f336b71937709dae5487166c180c87a'

class Checkscore(object):

	def __init__(self, score_address):
		super(Checkscore, self).__init__()
		self.score_apis = icon_service.get_score_api(score_address)

	def fill_methods(self):

		# remove fallback functions and eventlogs
		filtrd_fns = []
		for i in self.score_apis:
			if i['type'] == "function":
				filtrd_fns.append(i)

		# filter external, readonly and payable functions and reverse them 
		readonly_fns = reversed([d for i,d in enumerate(filtrd_fns) if 'readonly' in d])
		payable_fns = reversed([d for i,d in enumerate(filtrd_fns) if 'payable' in d])
		# for external, filter out payable functions, and then filter out readonly functions
		not_payable_fns = reversed([d for i,d in enumerate(filtrd_fns) if not 'payable' in d])
		external_fns = reversed([d for i,d in enumerate(not_payable_fns) if not 'readonly' in d])
        
		# loop through the functions, pass function name and input parameters
		for i in payable_fns:
			self.payable_function_content(i['name'],[(j['name'], j['type']) for j in i['inputs']])

		self.executable_markdown_cell("## Payable functions") 
		for i in external_fns:
			self.external_function_content(i['name'],[(j['name'], j['type']) for j in i['inputs']])

		self.executable_markdown_cell("## External Functions")
		for i in readonly_fns:
			self.readonly_function_content(i['name'],[(j['name'], j['type']) for j in i['inputs']])

		self.executable_markdown_cell("## Readonly functions")

	def external_function_content(self, fn_name:str, params:list):
		# no parameters
		parameters = ""
		fn = f"method = '{fn_name}'"  +"\n"
		wallet = "wallet = deployer_wallet" + "\n"
		# if there are parameters
		if params:
			attribs = {}
			for i in params:
				if i[1] == "int":
					attribs[i[0]] = 0
				else:
					attribs[i[0]] = ''
			parameters = (f'params = {str(attribs)}\n\n')

		self.create_new_cell(fn, wallet, parameters, None, "external")

	def payable_function_content(self,fn_name:str, params:list):
		fn = f"method = '{fn_name}'"  +"\n"
		wallet = "wallet = deployer_wallet" + "\n"
		parameters = ""
		val = "value = "
		if params:
			attribs = {}
			for i in params:
				if i[1] == "int":
					attribs[i[0]] = 0
				else:
					attribs[i[0]] = ''
			parameters = (f'params = {str(attribs)}\n\n')		

		self.create_new_cell(fn, wallet, parameters, val, "payable")

	def readonly_function_content(self,fn_name:str, params:list):
		fn = f"method = '{fn_name}'"  +"\n"
		parameters = ""
		if params:
			attribs = {}
			for i in params:
				if i[1] == "int":
					attribs[i[0]] = 0
				else:
					attribs[i[0]] = ''
			parameters = (f'params = {str(attribs)}\n\n')

		self.create_new_cell_readonly(fn, parameters)

	def create_new_cell_readonly(self, fn, parameters):
		if parameters != "":
			call = "readonly(method, params)"
		else:
			call = "readonly(method)"

		contents = parameters + fn  + '\n' + call
		payload = dict(
			source='set_next_input',
			text=contents,
			replace=False,
		)
		shell.payload_manager.write_payload(payload, single=False)

	def create_new_cell(self, fn, wallet, parameters, val:None, fn_type):
		if parameters != "":
			if fn_type == "external":
				call = "external(method, wallet, params)"
			if fn_type == "payable":
				call = "payable(method, wallet, value, params)"

			if val:
				contents = parameters + fn + wallet + val + "\n" + call
			else:
				contents = parameters + fn + wallet + "\n" + call
		else:
			if fn_type == "external":
				call = "external(method, wallet)"
			if fn_type == "payable":
				call = "payable(method, wallet, value)"

			if val:
				contents = fn + wallet + val + "\n" + call
			else:
				contents = fn + wallet + "\n" + call

		payload = dict(
			source='set_next_input',
			text=contents,
			replace=False,
		)
		shell.payload_manager.write_payload(payload, single=False)

	def executable_markdown_cell(self, contents):
		payload = dict(
			source='set_next_input',
			text=contents,
			replace=False,
		)
		shell.payload_manager.write_payload(payload, single=False)


def external(fn_name: str, wallet, params=None):
	call_transaction = CallTransactionBuilder()\
			    .from_(wallet.get_address())\
			    .to(SCORE_ADDRESS)\
			    .nid(3)\
			    .nonce(100)\
			    .method(fn_name)\
			    .params(params)\
			    .build()
	transaction(call_transaction, wallet)

def payable(fn_name: str, wallet, value, params=None):
	call_transaction = CallTransactionBuilder()\
			    .from_(wallet.get_address())\
			    .to(SCORE_ADDRESS)\
			    .nid(3)\
			    .nonce(100)\
			    .value(value)\
			    .method(fn_name)\
			    .params(params)\
			    .build()
	transaction(call_transaction, wallet)

def readonly(fn_name: str, params=None):
	call = CallBuilder().from_(RANDOM_ADDRESS)\
	                    .to(SCORE_ADDRESS)\
	                    .method(fn_name)\
	                    .params(params)\
	                    .build()
	print(icon_service.call(call))

def transaction(call_transaction, wallet):
	estimate_step = icon_service.estimate_step(call_transaction)
	step_limit = estimate_step + 100000
	signed_transaction = SignedTransaction(call_transaction, wallet, step_limit)

	tx_hash = icon_service.send_transaction(signed_transaction)
	print(tx_hash)
	print(get_tx_result(tx_hash))


@retry(JSONRPCException, tries=10, delay=1, back_off=2)	
def get_tx_result(tx_hash):
  tx_result = icon_service.get_transaction_result(tx_hash)
  return tx_result