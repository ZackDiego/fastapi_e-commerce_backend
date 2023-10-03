from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas
from ..database import get_db
from typing import List
from . import oauth2
from typing import Optional
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/products",
    tags = ["Product"]
)

# GET all product
@router.get('/', response_model= List[schemas.Response_Product])
def get_all_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user),
                limit: int = 3, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM product""")
    # products = cursor.fetchall()
    # products = db.query(models.Product).filter(models.Product.owner_id == current_user.id).filter(models.Product.product_name.contains(search)).limit(limit).offset(skip).all()
    
    
    # JOIN rating and Count
    result = db.query(models.Product, func.count(models.Rating.id)
                      .label("rating_num"), func.round(func.avg(models.Rating.rating),1).label("avg_rating")).join(models.Rating, models.Product.product_id == models.Rating.product_id, isouter=True).group_by(models.Product.product_id).filter(models.Product.product_name.contains(search)).limit(limit).offset(skip).all()
    
    return result

# GET by ID
@router.get('/{product_id}', response_model= schemas.Response_Product)
def get_post(product_id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM product WHERE product_id = (%s)""", 
    #                (str(product_id), ) )
    # product = cursor.fetchone()

    product = db.query(models.Product, func.count(models.Rating.id)
                      .label("rating_num"), func.round(func.avg(models.Rating.rating),1).label("avg_rating")).join(models.Rating, models.Product.product_id == models.Rating.product_id, isouter=True).group_by(models.Product.product_id).filter(models.Product.product_id == product_id).first()

    
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"product with id: {id} was not found")

    return product

# Create new product (POST)
@router.post('/', status_code = status.HTTP_201_CREATED, response_model= schemas.Product)
def add_new_product(product: schemas.Create_Product, db: Session = Depends(get_db),
                    current_user = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     """  INSERT INTO product(product_name, cost_price, quantity) VALUES (%s,  %s, %s) RETURNING *""",
    #     (product.product_name, product.cost_price, product.quantity)
    # )
    # new_product = cursor.fetchone()
    # conn.commit()
    new_product = models.Product(owner_id = current_user.id,**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# Delete product
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db),
                    current_user = Depends(oauth2.get_current_user)):

    
    product = db.query(models.Product).filter(models.Product.product_id == product_id)

    # try:
    #     # cursor.execute("""DELETE FROM product WHERE product_id= %s""", (str(product_id),))
    #     # conn.commit()
    # except Exception as error:
    #     print(error)
    if product.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"product with id: {product_id} does not exist")

    print(product.first().owner_id)
    print(current_user.id)
    if product.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform delete")

    product.delete(synchronize_session=False)
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