from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from typing import List
from . import oauth2
from typing import Optional

router = APIRouter(
    prefix="/rating",
    tags = ["Rating"]
)

# GET all rating
@router.get('/', response_model= List[schemas.Response_Rating])
def get_all_posts(db: Session = Depends(get_db), 
                limit: int = 3, skip: int = 0, product_id: Optional[int] = None):
    
    if product_id is None:
        ratings = db.query(models.Rating).limit(limit).offset(skip).all()
    else:
        ratings = db.query(models.Rating).filter(models.Rating.product_id == product_id).limit(limit).offset(skip).all()
    
    return ratings

# GET by ID
@router.get('/{rating_id}', response_model= schemas.Product)
def get_post(product_id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM product WHERE product_id = (%s)""", 
    #                (str(product_id), ) )
    # product = cursor.fetchone()

    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()

    
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"product with id: {id} was not found")

    return {"data": product}

# Create new rating (POST)
@router.post('/', status_code = status.HTTP_201_CREATED, response_model= schemas.Response_Rating)
def add_new_rating(rating: schemas.Create_Rating, db: Session = Depends(get_db),
                    current_user = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     """  INSERT INTO product(product_name, cost_price, quantity) VALUES (%s,  %s, %s) RETURNING *""",
    #     (product.product_name, product.cost_price, product.quantity)
    # )
    # new_product = cursor.fetchone()
    # conn.commit()
    product = db.query(models.Product).filter(models.Product.product_id == rating.product_id).first()
    if product is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Product ID {rating.product_id} does not exists!")

    found_rating = db.query(models.Rating).filter(models.Rating.product_id == rating.product_id, models.Rating.rater_id == current_user.id).first()
 
    print(found_rating)
    if found_rating:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= f"User {current_user.username} has already voted on product id {rating.product_id}")
    new_rating = models.Rating(rater_id = current_user.id,**rating.model_dump())
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating


# Delete raint
@router.delete("/{rating_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(rating_id: int, db: Session = Depends(get_db),
                    current_user = Depends(oauth2.get_current_user)):

    
    rating_query = db.query(models.Rating).filter(models.Rating.id == rating_id)

    # try:
    #     # cursor.execute("""DELETE FROM product WHERE product_id= %s""", (str(product_id),))
    #     # conn.commit()
    # except Exception as error:
    #     print(error)
    if rating_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"rating with id: {rating_id} does not exist")

    if rating_query.first().rater_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform delete")

    rating_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE product
@router.put("/{id}", response_model= List[schemas.Product])
def update_product(id: int, product: schemas.Update_Product, db: Session = Depends(get_db),
                    current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE product SET product_name=%s, cost_price=%s, quantity=%s WHERE product_id = %s RETURNING *""",
    #                 (product.product_name, product.cost_price, product.quantity, str(id)))
    # update_product = cursor.fetchone()
    # conn.commit()
    update_product = db.query(models.Product).filter(models.Product.product_id == id)
    # try:
    #     # cursor.execute("""DELETE FROM product WHERE product_id= %s""", (str(product_id),))
    #     # conn.commit()
    # except Exception as error:
    #     print(error)
    if update_product.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"product with id: {id} does not exist")

    update_product.update(product.model_dump(), synchronize_session=False)
    db.commit()
    if update_product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    return {"data": update_product.first()}