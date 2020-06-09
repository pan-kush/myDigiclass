class test:
	def __init__(self,cls_id="",test_id="",quest="",opts="",ans=""):
		self.cls_id=cls_id
		self.test_id=test_id
		self.quest="<sep>".join(quest)
		opt=[]
		for i in opts:
			opt.append("<opt>".join(i))
		self.opts="<quest>".join(opt)
		self.ans="<sep>".join(ans)

	@staticmethod
	def getMarks(self,c,test_id,ans):
		c.execute('select ans from test where test_id=?',(test_id,))
		# ans=self.ans.split("<sep>")
		corr_ans=c.fetchone()[0].split('<sep>')
		corr=0
		total=len(ans)
		for i in range(total):
			if ans[i]==corr_ans[i]:
				corr+=1
		return corr

	def add(self,c):
		c.execute("insert into test values (?,?,?,?,?)",(self.cls_id,self.test_id,self.quest,self.opts,self.ans))

	@staticmethod
	def addUserMarks(c,m,user_id,test_id):
		c.execute("insert into urtest values (?,?,?)",user_id,test_id,str(m))

	@staticmethod
	def getAllResults(c,test_id):
		c.execute("select cls_id from test where test_id=?",(test_id,))
		cls_id=c.fetchone()[0]
		c.execute("select user_id from urc where cls_id=?",(cls_id,))
		ids=c.fetchall()
		print(ids)
		ls=[]
		for i in ids:
			c.execute("select * from user where user_id=?",i)
			u=c.fetchone()
			if u[4] == 'teacher':
				continue
			c.execute("select marks from urtest where user_id=? and test_id=?",(u[0],test_id))
			m=c.fetchone()
			s = "NA" if not m else m[0]
			ls.append({'user_id':u[0],'cls_id':cls_id,'marks':s,'name':u[2],'roll':u[5]})

		print(ls)
		return ls

	@staticmethod
	def addtoclrtest(c,cls_id="",test_id="",test_name="",test_desc="",test_time=""):
		c.execute("insert into clrtest values (?,?,?,?,?)",(cls_id,test_id,test_name,test_desc,test_time))
