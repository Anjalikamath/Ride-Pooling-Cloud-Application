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
from dbr import Base,Ride,CRide
from place import Place
from datetime import datetime

engine=create_engine('sqlite:///users103.db?check_same_thread=False')
Base.metadata.bind=engine
DBSession=sessionmaker(bind=engine)
session=DBSession()


conn=sqlite3.connect('users103.db',check_same_thread=False)
c=conn.cursor()
Result=list()
Result2=[]
global count
no_of_req=[0]
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
								
	        elif method=="clearide":
                    sql="DELETE FROM ride"
                    c.execute(sql)
                    conn.commit()
                    return Response(status=200)
                elif method=="clearcride":
                     sql="DELETE FROM cride"
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

   		elif method=='count':
                        #print("IN count")
			sql="SELECT COUNT (*) FROM cride"
			c.execute(sql)
                        print("EXECUTED")
                        #print(c.fetchall()[0][0])
            		global count
                        count=c.fetchall()[0][0]
                        print(count)
                        #return count
                        #jsonify
                        return Response(status=200)
		
	except:
		return Response(status=400)




'''6.Join existing ride'''
@app.route('/api/v1/rides/<int:rideId>',methods=['POST','PUT','HEAD','OPTIONS'])
def join_ride(rideId):
                #res2=requests.get('http://0.0.0.0:7000/api/v1/_count')
                no_of_req[0]+=1

	        if request.method!='POST':
		 
		    return json.dumps({}),405

	        #try:
		rideId=str(rideId)
		task1={"method":"select","table":"cride","columns":["*"],"where":"rideId='"+rideId+"'"}
		#print(rideId)
		res1=requests.post('http://0.0.0.0:7000/api/v1/db/read',json=task1)
		
		if res1.status_code==404:
			#("Ride doesnt exist")
			return json.dumps({}),404

		else:
			tryjoin=request.json["username"]
			
                        #print("ALDS:")
			task1={"method":"select","table":"user","columns":["*"],"where":"username='"+tryjoin+"'"}
                        res1=requests.post('http://asn3-291163488.us-east-1.elb.amazonaws.com:80/api/v1/db/read',json=task1)
			
			if res1.status_code==404:

				#("user doesnt exist!")
				return json.dumps({}),404
			else:

				task1={"method":"joincrides","table":"cride","columns":["created_by","rideId"],"where":"rideId="+rideId+",created_by='"+tryjoin+"'"}

				res2=requests.post('http://0.0.0.0:7000/api/v1/db/read',json=task1)

				if res2.status_code==404:

					task3={"method":"joinrides","table":"ride","columns":["ujname","rideid"],"where":"rideid="+rideId+",ujname='"+tryjoin+"'"}

					res4=requests.post('http://0.0.0.0:7000/api/v1/db/read',json=task3)
					
					if res4.status_code==200:
						task2={"method":"insert" ,"insert":(tryjoin,rideId),"column":("ujname","rideid"),"table":"ride"}
						res3=requests.post('http://0.0.0.0:7000/api/v1/db/write',json=task2)
						if res3.status_code==200:
							
							return json.dumps({}),201
						else:
							return json.dumps({}),400
					else:
						
						return json.dumps({}),400
					

				else:
					#("User who created ride cant join ride")
					return json.dumps({}),400

	    #except:
	    #	json.dumps({}),400


'''7 Delete a ride'''
@app.route('/api/v1/rides/<int:rideId>',methods=['DELETE','PUT','HEAD'])

def delride(rideId):
        #res2=requests.get('http://0.0.0.0:7000/api/v1/_count')
        no_of_req[0]+=1

	if request.method!="DELETE":
		return json.dumps({}),405
	
	rideid=str(rideId)
	t={"method":"selectcount","table":"cride","columns":["*"],"where":"rideId='"+rideid+"'"}
	r=requests.post('http://0.0.0.0:7000/api/v1/db/read',json=t)
	if r.status_code==204:
		#("Db is empty")
		return json.dumps({}),204


	task1={"method":"selectdel","table":"cride","columns":["*"],"where":"rideId='"+rideid+"'"}

	res1=requests.post('http://0.0.0.0:7000/api/v1/db/read',json=task1)
	if res1.status_code==200:
		task2={"method":"delcride","table":"cride","insert":(rideid),"column":["rideId"]}
		res2=requests.post('http://0.0.0.0:7000/api/v1/db/write',json=task2)
		task3={"method":"delride","table":"ride","insert":(rideid),"column":["rideid"]}
		res3=requests.post('http://0.0.0.0:7000/api/v1/db/write',json=task3)
		if res3.status_code==200:
				return json.dumps({}),200
			
		else:	
			#"Ride doesnt exist")
			return Response({},status=400)
			

	else:
		return json.dumps({}),400


			

'''#5 List all details for a given ride'''

