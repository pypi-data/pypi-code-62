import os

def initPath(*data):
	path = ""
	if isinstance(data, str):
		return os.path.join(path, data)
	for pathData in data:
		path = os.path.join(path, pathData)
	return path


def mkdir(*data):
	dataPath = initPath(*data)
	if not os.path.isdir(dataPath):
		try:
			os.mkdir(dataPath)
		except:
			mkdir(os.path.dirname(dataPath))
			os.mkdir(dataPath)
		return True
	return False