# -*- coding: utf-8 -*-
""" Model definitions """

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, Integer, String

db = SQLAlchemy()


class Tilt(db.Model):  # pylint:disable=too-few-public-methods
    """ the Tilt Data model """
    __tablename__ = 'data'
    id = Column(Integer(), primary_key=True)  # pylint:disable=invalid-name
    gravity = Column(Integer)
    temp = Column(Integer)
    color = Column(String(16))
    mac = Column(String(17))
    timestamp = Column(DateTime(timezone=True))

    def serialize(self):
        """ Serializer method """
        return {
            "id": self.id,
            "color": self.color,
            "gravity": self.gravity,
            "temp": self.temp,
            "mac": self.mac,
            "timestamp": self.timestamp.isoformat(),
        }
