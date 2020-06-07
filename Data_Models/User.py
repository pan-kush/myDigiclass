class user:
	
	def __init__(self,user_id="",clg_id="",name="",password="",occ="",roll=""):
		self.user_id=user_id
		self.clg_id=clg_id
		self.name=name
		self.password=password
		self.occ=occ
		self.roll=roll

	def add(self,c):
		
		c.execute("insert into user values (?,?,?,?,?,?)",(self.user_id,self.clg_id,self.name,self.password,self.occ.lower(),self.roll))
	
	@staticmethod
	def user_validation(c,user_id,password):
		c.execute("select * from user where user_id=? and password=?",(user_id,password))
		f=c.fetchone()
		if f==None:
			return False
		u={'user_id':f[0],'clg_id':f[1],'name':f[2],'occ':f[4].lower(),'roll':f[5]}
		return u

	@staticmethod
	def check_avl(c,user_id):
		c.execute("select * from user where user_id=(?)",(user_id,))
		if c.fetchall()==[]:
			return True
		return False

	@staticmethod
	def get_occ(c,user_id):
		c.execute("select occ from user where user_id=?",(user_id,))
		k=c.fetchone()
		return k[0].lower()
	
	@staticmethod
	def getname_roll(c,user_id):
		c.execute("select name,roll from user where user_id=?",(user_id,))
		k=c.fetchone()
		return k

	@staticmethod
	def getTeachers(c,clg_id):
		c.execute("select user_id,name from user where clg_id=? and occ='teacher'",(clg_id,))
		ts = c.fetchall()
		ls=[]
		for t in ts:
			ls.append({'user_id':t[0],'name':t[1]})
		return ls


