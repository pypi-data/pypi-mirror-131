# myprofile.py

class Profile:
	'''
	Example:

	my = Profile('Loong')
	my.company = 'uncle-engineer'
	my.hobby = ['Youtuber','Reading','Sleeping']
	print(my.name)
	my.show_email()
	my.show_myart()
	my.show_hobby()

	'''
	def __init__(self,name):
		self.name = name
		self.company = ''
		self.hobby = []
		self.art = '''
			  |\\      _,,,---,,_
		ZZZzz /,`.-'`'    -.  ;-;;,_
		     |,4-  ) )-,_. ,\\ (  `'-'
		    '---''(_/--'  `-'\\_)  miao miao 
		'''
		self.art2 = '''
		 _._     _,-'""`-._
		(,-.`._,'(       |\\`-/|
		    `-.-' \\ )-`( , o o)
		          `-    \\`_`"'-
		'''

	def show_email(self):
		if self.company != '':
			print('{}@{}gmail.com'.format(self.name.lower(),self.company))
		else:	
			print('{}@gmail.com'.format(self.name.lower()))

	def	show_myart(self):
		print(self.art)

	def	show_cat(self):
		print(self.art2)	

	def show_hobby(self):
		if len(self.hobby) !=0:
			print('--------my hobby--------')
			for i,h in enumerate(self.hobby,start=1):
				print(i,h)
			print('--------------------')
		else:
			print('No hobby')


if __name__ == '__main__':
	my = Profile('Loong')
	my.company = 'uncle-engineer'
	my.hobby = ['Youtuber','Reading','Sleeping']
	print(my.name)
	my.show_email()
	my.show_myart()
	my.show_hobby()
	my.show_cat()
	#help(my)
	