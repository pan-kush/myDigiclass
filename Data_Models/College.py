class college:
	
	def __init__(self,name="",clg_id="",password=""):

		self.clg_id=clg_id
		self.name=name
		self.password=password
		

	def add_to_db(self,c):

		c.execute("insert into college values (?,?,?)",(self.clg_id,self.name,self.password))

	@staticmethod
	def collegelist(c):
		c.execute("select name,clg_id from college")
		l=c.fetchall()
		colg_list=[]
		for i in l:
			colg_list.append(i[0]+" "+"("+i[1]+")")
		return colg_list



	@staticmethod
	def getCollegeName(c,clg_id):

		c.execute("select name from college where clg_id=?",(clg_id,))
		l=c.fetchone()
		return l[0]