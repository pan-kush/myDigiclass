class announcements:

	def __init__(self,cls_id="",ann_id="",content="",file=""):
		
		self.cls_id=cls_id
		self.ann_id=ann_id
		self.content=content
		self.file=file

	def add(self,c):

		c.execute('''insert into announcements values (?,?,?,?)''',(self.cls_id,self.ann_id,self.content,self.file))

	@staticmethod
	def delete(c,ann_id):

		c.execute('''delete from announcements where ann_id=?''',(ann_id,))

	@staticmethod
	def getAnnouncements(c,cls_id):

		c.execute("select * from announcements where cls_id=?",(cls_id,))
		k=c.fetchall()
		ls=[]
		for i in k:

			ls.append({'cls_id':i[0],'ann_id':i[1],'data':i[2],'file':i[3]})

		return ls