@app.route('/api/v1/rides/<int:rideId>',methods=['GET','PUT','HEAD'])
def list_ride(rideId):
                #res2=requests.get('http://0.0.0.0:7000/api/v1/_count')
                no_of_req[0]+=1

    
        	if request.method!='GET':
	        	#("wrong method")
		    return json.dumps({}),405
                #try:
		rideId=str(rideId)
		task1={"method":"select","table":"cride","columns":["*"],"where":"rideid='"+rideId+"'"}
		
		res1=requests.post('http://0.0.0.0:7000/api/v1/db/read',json=task1)
		#("res1",res1)

		if res1.status_code==404:
			#("Ride doesnt exist")
			return json.dumps({}),404

		else:
			
			task2={"method":"listride","table":"cride","columns":["*"],"where":"rideid='"+rideId+"'"}

			res2=requests.post('http://0.0.0.0:7000/api/v1/db/read',json=task2)

			task3={"method":"selectuj","table":"ride","columns":["ujname"],"where":"rideid='"+rideId+"'"}
			res3=requests.post('http://0.0.0.0:7000/api/v1/db/read',json=task3)
			columns=["created_by","source","destination","timestamp","rideId"]
			data=[]

			d={}
			for i in range(0,len(Result[0])):
				d[columns[i]]=Result[0][i]

			d["users"]=Result2
			data.append(d)
			us=jsonify(data)
			#Result.clear()
                        del Result[:]
			#Result2.clear()	
                        del Result2[:]
			return us,200
            	#except:
		#json.dumps({}),400

@app.route('/api/v1/check',methods=['GET'])
def view():
    return Response(status=200)
'''
#just for reference

@app.route('/api/v1/db/read2',methods=['GET'])
def view():
	#conn=sqlite3.connect('user2.db',check_same_thread=False)
	#c=conn.cursor()
	#c.execute("SELECT * FROM cride")
	#rows=c.fetchall()
	#for i in rows:
	#return jsonify(users=[b for b in rows])
'''





'''#3.Create new ride'''

def dtformat(timestamp):
	try:
		ts=timestamp
		tf='%d-%m-%Y:%S-%M-%H'
		dob=datetime.strptime(ts,tf)
		
	except ValueError:
		return 0
        return 1


@app.route('/api/v1/rides',methods=['POST','DELETE','PUT','HEAD'])
def new_ride():
                #res2=requests.get('http://0.0.0.0:7000/api/v1/_count')
                no_of_req[0]+=1

	        #if request.method!="POST":
		#    #("Wrong method")
        	#	return json.dumps({}),405

                if request.method=='POST':	
        		username=request.json["created_by"]
	    	        ts=request.json["timestamp"]
                	src=int(request.json["source"])
        		dest=int(request.json["destination"])

	        	if Place.has_value(src)==True:
			
		        	pass
        		else:
        			#("Source doesnt exist")
	        		return json.dumps({}),400


		
            
	        	#pdest=Place(dest)
		
		        if Place.has_value(dest)==False:
			    print("Destination doesnt exist")
                            return json.dumps({}),400

        		else:
	        		pass
		        if src==dest:
			    return json.dumps({}),400

        		#print("Re1")
                        res1=requests.get("http://asn3-291163488.us-east-1.elb.amazonaws.com:80/api/v1/users")
		        print(res1.json())
        		print(res1.status_code)	
	    	
	        	if res1.status_code==204:
		            print("Username doesnt exist")
		            return json.dumps({}),404

        		else:
	        		d=res1.json()
		        	i=0
                                print(d[0])
        			l=len(d)
                                print(l)
		        	while l:
                                        #print(i,d[i])
				        if username==d[i]:
			
					    valtime=dtformat(ts)
                                            if valtime!=0:
				
						task2={"method":"insert" ,"insert":(username,ts,src,dest),"column":("created_by","timestamp","source","destination"),"table":"cride"}
						
						res3=requests.post('http://0.0.0.0:7000/api/v1/db/write',json=task2)
								
						if res3.status_code==200:
								
							return json.dumps({}),201
						else:
							return json.dumps({}),400
		
							
					    else:
						#("incorrect timeformat!")
						return json.dumps({}),400
				        else:
					    if(i==l-1):
						return json.dumps({}),400					
				            else:
                                                print("in i")
						i=i+1
                                            
                else:
                    return json.dumps({}),405
				
				
	
                    #print("In except")
                    #return json.dumps({}),400





'''4 List all upcoming rides for a given source and destination'''

