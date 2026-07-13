"""
All classes inheriting from Base class mapping the tables inside the database.
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from db.db_operations import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    family_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    gps_coordinates = Column(String)

    def __repr__(self):
        return f"User(Vorname: {self.vorname}, Nachname: {self.nachname}, Adresse: {self.adresse}, GPS: {self.gps})"

class Searchhistory(Base):
    __tablename__ = 'searchhistories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    distance = Column(Float)
    traveltime = Column(Integer) # Time in seconds or milliseconds
    theme = Column(String)
    transport_type = Column(String)
    group_size = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return (f"Searchhistory(Distance: {self.distance}, traveltime: {self.traveltime}), \""
                f"theme: {self.theme}, transport_type: {self.transport_type}, group_size: {self.group_size} \""
                f"user_id: {self.user_id}")


class Suggestions(Base):
    __tablename__ = 'suggestions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    est_trip_costs = Column(Float)
    sug_transport_type = Column(String)
    destination_coordinates = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    history_id = Column(Integer, ForeignKey('searchhistories.id'))

    def __repr__(self):
        return f"Suggestions(Title: {self.title}, Destination: {self.destination_coordinates}"


class Tripplans(Base):
    __tablename__ = 'tripplans'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
