from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
icon_service = IconService(HTTPProvider("https://bicon.net.solidwallet.io",3))

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
		other_fns = reversed([d for i,d in enumerate(filtrd_fns) if not 'payable' or not 'readonly' in d])
        
		# looop through the functions, pass function name and input parameters
		for i in payable_fns:
			self.payable_function_content(i['name'],[j['name'] for j in i['inputs']])

		self.create_new_cell("## Payable functions")
		for i in other_fns:
			self.external_function_content(i['name'],[j['name'] for j in i['inputs']])

		self.create_new_cell("## External Functions")
		for i in readonly_fns:
			self.readonly_function_content(i['name'],[j['name'] for j in i['inputs']])

		self.create_new_cell("## Readonly functions")

	def external_function_content(self, fn_name:str, params:list):
		# no parameters
		a = ""
		b = (f"call_{fn_name}" + " = " + "CallTransactionBuilder()\\" + "\n" +
		    "			.from_(deployer_wallet.get_address())\\" + "\n" +
		    "			.to(SCORE_ADDRESS)\\" + "\n" +
		    "			.step_limit(1000000)\\" + "\n" +
		    "			.nid(3)\\" + "\n" +
		    "			.nonce(100)\\" + "\n" +
		    f"			.method('{fn_name}')\\" + "\n" +
		    "			.build()" + "\n\n")

		# if there are parameters
		if params:
			attribs = {}
			for i in params:
				attribs[i] = ''
			a = (f'params = {str(attribs)}\n\n')
			b = (f"call_{fn_name}" + " = " + "CallTransactionBuilder()\\" + "\n" +
			    "			.from_(deployer_wallet.get_address())\\" + "\n" +
			    "			.to(SCORE_ADDRESS)\\" + "\n" +
			    "			.step_limit(1000000)\\" + "\n" +
			    "			.nid(3)\\" + "\n" +
			    "			.nonce(100)\\" + "\n" +
			    f"			.method('{fn_name}')\\" + "\n" +
			    "			.params(params)\\" + "\n" +
			    "			.build()" + "\n\n")

		c = (f"estimate_step = icon_service.estimate_step(call_{fn_name})" + "\n" +
					"step_limit = estimate_step + 100000" + "\n" +
					f"signed_transaction = SignedTransaction(call_{fn_name}, deployer_wallet, step_limit)" + "\n\n" +

					"tx_hash = icon_service.send_transaction(signed_transaction)" + "\n" +
					"print(tx_hash)" + "\n\n"+

					"get_tx_result(tx_hash)")

		contents = a + b + c
		self.create_new_cell(contents)

	def payable_function_content(self,fn_name:str, params:list):
		a = ""
		b = (f"call_{fn_name}" + " = " + "CallTransactionBuilder()\\" + "\n" +
		    "			.from_(deployer_wallet.get_address())\\" + "\n" +
		    "			.to(SCORE_ADDRESS)\\" + "\n" +
		    "			.step_limit(1000000)\\" + "\n" +
		    "			.nid(3)\\" + "\n" +
		    "			.nonce(100)\\" + "\n" +
		    "			.value()\\" + "\n" +
		    f"			.method('{fn_name}')\\" + "\n" +
		    "			.build()" + "\n\n")

		if params:
			attribs = {}
			for i in params:
				attribs[i] = ''
			a = (f'params = {str(attribs)}\n\n')
			b = (f"call_{fn_name}" + " = " + "CallTransactionBuilder()\\" + "\n" +
			    "			.from_(deployer_wallet.get_address())\\" + "\n" +
			    "			.to(SCORE_ADDRESS)\\" + "\n" +
			    "			.step_limit(1000000)\\" + "\n" +
			    "			.nid(3)\\" + "\n" +
			    "			.nonce(100)\\" + "\n" +
			    "			.value()\\" + "\n" +
			    f"			.method('{fn_name}')\\" + "\n" +
			    "			.params(params)\\" + "\n" +
			    "			.build()" + "\n\n")

		c = (f"estimate_step = icon_service.estimate_step(call_{fn_name})" + "\n" +
					"step_limit = estimate_step + 100000" + "\n" +
					f"signed_transaction = SignedTransaction(call_{fn_name}, deployer_wallet, step_limit)" + "\n\n" +

					"tx_hash = icon_service.send_transaction(signed_transaction)" + "\n" +
					"print(tx_hash)" + "\n\n"+

					"get_tx_result(tx_hash)" )

		contents = a + b + c
		self.create_new_cell(contents)

	def readonly_function_content(self,fn_name:str, params:list):
		a = ""
		b = (f"call_{fn_name}" + " = " + "CallBuilder()\\" + "\n" +
		    "			.from_(deployer_wallet.get_address())\\" + "\n" +
		    "			.to(SCORE_ADDRESS)\\" + "\n" +
		    f"			.method('{fn_name}')\\" + "\n" +
		    "			.build()" + "\n\n" + "\n" +
				f"print(icon_service.call(call_{fn_name}))")

		if params:
			attribs = {}
			for i in params:
				attribs[i] = ' '
			a = (f'params = {str(attribs)}\n\n')
			b = (f"call_{fn_name}" + " = " + "CallBuilder()\\" + "\n" +
			    "			.from_(deployer_wallet.get_address())\\" + "\n" +
			    "			.to(SCORE_ADDRESS)\\" + "\n" +
			    f"			.method('{fn_name}')\\" + "\n" +
			    "			.params(params)\\" + "\n" +
			    "			.build()" + "\n\n" + "\n" +
					f"print(icon_service.call(call_{fn_name}))")

		contents = a + b
		self.create_new_cell(contents)

	def create_new_cell(self, contents):
		from IPython.core.getipython import get_ipython
		shell = get_ipython()

		payload = dict(
			source='set_next_input',
			text=contents,
			replace=False,
		)
		shell.payload_manager.write_payload(payload, single=False)