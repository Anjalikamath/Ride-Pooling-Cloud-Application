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


engine=create_engine('sqlite:///users102.db')
Base.metadata.create_all(engine)
