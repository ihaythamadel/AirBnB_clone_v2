#!/usr/bin/python3
"""DB STORAGE MANAGEMENT"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import os

if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.place import place_amenity


class DBStorage:
    """A class defining methods and attributes for the database
    Attributes:
        __engine (sqlalchemy.Engine): The working SQLAlchemy engine.
        __session (sqlalchemy.Session): The working SQLAlchemy session.
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initializes the Object"""
        user = os.getenv('HBNB_MYSQL_USER')
        passwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        database = os.getenv('HBNB_MYSQL_DB')
        environ = os.getenv('HBNB_ENV')

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                user, passwd, host, database), pool_pre_ping=True)
        if environ == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query on current DB session all objects of the given cls
        If cls is None, queries all types of objects
        Return:
            A Dict of queried classes in the format <class name>.<obj id> = obj.
        """
        if cls is None:
            objs = self.__session.query(State).all()
            objs.extend(self.__session.query(City).all())
            objs.extend(self.__session.query(User).all())
            objs.extend(self.__session.query(Place).all())
            objs.extend(self.__session.query(Review).all())
            objs.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objs = self.__session.query(cls)
        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def new(self, obj):
        """
        Adds obj to current db session
        """
        self.__session.add(obj)

    def save(self):
        """
        commit all changes of current session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        delete obj from current db session
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        create all tables, create current db session
        """

        Base.metadata.create_all(self.__engine)
        session_maker = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_maker)
        self.__session = Session()

    def close(self):
        """
        closes the Running SQLAlchemy session
        """
        self.__session.close()
