from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    Boolean,
    Date,
    Time,
    ForeignKey,
    func,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    )


from pyramid_sacrud import PYRAMID_SACRUD_HOME, PYRAMID_SACRUD_VIEW, PYRAMID_SACRUD_CREATE, PYRAMID_SACRUD_UPDATE, PYRAMID_SACRUD_DELETE, PYRAMID_SACRUD_LIST


from pyramid.security import (
    Allow,
    Everyone,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    site = Column(String)


class Member(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    e_mail = Column(String)
    phone = Column(String(11), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'))
    company = relationship(Company)
  
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)    
    member_id = Column(Integer, ForeignKey('members.id'), nullable=False)
    member = relationship(Member)
    time_order = Column(Date, default=func.now(), nullable=False)
    payment_status = Column(Boolean, nullable=False)
    obtain_status = Column(Boolean, nullable=False)

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)    
    name = Column(String, nullable=False)
    date = Column(String)
    #address = Column(String)
    #date_of_end = Column(Date)
    description = Column(String)    
    img = Column(String)


class AccessControlList(object):   
    __acl__ = [ (Allow, 'group:editors', (PYRAMID_SACRUD_HOME, PYRAMID_SACRUD_VIEW, PYRAMID_SACRUD_CREATE, PYRAMID_SACRUD_UPDATE, PYRAMID_SACRUD_DELETE, PYRAMID_SACRUD_LIST)),
                (Allow, Everyone, PYRAMID_SACRUD_VIEW) ]
    def __init__(self, request):
        pass

# class AccessControlList(object):
#     __acl__  =  [ ( Allow ,  Everyone ,  'view' ), 
#                 ( Allow ,  'group:editors' ,  'edit' )  ]
#     def __init__(self, request):
#         pass        
