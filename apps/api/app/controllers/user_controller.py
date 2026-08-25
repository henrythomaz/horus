from app.models.operational.user import User
from app.schemas.user import UserCreate



def create(db, data: UserCreate):

    user = User(
        **data.model_dump()
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user



def get_all(db):

    return db.query(User).all()