@app.route('/api/v1/rides',methods=['GET','PUT',"DELETE",'HEAD'])
def list_updetails():
                #res2=requests.get('http://0.0.0.0:7000/api/v1/_count')
                no_of_req[0]+=1


	        if request.method!='GET':
                    #("wrong method")
		    return json.dumps({}),405

        	#try:
		
		src=request.args['source']
		dest=request.args['destination']

		t={"method":"selectcount","table":"cride","columns":["*"],"where":"src"}
		r=requests.post('http://0.0.0.0:7000/api/v1/db/read',json=t)
		if r.status_code==204:
			#("Db is empty")
			return json.dumps({}),204

		if(Place.has_value(int(src))==True and Place.has_value(int(dest))==True):

			task1={"method":"selectmultiple","table":"cride","columns":["*"],"where":"source='"+src+"'","where2":"destination='"+dest+"'"}


			#res=requests.post('http://0.0.0.0:7000/api/v1/read',json=task1)



			res1=requests.post('http://0.0.0.0:7000/api/v1/db/read',json=task1)
			if res1.status_code==404:
				#("No upcoming ride for given source and destination")
				return json.dumps({}),204
			
			else:
				
				task2={"method":"selectmultiple","table":"cride","columns":["*"],"where":"src'"+src+"'","where2":"dest='"+dest+"'"}
				#columns=["created_by:","timestamp:","rideId:"]
				data=[]
				D=[]
		                #print("IN ELSE")		
				for row in Result[0]:
					x=[]
					for i in range(len(row)):
						if i==1:
							pass
						elif i==2:
							pass
						else:
							x.append(row[i])
					D.append(x)
				#print(D)
				for ro in D:
					#print(ro)
					y=gettime(row[3])
					#print(y)
					if(y):
						d={}
						d["rideId"]=int(ro[2])
						d["created_by"]=ro[0]
						d["timestamp"]=ro[1]
						data.append(d)

				#Result.clear()
                                del Result[:]
				return Response(json.dumps(data),mimetype='application/json',status=200)

		else:
			if(Place.has_value(int(src))==False):
				#("Ivalid src")
				return json.dumps({}),400

			elif(Place.has_value(int(dest))==True):
				#("INVALID DEST")
				return json.dumps({}),400

	        #except:
                #	return json.dumps({}),400

'''Clear db--incomplete'''
@app.route('/api/v1/db/clear',methods=['POST'])
def clear_db():
	if request.method!='POST':
		return json.dumps({}),405
	#t1="SELECT * FROM cride"
	#c.execute(t1)
        #print(c.fetchone())
	#if c.fetchone() is None:
	#	return json.dumps({}),400
        #else:
        #t3="SELECT * FROM ride"
        #c.execute(t3)
        #if c.fetchall() is None:
        #    return Response(status=400)
        #else:
        task2={"method":"clearide","table":"ride","insert":("rideid"),"column":["rideId"]} 
        res1=requests.post('http://54.152.143.19:80/api/v1/db/write',json=task2)
        if res1.status_code==200:
                    task3={"method":"clearcride","table":"cride","insert":("rideid"),"column":["rideId"]}
                    res1=requests.post('http://54.152.143.19:80/api/v1/db/write',json=task3)
                    if res1.status_code==200:
                        print("Succesfully executed rides")
                        return json.dumps({}),200
                    else:
                        return json.dumps({}),400
                    #t2="DELETE FROM cride"
                    #c.execute(t2)
                    #conn.commit()
                    #return json.dumps({}),200
        else:
                    #t2="DELETE FROM cride"
                    #c.execute(t2)
                    #conn.commit()
                    return json.dumps({}),400


#count=0              
'''Count apis'''
@app.route('/api/v1/rides/count',methods=['GET','POST','PUT','DELETE','HEAD','OPTIONS'])
def count_api():
        no_of_req[0]+=1

	if request.method!='GET':
		return json.dumps({}),405
	
	task2={"method":"count","table":"cride","columns":["*"],"where":"1"}  
	res=requests.post('http://0.0.0.0:7000/api/v1/db/read',json=task2)
        if res.status_code==200:
            global count
            print(count)
            an=[count]
            return json.dumps(an),200
        #else:
        #    return json.dumps({}),400




#count number of http requests made to the microservice
@app.route('/api/v1/_count',methods=['GET'])
def count_req():
        #curr_url.append(request.base_url)
        if request.method=='GET':
            return Response(json.dumps(no_of_req),mimetype='application/json',status=200)

        else:
                return Response(status=405)

        #print(request.base_url)
        '''
        if(request.base_url!="http://0.0.0.0:7000/api/v1/_count"):
                no_of_req[0]+=1
                return Response(json.dumps(no_of_req),mimetype='application/json',status=200)
        else:
                return Response(json.dumps(no_of_req),mimetype='application/json',status=200)'''

#clear http requests
@app.route('/api/v1/_count',methods=['DELETE'])
def clear_count():
        if request.method!='DELETE':
                return json.dumps({}),405
        no_of_req[0]=0
        return json.dumps({}),200






if __name__=='__main__':
    app.run(host='0.0.0.0',port="7000",debug=True)

