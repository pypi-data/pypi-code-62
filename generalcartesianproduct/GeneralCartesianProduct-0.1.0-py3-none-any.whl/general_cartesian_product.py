class GeneralCartesianProduct:
	def __init__(self, variables, limits, return_type="array"):
		"""
		:param variables:       [i1, i2, ...]
		:param upperbounds:     {
									'i1': { 'end': m_half, },
									'i2': { 'end': m_half, },
									'j1': { 'end': 0, },
									'j2': { 'end': 0, },
									'u':  { 'end': min_symbolic(m_half-i1, m_half-i2), },
									'v':  { 'end': min_symbolic(m_half-i1, m_half-i2)-u, }
								}
		:param return_type: ["array", "dict", {}]
							if 'array' is select i cant guarantee correct position of the variables. return value is [[1,2], ...]
							if 'dict' is  selcted the reutn value is [{'i1': 1, 'i2': 2}, ...]
							if {} eg. a positioning dict is given. the return value is reordered like this.
								{
									'i1': 0,    # e.g. the position within the returning array
									'i2': 1,
									...
								}
		"""
		self.logging = True     # TODO disable
		self.variables = variables
		self.limits = limits
		self.return_type = return_type

		# error mngt
		if return_type != "array" and return_type != "dict" and type(return_type) != dict:
			print("'return_type' argument must be in ['array', 'dict', type(dict)]")

		# create a list of elements which depend on a different static/dynamic element
		#  e.g.: ['u', 'v']
		self.dynamic_elements = []
		# first work through elements of the config, which are static: e.g. they dont have a dynamic upper bound
		for key, item in self.limits.items():
			is_dep, dep = self.is_element_dynamic(item)
			if is_dep:
				self.dynamic_elements.append(key)

		# this +1 one is important: so both the upper and lower limit will be included.
		self.upperbound = self.get_upper_bound() + 1

		# DO NOT TOUCH
		self.dynamic_elements_iterative = [a for a in self.dynamic_elements]

		# the list holding the main data
		self.polytopes = []
		self.newton_polytope_generator()

	def __iter__(self):
		for polytope in self.polytopes:
			yield polytope

	def __len__(self):
		return len(self.polytopes)

	def __add__(self, other):
		# some error mngtm
		if self.variables != other.variables:
			print("Cant add two GeneralCartesianProduct with different variables.")
			return None

		if self.return_type != other.return_type:
			print("cant add two GeneralCartesianProduct with different return type.")
			return None

		r = GeneralCartesianProduct(self.variables, self.limits, self.return_type)
		r.polytopes = self.polytopes + other.polytopes

		return r

	def is_initialized(self):
		return len(self.polytopes) != 0

	def is_only_depending_on_statc_elements(self):
		return len(self.dynamic_elements) == 0

	def get_end(self, limit, element):
		"""
		access wrapper to limit dictonary

		:param limit:
		:param element:
		:return:
		"""
		try:
			return max(limit[element]['end'], 0)
		except:
			print("ERR: get_end() exception")
			return -1

	def cartesian_product(self, array):
		"""
		mit anderen wortern: gibt der funktion eine liste von listen und du bekommst das kartesische produkt
		:param array: array of upper limits: [range(0), range(1), range(3)]
										or lists
		:return:[
					[0, 0, 0],
					[0, 0, 1],
					[0, 0, 2],
					[0, 1, 0],
					[0, 1, 1],
					[0, 1, 2]
				]
		"""
		result = [[]]
		for a in array:
			result = [x + [y] for x in result for y in a]

		return result

	def half_cartesian_product_of_dict(self, big_dict, key, end, start = 0):
		"""
		so the name is a little bit wrong but who cares
		basic assumption: 'big_dict' consists of several elements = {'i1': 1, 'i2': 2}
					and 'key, start, end' = {'i3' : 2}
		:param big_dict:
		:param key, start, end describing a element
		:return:        = [ {'i1': 1, 'i2': 2, 'i3': 0},  {'i1': 1, 'i2': 2, 'i3': 1},  {'i1': 1, 'i2': 2, 'i3': 2}]
		"""
		# needed for deep copy
		import copy

		r = []
		for i in range(start, end+1):# inclusiv
			tmp_dict = copy.deepcopy(big_dict)
			tmp_dict[key] = i
			r.append(tmp_dict)
		return r

	def apply_dictionary_to_formular(self, dictionary, key):
		"""
		name sucks. But noone cares.

		apply the dictionary 'dictionary' to the rules of 'self.limits[key]'
		:param dictionary: {'i1': 0, 'i2': 1, 'j1': 0, 'j2': 0}
		:param key:     'i1'    a key of the 'self.limits' dictionary
		:return:
		"""
		formular = self.limits[key]
		d = {}
		for var in formular['end'].variables():
			d[var] = dictionary[str(var)]

		return formular['end'].subs(d)

	def get_upper_bound(self):
		"""
		gets the highest numerical value of the 'limits' description dictionary

		"""
		r = 0
		for _, item in self.limits.items():
			# skip every element which is dynamic
			flag, _ = self.is_element_dynamic(item)
			if flag:
				continue

			# this comparison is only well defined if dont allow variables
			if item['end'] > r:
				r = item['end']

		if self.logging:
			print("get_upper_bound: ", r)

		return r

	def is_element_dynamic(self, element):
		"""
		returns a list of dependencies of only ONE element
		and only in the end parameter
		"""
		try:
			flag = len(element['end'].variables()) != 0
			return flag, list(element['end'].variables())
		except:
			return False, []

	def is_formular_depending_only_on_static_elements(self, formular):
		"""
		this name is a little bit dump
		:param dynamic_element:
		:return:
		"""

		for var in formular.variables():
			if str(var) in self.dynamic_elements:
				return False

		return True

	def get_list_dynamic_elements_depending_on_static_elements(self):
		"""
		does what the name says
		:return:
		"""
		r = []
		for dyn_elements in self.dynamic_elements:
			if self.is_formular_depending_only_on_static_elements(self.limits[dyn_elements]['end']):
				r.append(dyn_elements)

		return r

	def is_formular_depending_only_on_exact_amount_of_dynamic_elements(self, formular, nr_of_dependencies):
		"""

		:param nr_of_dependencies:
		:return:
		"""
		i = 0
		for var in formular.variables():
			if str(var) in self.dynamic_elements:
				i += 1

		return i == nr_of_dependencies

	def get_list_dynamic_elements_depending_on_exact_amount_of_dynamic_elements(self, nr_of_dependencies):
		"""

		:param nr_of_dependecies:
		:return:
		"""
		r = []
		for dyn_elements in self.dynamic_elements:
			if self.is_formular_depending_only_on_exact_amount_of_dynamic_elements(self.limits[dyn_elements]['end'], nr_of_dependencies):
				r.append(dyn_elements)

		return r

	def get_static_upper_elements(self):
		"""

		:return:    e.g. {'i1': 2, 'i2': 2, 'j1': 0, 'j2': 0}
		"""

		static_elements = {}

		# first work through elements of the config, which are static: e.g. they dont have a dynamic upper bound
		for key, item in self.limits.items():
			is_dep, dep = self.is_element_dynamic(item)
			if not is_dep:
				static_elements[key] = self.get_end(self.limits, key) # min(self.upperbound, self.get_end(self.limits, key))

		# so now only the variables without a dependency are in 'current_upper_bound'
		if len(static_elements.keys()) == 0:
			print("no variable without a dependency? This cannot be right")
			return None

		return static_elements

	def from_upper_bound_dict_to_array(self, static_upper_elements):
		"""
		TODO comment

		:param d:
		:return:
		"""
		r = []
		for key, item in static_upper_elements.items():
			start = 0
			# check if a lower bound parameter is given. if so, set it as the starting point.
			if 'start' in self.limits[key]:
				start = self.limits[key]['start']

			# just some error/sanity checking
			if start > item:
				# this mostly occurs if we have a static start offset.
				print("this cant be? Why is start (%d) > end (%d): %s" % (start, item, key))
				r.append([start])
			else:
				r.append(list(range(start, item + 1)))

		return r

	def from_upper_bound_dict_to_cartesian_product_dict(self, static_upper_elements):
		"""
		given an dictionary where the values hold the upper bound for a given key.
		this functions returns all possible values generated by the cartesian product.
		:param d:           {'i1':1, 'i2': 1 }
		:param limits:      only important if they have starting values otherwise this is ignored.
		:return:            [{'i1': 0, 'i2': 0}, {'i1': 0, 'i2': 1}, {'i1': 1, 'i2': 0}, {'i1': 1, 'i2': 1}]
		"""
		# needed for deep copy
		import copy

		r = []
		cartesian_prod = self.cartesian_product(self.from_upper_bound_dict_to_array(static_upper_elements))
		for c_p in cartesian_prod:
			tmp_dict = copy.deepcopy(static_upper_elements)

			i = 0
			for key, item in tmp_dict.items():
				tmp_dict[key] = c_p[i]
				i += 1

			r.append(tmp_dict)

		return r

	def inject_dynamic_elements_with_dummy_values(self, current_static_dicts):
		"""

		:param current_static_dicts:
		:return:
		"""
		# needed for deep copy
		import copy

		# return value
		r = []

		for static_dict in current_static_dicts:
			# inject the dynamic still missing variables
			# but first copy it.
			tmp_dict = copy.deepcopy(static_dict)

			for dyn_var in self.dynamic_elements:
				# set it to a a dummy value.
				tmp_dict[dyn_var] = -1

			r.append(tmp_dict)
		return r

	def fill_dynamic_elements(self, fill_dynamic_elements):
		"""

		:param fill_dynamic_elements: [{'i1': 0, 'i2': 0, 'j1': 0, 'j2': 0}, {'i1': 0, 'i2': 1, 'j1': 0, 'j2': 0}]
		:return:
		"""
		# DO NOT COPY 'fill_dynamic_elements' into r. because then we would have a dict wheree not every element has the same amount of elements
		r = []
		dynmic_elements_ = fill_dynamic_elements.copy()

		# first substitute every dynamic element which only depends on static elements
		for dyn_element in self.get_list_dynamic_elements_depending_on_static_elements():
			r_internal = []
			# ok first make sure we set the correct value in the dynamic element fields of the dict.
			for element in dynmic_elements_:
				# print("dynamic element depending on static elements", dyn_element, element)
				d = self.apply_dictionary_to_formular(element, dyn_element)

				start = 0
				if 'start' in self.limits[dyn_element]:
					start = self.limits[dyn_element]['start']

				hcp = self.half_cartesian_product_of_dict(element, dyn_element, d, start=start)
				r_internal += hcp
				# print("hcp", hcp)

			dynmic_elements_ = r_internal
			r = r_internal

		r2 = []

		# we need to check if we have already checked all variabeles. eg.g all given elements are static
		if len(r[0].keys()) == len(self.limits.keys()):
			# ok we already checked all variables.
			r2 = r
		else:
			for element in r:
				# TODO loop reordering like above
				for nr_of_dep in range(1, 10):
					for dyn_element in self.get_list_dynamic_elements_depending_on_exact_amount_of_dynamic_elements(nr_of_dep):
						# print("dynamic element depending on " + str(nr_of_dep) +  " dynamic elements", dyn_element)
						d = self.apply_dictionary_to_formular(element, dyn_element)

						start = 0
						if 'start' in self.limits[dyn_element]:
							start = self.limits[dyn_element]['start']

						hcp = self.half_cartesian_product_of_dict(element, dyn_element, d, start=start)
						r2 += hcp

		return r2

	def newton_polytope_generator(self):
		static_upper_elements = self.get_static_upper_elements()
		cartesia_product_dict = self.from_upper_bound_dict_to_cartesian_product_dict(static_upper_elements)

		if len(self.dynamic_elements) != 0:
			# at this point we injected into every static cartesian product dict all dynamic elements with '-1' as a
			# dummy data. So we have to evaluate them correctly and add the missing range of these.
			dynamic_elements_dict = self.fill_dynamic_elements(cartesia_product_dict)
			# print("dynamic_elements_dict", dynamic_elements_dict, len(dynamic_elements_dict))
		else:
			# ok we dont have any dynamic elements. Nice that's easy
			dynamic_elements_dict = cartesia_product_dict

		# now just transform the output into the right form
		if self.return_type == "array":
			self.polytopes = [list(d.values()) for d in dynamic_elements_dict]
		elif self.return_type == "dict":
			self.polytopes = dynamic_elements_dict
		elif type(self.return_type) == dict:
			limit_len = len(self.limits.keys())
			return_type_len = len(self.return_type.keys())
			if limit_len != return_type_len:
				print("'return_type' dict is not of the right size", limit_len, return_type_len)

			# now copy each dict element into the right position of the newly created array
			for e in dynamic_elements_dict:
				p = [0]*return_type_len
				for key, item in self.return_type.items():
					p[item] = e[key]

				self.polytopes.append(p)
		else:
			print("sorry i dont know what to do.")
			self.polytopes = []

def test_sympy():
	from sympy import symbols
	i1, i2, i3 = symbols('i1 i2 i3')
	rules = {
		'i1': {'start': 1, 'end': 3, },
		'i2': {'start': 1, 'end': 3-i1, },
		'i3': {'end': min_symbolic(i1, i2), },
	}

	cp = GeneralCartesianProduct([i1, i2, i3], rules)
	for i in cp:
		print(i)

def test_sage():
	i1, i2, i3 = var('i1 i2 i3')
	rules = {
		'i1': {'start': 1, 'end': 3, },
		'i2': {'start': 1, 'end': 3-i1, },
		'i3': {'end': 3-i2, },
	}

	cp = GeneralCartesianProduct([i1, i2, i3], rules)
	for i in cp:
		print(i)

from sage.all import *
test_sage()
#test_sympy()