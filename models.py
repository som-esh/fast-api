from sqlalchemy import Text,  Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Country(Base):

    __tablename__ = 'country'
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String,  nullable=False)
    cca3 = Column(String,  nullable=False)
    currency_code = Column(String,  nullable=False)
    currency = Column(String,  nullable=False)
    capital = Column(String,  nullable=False)
    region = Column(String,  nullable=False)
    subregion = Column(String,  nullable=False)
    area = Column(Text[100], nullable=False)
    map_url = Column(String,  nullable=False)
    population = Column(Text[100])
    flag_url = Column(String,  nullable=False)

    country_r = relationship("CountryNeighbour", back_populates="neighbour_r")


class CountryNeighbour(Base):

    __tablename__ = 'neighbour'
    id = Column(String, nullable=False, primary_key=True)
    country_id = Column(Integer, ForeignKey(
        'country.id'), nullable=False)
    neighbour_id = Column(String,  nullable=False)
    created_at = Column(String,  nullable=False)
    updated_at = Column(String)

    neighbour_r = relationship("Country", back_populates="country_r")
