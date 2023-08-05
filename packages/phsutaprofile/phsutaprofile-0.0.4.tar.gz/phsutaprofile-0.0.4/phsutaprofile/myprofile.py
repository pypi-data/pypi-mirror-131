class Profile:
	'''
	Example:

	my = Profile('Tony')
	my.company = 'Phsuta'
	my.hobby = ['Developer','Reading','Programming']
	print(my.name)
	my.show_email()
	my.show_myart()
	my.show_hobby()
	my.show_mice()
	my.show_dolls()
	
	'''
	def __init__(self,name):
		self.name = name
		self.company = ''
		self.hobby = []
		self.art = '''
	 	_   ,_,   _
	   / `'=) (='` \\
	  /.-.-.\ /.-.-.\ 
	  `      "      `
			'''
		self.art2 = '''
           ____()()
          /      @@
	`~~~~~\_;m__m._>o
		    '''
		self.art3 = '''
       _    _    _    _    _ 
    __( )__( )__( )__( )__( )__
   '--. .--. .--. .--. .--. .--'
     / _ \/ _ \/ _ \/ _ \/ _ \\
     (/ \)(/ \)(/ \)(/ \)(/ \)
		
			'''
		
	def show_email(self):
		if self.company != '':
			print('{}@{}.com'.format(self.name.lower(),self.company))
		else:
			print('{}@gmail.com'.format(self.name.lower()))
	
	def show_myart(self):
		print(self.art)	

	def show_mice(self):
		print(self.art2)

	def show_dolls(self):
		print(self.art3)


	def show_hobby(self):
		if len(self.hobby) !=0:
			print('----my hobby----')
			for i,h in enumerate(self.hobby,start=1):
				print(i, h)
			print('----------------')
		else:
			print('No Hobby')

		
if __name__=='__main__':
	my = Profile('Tony')
	my.company = 'Phsuta'
	my.hobby = ['Developer','Programming','Reading','Diving']
	print(my.name)
	my.show_email()
	my.show_myart()
	my.show_hobby()
	my.show_mice()
	my.show_dolls()
	# help(my)
	