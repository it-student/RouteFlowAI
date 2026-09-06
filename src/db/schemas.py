"""
All classes inheriting from Base class mapping the tables inside the database.
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from db.db_operations import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    family_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    gps_coordinates = Column(String, nullable=True)

    def __repr__(self):
        return f"User(Vorname: {self.name}, Nachname: {self.family_name}, \
Adresse: {self.address}, GPS: {self.gps_coordinates})"

class Searchhistory(Base):
    __tablename__ = 'searchhistories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    starting_point = Column(String)
    distance = Column(Float)
    traveltime = Column(Integer) # Time in minutes or seconds or milliseconds
    theme = Column(String)
    transport_type = Column(String)
    group_size = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return (f"Searchhistory(Distance: {self.distance}, traveltime: {self.traveltime}), \""
                f"theme: {self.theme}, transport_type: {self.transport_type}, group_size: {self.group_size} \""
                f"user_id: {self.user_id}")


class Suggestion(Base):
    __tablename__ = 'suggestions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    sug_transport_type = Column(String)
    destination_coordinates = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    history_id = Column(Integer, ForeignKey('searchhistories.id'))

    def __repr__(self):
        return (f"Suggestions(Title: {self.title}, Description: {self.description}, \n"
                f"Destination: {self.destination_coordinates}, Transport type: {self.sug_transport_type}, \n")


class Tripplan(Base):
    __tablename__ = 'tripplans'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    stopps = Column(Integer)
    suggestion_id = Column(Integer, ForeignKey('suggestions.id'))
    search_id = Column(Integer, ForeignKey('searchhistories.id'))
    user_id = Column(Integer, ForeignKey('users.id'))