from flask import Flask,render_template,jsonify,abort,request,Response,redirect,url_for
import sqlite3
import base64
import re
import string
import hashlib
import datetime
import json
import datetime
import random
import requests
import os
app=Flask(__name__)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base,User
from place import Place
from datetime import datetime

engine=create_engine('sqlite:///users102.db?check_same_thread=False')
Base.metadata.bind=engine
DBSession=sessionmaker(bind=engine)
session=DBSession()

us=[]
conn=sqlite3.connect('users102.db',check_same_thread=False)
c=conn.cursor()
Result=list()
Result2=[]


def validationP(pwd):
	return all(i in string.hexdigits for i in pwd) and (len(pwd)==40)


def gettime(timestamp):
	now=datetime.now()
	now=datetime.strptime(str(datetime.now()),'%Y-%m-%d %H:%M:%S.%f').strftime('%d-%m-%Y:%S-%M-%H')
	ts=timestamp
	tf='%d-%m-%Y:%S-%M-%H'
	d1=datetime.strptime(ts,tf)
	d2=datetime.strptime(str(now),tf)
	diff=d1-d2
	diff=str(diff)
	dif=diff.split(",")
	d=dif[0].split(" ")
	tt=int(d[0])
	if(tt>0):
		return 1
	else:
		return 0



'''8 write to db'''
@app.route('/api/v1/db/write',methods=['POST'])
def writetodb():
	method=str(request.json["method"])
	data=request.json["insert"]
	col=request.json["column"]
	tbl=request.json["table"]

	try:
		if method == "insert":
			dictionary={}
			for i in range(len(col)):
				dictionary[col[i]]=data[i]			
			attrib_names = ", ".join(dictionary.keys())
			attrib_values = ", ".join("?" * len(dictionary.keys()))
			sql = "INSERT INTO "+tbl+"("+attrib_names+") VALUES ("+attrib_values+")"
			c.execute(sql, list(dictionary.values()))
			conn.commit()	
			return Response(status=200)
			
		elif method =="createride":
				src=int(data[2])
				dest=int(data[3])
				rideid=int(data[4])
				sql="UPDATE user SET created_by =?,timestamp=?,source=?,destination=?,rideId=? WHERE username=?"
				task=(data[0],data[1],src,dest,rideid,data[0])
				c.execute(sql,task)
				conn.commit()
				return Response(status=200)
				

			
		elif method == "delete":
				c.execute("DELETE FROM "+tbl+" WHERE "+col+"='"+data+"'")
				conn.commit()
				return Response(status=200)
					
		elif method=="delcride":
				
				sql="DELETE FROM cride WHERE rideId=?"
				t=(data,)
				c.execute(sql,t)
				conn.commit()
				return Response(status=200)

		elif method=="delride":
				
				sql="DELETE FROM ride WHERE rideid=?"
				t=(data,)
				c.execute(sql,t)
				conn.commit()
				return Response(status=200)
                elif method=="clearuser":
                    sql="DELETE FROM user"
                    c.execute(sql)
                    conn.commit()
                    return Response(status=200)
								
	except:
		return Response(status=400)



