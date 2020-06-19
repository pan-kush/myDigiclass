from datetime import datetime,timedelta
import os,platform
import pandas as pd

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
	def getMarks(c,test_id,ans):
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
		c.execute("insert into urtest values (?,?,?)",(user_id,test_id,str(m)))

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
		ls=sorted(ls,key=lambda x: x['roll'])

		opsystem=platform.system()

		d={'Name':[],'Roll':[],'Marks':[]}
		for i in d:
			for j in ls:
				d[i].append(str(j[i.lower()]))

		ts=str(test_id).split(":")
		tst="".join(ts)
		print(tst)
		
		df=pd.DataFrame(d)
		if opsystem=='Windows':
			df.to_excel('.\\uploads\\{}.xlsx'.format(tst),index=False)
		else:
			df.to_excel('./uploads/{}.xlsx'.format(tst),index=False)

		print(ls)
		return ls

	@staticmethod
	def addtoclrtest(c,cls_id="",test_id="",test_name="",test_desc="",test_time="",test_dur=""):
		c.execute("insert into clrtest values (?,?,?,?,?,?)",(cls_id,test_id,test_name,test_desc,test_time,test_dur))

	@staticmethod
	def getTests(c,cls_id,user_id):

		l=[]
		c.execute("select * from clrtest where cls_id=?",(cls_id,))
		tests=c.fetchall()
		for i in tests:
	
			c.execute("select marks from urtest where user_id=? and test_id=?",(user_id,i[1]))
			m=c.fetchone()
			d_obj=datetime.strptime(i[4],'%Y-%m-%dT%H:%M')
			d_obj1=d_obj+timedelta(minutes=int(i[5]))
			time_diff=str(datetime.now()-d_obj1)
			started=True if d_obj<=datetime.now() else False
			print(i[2],time_diff)
			ended=True if time_diff[0]!='-' else False
			print(ended)
			marks=m[0] if m else "NA"

			t=i[4].split("T")[0]

			t=t.split("-")
			t=reversed(t)
			t="-".join(t)
			test_time=t+"_"+i[4].split("T")[1]
			print(test_time)
			l.append({'marks':marks,'test_id':i[1],'test_name':i[2],'test_desc':i[3],'test_time':test_time,'test_dur':i[5],'ended':ended,'started':started})
		return l

	@staticmethod
	def getQuests(c,test_id):

		l=[]
		c.execute("select * from test where test_id=?",(test_id,))
		k=c.fetchone()
		ques=k[2].split("<sep>")
		opts=k[3].split("<quest>")

		for i in range(0,len(ques)):
			d={}
			d['ques']=ques[i]
			d['opts']=opts[i].split("<opt>")
			d['no']=i
			l.append(d)
		print(l)
		return l,len(ques)


	@staticmethod
	def getDetails(c,test_id):

		c.execute("select * from clrtest where test_id=?",(test_id,))
		dl=c.fetchone()
		t=dl[4].split("T")[0]
		t=t.split("-")
		t=reversed(t)
		t="-".join(t)
		test_time=t+"_"+dl[4].split("T")[1]
		return {'cls_id':dl[0],'test_id':dl[1],'test_name':dl[2],'test_desc':dl[3],'test_time':test_time,'test_dur':dl[5],'test_t':dl[4]}

	@staticmethod
	def test_validation(c,user_id,test_id):

		c.execute("select * from urtest where user_id=? and test_id=?",(user_id,test_id))
		return True if c.fetchone() else False

	@staticmethod
	def remove(c,test_id):

		c.execute("delete from test where test_id=?",(test_id,))
		c.execute("delete from clrtest where test_id=?",(test_id,))
		c.execute("delete from urtest where test_id=?",(test_id,))

