class chat:

	def __init__(self,cls_id="",user_id="",chat_id="",dtime="",text="",file=""):
		self.cls_id=cls_id
		self.user_id=user_id
		self.chat_id=chat_id
		self.dtime=dtime
		self.text=text
		self.file=file

	def add(self,c):

		c.execute("insert into chat values (?,?,?,?,?,?)",(self.cls_id,self.user_id,self.chat_id,self.dtime,self.text,self.file))
		c.execute("insert into clrch values (?,?)",(self.cls_id,self.chat_id))

	@staticmethod
	def getChats(c,cls_id):

		c.execute('select chat_id from clrch where cls_id=?',(cls_id,))
		ids = c.fetchall()
		l = []
		for i in ids :
			c.execute('select * from chat where chat_id=?',i)
			d=c.fetchone()
			c.execute('select occ,name from user where user_id=?',(d[1],))
			k = c.fetchone()
			img = True if d[5].split('.')[-1] in ['jpg','png','jpeg'] else False 
			l.append({
				'cls_id':d[0],'user_id':d[1],'chat_id':d[2],
				'time':d[3],'text':d[4],'file':d[5],'occ':k[0],'img':img,'name':k[1]
				})
		return l

	@staticmethod
	def isAllowed(c,user_id,cls_id):

		c.execute("select privilage from urc where user_id=? and cls_id=?",(user_id,cls_id))
		if c.fetchone()[0]:
			return True
		return False
	
	@staticmethod
	def delChat(c,chat_id):
		c.execute('delete from chat where chat_id=?',(chat_id,))
		c.execute('delete from clrch where chat_id=?',(chat_id,))
