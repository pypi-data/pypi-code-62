from tqdm import tqdm

lbar = None

def print_progress_state(_cur,_tot,_nam):
	if type(_nam) is not str:
		_nam = _nam.decode('utf-8')

	global lbar

#	if lbar is not None and lbar.desc.split(';')[0] != _nam.split(';')[0]:
#		lbar.close()
#		lbar = None

	if lbar is None:
		lbar = tqdm(total=_tot, desc=_nam, position=0, leave=True)

#	if A is not None and B is not None and len(A) >= 4 and len(B) >= 4:
#		if A[3] != B[3]:
#			print("\n")

	lbar.update(_cur - lbar.n)
	lbar.set_description(_nam)

	if _cur == _tot:
		lbar.close()
		lbar = None

def opt_progress_state(state_p):
	state = state_p.contents
	global lbar

	if lbar is None:
		lbar = tqdm(total=state.max_iterations)

	lbar.set_description( "{:.4f};{:.4f}".format(state.best_norm,state.best_obj) )
	lbar.update(1)

	if state.iteration == state.max_iterations:
		lbar.close()
		lbar = None