'''9 read from db -complete'''
@app.route('/api/v1/db/read',methods=['POST'])
def read():
	ride=0
	if request.method!='POST':
		return Response(status=405)

	method=str(request.json["method"])
	tbl=request.json["table"]
	
	col=request.json["columns"]
	
	try:	
		if method=="select":
			where=str(request.json["where"])
			x=where.split('=')
			x[0]=x[0].strip("'")		
			dictionary={}
			for i in range(len(col)):
				dictionary[col[i]]=0
			
			attr_names=",".join(dictionary.keys())
			
			sql= "SELECT "+attr_names+" FROM "+tbl+" WHERE "+x[0]+" ="+x[1]
			c.execute(sql)

			if c.fetchone() is None:
				return Response(status=404)

			else:
				return Response(status=200)

		if method=="selectdel":
			where=request.json["where"]
			x=where.split('=')
			x[0]=x[0].strip("'")	
			dictionary={}
			sql="SELECT rideId from cride WHERE rideId="+x[1]
			c.execute(sql)
			if c.fetchone() is None:
				return Response(status=404)

			else:

				return Response(status=200)
			
		
		elif method=="joincrides":
			
			where=str(request.json["where"])
			y=where.split(",")
			
			x=[]
			z=[]
			y[0]=y[0].replace("'","")
			
			x.append(y[0])
			x.append(y[1])
			x1=x[0].split('=')
			
			x1[0]=x1[0].strip("'")
			x1[1]=x1[1].strip('"')
			x2=x[1].split('=')
			
			x2[0]=x2[0].strip("'")
			x2[1]=x2[1].strip('"')
			
			z.append(x1)
			z.append(x2)
			
			sql="SELECT created_by FROM cride WHERE rideId=?"
			t=(z[0][1],)
			c.execute(sql,t)
			r=c.fetchall()[0]
			z[1][1]=z[1][1].strip("'")
			
			if (r[0]!=z[1][1]):
				
				return Response(status=404)


			else:
				return Response(status=200)
		

		elif method=="joinrides":
			
			where=str(request.json["where"])
			
			y=where.split(",")
			
			x=[]
			z=[]
			y[0]=y[0].replace("'","")
			
			x.append(y[0])
			x.append(y[1])
			x1=x[0].split('=')
			
			x1[0]=x1[0].strip("'")
			x1[1]=x1[1].strip('"')
			x2=x[1].split('=')
			
			x2[0]=x2[0].strip("'")
			x2[1]=x2[1].strip('"')
			
			z.append(x1)
			z.append(x2)
			sql="SELECT * FROM ride WHERE rideid=?"
			t=(z[0][1],)
			c.execute(sql,t)
			r=c.fetchall()
			
			z[1][1]=z[1][1].strip("'")
			
			
			for i in range(len(r)):
				
				if str(r[i][1])!=str(z[1][1]):
					'''("User has already joined the ride")
					break
				
					return Response(status=404)'''
					pass
				else:
					#res.clear()
					return Response(status=404)
			return Response(status=200)
		
																																																																																																																																																																																																																																																
		elif method=="listride":
			where=request.json["where"]
			x=where.split('=')

			x[1]=x[1].strip("'")
			#("x=",x[1])
			dictionary={}
			res=[]
			
			sql7="SELECT * FROM cride WHERE rideId="+x[1]
			z=c.execute(sql7)
			for i in c.fetchall():
				Result.append(i)

			return Response(status=200)

		elif method=="selectuj":
			
			where=str(request.json["where"])
			x=where.split('=')
			x[0]=x[0].strip("'")		
			x[1]=x[1].strip("'")
			dictionary={}
			for i in range(len(col)):
				dictionary[col[i]]=0
			
			attr_names=",".join(dictionary.keys())

			sql="SELECT ujname from ride where rideid="+x[1]
			c.execute(sql)
			for i in c.fetchall():
				Result2.append(i[0])
			return Response(status=200)


		elif method=="selectmultiple":
			src=str(request.json["where"])
			
			dest=str(request.json["where2"])
			
			x=src.split('=')
			x[1]=x[1].strip("'")
			y=dest.split('=')
			y[1]=y[1].strip("'")		
			dictionary={}
			for i in range(len(col)):
				dictionary[col[i]]=0

			attr_names=",".join(dictionary.keys())
			sql="SELECT * FROM cride WHERE source=? AND destination=?"
			t=(x[1],y[1])

			c.execute(sql,t)
			res=c.fetchall()
			if len(res)==0:
				#(x[0],y[0],"columns with values",x[1],y[1],"don't exist")
				return Response(status=404)

			else:
				Result.append(res)
				return Response(status=200)	
		elif method=="selectcount":
			sql="SELECT COUNT(*) FROM cride"
			c.execute(sql)
			if c.fetchall() is None:
				return Response(status=204)
			else:
				return Response(status=200)
		
		elif method=="selectuser":
			#print("IN select user")
			sql="SELECT * FROM user"
			c.execute(sql)
			#print("After sql")
			x=c.fetchall()
			#print("x=",x)
			#print(c.fetchall()[0])
			if len(x)==0:
				return Response(status=204)
			else:
								
				for i in range(len(x)):
					#print(x[i][0])
					us.append(x[i][0])
				#print("us=",us)
				return Response(status=200)
	except:
		return Response(status=400)





