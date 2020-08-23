class branch:

	def __init__(self):
		pass

class exectutable:

	def __init__(self, function):
		self.set = function

class root:
	
	def __init__(self):
		self.cmd = []

		'''
		FILE SECTION
		'''
		self.file = branch()
		self.file.read_case = exectutable(root.read_case)
		self.file.read_journal = exectutable(root.read_journal)
		self.file.mesh_replace = exectutable(root.mesh_replace)
		self.file.write_case = exectutable(root.write_case)
		self.write_case_data = exectutable(root.write_case_data)
		
		'''
		DEFINE SECTION
		'''
		self.define = branch()
		self.define.boundary_conditions = branch()
		self.define.boundary_conditions.velocity_inlet = exectutable(root.bc_velocity_inlet)
		self.define.boundary_conditions.pressure_outlet = exectutable(root.bc_pressure_outlet)
		self.define.boundary_conditions.wall = exectutable(root.bc_wall)

		self.define.models = branch()
		self.define.models.viscous = exectutable(root.viscous)

		'''
		SURFACE SECTION
		'''
		self.surface = branch()
		self.surface.line_surface = exectutable(root.line_surface)
		self.surface.point_surface = exectutable(root.point_surface)

		'''
		MESH SECTION
		'''
		self.mesh = branch()
		self.mesh.translate = exectutable(root.translate)

		self.mesh.modify_zones = branch()
		self.mesh.modify_zones.append_mesh = exectutable(root.append_mesh)
		self.mesh.modify_zones.merge_zones = exectutable(root.merge_zones)
		self.mesh.modify_zones.fuse_face_zones = exectutable(root.fuse_face_zones)
		self.mesh.modify_zones.zone_name = exectutable(root.zone_name)

		self.mesh.check = exectutable(root.check)

		self.mesh.repair_improve = branch()
		self.mesh.repair_improve.repair = exectutable(root.repair)

		'''
		SOLVE SECTION
		'''
		self.solve = branch()

		self.solve.monitors = branch()
		self.solve.monitors.residual = branch()
		self.solve.monitors.residual.convergence_criteria = exectutable(root.convergence_criteria)

		self.solve.initialize = branch()
		self.solve.initialize.initialize_flow = exectutable(root.initialize_flow)

		self.solve.initialize.compute_defaults = branch()
		self.solve.initialize.compute_defaults.velocity_inlet = exectutable(root.cd_velocity_inlet)

		self.solve.iterate = exectutable(root.iterate)

		'''
		REPORT SECTION
		'''
		self.report = branch()
		self.report.fluxes = branch()
		self.report.fluxes.mass_flow = exectutable(root.mass_flow)
		self.report.fluxes.heat_transfer = exectutable(root.heat_transfer)

		self.report.surface_integrals = branch()
		self.report.surface_integrals.facet_avg = exectutable(root.facet_avg)

	def save(self, path):
		with open(path, 'w') as f:
			for item in self.cmd:
				f.write('%s\n' % item)

	'''
	EXECUTABLES
	'''

	__yn = {
		True: 'yes',
		False: 'no'
	}

	'''
	FILE SECTION
	'''
	@staticmethod
	def read_case(root, case_path, overwrite=True):
		root.cmd += [
			'/file/read-case "{}" {} '.\
			format(case_path, root.__yn.get(overwrite))
		]

	@staticmethod
	def read_journal(root, jou_path):
		if type(jou_path) == str:
			jou_path = [jou_path]
		root.cmd += [
			'/file/read-journal\n {}'.\
			format('\n'.join(jou_path))
		]

	@staticmethod
	def write_case(root, case_path, overwrite=True):
		root.cmd += [
			'/file/write-case "{}" {} '.\
			format(case_path, root.__yn.get(overwrite))
		]

	@staticmethod
	def write_case_data(root, case_path, overwrite=True):
		root.cmd += [
			'/file/write-case-data "{}" {} '.\
			format(case_path, root.__yn.get(overwrite))
		]

	@staticmethod
	def mesh_replace(root, mesh_path, discard=True):
		root.cmd += [
			'/file/replace-mesh "{}" {} '.\
			format(mesh_path, root.__yn.get(discard))
		]

	'''
	DEFINE SECTION
	'''
	@staticmethod
	def bc_velocity_inlet(root, name, velocity, temperature):
		root.cmd += [
			'/define/boundary-conditions velocity-inlet {} no yes yes no 0 no {} no 0 no {} no no no yes 5 0.01 '.\
			format(name, velocity, temperature)
		]

	@staticmethod
	def bc_pressure_outlet(root, name, temperature):
		root.cmd += [
			'/define/boundary-conditions/pressure-outlet {} yes no 0. no {} no yes no no n yes 5. 0.01 yes no no no '.\
			format(name, temperature)
		]
	
	@staticmethod
	def bc_wall(root, name, temperature, fluid=True):
		if fluid:
			root.cmd += [
				'/define/boundary-conditions/wall {} 0. no 0. no yes temperature no {} no no no 0. no 0. no 1 '.\
				format(name, temperature)
			]
		else:
			root.cmd += [
				'/define/boundary-conditions/wall {} 0. no 0. no yes temperature no {} no 1 '.\
				format(name, temperature)
			]

	@staticmethod
	def viscous(root, model):
		root.cmd += [
			'/define/models/viscous/{} yes '.\
			format(model)
		]

	'''
	SURFACE SECTION
	'''
	@staticmethod
	def line_surface(root, name, x1, y1, x2, y2):
		root.cmd += [
			'/surface/line-surface {} {} {} {} {}'.\
			format(name, x1, y1, x2, y2)
		]
	
	@staticmethod
	def point_surface(root, name, x, y):
		root.cmd += [
			'/surface/point-surface {} {} {}'.\
			format(name, x, y)
		]

	'''
	MESH SECTION
	'''
	@staticmethod
	def translate(root, translate_x, translate_y):
		root.cmd += [
			'/mesh/translate {} {} '.\
			format(translate_x, translate_y)
		]

	@staticmethod
	def append_mesh(root, path):
		root.cmd += [
			'/mesh/modify-zones/append-mesh "{}" '.\
			format(path)
		]

	@staticmethod
	def merge_zones(root, list_zones):
		root.cmd += [
			'/mesh/modify-zones/merge-zones {} () '.\
			format(' '.join(list_zones))
		]

	@staticmethod
	def fuse_face_zones(root, list_zones, fused_name='()'):
		root.cmd += [
			'/mesh/modify-zones/fuse-face-zones {} () delete-me '.\
			format(' '.join(list_zones), fused_name)
		]

	@staticmethod
	def zone_name(root, old_name, new_name):
		root.cmd += [
			'/mesh/modify-zones/zone-name {} {} '.\
			format(old_name, new_name)
		]

	@staticmethod
	def check(root):
		root.cmd += [
			'/mesh/check '.\
			format()
		]
		
	@staticmethod
	def repair(root):
		root.cmd += [
			'/mesh/repair-improve/repair '.\
			format()
		]	

	'''
	SOLVE SECTION
	'''
	@staticmethod
	def convergence_criteria(root, criteria):
		root.cmd += [
			'/solve/monitors/residual convergence-criteria {0} {0} {0} {0} {0} {0}'.\
			format(criteria)
		]

	@staticmethod
	def cd_velocity_inlet(root, name):
		root.cmd += [
			'/solve/initialize/compute-defaults/velocity-inlet {} '.\
			format(name)
		]

	@staticmethod
	def initialize_flow(root):
		root.cmd += [
			'/solve/initialize initialize-flow yes '
		]

	@staticmethod
	def iterate(root, iterations):
		root.cmd += [
			'/solve/iterate {} '.\
			format(int(iterations))
		]

	'''
	REPORT SECTION
	'''
	@staticmethod
	def mass_flow(root, path, all_zones=True, list_zones=[]):
		if all_zones:
			root.cmd += [
				'/report/fluxes/mass-flow yes yes "{}" yes '.\
				format(path)
			]
		else:
			root.cmd += [
				'/report/fluxes/mass-flow no {} () yes "{}" yes '.\
				format(' '.join(list_zones), path)
			]

	def heat_transfer(root, path, all_zones=True, list_zones=[]):
		if all_zones:
			root.cmd += [
				'/report/fluxes/heat-transfer yes yes "{}" yes '.\
				format(path)
			]
		else:
			root.cmd += [
				'/report/fluxes/heat-transfer no {} () yes "{}" yes '.\
				format(' '.join(list_zones), path)
			]

	def facet_avg(root, path, value, list_zones):
		root.cmd += [
			'/report/surface-integrals/facet-avg {} () {} yes "{}" y '.\
			format(' '.join(list_zones), value, path)
		]

	@staticmethod
	def name(root, par):
		root.cmd += [
			''.\
			format(par)
		]