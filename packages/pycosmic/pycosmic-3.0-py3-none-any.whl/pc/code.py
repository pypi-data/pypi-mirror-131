import inspect 



def get_params(val):
	return inspect.signature(val)


def codeof(name):
	return inspect.getsource(name)


def get_doc(name):
	return inspect.getdoc(name)











	