'''
#just for reference

@app.route('/api/v1/db/read2',methods=['GET'])
def view():
	#conn=sqlite3.connect('user2.db',check_same_thread=False)
	#c=conn.cursor()
	c.execute("SELECT * FROM cride")
	rows=c.fetchall()
	#for i in rows:
	return jsonify(users=[b for b in rows])
'''


'''#1.add user'''
@app.route('/api/v1/users',methods=['PUT'])
def add_user():

	if request.method!='PUT':
		return json.dumps({}),405

	try:
		userm=request.json["username"]
		password=request.json["password"]
		
		if(validationP(password)==True):
			
			
			task1={"method":"select","table":"user","columns":["*"],"where":"username='"+userm+"'"}
			
			res1=requests.post('http://0.0.0.0:6000/api/v1/db/read',json=task1)
		
			if res1.status_code==404:

				task2={"method":"insert","insert":(userm,password),"column":("username","password"),"table":"user"}
				res=requests.post('http://0.0.0.0:6000/api/v1/db/write',json=task2)
				
				if res.status_code==404:
				
					return json.dumps({}),400
				else:
					return json.dumps({}),201
			else:
				#("username exists")
				return json.dumps({}),400
		
		else:
			#("password validation failed")
			return json.dumps({}),400


	except:
		return json.dumps({}),400


'''Delete user'''
@app.route('/api/v1/users/<string:username>',methods=['DELETE'])
def del_user(username):
	if request.method!="DELETE":
		#("Wrong method!")
		return json.dumps({}),405

	try:
		
		task1={"method":"select","table":"user","columns":["username"],"where":"username='"+username+"'"}
		res1=requests.post('http://0.0.0.0:6000/api/v1/db/read',json=task1)

		if res1.status_code==404:
			#("Username doesnt exist")
			return Response(status=400)
		else:
			
			task2={"method":"delete" ,"insert":(username),"column":("username"),"table":"user"}
			
			res3=requests.post('http://0.0.0.0:6000/api/v1/db/write',json=task2)
			task3={"method":"delete","insert":(username),"column":("created_by"),"table":"cride"}
                        res4=requests.post('http://34.238.29.50:8000/api/v1/db/write',json=task3)

			task4={"method":"delete","insert":(username),"column":("ujname"),"table":"ride"}
			res5=requests.post('http://34.238.29.50:8000/api/v1/db/write',json=task4)

			if res3.status_code==200:
		
				return json.dumps({}),200
			else:
				return json.dumps({}),400

	except:

		#("Username doesnt exist")
		return json.dumps({}),400

	
	

'''List all users'''
@app.route('/api/v1/users',methods=['GET'])
def list_user():

	if request.method!='GET':
		return json.dumps({}),405

	task1={"method":"selectuser","table":"user","columns":["username"],"where":""}
	res1=requests.post('http://0.0.0.0:6000/api/v1/db/read',json=task1)
	#print(res1.status_code)	
	if res1.status_code==204:
		return json.dumps({}),204
	else:
		res=jsonify(us)
                del us[:]
				
		return res,200

'''Clear db'''
@app.route('/api/v1/db/clear',methods=['POST'])
def clear_db():
	if request.method!='POST':
		return json.dumps({}),405
	#t1="SELECT * FROM user"
	#c.execute(t1)
	
	#if c.fetchone() is None:
	#	return json.dumps({}),400

        res=requests.post('http://34.238.29.50:8000/api/v1/db/clear')
        if res.status_code==200:
            task2={"method":"clearuser" ,"insert":("username"),"column":("username"),"table":"user"}

            res=requests.post('http://34.238.29.50:8080/api/v1/db/write',json=task2)

            if res.status_code==200:
                print("Succesfully executed")
                return json.dumps({}),200
            else:
                return json.dumps({}),400
            #t="DELETE FROM user"        
            #c.execute(t)
            #conn.commit()
            #return json.dumps({}),200
        else:
            #task2={"method":"clearuser" ,"insert":("username"),"column":("username"),"table":"user"}

            #res=requests.post('http://34.238.29.50:8080/api/v1/db/write',json=task2)

            #if res.status_code==200:
            #    return json.dumps({}),200
            #else:
            return json.dumps({}),400
            #t="DELETE FROM user"
            #c.execute(t)
            #conn.commit()
            #return json.dumps({}),200


if __name__=='__main__':
	app.run(host="0.0.0.0",port="6000",debug=True)
