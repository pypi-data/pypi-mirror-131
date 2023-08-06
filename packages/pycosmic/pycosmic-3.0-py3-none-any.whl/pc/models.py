from pc.utils import SetCode



def get_model(name):
	try:
		SetCode(filename=name,repo="models")
	except:
		print("Model Not Found")



if __name__ == '__main__':
	get_model('iris.pkl')
	


		
		
