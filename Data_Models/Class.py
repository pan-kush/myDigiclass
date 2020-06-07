class Class:

	def __init__(self,cls_id="",desc="",creator="",logged=False,c_id=""):  #logged=locked
		self.cls_id=cls_id
		self.desc=desc
		self.creator=creator
		self.logged=logged
		self.c_id=c_id

	def add(self,c,user_id):

		c.execute('''insert into class values (?,?,?,?,?)''',(self.cls_id,self.desc,self.creator,self.logged,self.c_id))
		c.execute('''insert into urc values (?,?,?)''',(user_id,self.cls_id,True))


	@staticmethod
	def delete(c,cls_id,user_id):

		# 	remove from class
		c.execute("delete from class where cls_id=?",(cls_id,))
		# 	remove from urc
		c.execute("delete from urc where cls_id=?",(cls_id,))

		c.execute("select ass_id from cra where cls_id=?",(cls_id,))
		ls=c.fetchall()
		for i in ls:
		# 	remove all asiignments from ura
			c.execute("delete from ura where ass_id=?",i)
			# delete files from upload

		# 	remove all assignments from cra
		c.execute("delete from cra where cls_id=?",(cls_id,))
		
		# 	remove from chat
		c.execute("delete from chat where cls_id=?",(cls_id,))
		#	remove chatid files from upload

	 	#   remove from clrch
		c.execute("delete from clrch where cls_id=?",(cls_id,))

		#   remove from assignment
		c.execute("delete from assignment where cls_id=?",(cls_id,))

	@staticmethod
	def remove(c,cls_id,user_id):

		c.execute("delete from urc where cls_id=? and user_id=?",(cls_id,user_id))


	@staticmethod
	def allclasses(c,user_id=None,cls_id=None):
		ids=[]
		if user_id :
			c.execute("select cls_id from urc where user_id=?",(user_id,))
			ids=c.fetchall()
		else:
			ids=[(cls_id,)]
		# print(ids)
		ls=[]
		for i in ids:
			c.execute("select * from class where cls_id=?",i)
			k=c.fetchone()
			c.execute("select user_id from urc where cls_id=?",i)
			sz=len(c.fetchall())-1
			ls.append({'cls_id':k[0].split("_")[1],'desc':k[1],'creator':k[2],'participants':sz})
			# change class id
		if cls_id:
			ls=ls[0]
		if type(ls)==type([]):
			print(ls)
			return reversed(ls)	
		return ls	


	@staticmethod
	def add_userclass(c,user_id,cl_id):

		c.execute('''select cls_id from class where cls_id=?''',(cl_id,))
		if c.fetchall()!=[]:
			c.execute('''insert into urc values (?,?,?)''',(user_id,cl_id,True))
			return True 

	@staticmethod
	def check_classavail(c,cls_id):

		c.execute('''select cls_id from class where cls_id=?''',(cls_id,))
		if c.fetchall()==[]:
			return 'Available'
		return 'In_use'

	@staticmethod
	def class_list(c,clg_id):

		c.execute("select cls_id from class where cls_id like '{}%'".format(clg_id))
		ids=c.fetchall()
		return [i[0].split('_')[1] for i in ids]

	@staticmethod
	def getteacher_desc(c,cls_id):

		c.execute("select creator,desc from class where cls_id=?",(cls_id,))
		return c.fetchone()

	@staticmethod
	def alreadyJoined(c,user_id,cls_id):

		c.execute("select * from urc where cls_id=? and user_id=?",(cls_id,user_id))
		if c.fetchone():
			return True
		return False

	@staticmethod
	def getAllStuds(c,cls_id):

		c.execute("select user_id from urc where cls_id=?",(cls_id,))
		ids=c.fetchall()
		# print (ids)
		ls=[]
		total=0
		blocked=0
		for i in ids:
			c.execute("select * from user where user_id=? and occ='student'",i)
			d=c.fetchone()
			# print(d)
			if d:
				c.execute("select privilage from urc where cls_id=? and user_id=?",(cls_id,d[0]))
				priv=c.fetchone()
				print(priv)
				# as of frontenf blocked means checked and here 1 means allowed
				priv=False if priv[0]==1 else True
				total+=1
				if priv :blocked+=1
				ls.append({'user_id':d[0],'name':d[2],'roll':'('+d[5][-4:]+")",'allowed':priv})
		return ls,str(blocked)+'/'+str(total)

	@staticmethod
	def changePrivilage(c,user_id,cls_id,check):
		check = 0 if check else 1
		print(user_id,cls_id,check)
		c.execute("update urc set privilage=? where user_id=? and cls_id=?",(check,user_id,cls_id))

	@staticmethod
	def getTeacherClasses(c,c_id):
		c.execute("select cls_id,desc from class where c_id=?",(c_id,))
		cs=c.fetchall()
		ls=[]
		for cl in cs :
			ls.append({'cls_id':cl[0].split("_")[1],'desc':cl[1]})

		return ls