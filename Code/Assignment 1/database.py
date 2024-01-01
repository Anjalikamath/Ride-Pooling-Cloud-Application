import sys
from sqlalchemy import Column,ForeignKey,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base=declarative_base()

class User(Base):
	__tablename__='user'
	
	username=Column(String(8000),primary_key=True,nullable=False)
	password=Column(String(8000),nullable=False)
	
	@property
	def serialize(self):
		return{
			'username':self.username,
			'password':self.password,
		}

class CRide(Base):
	__tablename__='cride'
	created_by=Column(String(8000),ForeignKey(User.username,ondelete='CASCADE'))
	source=Column(String(8000))
	destination=Column(String(8000))
	timestamp=Column(String(8000))
	rideId=Column(Integer,primary_key=True,autoincrement=True)


	@property
	def serialize(self):
		return{
			'created_by':self.created_by,
			'source':self.source,
			'destination':self.destination,
			'timestamp':self.timestamp,
			'rideId':self.rideId,
		}
	

class Ride(Base):
	__tablename__='ride'
	
	index=Column(Integer,primary_key=True)
	ujname=Column(String(8000),nullable=False)
	rideid=Column(Integer,ForeignKey(CRide.rideId,ondelete='CASCADE'),nullable=False)

	@property
	def serialize(self):
		return {'ujname':self.ujname,
			'rideid':self.rideid,
		}

engine=create_engine('sqlite:///users102.db')
Base.metadata.create_all(engine)
