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
	def delChat(c,chat_id):
		c.execute('delete from chat where chat_id=?',(chat_id,))
		c.execute('delete from clrch where chat_id=?',(chat_id,))
