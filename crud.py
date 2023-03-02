from math import ceil
from fastapi import Request
from sqlalchemy.orm import Session, joinedload
import models


def get_country(db: Session, request: Request,):

    params = ['a_to_z', 'z_to_a', 'population_high_to_low',
              'population_low_to_high', 'area_high_to_low', 'area_low_to_high']

    data = dict(request.query_params)
    name=region=sub_region=sort_by=''
    page=0
    limit=0

    if 'page' in data:
        page = int(data['page'])
    if 'limit' in data:
        limit = int(data['limit'])
    if 'name' in data:
        name = data['name']
    if 'region' in data:
        region = data['region']
    if 'subregion' in data:
        sub_region = data['subregion']
    if 'sort_by' in data:
        sort_by = data['sort_by']

    sort_query = ''
    search_query = ''

    if sort_by == params[0]:
        sort_query = '(models.Country.name)'
    elif sort_by == params[1]:
        sort_query = '(models.Country.name.desc())'
    elif sort_by == params[2]:
        sort_query = '(models.Country.population)'
    elif sort_by == params[3]:
        sort_query = '(models.Country.population.desc())'
    elif sort_by == params[4]:
        sort_query = '(models.Country.area)'
    elif sort_by == params[5]:
        sort_query = '(models.Country.area.desc())'

    if name or region or sub_region:
        if name:
            search_query += 'name=name,'
        if region:
            search_query += 'region=region,'
        if sub_region:
            search_query += 'subregion=sub_region'

    code = 'db.query(models.Country)'

    if search_query or sort_query:
        if search_query:
            code += f'.filter_by({search_query})'
        if sort_query:
            code += f'.order_by{sort_query}'
    else:
        code += '.order_by(models.Country.id)'

    # code += f'.paginate(page={page}, per_page={limit})'
    off=0
    if not limit: limit = 10
    if not page: page = 1
    else: off = limit*(page-1)+1

    code += f'.offset({off}).limit({limit}).all()'
    print(code)
    object = eval(code)

    # print(rows)

    jsonData = {}
    if object:
        alc = []
        for o in object:
            alc.append(o)
    
        country_data = {}
        jsonData['message'] = 'Country list'
        country_data['list'] = alc
        rows = len(db.query(models.Country).order_by(models.Country.id).all())
        country_data['has_next'] = True
        country_data['has_prev'] = False
        country_data['page'] = page
        country_data['pages'] = ceil(rows/limit)
        country_data['per_page'] = limit
        country_data['total'] = rows

        jsonData['data'] = country_data

        
    else:
        jsonData['message'] = 'Country not found'
        jsonData['data'] = {}

    return jsonData


def get_country_by_id(db: Session, id: int):
    object = db.query(models.Country).filter(models.Country.id == id).first()

    jsonData = {}
    if object:
        alc = []
        alc.append(object)
        country_data = {}
        jsonData['message'] = 'Country detail'
        country_data['country'] = alc
        jsonData['data'] = country_data
        
    else:
        jsonData['message'] = 'Country not found'
        jsonData['data'] = {}

    return jsonData


def create_country(db: Session, info: Request):
    data = info
    entry = models.Country(id=data['id'], name=data['name'], cca3=data['cca3'],
                           currency_code=data['currency_code'], currency=data['currency'], capital=data['capital'],
                           region=data['region'], subregion=data['subregion'],
                           area=data['area'],
                           map_url=data['map_url'],
                           population=data['population'],
                           flag_url=data['flag_url'])
    db.add(entry)
    db.commit()
    return 'received'


def create_country_neighbour(db: Session, info: Request):
    data = info
    entry = models.CountryNeighbour(id=data['id'], country_id=data['country_id'],
                                    neighbour_id=data['neighbour_id'],
                                    created_at=data['created_at'],
                                    updated_at=data['updated_at'],)
    db.add(entry)
    db.commit()
    return 'received'


def get_country_neighbour(db: Session, id: int):
    id = str(id)
    object = db.query(models.Country)\
        .join(models.CountryNeighbour, models.Country.id == models.CountryNeighbour.country_id)\
        .filter(models.CountryNeighbour.neighbour_id == id).all()
    
    does_country_exists = db.query(models.Country).filter(models.Country.id == id).first()
    
    jsonData = {}
    if object:
        alc = []
        for o in object:
            alc.append(o)
    
        country_data = {}
        jsonData['message'] = 'Country neighbours'
        country_data['countries'] = alc
        jsonData['data'] = country_data

    elif does_country_exists:
        jsonData['message'] = 'Country not found'
        jsonData['data'] = {}
    
    else:
        jsonData['message'] = 'Country neighbours'
        data = {}
        data['list'] = []
        jsonData['data'] = data

    return jsonData


def to_dict(country):
    obj = {}
    obj["id"] = country.id,
    obj["name"] = country.name,
    obj["cca"] = country.cca,
    obj["currency_code"] = country.currency_code,
    obj["currency"] = country.currency,
    obj["capital"] = country.capital,
    obj["region"] = country.region,
    obj["subregion"] = country.subregion,
    obj["area"] = country.area,
    obj["map_url"] = country.map_url,
    obj["population"] = country.population,
    obj["flag_url"] = country.flag_url
    return obj


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.CountryNeighbour).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.CountryNeighbour(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
