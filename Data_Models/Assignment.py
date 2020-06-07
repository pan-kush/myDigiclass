from datetime import datetime
import pandas as pd
class assignment:
	def __init__(self,ass_id="",cls_id="",ass_name="",deadline="",desc="",files=""):
		self.ass_id=ass_id
		self.cls_id=cls_id
		self.ass_name=ass_name
		self.deadline=deadline
		self.desc=desc
		self.files=files

	def add(self,c):


		c.execute("insert into assignment values (?,?,?,?,?,?)",(self.ass_id,self.cls_id,self.ass_name,self.deadline,self.desc,self.files))
		c.execute('''insert into cra values (?,?)''',(self.cls_id,self.ass_id))

	@staticmethod
	def remove(c,ass_id):

		# remove from assignment table
		c.execute("delete from assignment where ass_id=?",(ass_id,))
		# remove from cra
		c.execute("delete from cra where ass_id=?",(ass_id,))
		# remove from ura
		c.execute("delete from ura where ass_id=?",(ass_id,))
		# remove files from upload


		# print("remove not defined yet")

	@staticmethod
	def add_userass(c,user_id,ass_id,sub_time,content):
		c.execute('''insert into ura values (?,?,?,?)''',(user_id,ass_id,sub_time,content))

	@staticmethod
	def allass(c,user_id,cls_id):

		c.execute("select * from assignment where cls_id=?",(cls_id,))
		ids=c.fetchall()
		print(ids)
		ls=[]
		for i in ids:
			c.execute("select * from ura where user_id=? and ass_id=?",(user_id,i[0]))
			s= True if len(c.fetchall())>=1 else False
			d_obj=datetime.strptime(i[3],'%Y-%m-%d')
			time_diff=str(datetime.now().date()-d_obj.date())
			ended=True if time_diff[0]!='-' else False

			ls.append({'ass_id':i[0],'cls_id':i[1],'ass_name':i[2],'deadline':i[3],'desc':i[4],'submitted':s,'ended':ended})
		print(ls)
		return ls

	@staticmethod
	def getAssDetail(c,ass_id):
		print(ass_id)
		c.execute("select * from assignment where ass_id=?",(ass_id,))
		
		d=c.fetchone()
		return {'ass_id':d[0],'cls_id':d[1],'ass_name':d[2],'deadline':d[3],'desc':d[4]}

	@staticmethod
	def getSubmissions(c,ass_id,dload=True):

		cls_id='_'.join(ass_id.split("_")[:2])
		print(cls_id)
		c.execute("select user_id from urc where cls_id=?",(cls_id,))
		uids=c.fetchall()
		ls=[]
		for i in uids:
			c.execute("select user_id,name,roll from user where user_id=? and occ='student'",i)
			stud=c.fetchone()
			if stud:
				c.execute("select sub_time,content from ura where user_id=? and ass_id=?",(stud[0],ass_id))
				sub_detail=c.fetchone()
				if sub_detail:
					ls.append({'user_id':stud[0],'name':stud[1],'roll':stud[2],'time':sub_detail[0],'file':sub_detail[1],'status':'Done'})
				else:
					ls.append({'user_id':stud[0],'name':stud[1],'roll':stud[2],'time':'NA','file':'NA','status':'NA'})
		
		ls=sorted(ls,key=lambda x: x['roll'])

		if dload:
			d={'Name':[],'Roll':[],'Time':[],'Status':[]}
			for i in d:
				for j in ls:
					d[i].append(str(j[i.lower()]))
		
			df=pd.DataFrame(d)
			df.to_excel('.\\uploads\\{}.xlsx'.format(ass_id),index=False)

		print(ls)
		return ls

	@staticmethod
	def removeUserAss(c,ass_id,user_id):
		#we have to delete file from upload folder
		c.execute("delete from ura where ass_id=? and user_id=?",(ass_id,user_id))
		#remove files from upload
