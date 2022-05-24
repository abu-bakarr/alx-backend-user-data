#!/usr/bin/env python3
"""Module: Database and SQLAlchemy Libraries"""
from sqlalchemy import create_engine, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """Class: Database Method: _session, add_user, find_user_by"""

    def __init__(self):
        """Method: Constructor"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Method: Creating a Session"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Method: The method should save the user to the database."""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """ Method: Takes in arbitrary keyword arguments(kwargs)
        Return: First row found in the users table as filtered by arguments
        """
        if not kwargs:
            raise InvalidRequestError

        c_names = User.__table__.columns._data.keys()

        for key in kwargs.keys():
            if key in c_names:
                user = self._session.query(User).filter_by(**kwargs).first()
                if user is None:
                    raise NoResultFound
                return user
        raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Method: use to locate the user to update
        myId = self.find_user_by(id=user_id)
        setattr(myId, key, value)
        """
        columns = User.__table__.columns._data.keys()
        for key in kwargs.keys():
            if key not in columns:
                raise ValueError
        session = (update(User)
                   .where(User.id == user_id)
                   .values(**kwargs))
        self._session.execute(session)
        self._session.commit()
