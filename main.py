from typing import List
from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
import crud
from database import SessionLocal, engine
import models
import schemas

# uvicorn main:app --reload
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/ac/")
async def add_country(request: Request, db: Session = Depends(get_db)):
    db_country = await request.json()
    if not db_country:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_country(db=db, info=db_country)

@app.post("/an/")
async def add_country_neighbour(request: Request, db: Session = Depends(get_db)):
    db_country = await request.json()
    if not db_country:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_country_neighbour(db=db, info=db_country)


@app.get("/country/")
async def read_country(request: Request, db: Session = Depends(get_db)):
    country = crud.get_country(db, request=request)
    return country

@app.get("/country/{id}")
def read_country_by_id(id: int, db: Session = Depends(get_db)):
    country_id = crud.get_country_by_id(db, id=id)
    if country_id is None:
        raise HTTPException(status_code=404, detail="User not found")
    return country_id

@app.get("/country/{id}/neighbour")
def read_country_neighbour(id: int, db: Session = Depends(get_db)):
    country = crud.get_country_neighbour(db, id=id)
    return country

# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items

# @app.get("/country/", response_model=List[schemas.Country])
# async def read_country(request: Request, db: Session = Depends(get_db)):
#     country = crud.get_country(db, request=request)
#     return country