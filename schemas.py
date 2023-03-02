from pydantic import BaseModel


class Country(BaseModel):
    id: int
    name: str
    cca3: str
    currency_code: str
    currency: str
    capital: str
    region: str
    subregion: str
    area: float
    map_url: str
    population: float
    flag_url: str

    class Config:
        orm_mode = True


class CountryNeighbour(BaseModel):
    id: int
    country_id: int
    neighbour_id: str
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True
