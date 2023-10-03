from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db


router = APIRouter(
    prefix="/users",
    tags = ["User"]
)

# Create new user (POST)
@router.post('/', status_code = status.HTTP_201_CREATED, response_model= schemas.UserResponse)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """  INSERT INTO product(product_name, cost_price, quantity) VALUES (%s,  %s, %s) RETURNING *""",
    #     (product.product_name, product.cost_price, product.quantity)
    # )
    # new_product = cursor.fetchone()
    # conn.commit()
    hash_password = utils.hash(user.password) 
    user.password = hash_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# get User by id
@router.get('/{id}', response_model= schemas.UserResponse)
def get_by_id(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()
    print(user)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not found")

    return user